__author__ = 'alefur'

from spsClient.dcb.aten import SwitchButton
from spsClient.widgets import ValueGB, ControlPanel, CmdButton, CustomedCmd, CommandsGB, SwitchGB, SpinBoxGB


class BiaPeriod(ValueGB):
    def __init__(self, moduleRow):
        self.spinbox = SpinBoxGB('Period', 0, 65536)
        ValueGB.__init__(self, moduleRow, 'biaConfig', '', 0, '{:d}')

    def setText(self, txt):
        if not self.spinbox.locked:
            self.spinbox.setValue(txt)

    def getValue(self):
        return self.spinbox.getValue()


class BiaDuty(ValueGB):
    def __init__(self, moduleRow):
        self.spinbox = SpinBoxGB('Duty', 0, 255)
        ValueGB.__init__(self, moduleRow, 'biaConfig', '', 1, '{:d}')

    def setText(self, txt):
        if not self.spinbox.locked:
            self.spinbox.setValue(txt)

    def getValue(self):
        return self.spinbox.getValue()


class SetBiaParamCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SET PARAMETERS')

        self.period = BiaPeriod(moduleRow=self.controlPanel.moduleRow)
        self.duty = BiaDuty(moduleRow=self.controlPanel.moduleRow)

        self.addWidget(self.period.spinbox, 0, 1)
        self.addWidget(self.duty.spinbox, 0, 2)

    def buildCmd(self):
        cmdStr = '%s bia config period=%i duty=%i ' % (self.controlPanel.actorName, self.period.getValue(),
                                                       self.duty.getValue())

        return cmdStr


class SwitchBia(SwitchButton):
    def __init__(self, controlPanel):
        SwitchButton.__init__(self, controlPanel=controlPanel, key='bia', label='BIA', fmt='{:s}',
                              cmdHead='%s bia' % controlPanel.actorName)

    def setText(self, txt):
        bool = True if txt in ['undef', 'on'] else False

        self.buttonOn.setVisible(not bool)
        self.buttonOff.setVisible(bool)


class BiaCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s bsh status' % controlPanel.actorName)
        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='%s connect controller=bsh' % controlPanel.actorName)

        self.switchBia = SwitchBia(controlPanel=controlPanel)

        self.switchStrobe = SwitchButton(controlPanel=controlPanel, key='biaStrobe', label='STROBE',
                                         cmdHead='%s bia strobe' % controlPanel.actorName)

        self.setBiaParam = SetBiaParamCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.connectButton, 0, 1)
        self.grid.addWidget(self.switchBia, 1, 0)
        self.grid.addWidget(self.switchStrobe, 1, 1)

        self.grid.addLayout(self.setBiaParam, 2, 0, 1, 3)
        #self.grid.addWidget(self.empty, 3, 0, 1, 3)

    @property
    def buttons(self):
        return [self.statusButton, self.connectButton, self.setBiaParam.button] \
               + self.switchBia.buttons + self.switchStrobe.buttons


class BiaPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

        self.mode = ValueGB(self.moduleRow, 'bshMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'bshFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'bshFSM', '', 1, '{:s}')

        self.bia = ValueGB(self.moduleRow, 'bia', 'BIA', 0, '{:s}')
        self.biaStrobe = SwitchGB(self.moduleRow, 'biaStrobe', 'Strobe', 0, '{:g}')

        self.biaPeriod = ValueGB(self.moduleRow, 'biaConfig', 'Bia-Period', 0, '{:d}')
        self.biaDuty = ValueGB(self.moduleRow, 'biaConfig', 'Bia-Duty', 1, '{:d}')

        self.commands = BiaCommands(self)
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.bia, 1, 0)
        self.grid.addWidget(self.biaStrobe, 1, 1)

        self.grid.addWidget(self.biaPeriod, 2, 0)
        self.grid.addWidget(self.biaDuty, 2, 1)

        self.grid.addWidget(self.empty, 3, 0, 2, 3)
        self.grid.addWidget(self.commands, 0, 3, 3.6, 3)