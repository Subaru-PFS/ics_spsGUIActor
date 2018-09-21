__author__ = 'alefur'

from spsClient.widgets import ValueGB, SwitchGB, EnumGB, ControlPanel, CommandsGB, CmdButton, SwitchButton


class AtenPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

        self.mode = ValueGB(self.moduleRow, 'atenMode', '', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'atenFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'atenFSM', '', 1, '{:s}')

        self.labsphere = EnumGB(self.moduleRow, 'pow_labsphere', 'Labsphere', 0, '{:s}')
        self.mono = SwitchGB(self.moduleRow, 'pow_mono', 'Monochromator', 0, '{:g}')
        self.roughpump = SwitchGB(self.moduleRow, 'roughpump', 'Roughpump', 0, '{:g}')

        self.neon = SwitchGB(self.moduleRow, 'neon', 'Neon', 0, '{:g}')
        self.xenon = SwitchGB(self.moduleRow, 'xenon', 'Xenon', 0, '{:g}')
        self.hgar = SwitchGB(self.moduleRow, 'hgar', 'Hg-Ar', 0, '{:g}')
        self.krypton = SwitchGB(self.moduleRow, 'krypton', 'Krypton', 0, '{:g}')

        # self.sac = SwitchGB(self.moduleRow, 'sac', 'Sac', 0, '{:g}')
        # self.breva = SwitchGB(self.moduleRow, 'breva', 'Breva', 0, '{:g}')
        # self.bakeout = SwitchGB(self.moduleRow, 'bakeout', 'Bakeout', 0, '{:g}')

        self.voltage = ValueGB(self.moduleRow, 'atenVAW', 'Voltage', 0, '{:.2f}')
        self.current = ValueGB(self.moduleRow, 'atenVAW', 'Current', 1, '{:.2f}')
        self.power = ValueGB(self.moduleRow, 'atenVAW', 'Power', 2, '{:.2f}')

        self.commands = AtenCommands(self)

        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.voltage, 1, 0)
        self.grid.addWidget(self.current, 1, 1)
        self.grid.addWidget(self.power, 1, 2)

        self.grid.addWidget(self.labsphere, 2, 0)
        self.grid.addWidget(self.mono, 3, 0)
        self.grid.addWidget(self.roughpump, 4, 0)

        self.grid.addWidget(self.neon, 2, 1)
        self.grid.addWidget(self.xenon, 2, 2)
        self.grid.addWidget(self.hgar, 3, 1)
        self.grid.addWidget(self.krypton, 3, 2)

        self.grid.addWidget(self.commands, 0, 3, 5, 4)


class AtenButton(SwitchButton):
    def __init__(self, controlPanel, key, label, safetyCheck=False):
        cmdStrOn = 'dcb power on=%s' % key
        cmdStrOff = 'dcb power off=%s' % key
        SwitchButton.__init__(self, controlPanel=controlPanel, key=key, label=label, cmdHead='', cmdStrOn=cmdStrOn,
                              cmdStrOff=cmdStrOff, safetyCheck=safetyCheck)


class SwitchLabsphere(SwitchButton):
    def __init__(self, controlPanel):
        cmdStrOn = 'dcb power on=labsphere'
        cmdStrOff = 'dcb power off=labsphere'
        SwitchButton.__init__(self, controlPanel=controlPanel, key='pow_labsphere', label='Labsphere', fmt='{:s}',
                              cmdHead='', cmdStrOn=cmdStrOn, cmdStrOff=cmdStrOff, safetyCheck=False)

    def setText(self, txt):
        bool = True if txt in ['undef', 'on'] else False

        self.buttonOn.setVisible(not bool)
        self.buttonOff.setVisible(bool)


class AtenCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS', cmdStr='dcb aten status')
        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT', cmdStr='dcb connect controller=aten')

        self.switchLabsphere = SwitchLabsphere(controlPanel=controlPanel)
        self.switchMono = AtenButton(controlPanel=controlPanel, key='pow_mono', label='Monochromator')
        self.switchRoughpump = AtenButton(controlPanel=controlPanel, key='roughpump', label='RoughPump',
                                          safetyCheck=True)

        self.switchNeon = AtenButton(controlPanel=controlPanel, key='neon', label='Neon', )
        self.switchXenon = AtenButton(controlPanel=controlPanel, key='xenon', label='Xenon')
        self.switchHgar = AtenButton(controlPanel=controlPanel, key='hgar', label='Hg-Ar')
        self.switchKrypton = AtenButton(controlPanel=controlPanel, key='krypton', label='Krypton')

        # self.switchSac = SwitchButton(controlPanel=controlPanel, key='sac', label='Sac')
        # self.switchBreva = SwitchButton(controlPanel=controlPanel, key='breva', label='Breva')
        # self.switchBakeout = SwitchButton(controlPanel=controlPanel, key='bakeout', label='Bakeout')

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.connectButton, 0, 1)

        self.grid.addWidget(self.switchLabsphere, 1, 0)
        self.grid.addWidget(self.switchMono, 2, 0)
        self.grid.addWidget(self.switchRoughpump, 3, 0)

        self.grid.addWidget(self.switchNeon, 1, 1)
        self.grid.addWidget(self.switchXenon, 1, 2)

        self.grid.addWidget(self.switchHgar, 2, 1)
        self.grid.addWidget(self.switchKrypton, 2, 2)

    @property
    def buttons(self):
        return [self.statusButton, self.connectButton] + self.switchLabsphere.buttons + self.switchMono.buttons + \
               self.switchRoughpump.buttons + self.switchNeon.buttons + self.switchXenon.buttons + \
               self.switchHgar.buttons + self.switchKrypton.buttons
