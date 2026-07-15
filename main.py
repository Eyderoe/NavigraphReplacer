# -*- coding: utf-8 -*-

import sys

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from ui_struct import ToLissEFB


if __name__ == "__main__":
    QApplication.setOrganizationName("Eyderoe")
    QApplication.setApplicationName("ToLissEFB")
    QSettings.setDefaultFormat(QSettings.IniFormat)

    app = QApplication(sys.argv)
    window = ToLissEFB()
    window.show()
    sys.exit(app.exec())
