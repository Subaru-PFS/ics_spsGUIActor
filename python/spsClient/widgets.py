__author__ = 'alefur'
from datetime import datetime as dt
from functools import partial

import spsClient.styles as styles
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import QPlainTextEdit, QLabel, QPushButton, QDialog, QGroupBox, QVBoxLayout, QGridLayout, \
    QDialogButtonBox, QDoubleSpinBox, QSpinBox, QTabWidget, QMessageBox, QWidget, QSizePolicy

convertText = {'on': 'ON', 'off': 'OFF', 'nan': 'nan', 'undef': 'undef'}


class ValueGB(QGroupBox):
    def __init__(self, moduleRow, key, title, ind, fmt, fontSize=styles.smallFont, callNow=False):
        self.moduleRow = moduleRow
        self.keyvar = moduleRow.keyVarDict[key]
        self.title = title
        self.fontSize = fontSize

        QGroupBox.__init__(self)
        self.setTitle('%s' % self.title)

        self.grid = QGridLayout()
        self.value = QLabel()

        self.grid.addWidget(self.value, 0, 0)
        self.setLayout(self.grid)

        self.cb = partial(self.updateVals, ind, fmt)
        self.keyvar.addCallback(self.cb, callNow=callNow)

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

    def setBackground(self, background):
        col1, col2 = styles.colormap(background)
        bckColor = 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0  %s, stop: 1 %s)' % (col1, col2)

        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; background-color: %s ;border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " % (
                self.fontSize - 1, bckColor) +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        return bckColor

    def setColor(self, background, police='white'):
        self.setBackground(background=background)
        self.value.setStyleSheet(
            "QLabel{font-size: %ipt; qproperty-alignment: AlignCenter; color:%s;}" % (self.fontSize, police))

    def setText(self, txt):
        self.value.setText(txt)
        self.customize()

    def customize(self):
        text = self.value.text()

        try:
            background, police = styles.colorWidget(text)
        except KeyError:
            background, police = styles.colorWidget('default')

        self.setColor(background=background, police=police)
        self.setEnabled(self.moduleRow.isOnline)

    def setEnabled(self, isOnline):
        if not isOnline:
            self.setColor(*styles.colorWidget('offline'))


class Coordinates(QGroupBox):
    posName = ['X', 'Y', 'Z', 'U', 'V', 'W']

    def __init__(self, moduleRow, key, title, fontSize=styles.smallFont):
        QGroupBox.__init__(self)
        self.grid = QGridLayout()

        self.widgets = [ValueGB(moduleRow, key, pos, i, '{:.5f}', fontSize) for i, pos in
                        enumerate(Coordinates.posName)]

        for i, widget in enumerate(self.widgets):
            self.grid.addWidget(widget, 0, i)

        self.setTitle(title)
        self.setLayout(self.grid)
        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; border: 1px solid #d7d4d1;border-radius: 3px;margin-top: 1ex;} " % (fontSize) +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")


