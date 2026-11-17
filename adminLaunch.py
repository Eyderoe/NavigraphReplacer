"""Explicit UAC restart; importing this module does not request elevation."""

import ctypes
import os
from pathlib import Path
import subprocess
import sys


def is_admin():
    return os.name == "nt" and bool(ctypes.windll.shell32.IsUserAnAdmin())


def restart_as_admin():
    if os.name != "nt":
        raise OSError("管理员重启目前仅支持 Windows。")
    entry = Path(__file__).resolve().with_name("main.py")
    executable = Path(sys.executable)
    windowed_python = executable.with_name("pythonw.exe")
    if not getattr(sys, "frozen", False) and windowed_python.is_file():
        executable = windowed_python
    shell_execute = ctypes.windll.shell32.ShellExecuteW
    shell_execute.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_wchar_p,
                             ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_int]
    shell_execute.restype = ctypes.c_void_p
    result = shell_execute(None, "runas", str(executable),
                           subprocess.list2cmdline([str(entry)]), str(entry.parent), 1)
    if not result or result <= 32:
        raise OSError("未获得管理员授权，程序没有重启。")
