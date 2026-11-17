"""为 X-Plane 子进程设置代理，不修改用户或系统环境变量。"""

import csv
import io
import logging
import os
from pathlib import Path
import re
import socket
import ssl
import subprocess
import json
from http.client import HTTPConnection

from hostsService import DOMAINS


def prepare_steam_launch(executable):
    """按 Steamworks 的直接启动方式指定 App ID，避免 Steam 重启进程丢失环境。"""
    executable = Path(executable)
    if not (executable.parent / "steam_api64.dll").is_file():
        return None
    steamapps = executable.parent.parent.parent
    app_id = None
    for manifest in steamapps.glob("appmanifest_*.acf"):
        contents = manifest.read_text(encoding="utf-8-sig")
        install_dir = re.search(r'"installdir"\s+"([^"\r\n]+)"', contents)
        manifest_id = re.search(r'"appid"\s+"(\d+)"', contents)
        if install_dir and install_dir.group(1).casefold() == executable.parent.name.casefold():
            if manifest_id and manifest.stem == "appmanifest_" + manifest_id.group(1):
                app_id = manifest_id.group(1)
                break
    if app_id is None:
        raise ValueError("检测到 Steam 版，但找不到匹配的 appmanifest，无法保证代理环境在启动后保留。")
    app_id_file = executable.parent / "steam_appid.txt"
    try:
        with app_id_file.open("x", encoding="ascii") as stream:
            stream.write(app_id + "\n")
    except FileExistsError:
        if app_id_file.read_text(encoding="utf-8-sig").strip() != app_id:
            raise ValueError("已有 steam_appid.txt 与安装清单不一致，请检查：{}".format(app_id_file))
    logging.getLogger("toliss_efb.osm").info(
        "[Steam启动] appid=%s 使用 %s，避免 Steam 二次启动丢失代理环境", app_id, app_id_file
    )
    return app_id


def proxy_environment(port, environ=None):
    if not 1 <= int(port) <= 65535:
        raise ValueError("代理端口必须在 1–65535 之间")
    source = os.environ if environ is None else environ
    proxy_keys = {"http_proxy", "https_proxy", "all_proxy", "no_proxy"}
    # Windows 环境变量不区分大小写；先清掉旧值，避免继承 Clash 的 7899。
    env = {key: value for key, value in source.items()
           if key.lower() not in proxy_keys}
    proxy = "http://127.0.0.1:{}".format(int(port))
    env.update(http_proxy=proxy, https_proxy=proxy, all_proxy=proxy,
               no_proxy="127.0.0.1,localhost,::1")
    return env


def _check_executable(executable):
    executable = Path(executable).resolve()
    if not executable.is_file():
        raise ValueError("找不到 X-Plane.exe：{}".format(executable))
    result = subprocess.run(
        ["tasklist", "/FI", "IMAGENAME eq X-Plane.exe", "/FO", "CSV", "/NH"],
        capture_output=True, text=True, errors="replace", check=True,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    if any(row and row[0].lower() == "x-plane.exe"
           for row in csv.reader(io.StringIO(result.stdout))):
        raise ValueError("请先退出已经运行的 X-Plane，再通过此按钮启动。已有进程无法继承新的代理环境变量。")
    return executable


def _spawn_xplane(executable, env):
    app_id = prepare_steam_launch(executable)
    if app_id:
        for key in list(env):
            if key.lower() in ("steamappid", "steamgameid"):
                del env[key]
        env.update(SteamAppId=app_id, SteamGameId=app_id)
    return subprocess.Popen([str(executable)], cwd=str(executable.parent), env=env)


def launch_xplane(executable, port):
    executable = _check_executable(executable)
    try:
        with socket.create_connection(("127.0.0.1", int(port)), timeout=1):
            pass
    except OSError as exc:
        raise ValueError("航图代理尚未监听端口 {}，请先开启服务，稍等后重试。".format(port)) from exc
    env = proxy_environment(port)
    return _spawn_xplane(executable, env)


def hosts_environment(environ=None):
    source = os.environ if environ is None else environ
    proxy_keys = {"http_proxy", "https_proxy", "all_proxy", "no_proxy"}
    env = {key: value for key, value in source.items() if key.lower() not in proxy_keys}
    env["no_proxy"] = ",".join(("127.0.0.1", "localhost", "::1", *DOMAINS))
    return env


def verify_local_origin(ca_path, port=443):
    context = ssl.create_default_context(cafile=str(ca_path))
    connection = HTTPConnection("identity.api.navigraph.com", timeout=3)
    raw = socket.create_connection(("127.0.0.1", port), timeout=3)
    try:
        connection.sock = context.wrap_socket(raw, server_hostname="identity.api.navigraph.com")
        raw = None  # owned by connection from this point on
        connection.request("GET", "/connect/userinfo", headers={
            "Host": "identity.api.navigraph.com", "User-Agent": "ToLissEFB-Launcher/1"})
        response = connection.getresponse()
        body = json.loads(response.read(65536))
        if response.status != 200 or body.get("sub") != "toliss-efb-local":
            raise ValueError("本地 HTTPS 未返回 Local Charts 身份，请重启航图服务。")
    finally:
        connection.close()
        if raw is not None:
            raw.close()


def launch_xplane_hosts(executable, ca_path):
    executable = _check_executable(executable)
    verify_local_origin(ca_path)
    env = hosts_environment()
    process = _spawn_xplane(executable, env)
    logging.getLogger("toliss_efb.osm").info(
        "[hosts 启动 X-Plane] PID=%s；已验证本地 HTTPS，子进程不继承代理环境变量", process.pid)
    return process
