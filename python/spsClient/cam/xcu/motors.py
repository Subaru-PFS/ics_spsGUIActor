__author__ = 'alefur'
from PyQt5.QtWidgets import QComboBox, QGroupBox, QGridLayout, QCheckBox
from spsClient import smallFont
from spsClient.widgets import ValueGB, ControlPanel, CmdButton, CommandsGB, CustomedCmd, DoubleSpinBoxGB, AbortButton


class MoveCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='MOVE')

        self.comboMotors = QComboBox()
        self.comboMotors.addItems(['piston', 'a', 'b', 'c'])
        self.distance = DoubleSpinBoxGB('Dist', -300, 300, 3)
        self.microns = QCheckBox('microns')
        self.abs = QCheckBox('abs')

        self.microns.setChecked(True)
        self.abs.setChecked(True)

        self.addWidget(self.comboMotors, 0, 1)
        self.addWidget(self.distance, 0, 2)
        self.addWidget(self.microns, 0, 3)
        self.addWidget(self.abs, 0, 4)

    def buildCmd(self):
        microns = 'microns' if self.microns.isChecked() else ''
        abs = 'abs' if self.microns.isChecked() else ''

        cmdStr = '%s motors move %s=%.3f %s %s' % (self.controlPanel.actorName,
                                                   self.comboMotors.currentText(),
                                                   self.distance.getValue(),
                                                   microns,
                                                   abs)

        return cmdStr


class HomeCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='HOME')

        self.comboMotors = QComboBox()
        self.comboMotors.addItems(['All', 'Motor A', 'Motor B', 'Motor C'])

        self.addWidget(self.comboMotors, 0, 1)

    def buildCmd(self):
        motor = self.comboMotors.currentText()
        motor = 'a,b,c' if motor == 'All' else self.comboMotors.currentText()[-1].lower()

        cmdStr = '%s motors home axes=%s' % (self.controlPanel.actorName, motor)

        return cmdStr


class MotorsCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s motors status' % controlPanel.actorName)
        self.initButton = CmdButton(controlPanel=controlPanel, label='INIT',
                                    cmdStr='%s motors init' % controlPanel.actorName)

        self.abortButton = AbortButton(controlPanel=controlPanel, cmdStr='%s motors halt' % controlPanel.actorName)

        self.homeCmd = HomeCmd(controlPanel=controlPanel)
        self.moveCmd = MoveCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.initButton, 1, 0)
        self.grid.addWidget(self.abortButton, 1, 1)
        self.grid.addLayout(self.homeCmd, 2, 0, 1, 2)
        self.grid.addLayout(self.moveCmd, 3, 0, 1, 5)

    @property
    def buttons(self):
        return [self.statusButton, self.initButton, self.abortButton, self.homeCmd.button, self.moveCmd.button]


class CcdMotor(QGroupBox):
    motorNames = {1: 'A', 2: 'B', 3: 'C'}

    def __init__(self, moduleRow, motorId):
        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setTitle('Motor %s' % self.motorNames[motorId])
        self.status = ValueGB(moduleRow, 'ccdMotor%i' % motorId, 'status', 0, '{:s}')
        self.homeSwitch = ValueGB(moduleRow, 'ccdMotor%i' % motorId, 'homeSwitch', 1, '{:d}')
        self.farSwitch = ValueGB(moduleRow, 'ccdMotor%i' % motorId, 'farSwitch', 2, '{:d}')
        self.steps = ValueGB(moduleRow, 'ccdMotor%i' % motorId, 'steps', 3, '{:g}')
        self.position = ValueGB(moduleRow, 'ccdMotor%i' % motorId, 'position', 4, '{:.2f}')

        for j, widget in enumerate(self.widgets):
            self.grid.addWidget(widget, 0, j)

        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; border: 1px solid #d7d4d1;border-radius: 3px;margin-top: 1ex;} " % (
                smallFont) +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

    @property
    def widgets(self):
        return [self.status, self.homeSwitch, self.farSwitch, self.steps, self.position]


class MotorsPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

        self.motorA = CcdMotor(self.moduleRow, motorId=1)
        self.motorB = CcdMotor(self.moduleRow, motorId=2)
        self.motorC = CcdMotor(self.moduleRow, motorId=3)

        for i, motor in enumerate(self.motors):
            self.grid.addWidget(motor, i, 0, 1, 5)

        self.commands = MotorsCommands(self)

        self.grid.addWidget(self.commands, 0, 5, 4, 3)


    @property
    def motors(self):
        return [self.motorA, self.motorB, self.motorC]

    @property
    def customWidgets(self):
        return self.motorA.widgets + self.motorB.widgets + self.motorC.widgets
