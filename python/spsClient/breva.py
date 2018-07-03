__author__ = 'alefur'

from PyQt5.QtWidgets import QComboBox, QGridLayout
from spsClient.modulerow import ModuleRow
from spsClient.widgets import Coordinates, ValueGB, CommandsGB, ControlDialog, ControlPannel, CmdButton, DoubleSpinBoxGB


class BrevaCommands(CommandsGB):
    def __init__(self, controlPannel):
        CommandsGB.__init__(self, controlPannel)
        self.initButton = InitButton(controlPannel=controlPannel)
        self.motorsOn = MotorsOn(controlPannel=controlPannel)
        self.motorsOff = MotorsOff(controlPannel=controlPannel)

        self.moveCmd = MoveCmd(controlPannel=controlPannel)
        self.gotoCmd = GotoCmd(controlPannel=controlPannel)

        self.grid.addWidget(self.initButton, 0, 0)
        self.grid.addWidget(self.motorsOn, 0, 1)
        self.grid.addWidget(self.motorsOff, 0, 1)
        self.grid.addLayout(self.moveCmd, 1, 0, 2, 7)
        self.grid.addLayout(self.gotoCmd, 3, 0, 1, 2)

        self.setMotorState()

    def setMotorState(self):
        state = self.controlPannel.controlDialog.moduleRow.motorState.value.text()

        if state == 'ON':
            self.motorsOn.setVisible(False)
            self.motorsOff.setVisible(True)
        else:
            self.motorsOn.setVisible(True)
            self.motorsOff.setVisible(False)

    @property
    def buttons(self):
        return [self.initButton, self.motorsOn, self.motorsOff, self.moveCmd.button, self.gotoCmd.button]


