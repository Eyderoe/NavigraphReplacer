# -*- coding: utf-8 -*-

import os
import subprocess

################################################################################
## Form generated from reading UI file 'toliss_efb.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSettings, QSize, QTime, QUrl, Qt, QTimer)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QRadioButton,
    QScrollArea, QSizePolicy, QVBoxLayout, QWidget, QPushButton, QFileDialog,
    QMessageBox, QTabWidget)

# lineEdit 与 QSettings key 的映射
_LINE_EDIT_KEYS = {
    "lineEdit":    "Clash/mixed_port",
    "lineEdit_2":  "Clash/socks_port",
    "lineEdit_3":  "Clash/http_port",
    "lineEdit_4":  "OSM/border_file",
    "lineEdit_5":  "OSM/map_file",
    "lineEdit_6":  "OSM/point1_x",
    "lineEdit_7":  "OSM/point1_y",
    "lineEdit_8":  "OSM/point1_lat",
    "lineEdit_9":  "OSM/point1_long",
    "lineEdit_10": "OSM/point2_long",
    "lineEdit_11": "OSM/point2_y",
    "lineEdit_12": "OSM/point2_x",
    "lineEdit_13": "OSM/point2_lat",
    "lineEdit_14": "Map/map_folder",
    "lineEdit_15": "Map/config_file",
}

