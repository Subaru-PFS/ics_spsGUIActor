__author__ = 'alefur'

from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB, SwitchGB, EnumGB, ControlDialog, ControlPanel, CommandsGB, CmdButton, \
    CustomedCmd, SpinBoxGB, QLabel


class DcbRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='dcb', actorLabel='DCB')

        self.state = ValueGB(self, 'metaFSM', '', 0, '{:s}')
        self.substate = ValueGB(self, 'metaFSM', '', 1, '{:s}')
        self.labsphere = EnumGB(self, 'pow_labsphere', 'Labsphere', 0, '{:s}')
        self.hgar = SwitchGB(self, 'hgar', 'Hg-Ar', 0, '{:g}')
        self.neon = SwitchGB(self, 'neon', 'Neon', 0, '{:g}')
        self.xenon = SwitchGB(self, 'xenon', 'Xenon', 0, '{:g}')
        self.halogen = SwitchGB(self, 'halogen', 'Halogen', 0, '{:g}')
        self.photodiode = ValueGB(self, 'photodiode', 'photodiode', 0, '{:g}')
        self.attenuator = ValueGB(self, 'attenuator', 'attenuator', 0, '{:g}')

    @property
    def customWidgets(self):
        return [self.state, self.substate, self.labsphere, self.hgar, self.neon, self.xenon, self.halogen,
                self.photodiode, self.attenuator]

    def showDetails(self):
        self.controlDialog = DcbDialog(self)
        self.controlDialog.show()


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


class LabspherePanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog, 'Labsphere')

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


class DcbDialog(ControlDialog):
    def __init__(self, sacRow):
        ControlDialog.__init__(self, moduleRow=sacRow)

        self.atenPanel = AtenPanel(self)
        self.labspherePanel = LabspherePanel(self)

        self.grid.addWidget(self.atenPanel, 0, 0)
        self.grid.addWidget(self.labspherePanel, 1, 0)

    @property
    def customWidgets(self):
        return self.atenPanel.customWidgets + self.labspherePanel.customWidgets
