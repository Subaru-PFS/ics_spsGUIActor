__author__ = 'alefur'
from functools import partial

from spsClient.common import CheckBox
from spsClient.control import ControlPanel, CommandsGB
from spsClient.widgets import ValueGB, CmdButton, MonitorCmd, CustomedCmd


class OpenCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='OPEN', safetyCheck=True)

        self.atAtmosphere = CheckBox('atAtmosphere')
        self.underVacuum = CheckBox('underVacuum')

        self.atAtmosphere.setChecked(True)
        self.underVacuum.setChecked(False)

        self.atAtmosphere.stateChanged.connect(partial(self.stateChanged, self.underVacuum))
        self.underVacuum.stateChanged.connect(partial(self.stateChanged, self.atAtmosphere))

        self.addWidget(self.atAtmosphere, 0, 1)
        self.addWidget(self.underVacuum, 0, 2)

    def stateChanged(self, other, state):
        state = 2 if not state else 0
        other.blockSignals(True)
        other.setChecked(state)
        other.blockSignals(False)

    def buildCmd(self):
        atAtmosphere = 'atAtmosphere' if self.atAtmosphere.isChecked() else ''
        underVacuum = 'underVacuum' if self.underVacuum.isChecked() else ''

        return '%s gatevalve open %s %s' % (self.controlPanel.actorName, atAtmosphere, underVacuum)


class GVPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

    def createWidgets(self):
        self.position = ValueGB(self.moduleRow, 'gatevalve', 'Position', 1, '{:s}')
        self.controlState = ValueGB(self.moduleRow, 'gatevalve', 'controlState', 2, '{:s}')
        self.samPOW = ValueGB(self.moduleRow, 'sampower', 'SAM POWER', 0, '{:g}')

    def setInLayout(self):
        self.grid.addWidget(self.position, 0, 0)
        self.grid.addWidget(self.controlState, 0, 1)
        self.grid.addWidget(self.samPOW, 1, 0)

    def addCommandSet(self):
        self.commands = GVCommands(self)
        self.grid.addWidget(self.commands, 0, 4, 5, 3)


class GVCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s gatevalve status' % controlPanel.actorName)
        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='%s connect controller=gatevalve' % controlPanel.actorName)
        self.monitorCmd = MonitorCmd(controlPanel=controlPanel, controllerName='gatevalve')
        self.openCmd = OpenCmd(controlPanel=controlPanel)
        self.closeButton = CmdButton(controlPanel=controlPanel, label='CLOSE',
                                     cmdStr='%s gatevalve close' % controlPanel.actorName, safetyCheck=True)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.connectButton, 0, 1)
        self.grid.addLayout(self.monitorCmd, 1, 0, 1, 2)
        self.openCmd.addWidget(self.closeButton, 1, 0)
        self.grid.addLayout(self.openCmd, 2, 0, 1, 3)
