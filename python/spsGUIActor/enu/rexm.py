__author__ = 'alefur'

from spsGUIActor.common import ComboBox, CheckBox
from spsGUIActor.control import ControllerPanel, ControllerCmd
from spsGUIActor.widgets import ValueGB, CustomedCmd, AbortButton, DoubleSpinBoxGB
from spsGUIActor.enu import EnuDeviceCmd

class InitCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='INIT')

        self.skipHoming = CheckBox('skipHoming')
        self.skipHoming.setChecked(False)
        self.addWidget(self.skipHoming, 0, 1)

    def buildCmd(self):
        skipHoming = 'skipHoming' if self.skipHoming.isChecked() else ''
        return '%s rexm init %s' % (self.controlPanel.actorName, skipHoming)


class GoCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='GOTO')

        self.combo = ComboBox()
        self.combo.addItems(['low', 'med'])

        self.addWidget(self.combo, 0, 1)

    def buildCmd(self):
        cmdStr = '%s rexm %s ' % (self.controlPanel.actorName, self.combo.currentText())
        return cmdStr


class MoveCmd(CustomedCmd):
    limits = (0, 420, 1)

    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='MOVE')
        self.distSpinbox = DoubleSpinBoxGB('Relative(mm)', *self.limits)
        self.addWidget(self.distSpinbox, 0, 1)

    def buildCmd(self):
        cmdStr = '%s rexm move relative=%.1f' % (self.controlPanel.actorName, self.distSpinbox.getValue())
        return cmdStr


class RexmPanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'rexm')
        self.addCommandSet(RexmCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'rexmMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'rexmFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'rexmFSM', '', 1, '{:s}')
        self.position = ValueGB(self.moduleRow, 'rexm', 'Position', 0, '{:s}')

        self.switchA = ValueGB(self.moduleRow, 'rexmInfo', 'SwitchA', 0, '{:d}')
        self.switchB = ValueGB(self.moduleRow, 'rexmInfo', 'switchB', 1, '{:d}')
        self.speed = ValueGB(self.moduleRow, 'rexmInfo', 'Speed', 2, '{:d}')
        self.steps = ValueGB(self.moduleRow, 'rexmInfo', 'Steps', 3, '{:d}')

        self.usrs = ValueGB(self.moduleRow, 'rexmConfig', 'Step Resolution', 7, '{:d}')
        self.pulseDivisor = ValueGB(self.moduleRow, 'rexmConfig', 'Pulse Divisor', 10, '{:d}')

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)
        self.grid.addWidget(self.position, 0, 3)

        self.grid.addWidget(self.usrs, 1, 0)
        self.grid.addWidget(self.pulseDivisor, 1, 1)

        self.grid.addWidget(self.switchA, 2, 0)
        self.grid.addWidget(self.switchB, 2, 1)
        self.grid.addWidget(self.speed, 2, 2)
        self.grid.addWidget(self.steps, 2, 3)


class RexmCommands(EnuDeviceCmd):
    def __init__(self, controlPanel):
        EnuDeviceCmd.__init__(self, controlPanel)
        self.initButton = InitCmd(controlPanel=controlPanel)
        self.abortButton = AbortButton(controlPanel=controlPanel, cmdStr='%s rexm abort' % controlPanel.actorName)

        self.goCmd = GoCmd(controlPanel=controlPanel)
        self.moveCmd = MoveCmd(controlPanel=controlPanel)

        self.grid.addLayout(self.initButton, 1, 0, 1, 2)
        self.grid.addWidget(self.abortButton, 2, 2)
        self.grid.addLayout(self.goCmd, 2, 0, 1, 2)
        self.grid.addLayout(self.moveCmd, 3, 0, 1, 2)
