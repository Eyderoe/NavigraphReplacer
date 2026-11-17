from mitmproxy import http
from mitmproxy import ctx

import threading
import time
import winreg
import sys
import os
import re
import atexit
import logging
import subprocess

import cv2

from tileProcess import get_tile
from naviInfoManage import NaviInfoManage


# ================= 配置区 =================

MITMPROXY_PORT = 8080

CLASH_HTTP_PORT = None

UPSTREAM_PROXY = None

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_FILE = os.path.join(
    _BASE_DIR,
    "osm.log"
)

# =========================================


# =============== 日志 ====================

# mitmdump 已配置 root logger 时，basicConfig 不会生效。为插件单独配置日志。
log = logging.getLogger("toliss_efb.osm")
log.setLevel(logging.INFO)
log.propagate = False
if not log.handlers:
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"
    )
    handlers = [logging.FileHandler(LOG_FILE, encoding="utf-8")]
    if sys.stdout is not None:
        handlers.append(logging.StreamHandler(sys.stdout))
    for handler in handlers:
        handler.setFormatter(formatter)
        log.addHandler(handler)


# =========== 保存原始代理 ================

_original_proxy_enabled = None
_original_proxy_server = None


def get_current_proxy():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            0,
            winreg.KEY_READ
        )

        enabled = winreg.QueryValueEx(
            key,
            "ProxyEnable"
        )[0]

        try:
            server = winreg.QueryValueEx(
                key,
                "ProxyServer"
            )[0]
        except Exception:
            server = ""

        winreg.CloseKey(key)

        return bool(enabled), server

    except Exception:
        return False, ""


def save_original_proxy():
    global _original_proxy_enabled
    global _original_proxy_server

    (
        _original_proxy_enabled,
        _original_proxy_server
    ) = get_current_proxy()

    print(
        f"已保存原始代理: "
        f"{'开启' if _original_proxy_enabled else '关闭'} "
        f"{_original_proxy_server}"
    )


# =========== 设置系统代理 ================

def set_system_proxy(
        enable: bool,
        proxy_server: str = ""
):

    try:

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            0,
            winreg.KEY_SET_VALUE
        )


        if enable:

            winreg.SetValueEx(
                key,
                "ProxyEnable",
                0,
                winreg.REG_DWORD,
                1
            )


            winreg.SetValueEx(
                key,
                "ProxyServer",
                0,
                winreg.REG_SZ,
                proxy_server
            )

            log.info(
                f"系统代理已设为: {proxy_server}"
            )


        else:

            winreg.SetValueEx(
                key,
                "ProxyEnable",
                0,
                winreg.REG_DWORD,
                0
            )

            log.info(
                "系统代理已关闭"
            )


        winreg.CloseKey(key)


    except Exception as e:

        print(
            f"设置代理失败: {e}"
        )


def restore_original_proxy():

    global _original_proxy_enabled

    if _original_proxy_enabled is None:
        return


    try:

        if _original_proxy_enabled:

            set_system_proxy(
                True,
                _original_proxy_server
            )

            print(
                f"恢复原始代理: {_original_proxy_server}"
            )

        else:

            set_system_proxy(
                False
            )

            print(
                "恢复原始代理:关闭"
            )


    except Exception as e:

        print(
            f"恢复代理失败:{e}"
        )


# =========== 代理守卫 ====================

_guard_running = True


def proxy_guard():

    target = (
        f"127.0.0.1:{MITMPROXY_PORT}"
    )


    while _guard_running:

        try:

            enabled, current = get_current_proxy()


            if (
                    not enabled
                    or current != target
            ):

                log.warning(
                    f"代理被修改: "
                    f"{current if enabled else '关闭'}"
                )

                set_system_proxy(
                    True,
                    target
                )


        except Exception as e:

            print(
                f"代理检查失败:{e}"
            )


        time.sleep(3)


def start_guard():
    global _guard_running
    _guard_running = True

    t = threading.Thread(
        target=proxy_guard,
        daemon=True
    )

    t.start()

    log.info(
        f"代理守卫启动 "
        f"检查127.0.0.1:{MITMPROXY_PORT}"
    )


def stop_guard():

    global _guard_running

    _guard_running = False


# ============ Tunnel 断开控制 ==================

_visited_airports = set()
_DISCONNECT_AFTER = 5


def _disconnect_navigraph_tunnel(flow: http.HTTPFlow):
    if flow.server_conn and flow.server_conn.connected:
        flow.server_conn.error = Exception("强制断开 tunnel 连接")
        log.info(f"[Tunnel] 已断开连接: api.navigraph.com")
        global _visited_airports
        _visited_airports = set()


