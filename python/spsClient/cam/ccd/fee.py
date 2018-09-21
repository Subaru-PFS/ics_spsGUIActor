__author__ = 'alefur'
from spsClient.widgets import ValueGB, ControlPanel, CmdButton, CommandsGB, MonitorCmd


class FeeCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s status' % controlPanel.actorName)

        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='%s connect controller=fee' % controlPanel.actorName)

        self.monitorCmd = MonitorCmd(controlPanel=controlPanel, controllerName='temps')

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.connectButton, 0, 1)
        self.grid.addLayout(self.monitorCmd, 1, 0, 1, 2)

    @property
    def buttons(self):
        return [self.statusButton, self.connectButton, self.monitorCmd.button]


class FeePanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

        self.preamp = ValueGB(self.moduleRow, 'ccdTemps', 'Preamp', 0, '{:.2f}')
        self.ccd0 = ValueGB(self.moduleRow, 'ccdTemps', 'Ccd0', 1, '{:.2f}')
        self.ccd1 = ValueGB(self.moduleRow, 'ccdTemps', 'Ccd1', 2, '{:.2f}')

        self.commands = FeeCommands(self)

        self.grid.addWidget(self.preamp, 0, 0)
        self.grid.addWidget(self.ccd0, 0, 1)
        self.grid.addWidget(self.ccd1, 0, 2)

        self.grid.addWidget(self.commands, 0, 4, 4, 3)