class EmptyWidget(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


class CommandsGB(QGroupBox):
    def __init__(self, controlPanel, fontSize=styles.smallFont):
        self.controlPanel = controlPanel
        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.empty = EmptyWidget()

        self.setTitle('Commands')
        self.setLayout(self.grid)
        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; border: 1px solid #d7d4d1;border-radius: 3px;margin-top: 1ex;} " % (fontSize) +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

    @property
    def buttons(self):
        return []


class ControlPanel(QGroupBox):
    def __init__(self, controlDialog):
        QGroupBox.__init__(self)
        self.controlDialog = controlDialog
        self.grid = QGridLayout()
        self.empty = EmptyWidget()
        self.setLayout(self.grid)

        self.commands = CommandsGB(self)

    @property
    def moduleRow(self):
        return self.controlDialog.moduleRow

    @property
    def actorName(self):
        return self.controlDialog.moduleRow.actorName

    @property
    def basicWidgets(self):
        return [self.grid.itemAt(i).widget() for i in range(self.grid.count())] + self.commands.buttons

    @property
    def customWidgets(self):
        return []

    @property
    def allWidgets(self):
        return self.basicWidgets + self.customWidgets


class ControlDialog(QDialog):
    def __init__(self, moduleRow, title=False):
        title = moduleRow.actorLabel if not title else title
        QDialog.__init__(self, parent=moduleRow.mwindow.spsClient)

        self.vbox = QVBoxLayout()
        self.tabWidget = QTabWidget(self)
        self.cmdBuffer = dict()

        self.moduleRow = moduleRow

        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Discard)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.sendCommands)
        buttonBox.button(QDialogButtonBox.Discard).clicked.connect(self.cancelCommands)

        self.reload = ReloadButton(self)
        self.vbox.addWidget(self.reload)
        self.vbox.addWidget(self.tabWidget)
        self.vbox.addWidget(buttonBox)

        self.setLayout(self.vbox)
        self.setWindowTitle(title)
        self.setVisible(False)

    def addCommand(self, button, cmdStr):
        self.cmdBuffer[button] = cmdStr

    def clearCommand(self, button):
        self.cmdBuffer.pop(button, None)

    def sendCommands(self):
        for button, cmdStr in self.cmdBuffer.items():
            self.moduleRow.mwindow.sendCommand(fullCmd=cmdStr)
            button.setChecked(0)

        self.cmdBuffer.clear()

    def cancelCommands(self):
        self.cmdBuffer.clear()

    def close(self):
        self.setVisible(False)


class DoubleSpinBoxGB(QGroupBox):
    def __init__(self, title, vmin, vmax, decimals):
        QGroupBox.__init__(self)
        self.setTitle('%s' % title)

        self.grid = QGridLayout()
        self.value = QDoubleSpinBox()
        self.value.setValue(0)
        self.value.setDecimals(decimals)
        self.value.setRange(vmin, vmax)
        self.grid.addWidget(self.value, 0, 0)

        self.setLayout(self.grid)

    def setValue(self, value):
        self.value.setValue(float(value))

    def getValue(self):
        return float(self.value.value())


class LockSpinBox(QSpinBox):
    def __init__(self):
        self.locked = False
        QSpinBox.__init__(self)

    def focusInEvent(self, event):
        self.locked = True
        QSpinBox.focusInEvent(self, event)

    def focusOutEvent(self, event):
        self.locked = False
        QSpinBox.focusOutEvent(self, event)


class SpinBoxGB(QGroupBox):
    def __init__(self, title, vmin, vmax):
        QGroupBox.__init__(self)
        self.setTitle('%s' % title)

        self.grid = QGridLayout()
        self.value = LockSpinBox()
        self.value.setValue(0)
        self.value.setRange(vmin, vmax)
        self.grid.addWidget(self.value, 0, 0)

        self.setLayout(self.grid)

    @property
    def locked(self):
        return self.value.locked

    def setValue(self, value):
        try:
            value = int(value)
        except ValueError:
            value = 0

        self.value.setValue(value)

    def getValue(self):
        return int(self.value.value())


class CmdButton(QPushButton):
    def __init__(self, controlPanel, label, cmdStr=False, safetyCheck=False):
        self.controlPanel = controlPanel
        self.cmdStr = cmdStr
        self.safetyCheck = safetyCheck
        QPushButton.__init__(self, label)
        self.setCheckable(True)
        self.clicked.connect(self.getCommand)
        self.setEnabled(controlPanel.moduleRow.isOnline)

    @property
    def controlDialog(self):
        return self.controlPanel.controlDialog

    def buildCmd(self):
        return self.cmdStr

    def getCommand(self):
        if self.isChecked():
            cmdStr = self.buildCmd()
            if self.safetyCheck:
                msg = 'Are you sure you want to send the following command ? \n\r\n %s' % cmdStr
                if QMessageBox.critical(self, 'Warning', msg, QMessageBox.Ok, QMessageBox.Cancel) != QMessageBox.Ok:
                    self.setChecked(False)
                    return

            self.controlDialog.addCommand(button=self, cmdStr=cmdStr)
        else:
            self.controlDialog.clearCommand(button=self)

    def setColor(self, background, color="white"):
        self.setStyleSheet("QPushButton {font: 9pt; background-color: %s;color : %s ;}" % (background, color))


