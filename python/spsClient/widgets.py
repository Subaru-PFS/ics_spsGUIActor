__author__ = 'alefur'
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QPlainTextEdit, QLabel
from datetime import datetime as dt

class ValueGB(QGroupBox):
    colors = {"WIPING": ('blue', 'white'),
              "INTEGRATING": ('yellow', 'black'),
              "READING": ('orange', 'white'),
              "EXPOSING": ('yellow', 'black'),
              "IDLE": ('green', 'white'),
              "LOADING": ('blue', 'white'),
              "LOADED": ('blue', 'white'),
              "INITIALISING": ('yellow', 'black'),
              "WARMING": ('orange', 'white'),
              "MOVING": ('orange', 'white'),
              "BUSY": ('orange', 'white'),
              "NAN": ('red', 'white'),
              "FAILED": ('red', 'white'),
              "ONLINE": ('green', 'white'),
              "OFFLINE": ('red', 'white'),
              "ON": ('green', 'white'),
              "OFF": ('red', 'white'),
              "CONNECTED": ('green', 'white'),
              }

    def __init__(self, title):
        self.title = title

        QGroupBox.__init__(self)
        self.setTitle('%s' % self.title)

        self.grid = QGridLayout()
        self.value = QLabel()

        self.grid.addWidget(self.value, 0, 0)
        self.setLayout(self.grid)
        self.setColor('green')

    def setColor(self, background, police='white'):
        if background == "red":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f43131, stop: 1 #5e1414);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "green":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #45f42e, stop: 1 #195511);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "blue":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #3168f4, stop: 1 #14195e);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "yellow":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #edf431, stop: 1 #5e5b14);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "orange":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f4a431, stop: 1 #5e4a14);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

        elif background == "black":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #dfdfdf, stop: 1 #000000);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

        self.value.setStyleSheet("QLabel{font-size: 11pt; qproperty-alignment: AlignCenter; color:%s;}" % police)

    def setText(self, txt):
        try:
            background, police = ValueGB.colors[txt]
            self.setColor(background=background, police=police)
        except KeyError:
            pass

        self.value.setText(txt)

    def pimpMe(self):
        pass


class LogArea(QPlainTextEdit):
    def __init__(self):
        QPlainTextEdit.__init__(self)
        self.logArea = QPlainTextEdit()
        self.setMaximumBlockCount(10000)
        self.setReadOnly(True)

        self.setStyleSheet("background-color: black;color:white;")
        self.setFont(QFont("Monospace", 8))

    def newLine(self, line):
        self.insertPlainText("\n%s  %s" % (dt.now().strftime("%H:%M:%S.%f"), line))
        self.moveCursor(QTextCursor.End)
        self.ensureCursorVisible()

    def trick(self, qlineedit):
        self.newLine(qlineedit.text())