__author__ = 'alefur'
from functools import partial

import spsGUIActor.styles as styles
from PyQt5.QtWidgets import QLabel, QGroupBox, QMessageBox
from spsGUIActor.common import PushButton, DoubleSpinBox, SpinBox, GridLayout, GBoxGrid

convertText = {'on': 'ON', 'off': 'OFF', 'nan': 'nan', 'undef': 'undef', 'pending': 'OFF'}


class ValueGB(QGroupBox):
    def __init__(self, moduleRow, key, title, ind, fmt, fontSize=styles.smallFont, callNow=False):
        self.moduleRow = moduleRow
        self.keyvar = moduleRow.keyVarDict[key]
        self.title = title
        self.fontSize = fontSize

        QGroupBox.__init__(self)
        self.setTitle('%s' % self.title)

        self.grid = GridLayout()
        self.grid.setContentsMargins(*((fontSize - 1,) * 4))

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
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 1px;}")
        return bckColor

    def setColor(self, background, police='white'):
        self.setBackground(background=background)
        self.value.setStyleSheet(
            "QLabel{font-size: %ipt; qproperty-alignment: AlignCenter; color:%s;}" % (self.fontSize, police))

    def setText(self, txt):
        self.value.setText(txt)
        self.moduleRow.heartBeat()
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


class ValuesRow(QGroupBox):
    def __init__(self, widgets, title, fontSize=styles.smallFont):
        QGroupBox.__init__(self)
        self.grid = GBoxGrid(title=title)

        for i, widget in enumerate(widgets):
            self.grid.addWidget(widget, 0, i)

        self.setTitle(title)
        self.setLayout(self.grid)
        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; border: 1px solid #d7d4d1;border-radius: 3px;margin-top: 1ex;} " % (fontSize) +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

    def setEnabled(self, a0: bool):
        QGroupBox.setEnabled(self, a0)
        for widget in [self.grid.itemAt(i).widget() for i in range(self.grid.count())]:
            widget.setEnabled(a0)


class Coordinates(ValuesRow):
    posName = ['X', 'Y', 'Z', 'U', 'V', 'W']

    def __init__(self, moduleRow, key, title, fontSize=styles.smallFont):
        widgets = [ValueGB(moduleRow, key, c, i, '{:.5f}', fontSize) for i, c in enumerate(Coordinates.posName)]
        ValuesRow.__init__(self, widgets, title=title, fontSize=fontSize)


class DoubleSpinBoxGB(QGroupBox):
    def __init__(self, title, vmin, vmax, decimals, fontSize=styles.smallFont):
        QGroupBox.__init__(self)
        self.setTitle('%s' % title)

        self.grid = GBoxGrid(title=title)
        self.value = DoubleSpinBox()
        self.value.setValue(0)
        self.value.setDecimals(decimals)
        self.value.setRange(vmin, vmax)
        self.grid.addWidget(self.value, 0, 0)

        self.setLayout(self.grid)

        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; border: 1px solid #d7d4d1;border-radius: 3px;margin-top: 1ex;} " % (
                    fontSize - 1) +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

    def setValue(self, value):
        self.value.setValue(float(value))

    def getValue(self):
        return float(self.value.value())


class LockSpinBox(SpinBox):
    def __init__(self):
        self.locked = False
        SpinBox.__init__(self)

    def focusInEvent(self, event):
        self.locked = True
        SpinBox.focusInEvent(self, event)

    def focusOutEvent(self, event):
        self.locked = False
        SpinBox.focusOutEvent(self, event)


class SpinBoxGB(QGroupBox):
    def __init__(self, title, vmin, vmax, fontSize=styles.smallFont):
        QGroupBox.__init__(self)
        self.setTitle('%s' % title)

        self.grid = GBoxGrid(title=title)
        self.value = LockSpinBox()
        self.value.setValue(0)
        self.value.setRange(vmin, vmax)
        self.grid.addWidget(self.value, 0, 0)

        self.setLayout(self.grid)

        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; border: 1px solid #d7d4d1;border-radius: 3px;margin-top: 1ex;} " % (
                    fontSize - 1) +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

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


class CmdButton(PushButton):
    def __init__(self, controlPanel, label, controlDialog=False, cmdStr=False, safetyCheck=False):
        self.controlDialog = controlPanel.controlDialog if controlPanel is not None else controlDialog
        self.cmdStr = cmdStr
        self.safetyCheck = safetyCheck
        PushButton.__init__(self, label)
        self.setCheckable(True)
        self.clicked.connect(self.getCommand)
        self.setEnabled(self.controlDialog.moduleRow.isOnline)

    def buildCmd(self):
        return self.cmdStr

    def getCommand(self):
        if self.isChecked():
            cmdStr = self.buildCmd()
            if not self.accessGranted(cmdStr=cmdStr):
                return

            self.controlDialog.addCommand(button=self, cmdStr=cmdStr)
        else:
            self.controlDialog.clearCommand(button=self)

    def accessGranted(self, cmdStr):
        granted = True
        if self.safetyCheck:
            msg = 'Are you sure you want to send the following command ? \n\r\n %s' % cmdStr
            if QMessageBox.critical(self, 'Warning', msg, QMessageBox.Ok, QMessageBox.Cancel) != QMessageBox.Ok:
                self.setChecked(False)
                granted = True

        return granted

    def setColor(self, background, color="white"):
        self.setStyleSheet(
            "QPushButton {font: %dpt; background-color: %s;color : %s ;}" % (styles.smallFont, background, color))


