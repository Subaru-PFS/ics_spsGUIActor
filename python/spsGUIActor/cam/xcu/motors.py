__author__ = 'alefur'
import spsGUIActor.styles as styles
from PyQt5.QtWidgets import QGroupBox, QGridLayout
from spsGUIActor.common import ComboBox, CheckBox, LineEdit
from spsGUIActor.control import CommandsGB, ControllerPanel
from spsGUIActor.widgets import ValueGB, CmdButton, CustomedCmd, DoubleSpinBoxGB, AbortButton


class MoveCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='MOVE')

        self.comboMotors = ComboBox()
        self.comboMotors.addItems(['piston', 'a', 'b', 'c'])
        self.distance = DoubleSpinBoxGB('Dist', -300, 300, 3)
        self.microns = CheckBox('microns')
        self.abs = CheckBox('abs')

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

        self.comboMotors = ComboBox()
        self.comboMotors.addItems(['All', 'Motor A', 'Motor B', 'Motor C'])

        self.addWidget(self.comboMotors, 0, 1)

    def buildCmd(self):
        motor = self.comboMotors.currentText()
        motor = 'a,b,c' if motor == 'All' else self.comboMotors.currentText()[-1].lower()

        cmdStr = '%s motors home axes=%s' % (self.controlPanel.actorName, motor)

        return cmdStr


class ToSwitchCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='TO SWITCH')

        self.comboMotors = ComboBox()
        self.comboMotors.addItems(['a', 'b', 'c'])

        self.comboSide = ComboBox()
        self.comboSide.addItems(['home', 'far'])

        self.comboCmd = ComboBox()
        self.comboCmd.addItems(['set', 'clear'])

        self.addWidget(self.comboMotors, 0, 1)
        self.addWidget(self.comboSide, 0, 2)
        self.addWidget(self.comboCmd, 0, 3)

    def buildCmd(self):
        cmdStr = '%s motors toSwitch %s %s %s' % (self.controlPanel.actorName,
                                                  self.comboMotors.currentText(),
                                                  self.comboSide.currentText(),
                                                  self.comboCmd.currentText())

        return cmdStr


class RawCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='RAW')

        self.rawCmd = LineEdit()
        self.addWidget(self.rawCmd, 0, 1)

    def buildCmd(self):
        cmdStr = '%s motors raw=%s' % (self.controlPanel.actorName, self.rawCmd.text())
        return cmdStr


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
                styles.smallFont) +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

    @property
    def widgets(self):
        return [self.status, self.homeSwitch, self.farSwitch, self.steps, self.position]


class MotorsPanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'PCM')
        self.addCommandSet(MotorsCommands(self))

    @property
    def motors(self):
        return [self.motorA, self.motorB, self.motorC]

    def createWidgets(self):
        self.motorA = CcdMotor(self.moduleRow, motorId=1)
        self.motorB = CcdMotor(self.moduleRow, motorId=2)
        self.motorC = CcdMotor(self.moduleRow, motorId=3)

    def setInLayout(self):
        for i, motor in enumerate(self.motors):
            self.grid.addWidget(motor, i, 0, 1, 5)


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
        self.toSwitchCmd = ToSwitchCmd(controlPanel=controlPanel)
        self.rawCmd = RawCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.initButton, 1, 0)
        self.grid.addWidget(self.abortButton, 1, 1)
        self.grid.addLayout(self.homeCmd, 2, 0, 1, 2)
        self.grid.addLayout(self.moveCmd, 3, 0, 1, 5)
        self.grid.addLayout(self.toSwitchCmd, 4, 0, 1, 5)
        self.grid.addLayout(self.rawCmd, 5, 0, 1, 5)