class AbortButton(CmdButton):
    def __init__(self, controlPanel, cmdStr):
        CmdButton.__init__(self, controlPanel=controlPanel, label='ABORT', cmdStr=cmdStr)
        self.setColor(*styles.colorWidget('abort'))


class ReloadButton(QPushButton):
    def __init__(self, controlDialog):
        self.controlDialog = controlDialog
        self.cmdStr = '%s reloadConfiguration' % controlDialog.moduleRow.actorName
        QPushButton.__init__(self, 'Reload Config')
        self.setCheckable(True)
        self.clicked.connect(self.getCommand)
        self.setEnabled(controlDialog.moduleRow.isOnline)
        self.setMaximumWidth(200)

    def buildCmd(self):
        return self.cmdStr

    def getCommand(self):
        if self.isChecked():
            cmdStr = self.buildCmd()
            self.controlDialog.addCommand(button=self, cmdStr=cmdStr)
        else:
            self.controlDialog.clearCommand(button=self)


class InnerButton(CmdButton):
    def __init__(self, upperCmd, label):
        self.upperCmd = upperCmd
        CmdButton.__init__(self, controlPanel=upperCmd.controlPanel, label=label)

    def buildCmd(self):
        return self.upperCmd.buildCmd()


class SwitchGB(ValueGB):
    def __init__(self, moduleRow, key, title, ind, fmt, fontSize=styles.smallFont):
        self.moduleRow = moduleRow
        ValueGB.__init__(self, moduleRow, key=key, title=title, ind=ind, fmt=fmt, fontSize=fontSize)

    def setText(self, txt):
        try:
            txt = 'ON' if int(txt) else 'OFF'
        except ValueError:
            txt = convertText[txt]

        self.value.setText(txt)
        self.customize()


class SwitchButton(SwitchGB):
    def __init__(self, controlPanel, key, label, cmdHead, ind=0, fmt='{:g}', cmdStrOn='', cmdStrOff='',
                 safetyCheck=False):

        cmdStrOn = '%s on' % cmdHead if not cmdStrOn else cmdStrOn
        cmdStrOff = '%s off' % cmdHead if not cmdStrOff else cmdStrOff

        self.buttonOn = CmdButton(controlPanel=controlPanel, label='ON', cmdStr=cmdStrOn, safetyCheck=safetyCheck)
        self.buttonOff = CmdButton(controlPanel=controlPanel, label='OFF', cmdStr=cmdStrOff, safetyCheck=safetyCheck)

        SwitchGB.__init__(self, controlPanel.moduleRow, key=key, title='', ind=ind, fmt=fmt)

        self.grid.removeWidget(self.value)
        self.grid.addWidget(self.buttonOn, 0, 0)
        self.grid.addWidget(self.buttonOff, 0, 0)

        self.setTitle(label)
        self.setFixedHeight(50)

    @property
    def buttons(self):
        return [self.buttonOn, self.buttonOff]

    def setText(self, txt):
        try:
            self.buttonOn.setVisible(not int(txt))
            self.buttonOff.setVisible(int(txt))

        except ValueError:
            pass


class EnumGB(ValueGB):
    def __init__(self, moduleRow, key, title, ind, fmt, fontSize=styles.smallFont):
        self.moduleRow = moduleRow
        ValueGB.__init__(self, moduleRow, key=key, title=title, ind=ind, fmt=fmt, fontSize=fontSize)

    def setText(self, txt):
        txt = txt.upper()
        ValueGB.setText(self, txt=txt)


class CustomedCmd(QGridLayout):
    def __init__(self, controlPanel, buttonLabel):
        QGridLayout.__init__(self)
        self.controlPanel = controlPanel
        self.button = InnerButton(self, label=buttonLabel)
        self.addWidget(self.button, 0, 0)

    def buildCmd(self):
        pass


class MonitorCmd(CustomedCmd):
    def __init__(self, controlPanel, controllerName):
        self.controllerName = controllerName
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='MONITOR')

        self.period = SpinBoxGB('Period', 0, 120)
        self.period.setValue(15)

        self.addWidget(self.period, 0, 1)

    def buildCmd(self):
        cmdStr = '%s monitor controllers=%s period=%d' % (self.controlPanel.actorName,
                                                          self.controllerName,
                                                          self.period.getValue())

        return cmdStr


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
