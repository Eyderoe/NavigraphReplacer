"""Temporary WinINet direct-connect exceptions for local origins."""

import ctypes
import json
import os
from pathlib import Path
import winreg

from hostsService import DOMAINS, _create_backup

KEY = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"


def _read_override():
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY) as key:
        try:
            value, kind = winreg.QueryValueEx(key, "ProxyOverride")
            return {"exists": True, "value": value, "kind": kind}
        except FileNotFoundError:
            return {"exists": False, "value": "", "kind": winreg.REG_SZ}


def _write_override(value):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, KEY, 0, winreg.KEY_SET_VALUE) as key:
        if value["exists"]:
            winreg.SetValueEx(key, "ProxyOverride", 0, value["kind"], value["value"])
        else:
            try:
                winreg.DeleteValue(key, "ProxyOverride")
            except FileNotFoundError:
                pass
    # Tell WinINet clients to reread their settings; do not change ProxyEnable/ProxyServer.
    for option in (39, 37):
        ctypes.windll.wininet.InternetSetOptionW(None, option, None, 0)


class ProxyBypass:
    def __init__(self, state_path=None):
        self.path = Path(state_path) if state_path else (
            Path(os.environ.get("LOCALAPPDATA", Path.home())) / "ToLissEFB" / "proxy-bypass.json")

    def needs_restore(self):
        return self.path.exists()

    def enable(self):
        if self.needs_restore():
            raise ValueError("检测到遗留的代理直连例外，请先关闭开关恢复。")
        original = _read_override()
        parts = [part.strip() for part in original["value"].split(";") if part.strip()]
        existing = {part.casefold() for part in parts}
        added = [domain for domain in DOMAINS if domain.casefold() not in existing]
        if not added:
            return
        installed = {"exists": True, "value": ";".join(parts + added), "kind": winreg.REG_SZ}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Persist the complete original before changing the registry.
        _create_backup(self.path, json.dumps(
            {"original": original, "installed": installed, "added": added}).encode("utf-8"))
        _write_override(installed)

    def disable(self):
        if not self.needs_restore():
            return
        state = json.loads(self.path.read_text(encoding="utf-8"))
        current = _read_override()
        if current == state["installed"] or current == state["original"]:
            restored = state["original"]
        else:
            # Preserve edits made by another program while serving.
            added = {domain.casefold() for domain in state["added"]}
            restored = {**current, "value": ";".join(
                part for part in current["value"].split(";") if part.strip().casefold() not in added)}
        _write_override(restored)
        self.path.unlink()
