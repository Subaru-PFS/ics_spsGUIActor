__author__ = 'alefur'

from spsClient.widgets import ValueGB, SwitchGB, EnumGB, ControlPanel, CommandsGB, CmdButton


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


class SwitchButton(SwitchGB):
    def __init__(self, controlPanel, key, label, ind=0, fmt='{:g}', cmdHead='dcb power', cmdTail='', safetyCheck=False):
        cmdTail = 'channel=%s' % key if not cmdTail else cmdTail
        cmdStrOn = '%s on %s' % (cmdHead, cmdTail)
        cmdStrOff = '%s off %s' % (cmdHead, cmdTail)

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

class SwitchLabsphere(SwitchButton):
    def __init__(self, controlPanel):
        SwitchButton.__init__(self, controlPanel=controlPanel, key='pow_labsphere', label='Labsphere', fmt='{:s}',
                              cmdTail='labsphere')

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
        self.switchMono = SwitchButton(controlPanel=controlPanel, key='pow_mono', label='Monochromator')
        self.switchRoughpump = SwitchButton(controlPanel=controlPanel, key='roughpump', label='RoughPump',
                                            safetyCheck=True)

        self.switchNeon = SwitchButton(controlPanel=controlPanel, key='neon', label='Neon', )
        self.switchXenon = SwitchButton(controlPanel=controlPanel, key='xenon', label='Xenon')
        self.switchHgar = SwitchButton(controlPanel=controlPanel, key='hgar', label='Hg-Ar')
        self.switchKrypton = SwitchButton(controlPanel=controlPanel, key='krypton', label='Krypton')

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
