"""Run hosts-mode lifecycle operations away from the Qt GUI thread."""

import logging
import os

from PySide6.QtCore import QThread, Signal

from naviInfoManage import NaviInfoManage
from xplaneLaunch import launch_xplane_hosts

log = logging.getLogger("toliss_efb.osm")


class HostOperation(QThread):
    progress = Signal(str)
    completed = Signal(bool, str, bool)

    def __init__(self, service, enable, chart_folder="", config_folder="", parent=None, executable=None, restore_universal=False):
        super().__init__(parent)
        self.service = service
        self.enable = enable
        self.chart_folder = chart_folder
        self.config_folder = config_folder
        self.executable = executable
        self.restore_universal = restore_universal

    def _progress(self, message):
        log.info("[hosts] %s", message)
        self.progress.emit(message)

    def run(self):
        try:
            if self.restore_universal:
                self._progress("正在通过 hosts.uni_backup 还原 hosts…")
                self.service.stop(restore_universal=True)
            elif self.executable is not None:
                self._progress("正在检查本地 HTTPS 并启动 X-Plane…")
                launch_xplane_hosts(self.executable, self.service.certificate.ca_path)
            elif self.enable:
                self._progress("正在检查 hosts 写入权限…")
                self.service.redirect.check_writable()
                if self.service.needs_restore():
                    raise ValueError("检测到遗留的 hosts 修改，请先关闭开关恢复，再重新开启。")
                if not os.path.isdir(self.chart_folder) or not os.path.isdir(self.config_folder):
                    raise ValueError("请填写有效的航图文件夹和包含 .Tnavi 的配置文件夹。")
                self._progress("正在扫描本地航图…")
                manager = NaviInfoManage(self.chart_folder)
                self._progress("正在加载 .Tnavi 配置…")
                manager.load_folder(self.config_folder)
                if not any(manager.get_ap_charts(icao) for icao in manager.get_available_ap()):
                    raise ValueError("当前配置没有匹配到本地航图，请检查 PDF 和 .Tnavi 文件。")
                self.service.start(manager=manager, progress=self._progress)
            else:
                self._progress("正在恢复 hosts 并停止 HTTPS…")
                self.service.stop()
        except Exception as exc:
            log.exception("[hosts] %s失败", "开启" if self.enable else "关闭")
            try:
                pending = self.service.needs_restore()
            except Exception:
                pending = not self.enable
            self.completed.emit(False, str(exc), pending)
        else:
            self.completed.emit(True, "", self.enable)