def _should_disconnect_tunnel(icao: str) -> bool:
    global _visited_airports
    _visited_airports.add(icao)
    log.debug(f"[Tunnel] 已访问机场: {_visited_airports}, 计数: {len(_visited_airports)}")
    return len(_visited_airports) >= _DISCONNECT_AFTER


# ============ mitmproxy addon ==================


def load(loader):
    if UPSTREAM_PROXY:
        ctx.options.mode = f"upstream:{UPSTREAM_PROXY}"
        log.info(f"上游代理:{UPSTREAM_PROXY}")
    else:
        log.info("未配置上游代理，直接连接")
    log.info("[捕获] 插件已加载，日志=%s", LOG_FILE)


def _is_navigraph_host(host):
    host = host.lower().rstrip(".")
    return host == "navigraph.com" or host.endswith(".navigraph.com")


def _safe_request_url(flow):
    # 不记录查询参数、Authorization 或响应正文。
    return "{}://{}{}".format(
        flow.request.scheme, flow.request.pretty_host,
        flow.request.path.split("?", 1)[0]
    )


def http_connect(flow: http.HTTPFlow):
    log.info("[捕获 CONNECT] %s:%s", flow.request.host, flow.request.port)


def tls_failed_client(data):
    log.warning("[捕获 TLS失败] 客户端=%s 目标=%s；检查客户端是否信任 mitmproxy CA",
                data.conn.peername, data.context.server.address)


def tls_failed_server(data):
    log.warning("[捕获 TLS失败] 上游目标=%s", data.context.server.address)


def response(flow: http.HTTPFlow):
    if _is_navigraph_host(flow.request.pretty_host):
        log.info("[捕获响应] %s status=%s 来源=%s bytes=%s",
                 _safe_request_url(flow), flow.response.status_code,
                 "本地" if flow.metadata.get("navigraph_local") else "上游",
                 len(flow.response.raw_content or b""))


def error(flow: http.HTTPFlow):
    log.warning("[捕获请求失败] %s；检查上游代理和 TLS 连接", _safe_request_url(flow))


def request(flow: http.HTTPFlow):

    host = flow.request.pretty_host
    
    log.debug(f"收到请求: {flow.request.method} {_safe_request_url(flow)}")
    log.debug(f"Host: {host}")
    log.debug(f"Path: {flow.request.path.split('?', 1)[0]}")


    if (
            "tile.openstreetmap.org"
            in host
    ):

        log.info(f"匹配到OSM瓦片请求: {flow.request.path}")

        m = re.match(
            r"/(\d+)/(\d+)/(\d+)\.png",
            flow.request.path
        )

        if m:
            z = int(m.group(1))
            x = int(m.group(2))
            y = int(m.group(3))
            
            log.info(f"解析瓦片坐标: z={z}, x={x}, y={y}")

            try:
                tile = get_tile(x, y, z)
                
                if tile is not None:
                    success, data = cv2.imencode(
                        ".png",
                        tile
                    )

                    if success:
                        flow.response = http.Response.make(
                            200,
                            data.tobytes(),
                            {
                                "Content-Type":
                                    "image/png"
                            }
                        )

                        log.info(
                            f"替换瓦片:"
                            f"{flow.request.path}"
                        )

                        return
                    else:
                        log.info(f"cv2.imencode失败，放过瓦片: {flow.request.path}")
                else:
                    log.info(f"get_tile返回None，放过瓦片: {flow.request.path}")
            except Exception as e:
                log.error(f"get_tile调用失败: {e}")
                log.info(f"放过瓦片: {flow.request.path}")

        log.info(
            f"放过瓦片:"
            f"{flow.request.path}"
        )


    if _is_navigraph_host(host):
        log.info("[捕获请求] %s %s", flow.request.method, _safe_request_url(flow))
    if host.lower().rstrip(".") == "api.navigraph.com":
        _handle_navigraph(flow)


