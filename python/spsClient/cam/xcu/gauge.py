__author__ = 'alefur'
from spsClient.control import ControlPanel, CommandsGB
from spsClient.widgets import ValueGB, CmdButton, MonitorCmd


class GaugePanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

    def createWidgets(self):
        self.pressure = ValueGB(self.moduleRow, 'pressure', 'Pressure(Torr)', 0, '{:g}')

    def setInLayout(self):
        self.grid.addWidget(self.pressure, 0, 0)

    def addCommandSet(self):
        self.commands = GaugeCommands(self)
        self.grid.addWidget(self.commands, 0, 5, 4, 3)


class GaugeCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s gauge status' % controlPanel.actorName)
        self.monitorCmd = MonitorCmd(controlPanel=controlPanel, controllerName='gauge')

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addLayout(self.monitorCmd, 1, 0, 1, 2)
        self.grid.addWidget(self.emptySpace(100), 2, 0)