class AbortButton(CmdButton):
    def __init__(self, controlPanel, cmdStr):
        CmdButton.__init__(self, controlPanel=controlPanel, label='ABORT', cmdStr=cmdStr)
        self.setColor(*styles.colorWidget('abort'))


class InnerButton(CmdButton):
    def __init__(self, upperCmd, label, safetyCheck=False):
        self.upperCmd = upperCmd
        CmdButton.__init__(self, controlPanel=upperCmd.controlPanel, label=label, safetyCheck=safetyCheck)

    def buildCmd(self):
        return self.upperCmd.buildCmd()


class SwitchGB(ValueGB):
    def __init__(self, moduleRow, key, title, ind, fmt, fontSize=styles.smallFont):
        self.moduleRow = moduleRow
        ValueGB.__init__(self, moduleRow, key=key, title=title, ind=ind, fmt=fmt, fontSize=fontSize)
        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; border: 1px solid #d7d4d1;border-radius: 3px;margin-top: 1ex;} " % (
                    fontSize - 1) +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

    def setText(self, txt):
        try:
            txt = 'ON' if int(txt) else 'OFF'
        except ValueError:
            txt = convertText[txt]

        self.value.setText(txt)
        self.customize()


class SwitchButton(SwitchGB):
    def __init__(self, controlPanel, key, label, cmdHead, ind=0, fmt='{:g}', cmdStrOn='', cmdStrOff='', labelOn='ON',
                 labelOff='OFF', safetyCheck=False):

        cmdStrOn = '%s on' % cmdHead if not cmdStrOn else cmdStrOn
        cmdStrOff = '%s off' % cmdHead if not cmdStrOff else cmdStrOff

        self.buttonOn = CmdButton(controlPanel=controlPanel, label=labelOn, cmdStr=cmdStrOn, safetyCheck=safetyCheck)
        self.buttonOff = CmdButton(controlPanel=controlPanel, label=labelOff, cmdStr=cmdStrOff, safetyCheck=safetyCheck)

        SwitchGB.__init__(self, controlPanel.moduleRow, key=key, title='', ind=ind, fmt=fmt)

        self.grid.removeWidget(self.value)
        self.grid.addWidget(self.buttonOn, 0, 0)
        self.grid.addWidget(self.buttonOff, 0, 0)

        self.setTitle(label)
        self.grid.setContentsMargins(1, 8, 1, 1)

    def setText(self, txt):
        try:
            self.buttonOn.setVisible(not int(txt))
            self.buttonOff.setVisible(int(txt))

        except ValueError:
            pass

    def setEnabled(self, isOnline):
        self.buttonOff.setEnabled(isOnline)
        self.buttonOn.setEnabled(isOnline)


class EnumGB(ValueGB):
    def __init__(self, moduleRow, key, title, ind, fmt, fontSize=styles.smallFont):
        self.moduleRow = moduleRow
        ValueGB.__init__(self, moduleRow, key=key, title=title, ind=ind, fmt=fmt, fontSize=fontSize)

    def setText(self, txt):
        txt = txt.upper()
        ValueGB.setText(self, txt=txt)


class CustomedCmd(GridLayout):
    def __init__(self, controlPanel, buttonLabel, safetyCheck=False):
        GridLayout.__init__(self)
        self.controlPanel = controlPanel
        self.button = InnerButton(self, label=buttonLabel, safetyCheck=safetyCheck)
        self.addWidget(self.button, 0, 0)

    def buildCmd(self):
        pass

    def setEnabled(self, a0: bool):
        GridLayout.setEnabled(self, a0)
        for button in [self.itemAt(i).widget() for i in range(self.count())]:
            button.setEnabled(a0)


class Controllers(ValueGB):
    def __init__(self, moduleRow):
        ValueGB.__init__(self, moduleRow, 'controllers', 'Controllers', 0, '{:s}', fontSize=styles.bigFont)

    def updateVals(self, ind, fmt, keyvar):
        controllers = keyvar.getValue(doRaise=False)

        for widget in self.moduleRow.widgets + self.moduleRow.controlDialog.pannels:
            if not widget.controllerName:
                continue

            widget.setEnabled(widget.controllerName in controllers)


class ValueMRow(ValueGB):
    def __init__(self, moduleRow, key, title, ind, fmt, controllerName='', fontSize=styles.bigFont):
        ValueGB.__init__(self, moduleRow, key, title, ind, fmt, fontSize=fontSize)
        self.controllerName = controllerName


class SwitchMRow(SwitchGB):
    def __init__(self, moduleRow, key, title, ind, fmt, controllerName='', fontSize=styles.bigFont):
        SwitchGB.__init__(self, moduleRow, key, title, ind, fmt, fontSize=fontSize)
        self.controllerName = controllerName


class EnumMRow(EnumGB):
    def __init__(self, moduleRow, key, title, ind, fmt, controllerName='', fontSize=styles.bigFont):
        EnumGB.__init__(self, moduleRow, key, title, ind, fmt, fontSize=fontSize)
        self.controllerName = controllerName


class MonitorCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='MONITOR')

        self.period = SpinBoxGB('Period', 0, 120)
        self.period.setValue(15)

        self.addWidget(self.period, 0, 1)

    def buildCmd(self):
        cmdStr = '%s monitor controllers=%s period=%d' % (self.controlPanel.actorName,
                                                          self.controlPanel.controllerName,
                                                          self.period.getValue())

        return cmdStr