def _handle_navigraph(flow: http.HTTPFlow):
    """拦截 Navigraph API 请求，优先返回本地数据"""
    if _navi_mgr is None:
        log.info("[航图] 未初始化本地航图，透传 %s", _safe_request_url(flow))
        return

    full_url = _safe_request_url(flow)
    path = flow.request.path.split("?")[0]

    # /v2/charts/{ICAO}/{id}_d.png 或 {id}_n.png
    m_chart_img = re.match(r"^/v2/charts/([a-zA-Z]{4})/([a-zA-Z0-9]+)_([dn])\.png$", path)
    if m_chart_img:
        uni_id = m_chart_img.group(2)
        night = (m_chart_img.group(3) == "n")
        pic = _navi_mgr.get_pic(uni_id, night)
        if pic is not None:
            success, data = cv2.imencode(".png", pic)
            if success:
                flow.response = http.Response.make(
                    200,
                    data.tobytes(),
                    {"Content-Type": "image/png"}
                )
                flow.metadata["navigraph_local"] = True
                log.info(f"[航图] 【本地】 {full_url} -> 图片 {pic.shape[1]}x{pic.shape[0]}, {len(data)}bytes")
            else:
                log.info(f"[航图] 【透传】 {full_url} (cv2编码失败)")
        else:
            log.info(f"[航图] 【透传】 {full_url} (本地无此图表)")
        return

    # /v2/charts/{ICAO}?version=STD
    m_charts = re.match(r"^/v2/charts/([a-zA-Z]{4})$", path)
    if m_charts:
        icao = m_charts.group(1).upper()
        charts = _navi_mgr.get_ap_charts(icao)
        if charts is not None:
            import json
            body = json.dumps(charts, ensure_ascii=False)
            flow.response = http.Response.make(
                200,
                body,
                {"Content-Type": "application/json"}
            )
            flow.metadata["navigraph_local"] = True
            log.info(f"[航图] 【本地】 {full_url} -> {len(charts.get('charts', []))} 个图表")
        else:
            log.info(f"[航图] 【透传】 {full_url} (本地无此机场)")
        return

    # /v2/airport/{ICAO}
    m_ap = re.match(r"^/v2/airport/([a-zA-Z]{4})$", path)
    if m_ap:
        icao = m_ap.group(1).upper()
        info = _navi_mgr.get_ap_info(icao)
        if info is not None:
            import json
            body = json.dumps(info, ensure_ascii=False)
            flow.response = http.Response.make(
                200,
                body,
                {"Content-Type": "application/json"}
            )
            flow.metadata["navigraph_local"] = True
            ap_name = info.get("airport_name", icao)
            log.info(f"[航图] 【本地】 {full_url} -> {icao} {ap_name}")
        else:
            log.info(f"[航图] 【透传】 {full_url} (本地无此机场)")
        
        if _should_disconnect_tunnel(icao):
            _disconnect_navigraph_tunnel(flow)
        
        return

    log.info("[航图] 未匹配本地替换规则，透传 %s", full_url)


def done():

    stop_guard()

    restore_original_proxy()

    print(
        "mitmproxy退出，代理已恢复"
    )


# ============ 服务控制 =====================

_service_started = False
_mitmproxy_process = None
_navi_mgr = None

_navi_chart_folder = None
_navi_load_folder = None


def configure_ports(clash_http_port: int = None, mitmproxy_port: int = 8080):
    """在启动服务前配置端口。只有传入了 clash_http_port 才配置链式代理。"""
    global CLASH_HTTP_PORT, MITMPROXY_PORT, UPSTREAM_PROXY
    
    MITMPROXY_PORT = mitmproxy_port
    
    if clash_http_port:
        CLASH_HTTP_PORT = clash_http_port
        UPSTREAM_PROXY = f"http://127.0.0.1:{CLASH_HTTP_PORT}"
        log.info(f"配置链式代理: mitmproxy={MITMPROXY_PORT}, clash={CLASH_HTTP_PORT}")
    else:
        CLASH_HTTP_PORT = None
        UPSTREAM_PROXY = None
        log.info(f"配置直连模式: mitmproxy={MITMPROXY_PORT}")


def configure_navi(chart_folder: str = None, load_folder: str = None):
    """配置航图拦截的文件夹路径。在启动服务前调用。"""
    global _navi_chart_folder, _navi_load_folder
    _navi_chart_folder = chart_folder
    _navi_load_folder = load_folder
    if chart_folder or load_folder:
        log.info(f"配置航图拦截: chart={chart_folder}, load={load_folder}")
    else:
        log.info("未配置航图拦截")


def _find_mitmdump():
    executable_dir = os.path.dirname(sys.executable)
    for mitmdump_path in (os.path.join(executable_dir, "mitmdump.exe"),
                          os.path.join(executable_dir, "Scripts", "mitmdump.exe")):
        if os.path.isfile(mitmdump_path):
            return mitmdump_path
    return "mitmdump"


def _read_subprocess_output(proc):
    while proc.poll() is None:
        try:
            line = proc.stdout.readline()
            if line:
                log.info(f"[mitmdump] {line.strip()}")
        except:
            break
    
    try:
        remaining = proc.stdout.read()
        if remaining:
            log.info(f"[mitmdump] {remaining.strip()}")
    except:
        pass


