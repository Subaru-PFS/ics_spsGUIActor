__author__ = 'alefur'
from spsClient.widgets import ValueGB, ControlPanel, CmdButton, CommandsGB, MonitorCmd


class GaugeCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s gauge status' % controlPanel.actorName)
        self.monitorCmd = MonitorCmd(controlPanel=controlPanel, controllerName='gauge')

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addLayout(self.monitorCmd, 1, 0, 1, 2)

    @property
    def buttons(self):
        return [self.statusButton, self.monitorCmd.button]


class GaugePanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

        self.pressure = ValueGB(self.moduleRow, 'pressure', 'Pressure(Torr)', 0, '{:g}')
        self.grid.addWidget(self.pressure, 0, 0)
        self.grid.addWidget(self.empty, 1, 0, 3, 1)

        self.commands = GaugeCommands(self)

        self.grid.addWidget(self.commands, 0, 5, 2, 2)