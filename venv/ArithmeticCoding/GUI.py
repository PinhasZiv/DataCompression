from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplications, QMainWindow
import sys


def window():
    app = QApplications(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("Arithmetic Compression")

    win.show()
    sys.exit(app.exec_())

    window()