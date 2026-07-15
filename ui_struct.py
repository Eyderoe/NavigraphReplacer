# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'toliss_efb.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSettings, QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QRadioButton,
    QScrollArea, QSizePolicy, QVBoxLayout, QWidget)

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
        self.scrollArea = QScrollArea(toliss_efb)
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

        self.verticalLayout_2.addWidget(self.scrollArea)


        self.retranslateUi(toliss_efb)

        QMetaObject.connectSlotsByName(toliss_efb)
    # setupUi

    def retranslateUi(self, toliss_efb):
        toliss_efb.setWindowTitle(QCoreApplication.translate("toliss_efb", u"toliss_efb", None))
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


class ToLissEFB(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_toliss_efb()
        self.ui.setupUi(self)

        self.ui.load_settings()
        self.ui.radioButton.setChecked(False)
        self.ui.connect_settings()

        self._init_tile_process_from_ui()

        self.ui.radioButton.toggled.connect(self._on_switch_toggled)

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
        if checked:
            self._start_proxy()
        else:
            self._stop_proxy()

    def _start_proxy(self):
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