def _run_mitmproxy():
    global _mitmproxy_process
    import json
    
    script_path = os.path.abspath(__file__)
    
    env = os.environ.copy()
    env['OSM_SERVICE_SKIP_INIT'] = '1'
    env['OSM_MITMPROXY_PORT'] = str(MITMPROXY_PORT)
    if CLASH_HTTP_PORT:
        env['OSM_CLASH_HTTP_PORT'] = str(CLASH_HTTP_PORT)
    
    from tileProcess import get_tile_config
    tile_config = get_tile_config()
    if tile_config['border_file'] and tile_config['map_file']:
        env['OSM_TILE_BORDER_FILE'] = tile_config['border_file']
        env['OSM_TILE_MAP_FILE'] = tile_config['map_file']
        if tile_config['points']:
            env['OSM_TILE_POINTS'] = json.dumps(tile_config['points'])
        log.info(f"传递瓦片配置: border={tile_config['border_file']}, map={tile_config['map_file']}")

    if _navi_chart_folder and _navi_load_folder:
        env['OSM_NAVI_CHART_FOLDER'] = _navi_chart_folder
        env['OSM_NAVI_LOAD_FOLDER'] = _navi_load_folder
        log.info(f"传递航图配置: chart={_navi_chart_folder}, load={_navi_load_folder}")
    
    cmd = [
        _find_mitmdump(),
        "--listen-host", "127.0.0.1",
        "--listen-port", str(MITMPROXY_PORT),
        "-s", script_path,
        "--set", "ssl_insecure=true",
        "--set", "errorcheck=false",
        "--quiet"
    ]
    
    log.info(f"启动 mitmproxy: {' '.join(cmd)}")
    
    try:
        _mitmproxy_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )
        
        t = threading.Thread(target=_read_subprocess_output, args=(_mitmproxy_process,), daemon=True)
        t.start()
        
        _mitmproxy_process.wait()
        
    except Exception as e:
        log.error(f"启动 mitmproxy 失败: {e}")
        stop_service()


def start_service():
    global _service_started
    if _service_started:
        return
    
    # 启动时清空日志
    try:
        open(LOG_FILE, "w").close()
    except Exception:
        pass
    
    save_original_proxy()
    
    atexit.register(
        restore_original_proxy
    )
    
    set_system_proxy(
        True,
        f"127.0.0.1:{MITMPROXY_PORT}"
    )
    
    start_guard()
    
    t = threading.Thread(
        target=_run_mitmproxy,
        daemon=True
    )
    t.start()
    
    log.info("=" * 40)
    log.info(
        "OSM 在线拦截已启动"
    )
    log.info("[代理链路] X-Plane -> 127.0.0.1:%s -> %s", MITMPROXY_PORT,
             UPSTREAM_PROXY or "直接联网")
    log.info("[启动提示] Falcon/SASL 使用 libcurl，单改系统代理可能无效；请使用界面的启动 X-Plane 按钮")
    log.info(
        f"日志文件:{LOG_FILE}"
    )
    log.info("=" * 40)
    
    _service_started = True


def stop_service():
    global _service_started, _mitmproxy_process
    
    stop_guard()
    
    if _mitmproxy_process:
        try:
            _mitmproxy_process.terminate()
            _mitmproxy_process.wait(timeout=5)
            log.info("mitmproxy 已停止")
        except Exception as e:
            log.error(f"停止 mitmproxy 失败: {e}")
        finally:
            _mitmproxy_process = None
    
    restore_original_proxy()
    
    _service_started = False


# ============ mitmdump 子进程初始化 =====================

if os.environ.get('OSM_SERVICE_SKIP_INIT') == '1':
    env_port = os.environ.get('OSM_MITMPROXY_PORT')
    if env_port:
        MITMPROXY_PORT = int(env_port)
    
    env_clash = os.environ.get('OSM_CLASH_HTTP_PORT')
    if env_clash:
        CLASH_HTTP_PORT = int(env_clash)
        UPSTREAM_PROXY = f"http://127.0.0.1:{CLASH_HTTP_PORT}"

    env_navi_chart = os.environ.get('OSM_NAVI_CHART_FOLDER')
    env_navi_load = os.environ.get('OSM_NAVI_LOAD_FOLDER')
    if env_navi_chart and env_navi_load:
        try:
            _navi_mgr = NaviInfoManage(env_navi_chart)
            _navi_mgr.load_folder(env_navi_load)
            log.info(f"航图拦截已初始化: {len(_navi_mgr.get_available_ap())} 个机场可用")
        except Exception as e:
            log.error(f"航图拦截初始化失败: {e}")
