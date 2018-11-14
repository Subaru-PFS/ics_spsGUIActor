__author__ = 'alefur'
from spsClient import smallFont
from spsClient.widgets import ValueGB, SwitchGB, ControlPanel, CommandsGB, CmdButton, CustomedCmd, SpinBoxGB, \
    SwitchButton


class LabspherePanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

        self.mode = ValueGB(self.moduleRow, 'labsphereMode', '', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'labsphereFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'labsphereFSM', '', 1, '{:s}')

        self.halogen = SwitchGB(self.moduleRow, 'halogen', 'Halogen', 0, '{:s}')
        self.photodiode = ValueGB(self.moduleRow, 'photodiode', 'photodiode', 0, '{:g}')
        self.attenuator = AttenuatorValue(self.moduleRow)

        self.commands = LabsphereCommands(self)

        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.halogen, 1, 0)
        self.grid.addWidget(self.photodiode, 1, 1)
        self.grid.addWidget(self.attenuator, 1, 2)

        self.grid.addWidget(self.empty, 2, 0, 3, 3)
        self.grid.addWidget(self.commands, 0, 3, 5, 3)


class AttenuatorValue(ValueGB):
    def __init__(self, moduleRow, fontSize=smallFont):
        ValueGB.__init__(self, moduleRow, 'attenuator', 'attenuator', 0, '{:g}', fontSize=fontSize)

    def setText(self, txt):
        if txt == '0':
            txt = 'open'
        elif txt == '255':
            txt = 'closed'

        self.value.setText(txt)
        self.customize()


class AttenuatorCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET VALUE')

        self.value = SpinBoxGB('attenuator', 0, 255)
        self.addWidget(self.value, 0, 1)

    def buildCmd(self):
        cmdStr = 'dcb labsphere attenuator=%i' % self.value.getValue()
        return cmdStr


class SwitchHalogen(SwitchButton):
    def __init__(self, controlPanel):
        SwitchButton.__init__(self, controlPanel=controlPanel, key='halogen', label='Halogen', fmt='{:s}',
                              cmdHead='dcb labsphere halogen')

    def setText(self, txt):
        bool = True if txt in ['undef', 'on'] else False

        self.buttonOn.setVisible(not bool)
        self.buttonOff.setVisible(bool)


class LabsphereCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS', cmdStr='dcb labsphere status')
        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='dcb connect controller=labsphere')
        self.initButton = CmdButton(controlPanel=controlPanel, label='INIT', cmdStr='dcb labsphere init')
        self.attenuatorCmd = AttenuatorCmd(controlPanel=controlPanel)
        self.switchHalogen = SwitchHalogen(controlPanel=controlPanel)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.connectButton, 0, 1)

        self.grid.addWidget(self.initButton, 1, 0)
        self.grid.addLayout(self.attenuatorCmd, 2, 0, 1, 2)

        self.grid.addWidget(self.switchHalogen, 3, 0)

    @property
    def buttons(self):
        return [self.statusButton, self.connectButton, self.initButton, self.attenuatorCmd.button] \
               + self.switchHalogen.buttons
