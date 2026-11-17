"""Reversible hosts redirects. Importing this module never changes the system."""

import codecs
import ctypes
import logging
import os
from pathlib import Path
import secrets


DOMAINS = (
    "identity.api.navigraph.com",
    "api.navigraph.com",
    "charts.api.navigraph.com",
    "subscriptions.api.navigraph.com",
)
BEGIN = "# BEGIN ToLissEFB hosts"
END = "# END ToLissEFB hosts"
log = logging.getLogger(__name__)


def _decode(data):
    for bom, encoding in ((codecs.BOM_UTF16_LE, "utf-16-le"),
                          (codecs.BOM_UTF16_BE, "utf-16-be"),
                          (codecs.BOM_UTF8, "utf-8")):
        if data.startswith(bom):
            return data[len(bom):].decode(encoding), encoding, bom
    # Domain names are ASCII. Latin-1 round-trips all other bytes unchanged.
    return data.decode("latin-1"), "latin-1", b""


def redirected_hosts(data):
    text, encoding, bom = _decode(data)
    newline = "\r\n" if "\r\n" in text or not text else "\n"
    lines = []
    in_block = False
    for line in text.splitlines(keepends=True):
        if line.strip() == BEGIN:
            if in_block:
                raise ValueError("hosts 中存在嵌套的 ToLissEFB 标记，请先恢复备份。")
            in_block = True
            continue
        if line.strip() == END:
            if not in_block:
                raise ValueError("hosts 中的 ToLissEFB 标记不完整，请先恢复备份。")
            in_block = False
            continue
        if in_block:
            continue
        body, separator, comment = line.rstrip("\r\n").partition("#")
        tokens = body.split()
        if len(tokens) > 1:
            aliases = [name for name in tokens[1:]
                       if name.lower().rstrip(".") not in DOMAINS]
            if len(aliases) != len(tokens) - 1:
                ending = line[len(line.rstrip("\r\n")):]
                if aliases:
                    line = tokens[0] + " " + " ".join(aliases)
                    if separator:
                        line += " #" + comment
                    line += ending
                else:
                    line = ("#" + comment + ending) if separator else ""
        lines.append(line)
    if in_block:
        raise ValueError("hosts 中的 ToLissEFB 标记不完整，请先恢复备份。")
    result = "".join(lines)
    if result and not result.endswith(("\r", "\n")):
        result += newline
    result += BEGIN + newline
    result += "".join(f"127.0.0.1 {domain}{newline}" for domain in DOMAINS)
    result += END + newline
    return bom + result.encode(encoding)


def _temporary_file(directory, prefix):
    """Fail immediately on permission errors (Windows mkstemp may retry them)."""
    for _ in range(4):
        path = Path(directory) / (prefix + secrets.token_hex(12))
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_RDWR | getattr(os, "O_BINARY", 0), 0o600)
            return fd, path
        except FileExistsError:
            continue
    raise FileExistsError("无法分配 hosts 临时文件名。")


def _create_backup(path, data):
    """Publish a complete backup atomically, without replacing an existing file."""
    if path.exists():
        return
    fd, temporary = _temporary_file(path.parent, ".toliss-backup-")
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            pass
    finally:
        os.unlink(temporary)


def _replace_hosts(path, data):
    if path.read_bytes() == data:
        return
    fd, temporary = _temporary_file(path.parent, ".toliss-hosts-")
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.replace(temporary, path)
        except PermissionError:
            # Windows readers may allow writes but deny renaming/deleting hosts.
            # Keep its file identity and ACL instead of replacing the directory entry.
            _write_hosts_in_place(path, data)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _write_hosts_in_place(path, data):
    # r+b opens without truncation: a denied open cannot damage the original file.
    with path.open("r+b") as stream:
        original = stream.read()
        try:
            stream.seek(0)
            stream.write(data)
            stream.truncate()
            stream.flush()
            os.fsync(stream.fileno())
        except OSError:
            try:
                stream.seek(0)
                stream.write(original)
                stream.truncate()
                stream.flush()
                os.fsync(stream.fileno())
            except OSError:
                log.exception("hosts 原位写入及回滚失败；恢复备份仍保留在 hosts 同目录。")
            raise


def flush_dns():
    if os.name == "nt":
        try:
            if not ctypes.WinDLL("dnsapi").DnsFlushResolverCache():
                log.warning("hosts 已更新，但 DNS 缓存刷新失败。")
        except OSError:
            log.warning("hosts 已更新，但 DNS 缓存刷新失败。", exc_info=True)


class HostsRedirect:
    def __init__(self, hosts_path=None):
        self.path = Path(hosts_path) if hosts_path is not None else (
            Path(os.environ.get("SystemRoot", r"C:\Windows"))
            / "System32" / "drivers" / "etc" / "hosts"
        )
        self.universal_backup = self.path.with_name("hosts.uni_backup")
        self.session_backup = self.path.with_name("hosts.toliss_backup")

    def check_writable(self):
        """Check access before scanning charts, generating certificates or binding TLS."""
        try:
            fd = os.open(self.path, os.O_RDWR | getattr(os, "O_BINARY", 0))
            os.close(fd)
            fd, probe = _temporary_file(self.path.parent, ".toliss-access-")
            os.close(fd)
            probe.unlink()
        except PermissionError as exc:
            raise PermissionError("没有权限写入系统 hosts 或备份目录，请以管理员身份运行程序。") from exc

    def needs_restore(self):
        if self.session_backup.exists():
            return True
        text, _, _ = _decode(self.path.read_bytes())
        return BEGIN in text.splitlines()

    def enable(self):
        current = self.path.read_bytes()
        text, _, _ = _decode(current)
        marked = BEGIN in text.splitlines()
        if marked:
            if not (self.session_backup.exists() or self.universal_backup.exists()):
                raise ValueError("hosts 已被修改，但找不到恢复备份；拒绝把修改后的内容备份为原始文件。")
            return
        if self.session_backup.exists():
            raise ValueError("检测到上次遗留的 hosts 备份，请先关闭开关恢复，再重新开启。")
        updated = redirected_hosts(current)
        _create_backup(self.universal_backup, current)
        _create_backup(self.session_backup, current)
        _replace_hosts(self.path, updated)
        flush_dns()

    def disable(self):
        if not self.needs_restore():
            return
        # The per-activation snapshot restores this session's actual original hosts.
        # The never-overwritten universal backup remains available after a crash.
        backup = self.session_backup if self.session_backup.exists() else self.universal_backup
        if not backup.exists():
            raise ValueError("找不到 hosts 恢复备份，请手动检查 hosts 文件。")
        _replace_hosts(self.path, backup.read_bytes())
        if self.session_backup.exists():
            self.session_backup.unlink()
        flush_dns()

    def restore_universal(self):
        """Explicitly restore the permanent backup, regardless of session state."""
        if not self.universal_backup.is_file():
            raise FileNotFoundError(f"找不到永久备份：{self.universal_backup}，hosts 未被修改。")
        original = self.universal_backup.read_bytes()
        _replace_hosts(self.path, original)
        if self.session_backup.exists():
            self.session_backup.unlink()
        flush_dns()
