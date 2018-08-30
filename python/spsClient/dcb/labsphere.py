__author__ = 'alefur'

from spsClient.dcb.aten import SwitchButton
from spsClient.widgets import ValueGB, SwitchGB, ControlPanel, CommandsGB, CmdButton, CustomedCmd, SpinBoxGB


class LabspherePanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

        self.mode = ValueGB(self.moduleRow, 'labsphereMode', '', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'labsphereFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'labsphereFSM', '', 1, '{:s}')

        self.halogen = SwitchGB(self.moduleRow, 'halogen', 'Halogen', 0, '{:g}')
        self.photodiode = ValueGB(self.moduleRow, 'photodiode', 'photodiode', 0, '{:g}')
        self.attenuator = ValueGB(self.moduleRow, 'attenuator', 'attenuator', 0, '{:g}')

        self.commands = LabsphereCommands(self)

        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.halogen, 1, 0)
        self.grid.addWidget(self.photodiode, 1, 1)
        self.grid.addWidget(self.attenuator, 1, 2)

        self.grid.addWidget(self.commands, 0, 3, 3, 3)

    @property
    def customWidgets(self):
        return [self.grid.itemAt(i).widget() for i in range(self.grid.count())] + self.commands.buttons


class AttenuatorCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET VALUE')

        self.value = SpinBoxGB('attenuator', 0, 255)

        self.addWidget(self.value, 0, 1)

    def buildCmd(self):
        cmdStr = 'dcb labsphere attenuator=%i' % self.value.getValue()
        return cmdStr


class LabsphereCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='dcb connect controller=labsphere')
        self.initButton = CmdButton(controlPanel=controlPanel, label='INIT', cmdStr='dcb labsphere init')
        self.attenuatorCmd = AttenuatorCmd(controlPanel=controlPanel)
        self.switchHalogen = SwitchButton(controlPanel=controlPanel, key='halogen', label='Halogen',
                                          cmdHead='dcb labsphere switch', cmdTail=' ')

        self.grid.addWidget(self.connectButton, 0, 0)
        self.grid.addWidget(self.initButton, 0, 1)
        self.grid.addLayout(self.attenuatorCmd, 1, 0, 1, 2)

        self.switchHalogen.setGrid(self.grid, 2, 0)

    @property
    def buttons(self):
        return [self.connectButton, self.initButton, self.attenuatorCmd.button] + self.switchHalogen.buttons
