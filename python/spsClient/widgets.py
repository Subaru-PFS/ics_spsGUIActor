__author__ = 'alefur'
from datetime import datetime as dt
from functools import partial

from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import QGridLayout, QGroupBox, QPlainTextEdit, QLabel, QPushButton

state2color = {"WIPING": ('blue', 'white'),
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
               "operation": ('green', 'white'),
               "simulation": ('orange', 'white'),
               "nan": ('red', 'white'),
               "undef": ('red', 'white'),
               "off": ('red', 'white'),
               "on": ('green', 'white'),
               }


class ValueGB(QGroupBox):
    def __init__(self, keyvar, title, ind, fmt, fontSize=11, callNow=True):
        self.keyvar = keyvar
        self.title = title
        self.fontSize = fontSize

        QGroupBox.__init__(self)
        self.setTitle('%s' % self.title)

        self.grid = QGridLayout()
        self.value = QLabel()

        self.grid.addWidget(self.value, 0, 0)
        self.setLayout(self.grid)
        self.setColor('black')

        self.cb = partial(self.updateVals, ind, fmt)
        keyvar.addCallback(self.cb, callNow=callNow)

    def __del__(self):
        self.keyvar.removeCallback(self.cb)

    def updateVals(self, ind, fmt, keyvar):
        values = keyvar.getValue(doRaise=False)
        values = (values,) if not isinstance(values, tuple) else values

        value = values[ind]

        try:
            strValue = fmt.format(value)
        except TypeError:
            strValue = 'nan'

        self.setText(strValue)

    def setColor(self, background, police='white'):
        if background == "red":
            bckColor = 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0  #f43131, stop: 1 #5e1414)'

        elif background == "green":
            bckColor = 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0  #45f42e, stop: 1 #195511)'

        elif background == "blue":
            bckColor = 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0  #3168f4, stop: 1 #14195e)'

        elif background == "yellow":
            bckColor = 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0  #edf431, stop: 1 #5e5b14)'

        elif background == "orange":
            bckColor = 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0  #f4a431, stop: 1 #5e4a14)'

        else:
            bckColor = 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0  #dfdfdf, stop: 1 #000000)'

        self.setStyleSheet(
            "QGroupBox {font-size: 9pt; background-color: %s ;border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " % bckColor +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

        self.value.setStyleSheet(
            "QLabel{font-size: %ipt; qproperty-alignment: AlignCenter; color:%s;}" % (self.fontSize, police))

        return bckColor

    def setText(self, txt):
        self.value.setText(txt)
        self.customize()

    def customize(self):
        text = self.value.text()

        try:
            background, police = state2color[text]
        except KeyError:
            background, police = 'green', 'white'

        self.setColor(background=background, police=police)


class ActorGB(ValueGB):
    def __init__(self, device, keyvar):
        self.device = device
        self.button = QPushButton()
        self.button.setFlat(True)

        ValueGB.__init__(self, keyvar, 'ACTOR', 0, '{:s}', callNow=False)
        self.grid.removeWidget(self.value)
        self.setText(device.deviceName)
        self.grid.addWidget(self.button, 0, 0)

    def updateVals(self, ind, fmt, keyvar):
        background, color = ('green', 'white') if self.device.isOnline else ('red', 'white')
        self.setColor(background, color)
        self.device.setOnline()

    def setColor(self, background, police='white'):
        bckColor = ValueGB.setColor(self, background=background, police=police)
        self.button.setStyleSheet("QPushButton{font-size: 11pt; background: %s; color:%s; }" % (bckColor, police))

    def setText(self, txt):
        self.button.setText(txt)


class Coordinates(QGroupBox):
    posName = ['X', 'Y', 'Z', 'U', 'V', 'W']

    def __init__(self, keyvar, title, fontSize=11):
        QGroupBox.__init__(self)
        self.grid = QGridLayout()

        self.widgets = [ValueGB(keyvar, pos, i, '{:.5f}', fontSize) for i, pos in enumerate(Coordinates.posName)]

        for i, widget in enumerate(self.widgets):
            self.grid.addWidget(widget, 0, i)

        self.setTitle(title)
        self.setLayout(self.grid)
        self.setStyleSheet(
            "QGroupBox {font-size: 9pt; border: 1px solid #d7d4d1;border-radius: 3px;margin-top: 1ex;} " +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")


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
