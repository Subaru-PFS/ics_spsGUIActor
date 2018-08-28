__author__ = 'alefur'

from spsClient.widgets import ValueGB, SwitchGB, EnumGB, ControlPanel, CommandsGB, CmdButton


class AtenPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog, 'Aten')

        self.mode = ValueGB(self.moduleRow, 'atenMode', '', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'atenFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'atenFSM', '', 1, '{:s}')

        self.labsphere = EnumGB(self.moduleRow, 'pow_labsphere', 'Labsphere', 0, '{:s}')
        self.sac = SwitchGB(self.moduleRow, 'sac', 'Sac', 0, '{:g}')
        self.breva = SwitchGB(self.moduleRow, 'breva', 'Breva', 0, '{:g}')

        self.hgar = SwitchGB(self.moduleRow, 'hgar', 'Hg-Ar', 0, '{:g}')
        self.neon = SwitchGB(self.moduleRow, 'neon', 'Neon', 0, '{:g}')
        self.xenon = SwitchGB(self.moduleRow, 'xenon', 'Xenon', 0, '{:g}')
        self.krypton = SwitchGB(self.moduleRow, 'krypton', 'Krypton', 0, '{:g}')

        self.bakeout = SwitchGB(self.moduleRow, 'bakeout', 'Bakeout', 0, '{:g}')
        self.roughpump = SwitchGB(self.moduleRow, 'roughpump', 'Roughpump', 0, '{:g}')

        self.voltage = ValueGB(self.moduleRow, 'atenVAW', 'Voltage', 0, '{:.2f}')
        self.current = ValueGB(self.moduleRow, 'atenVAW', 'Current', 1, '{:.2f}')
        self.power = ValueGB(self.moduleRow, 'atenVAW', 'Power', 2, '{:.2f}')

        self.commands = AtenCommands(self)

        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.labsphere, 1, 0)
        self.grid.addWidget(self.sac, 1, 1)
        self.grid.addWidget(self.breva, 1, 2)

        self.grid.addWidget(self.hgar, 2, 0)
        self.grid.addWidget(self.neon, 2, 1)
        self.grid.addWidget(self.xenon, 2, 2)
        self.grid.addWidget(self.krypton, 2, 3)

        self.grid.addWidget(self.bakeout, 3, 0)
        self.grid.addWidget(self.roughpump, 3, 1)

        self.grid.addWidget(self.voltage, 4, 0)
        self.grid.addWidget(self.current, 4, 1)
        self.grid.addWidget(self.power, 4, 2)

        self.grid.addWidget(self.commands, 0, 4, 4, 3)

    @property
    def customWidgets(self):
        return [self.grid.itemAt(i).widget() for i in range(self.grid.count())] + self.commands.buttons


class SwitchButton(SwitchGB):
    def __init__(self, controlPanel, key, label, ind=0, fmt='{:g}', cmdHead='dcb power', cmdTail=''):
        cmdTail = 'channel=%s' % key if not cmdTail else cmdTail
        cmdStrOn = '%s on %s' % (cmdHead, cmdTail)
        cmdStrOff = '%s off %s' % (cmdHead, cmdTail)

        self.buttonOn = CmdButton(controlPanel=controlPanel, label='%s ON' % label, cmdStr=cmdStrOn)
        self.buttonOff = CmdButton(controlPanel=controlPanel, label='%s OFF' % label, cmdStr=cmdStrOff)

        ValueGB.__init__(self, controlPanel.moduleRow, key=key, title='', ind=ind, fmt=fmt)

    @property
    def buttons(self):
        return [self.buttonOn, self.buttonOff]

    def setText(self, txt):
        try:
            self.buttonOn.setVisible(not int(txt))
            self.buttonOff.setVisible(int(txt))

        except ValueError:
            pass

    def setGrid(self, grid, row, col):
        grid.addWidget(self.buttonOn, row, col)
        grid.addWidget(self.buttonOff, row, col)


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
        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT', cmdStr='dcb connect controller=aten')

        self.switchLabsphere = SwitchLabsphere(controlPanel=controlPanel)
        self.switchSac = SwitchButton(controlPanel=controlPanel, key='sac', label='Sac')
        self.switchBreva = SwitchButton(controlPanel=controlPanel, key='breva', label='Breva')

        self.switchHgar = SwitchButton(controlPanel=controlPanel, key='hgar', label='Hg-Ar')
        self.switchNeon = SwitchButton(controlPanel=controlPanel, key='neon', label='Neon', )
        self.switchXenon = SwitchButton(controlPanel=controlPanel, key='xenon', label='Xenon')
        self.switchKrypton = SwitchButton(controlPanel=controlPanel, key='krypton', label='Krypton')

        self.switchBakeout = SwitchButton(controlPanel=controlPanel, key='bakeout', label='Bakeout')
        self.switchRoughpump = SwitchButton(controlPanel=controlPanel, key='roughpump', label='RoughPump')

        self.grid.addWidget(self.connectButton, 0, 0)

        self.switchLabsphere.setGrid(self.grid, 1, 0)
        self.switchSac.setGrid(self.grid, 1, 1)
        self.switchBreva.setGrid(self.grid, 1, 2)

        self.switchHgar.setGrid(self.grid, 2, 0)
        self.switchNeon.setGrid(self.grid, 2, 1)
        self.switchXenon.setGrid(self.grid, 2, 2)
        self.switchKrypton.setGrid(self.grid, 2, 3)

        self.switchBakeout.setGrid(self.grid, 3, 0)
        self.switchRoughpump.setGrid(self.grid, 3, 1)

    @property
    def buttons(self):
        return [self.connectButton] + self.switchLabsphere.buttons + self.switchSac.buttons + \
               self.switchBreva.buttons + self.switchBakeout.buttons + self.switchHgar.buttons + \
               self.switchNeon.buttons + self.switchXenon.buttons + self.switchKrypton.buttons