class Ui_toliss_efb(object):
    def setupUi(self, toliss_efb):
        if not toliss_efb.objectName():
            toliss_efb.setObjectName(u"toliss_efb")
        toliss_efb.resize(561, 397)
        self.verticalLayout_2 = QVBoxLayout(toliss_efb)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(toliss_efb)
        self.tabWidget.setObjectName(u"tabWidget")
        self.settingsPage = QWidget()
        self.settingsPage.setObjectName(u"settingsPage")
        self.settingsPageLayout = QVBoxLayout(self.settingsPage)
        self.settingsPageLayout.setContentsMargins(0, 0, 0, 0)
        self.secondPage = QWidget()
        self.secondPage.setObjectName(u"secondPage")
        self.tabWidget.addTab(self.settingsPage, "")
        self.tabWidget.addTab(self.secondPage, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.scrollArea = QScrollArea(self.settingsPage)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 530, 385))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.formLayout = QFormLayout(self.groupBox_3)
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.lineEdit = QLineEdit(self.groupBox_3)
        self.lineEdit.setObjectName(u"lineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.lineEdit_2 = QLineEdit(self.groupBox_3)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_2)

        self.lineEdit_3 = QLineEdit(self.groupBox_3)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_3)

        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)


        self.verticalLayout_5.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout.addWidget(self.label_5)

        self.lineEdit_4 = QLineEdit(self.groupBox)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.horizontalLayout.addWidget(self.lineEdit_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_2.addWidget(self.label_6)

        self.lineEdit_5 = QLineEdit(self.groupBox)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.horizontalLayout_2.addWidget(self.lineEdit_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 0, 1, 1, 1)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 0, 2, 1, 1)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout.addWidget(self.label_10, 0, 3, 1, 1)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout.addWidget(self.label_11, 0, 4, 1, 1)

        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")

        self.gridLayout.addWidget(self.label_12, 1, 0, 1, 1)

        self.lineEdit_6 = QLineEdit(self.groupBox)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.gridLayout.addWidget(self.lineEdit_6, 1, 1, 1, 1)

        self.lineEdit_7 = QLineEdit(self.groupBox)
        self.lineEdit_7.setObjectName(u"lineEdit_7")

        self.gridLayout.addWidget(self.lineEdit_7, 1, 2, 1, 1)

        self.lineEdit_8 = QLineEdit(self.groupBox)
        self.lineEdit_8.setObjectName(u"lineEdit_8")

        self.gridLayout.addWidget(self.lineEdit_8, 1, 3, 1, 1)

        self.lineEdit_9 = QLineEdit(self.groupBox)
        self.lineEdit_9.setObjectName(u"lineEdit_9")

        self.gridLayout.addWidget(self.lineEdit_9, 1, 4, 1, 1)

        self.label_13 = QLabel(self.groupBox)
        self.label_13.setObjectName(u"label_13")

        self.gridLayout.addWidget(self.label_13, 2, 0, 1, 1)

        self.lineEdit_12 = QLineEdit(self.groupBox)
        self.lineEdit_12.setObjectName(u"lineEdit_12")

        self.gridLayout.addWidget(self.lineEdit_12, 2, 1, 1, 1)

        self.lineEdit_11 = QLineEdit(self.groupBox)
        self.lineEdit_11.setObjectName(u"lineEdit_11")

        self.gridLayout.addWidget(self.lineEdit_11, 2, 2, 1, 1)

        self.lineEdit_13 = QLineEdit(self.groupBox)
        self.lineEdit_13.setObjectName(u"lineEdit_13")

        self.gridLayout.addWidget(self.lineEdit_13, 2, 3, 1, 1)

        self.lineEdit_10 = QLineEdit(self.groupBox)
        self.lineEdit_10.setObjectName(u"lineEdit_10")

        self.gridLayout.addWidget(self.lineEdit_10, 2, 4, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)


        self.verticalLayout_5.addWidget(self.groupBox)

        self.groupBox_4 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_15 = QLabel(self.groupBox_4)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_4.addWidget(self.label_15)

        self.lineEdit_15 = QLineEdit(self.groupBox_4)
        self.lineEdit_15.setObjectName(u"lineEdit_15")

        self.horizontalLayout_4.addWidget(self.lineEdit_15)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_14 = QLabel(self.groupBox_4)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_3.addWidget(self.label_14)

        self.lineEdit_14 = QLineEdit(self.groupBox_4)
        self.lineEdit_14.setObjectName(u"lineEdit_14")

        self.horizontalLayout_3.addWidget(self.lineEdit_14)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout_5.addWidget(self.groupBox_4)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.radioButton = QRadioButton(self.groupBox_2)
        self.radioButton.setObjectName(u"radioButton")

        self.verticalLayout.addWidget(self.radioButton)


        self.verticalLayout_5.addWidget(self.groupBox_2)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.settingsPageLayout.addWidget(self.scrollArea)


        self.retranslateUi(toliss_efb)
        self._setup_host_page()

        QMetaObject.connectSlotsByName(toliss_efb)
    # setupUi

    def _setup_host_page(self):
        """在 host 页显示共享配置，双向同步到原有控件及其保存逻辑。"""
        page_layout = QVBoxLayout(self.secondPage)
        page_layout.setContentsMargins(0, 0, 0, 0)
        self.hostScrollArea = QScrollArea(self.secondPage)
        self.hostScrollArea.setObjectName("hostScrollArea")
        self.hostScrollArea.setWidgetResizable(True)
        contents = QWidget()
        layout = QVBoxLayout(contents)
        layout.setAlignment(Qt.AlignTop)
        self.hostFields = {}

        def shared_field(name, parent):
            original = getattr(self, name)
            field = QLineEdit(parent)
            field.setObjectName("host_" + name)
            field.setText(original.text())
            original.textChanged.connect(field.setText)
            field.textChanged.connect(original.setText)
            self.hostFields[name] = field
            return field

        self.hostMapGroup = QGroupBox(self.groupBox_4.title(), contents)
        map_layout = QFormLayout(self.hostMapGroup)
        for label, name in ((self.label_15, "lineEdit_15"),
                            (self.label_14, "lineEdit_14")):
            map_layout.addRow(label.text(), shared_field(name, self.hostMapGroup))
        layout.addWidget(self.hostMapGroup)
        self.hostSwitchGroup = QGroupBox("开关", contents)
        switch_layout = QVBoxLayout(self.hostSwitchGroup)
        self.hostEnableButton = QRadioButton("开启", self.hostSwitchGroup)
        self.hostEnableButton.setObjectName("hostEnableButton")
        self.hostEnableButton.setAutoExclusive(False)
        self.hostEnableButton.setToolTip("开启本地 HTTPS 并修改 hosts；取消选中恢复 hosts 并停止服务。")
        switch_layout.addWidget(self.hostEnableButton)
        layout.addWidget(self.hostSwitchGroup)
        self.adminHint = QLabel("需要管理员权限，请先点击“以管理员身份重启”。", contents)
        self.adminHint.setWordWrap(True)
        layout.addWidget(self.adminHint)
        self.adminButton = QPushButton("以管理员身份重启", contents)
        layout.addWidget(self.adminButton)
        self.hostLaunchButton = QPushButton("启动 X-Plane（使用本地航图）", contents)
        layout.addWidget(self.hostLaunchButton)
        self.restoreHostsButton = QPushButton("还原 hosts（使用 hosts.uni_backup）", contents)
        self.restoreHostsButton.setToolTip("使用永久备份还原 hosts，并停止本地航图服务；保留 hosts.uni_backup。")
        layout.addWidget(self.restoreHostsButton)
        self.hostScrollArea.setWidget(contents)
        page_layout.addWidget(self.hostScrollArea)

    def retranslateUi(self, toliss_efb):
        toliss_efb.setWindowTitle(QCoreApplication.translate("toliss_efb", u"toliss_efb", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settingsPage), QCoreApplication.translate("toliss_efb", "mitproxy部分替换", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.secondPage), QCoreApplication.translate("toliss_efb", "host全量替换", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("toliss_efb", u"Clash", None))
        self.label_2.setText(QCoreApplication.translate("toliss_efb", u"\u6df7\u5408\u7aef\u53e3", None))
        self.label_3.setText(QCoreApplication.translate("toliss_efb", u"SOCKS", None))
        self.label_4.setText(QCoreApplication.translate("toliss_efb", u"HTTP", None))
        self.groupBox.setTitle(QCoreApplication.translate("toliss_efb", u"OSM\u66ff\u6362", None))
        self.label_5.setText(QCoreApplication.translate("toliss_efb", u"\u56fd\u5883\u7ebf\u6587\u4ef6", None))
        self.label_6.setText(QCoreApplication.translate("toliss_efb", u"\u822a\u56fe\u6587\u4ef6", None))
        self.label_7.setText(QCoreApplication.translate("toliss_efb", u"\u63a7\u5236\u70b9", None))
        self.label_8.setText(QCoreApplication.translate("toliss_efb", u"x", None))
        self.label_9.setText(QCoreApplication.translate("toliss_efb", u"y", None))
        self.label_10.setText(QCoreApplication.translate("toliss_efb", u"lati", None))
        self.label_11.setText(QCoreApplication.translate("toliss_efb", u"longi", None))
        self.label_12.setText(QCoreApplication.translate("toliss_efb", u"\u70b91", None))
        self.label_13.setText(QCoreApplication.translate("toliss_efb", u"\u70b92", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("toliss_efb", u"\u822a\u56fe\u66ff\u6362", None))
        self.label_15.setText(QCoreApplication.translate("toliss_efb", u"\u914d\u7f6e\u6587\u4ef6", None))
        self.label_14.setText(QCoreApplication.translate("toliss_efb", u"\u822a\u56fe\u6587\u4ef6\u5939", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("toliss_efb", u"\u5f00\u5173", None))
        self.label.setText(QCoreApplication.translate("toliss_efb", u"\u82e5\u4f7f\u7528Clash\uff0c\u5fc5\u987b\u5148\u542f\u52a8Clash\u4ee3\u7406\uff0c\u518d\u5f00\u542f\u8be5\u7a0b\u5e8f\u3002\u5982\u679c\u4ee3\u7406\u670d\u52a1\u5668\u5f02\u5e38\uff0c\u5173\u95ed\u6b64\u7a0b\u5e8f\u540e\uff0c\u5173-\u5f00-\u5173-\u5f00 Clash\u4ee3\u7406\u3002", None))
        self.radioButton.setText(QCoreApplication.translate("toliss_efb", u"\u5f00\u542f", None))
    # retranslateUi

    def connect_settings(self):
        """监听所有 lineEdit 和 radioButton 的变化，自动写入 QSettings"""
        settings = QSettings()
        for attr, key in _LINE_EDIT_KEYS.items():
            widget = getattr(self, attr, None)
            if isinstance(widget, QLineEdit):
                widget.textChanged.connect(
                    lambda text, k=key, s=settings: s.setValue(k, text)
                )
        self.radioButton.toggled.connect(
            lambda checked, s=settings: s.setValue("switch/enabled", checked)
        )

    def load_settings(self):
        """从 QSettings 恢复所有控件值"""
        settings = QSettings()
        for attr, key in _LINE_EDIT_KEYS.items():
            widget = getattr(self, attr, None)
            if isinstance(widget, QLineEdit):
                saved = settings.value(key)
                if saved is not None:
                    widget.setText(saved)
        enabled = settings.value("switch/enabled", False, type=bool)
        self.radioButton.setChecked(enabled)


from tileProcess import init_tile_process
import osmService
from xplaneLaunch import launch_xplane
from hostsService import HostsRedirect
from hostHttpsService import HostHttpsService
from hostOperation import HostOperation
from adminLaunch import is_admin, restart_as_admin


class ToLissEFB(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_toliss_efb()
        self.ui.setupUi(self)
        self.ui.label.setWordWrap(True)

        self.proxy_hint = QLabel(
            f"航图拦截端口：127.0.0.1:{osmService.MITMPROXY_PORT}（程序内部端口）\n"
            "上方 Clash HTTP 是上游端口。Falcon 8X 请先开启服务，再从此处启动 X-Plane。",
            self
        )
        self.proxy_hint.setWordWrap(True)
        self.ui.verticalLayout.addWidget(self.proxy_hint)
        self.launch_button = QPushButton("启动 X-Plane（使用航图代理）", self)
        self.launch_button.clicked.connect(self._launch_xplane)
        self.ui.verticalLayout.addWidget(self.launch_button)

        self.ui.load_settings()
        self.ui.radioButton.setChecked(False)
        self.ui.connect_settings()

        self.hosts_redirect = HostsRedirect()
        self.host_https = HostHttpsService(redirect=self.hosts_redirect)
        self._host_worker = None
        self._close_requested = False
        self._restarting_as_admin = False
        self.ui.adminButton.clicked.connect(self._restart_as_admin)
        self.ui.hostLaunchButton.clicked.connect(self._launch_xplane_hosts)
        self.ui.restoreHostsButton.clicked.connect(self._restore_hosts_universal)
        self.ui.restoreHostsButton.setEnabled(is_admin())
        self.ui.hostEnableButton.setEnabled(is_admin())
        self.ui.adminHint.setVisible(not is_admin())
        if is_admin():
            self.ui.adminButton.setText("已具有管理员权限")
            self.ui.adminButton.setEnabled(False)
        try:
            pending = self.host_https.needs_restore()
            self.ui.hostEnableButton.setChecked(pending)
            if pending:
                osmService.log.warning("[hosts] 检测到遗留修改；请取消第二页的开启选项恢复 hosts，再重新开启服务。")
        except (OSError, ValueError) as exc:
            osmService.log.warning("[hosts] 无法检查恢复状态: %s", exc)
        self.ui.hostEnableButton.toggled.connect(self._on_host_switch_toggled)
        self.ui.radioButton.setAutoExclusive(False)
        self.ui.radioButton.toggled.connect(self._on_switch_toggled)

    def _on_host_switch_toggled(self, checked):
        if self._host_worker is not None:
            return
        if checked and not is_admin():
            self._set_host_checked(False)
            return
        if checked and self.ui.radioButton.isChecked():
            self._set_host_checked(False)
            QMessageBox.information(self, "hosts 替换", "请先关闭 mitproxy 模式，再开启 hosts 替换。")
            return
        self._begin_host_operation(checked)

    def _begin_host_operation(self, checked, executable=None, restore_universal=False):
        worker = HostOperation(self.host_https, checked,
                               self.ui.lineEdit_14.text().strip(),
                               self.ui.lineEdit_15.text().strip(), self, executable=executable,
                               restore_universal=restore_universal)
        self._host_worker = worker
        self.ui.hostEnableButton.setEnabled(False)
        self.ui.radioButton.setEnabled(False)
        self.ui.adminButton.setEnabled(False)
        self.ui.hostLaunchButton.setEnabled(False)
        self.ui.restoreHostsButton.setEnabled(False)
        self.ui.hostEnableButton.setText("正在开启…" if checked else "正在关闭…")
        worker.progress.connect(self.ui.hostEnableButton.setText)
        worker.completed.connect(self._host_operation_completed)
        worker.finished.connect(self._host_operation_finished)
        worker.finished.connect(worker.deleteLater)
        worker.start()

    def _host_operation_completed(self, success, error, checked):
        self._set_host_checked(checked)
        self.ui.hostEnableButton.setText("开启")
        if not success:
            self._close_requested = False
            hint = ("当前已有管理员权限；若 hosts 仍拒绝写入，请检查该文件的访问权限、占用或 hosts 保护设置。"
                    if is_admin() else "权限不足时可点击“以管理员身份重启”。")
            QMessageBox.warning(
                self, "hosts 操作失败",
                f"{error}\n\n{hint}\n如有遗留备份，可关闭此开关重试恢复。"
            )

    def _host_operation_finished(self):
        self._host_worker = None
        self.ui.hostEnableButton.setEnabled(is_admin())
        self.ui.radioButton.setEnabled(True)
        self.ui.adminButton.setEnabled(not is_admin())
        self.ui.hostLaunchButton.setEnabled(True)
        self.ui.restoreHostsButton.setEnabled(is_admin())
        if self._close_requested:
            QTimer.singleShot(0, self.close)

    def _restart_as_admin(self):
        if self._host_worker is not None:
            return
        if self.ui.radioButton.isChecked() or self.host_https.server is not None:
            QMessageBox.information(self, "管理员重启", "请先关闭正在运行的服务，再重启程序。")
            return
        QSettings().sync()
        try:
            restart_as_admin()
        except OSError as exc:
            QMessageBox.warning(self, "管理员重启", str(exc))
            return
        self._restarting_as_admin = True
        self.close()

    def _set_host_checked(self, checked):
        button = self.ui.hostEnableButton
        previous = button.blockSignals(True)
        button.setChecked(checked)
        button.blockSignals(previous)

    def _restore_hosts_universal(self):
        if self._host_worker is not None or not is_admin():
            return
        self._begin_host_operation(False, restore_universal=True)

    def _launch_xplane_hosts(self):
        if self._host_worker is not None:
            return
        if self.host_https.server is None:
            QMessageBox.information(self, "本地航图", "请先开启第二页的本地航图服务。")
            return
        settings = QSettings()
        executable = settings.value("XPlane/executable", "")
        if not executable or not os.path.isfile(executable):
            executable, _ = QFileDialog.getOpenFileName(
                self, "选择 X-Plane.exe", executable, "X-Plane (X-Plane.exe)")
            if not executable:
                return
        settings.setValue("XPlane/executable", executable)
        self._begin_host_operation(True, executable=executable)

    def _init_tile_process_from_ui(self):
        """从 UI 控件读取配置并初始化 tileProcess"""
        border_file = self.ui.lineEdit_4.text()
        map_file = self.ui.lineEdit_5.text()

        p1_x = int(self.ui.lineEdit_6.text()) if self.ui.lineEdit_6.text() else 3142
        p1_y = int(self.ui.lineEdit_7.text()) if self.ui.lineEdit_7.text() else 7472
        p1_lat = float(self.ui.lineEdit_8.text()) if self.ui.lineEdit_8.text() else 46
        p1_lon = float(self.ui.lineEdit_9.text()) if self.ui.lineEdit_9.text() else 80

        p2_x = int(self.ui.lineEdit_12.text()) if self.ui.lineEdit_12.text() else 18878
        p2_y = int(self.ui.lineEdit_11.text()) if self.ui.lineEdit_11.text() else 16910
        p2_lat = float(self.ui.lineEdit_13.text()) if self.ui.lineEdit_13.text() else 22
        p2_lon = float(self.ui.lineEdit_10.text()) if self.ui.lineEdit_10.text() else 120

        points = [
            [p1_x, p1_y, p1_lat, p1_lon],
            [p2_x, p2_y, p2_lat, p2_lon]
        ]

        if border_file and map_file:
            init_tile_process(border_file, map_file, points)

    def _on_switch_toggled(self, checked: bool):
        if checked and self.ui.hostEnableButton.isChecked():
            previous = self.ui.radioButton.blockSignals(True)
            self.ui.radioButton.setChecked(False)
            self.ui.radioButton.blockSignals(previous)
            QSettings().setValue("switch/enabled", False)
            QMessageBox.information(self, "航图代理", "请先关闭 hosts 替换，再开启 mitproxy 模式。")
            return
        if checked:
            self._start_proxy()
        else:
            self._stop_proxy()

    def _start_proxy(self):
        self._init_tile_process_from_ui()
        clash_http_port_text = self.ui.lineEdit_3.text().strip()
        
        if clash_http_port_text:
            try:
                clash_http_port = int(clash_http_port_text)
                osmService.configure_ports(clash_http_port=clash_http_port)
            except ValueError:
                osmService.configure_ports()
        else:
            osmService.configure_ports()
        
        chart_folder = self.ui.lineEdit_14.text().strip() or None
        load_folder = self.ui.lineEdit_15.text().strip() or None
        osmService.configure_navi(chart_folder=chart_folder, load_folder=load_folder)
        
        osmService.start_service()

    def _stop_proxy(self):
        osmService.stop_service()

    def _launch_xplane(self):
        if not self.ui.radioButton.isChecked():
            QMessageBox.information(self, "航图代理", "请先勾选“开启”，再启动 X-Plane。")
            return
        settings = QSettings()
        executable = settings.value("XPlane/executable", "")
        if not executable or not os.path.isfile(executable):
            executable, _ = QFileDialog.getOpenFileName(
                self, "选择 X-Plane.exe", executable, "X-Plane (X-Plane.exe)"
            )
            if not executable:
                return
        try:
            process = launch_xplane(executable, osmService.MITMPROXY_PORT)
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            QMessageBox.warning(self, "启动失败", str(exc))
            return
        settings.setValue("XPlane/executable", executable)
        osmService.log.info("[启动 X-Plane] PID=%s 代理=http://127.0.0.1:%s",
                            process.pid, osmService.MITMPROXY_PORT)

    def closeEvent(self, event):
        if self._host_worker is not None:
            self._close_requested = True
            event.ignore()
            return
        if not self._restarting_as_admin and self.ui.hostEnableButton.isChecked():
            self._close_requested = True
            self._on_host_switch_toggled(False)
            event.ignore()
            return
        self._stop_proxy()
        super().closeEvent(event)