class MoveCmd(QGridLayout):
    def __init__(self, controlPannel):
        QGridLayout.__init__(self)
        self.controlPannel = controlPannel

        self.spinboxes = [DoubleSpinBoxGB('X', -10, 10, 4),
                          DoubleSpinBoxGB('Y', -10, 10, 4),
                          DoubleSpinBoxGB('Z', -10, 10, 4),
                          DoubleSpinBoxGB('U', -10, 10, 4),
                          DoubleSpinBoxGB('V', -10, 10, 4),
                          DoubleSpinBoxGB('W', -5, 10, 4)]

        self.combo = QComboBox()
        self.combo.addItems(['abs', 'relo', 'relu'])
        self.combo.currentIndexChanged.connect(self.resetCoords)

        self.button = MoveButton(self)

        self.addWidget(self.combo, 0, 0)
        for i, spinbox in enumerate(self.spinboxes):
            self.addWidget(spinbox, i // 3, i % 3 + 1)

        self.addWidget(self.button, 1, 0)

    def resetCoords(self, ind):
        if ind == 0:
            vals = [float(valueGB.value.text()) for valueGB in self.controlPannel.coordinates.widgets]
        else:
            vals = 6 * [0]

        for spinbox, val in zip(self.spinboxes, vals):
            spinbox.setValue(val)

    def buildCmd(self):
        labels = ['x', 'y', 'z', 'rx', 'ry', 'rz']
        values = [spinbox.getValue() for spinbox in self.spinboxes]

        cmdStr = 'breva move %s ' % self.combo.currentText()
        cmdStr += (" ".join(['%s=%.4f' % (label, value) for label, value in zip(labels, values)]))

        return cmdStr


class MoveButton(CmdButton):
    def __init__(self, moveCmd):
        self.moveCmd = moveCmd
        CmdButton.__init__(self, controlPannel=moveCmd.controlPannel, label='MOVE')

    def getCommand(self):
        if self.isChecked():
            cmdStr = self.moveCmd.buildCmd()
            self.controlDialog.addCommand(button=self, cmdStr=cmdStr)
        else:
            self.controlDialog.clearCommand(button=self)


class GotoCmd(QGridLayout):
    def __init__(self, controlPannel):
        QGridLayout.__init__(self)
        self.controlPannel = controlPannel

        self.comboFiber = QComboBox()
        self.comboFiber.addItems(['topend', 'topmid', 'botmid', 'botend'])

        self.button = GotoButton(self)

        self.addWidget(self.button, 0, 0)
        self.addWidget(self.comboFiber, 0, 1)

    def buildCmd(self):
        cmdStr = 'breva goto %s ' % self.comboFiber.currentText()

        return cmdStr


class GotoButton(CmdButton):
    def __init__(self, gotoCmd):
        self.gotoCmd = gotoCmd
        CmdButton.__init__(self, controlPannel=gotoCmd.controlPannel, label='GO TO')

    def getCommand(self):
        if self.isChecked():
            cmdStr = self.gotoCmd.buildCmd()
            self.controlDialog.addCommand(button=self, cmdStr=cmdStr)
        else:
            self.controlDialog.clearCommand(button=self)


class MotorsOn(CmdButton):
    def __init__(self, controlPannel):
        CmdButton.__init__(self, controlPannel=controlPannel, label='MOTORS ON')
        self.setVisible(False)

    def getCommand(self):
        if self.isChecked():
            self.controlDialog.addCommand(button=self, cmdStr='breva motor on')
        else:
            self.controlDialog.clearCommand(button=self)


class MotorsOff(CmdButton):
    def __init__(self, controlPannel):
        CmdButton.__init__(self, controlPannel=controlPannel, label='MOTORS OFF')

    def getCommand(self):
        if self.isChecked():
            self.controlDialog.addCommand(button=self, cmdStr='breva motor off')
        else:
            self.controlDialog.clearCommand(button=self)


class InitButton(CmdButton):
    def __init__(self, controlPannel):
        CmdButton.__init__(self, controlPannel=controlPannel, label='INIT')

    def getCommand(self):
        if self.isChecked():
            self.controlDialog.addCommand(button=self, cmdStr='breva init')
        else:
            self.controlDialog.clearCommand(button=self)


class BrevaPannel(ControlPannel):
    def __init__(self, controlDialog):
        ControlPannel.__init__(self, controlDialog, title='breva')

        self.coordinates = Coordinates(self.moduleRow, 'position', title='Position', fontSize=9)
        self.repobj = Coordinates(self.moduleRow, 'REPOBJ', title='REPOBJ', fontSize=9)
        self.reputil = Coordinates(self.moduleRow, 'REPUTIL', title='REPUTIL', fontSize=9)
        self.commands = BrevaCommands(self)

        self.grid.addWidget(self.coordinates, 0, 0, 1, 6)
        self.grid.addWidget(self.repobj, 1, 0, 1, 6)
        self.grid.addWidget(self.reputil, 2, 0, 1, 6)
        self.grid.addWidget(self.commands, 0, 7, 3, 6)

    @property
    def customWidgets(self):
        return self.coordinates.widgets + self.repobj.widgets + self.reputil.widgets + self.commands.buttons


class BrevaDialog(ControlDialog):
    def __init__(self, brevaRow):
        ControlDialog.__init__(self, moduleRow=brevaRow)
        self.controlPannel = BrevaPannel(self)
        self.grid.addWidget(self.controlPannel, 0, 0)

    @property
    def customWidgets(self):
        return self.controlPannel.customWidgets


class BrevaRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='breva', actorLabel='BREVA')

        self.state = ValueGB(self, 'hexaFSM', '', 0, '{:s}')
        self.substate = ValueGB(self, 'hexaFSM', '', 1, '{:s}')
        self.motorState = MotorState(self)
        self.fiberTargeted = ValueGB(self, 'targetedFiber', 'Targeted Fiber', 0, '{:s}')

    @property
    def customWidgets(self):
        widgets = [self.state, self.substate, self.motorState, self.fiberTargeted]

        try:
            widgets += self.controlDialog.customWidgets
        except AttributeError:
            pass

        return widgets

    def showDetails(self):
        self.controlDialog = BrevaDialog(self)
        self.controlDialog.show()


class MotorState(ValueGB):
    def __init__(self, moduleRow):
        self.moduleRow = moduleRow
        ValueGB.__init__(self, moduleRow, key='motors_on', title='MOTORS', ind=0, fmt='{:g}')

    def setText(self, txt):
        try:
            txt = 'ON' if int(txt) else 'OFF'

        except ValueError:
            pass

        self.value.setText(txt)

        try:
            self.moduleRow.controlDialog.controlPannel.commands.setMotorState()
        except AttributeError:
            pass

        self.customize()
