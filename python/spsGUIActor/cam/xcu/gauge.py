__author__ = 'alefur'
from spsGUIActor.control import CommandsGB, ControllerPanel
from spsGUIActor.widgets import ValueGB, CmdButton


class GaugePanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'PCM')
        self.addCommandSet(GaugeCommands(self))

    def createWidgets(self):
        self.pressure = ValueGB(self.moduleRow, 'pressure', 'Pressure(Torr)', 0, '{:g}')

    def setInLayout(self):
        self.grid.addWidget(self.pressure, 0, 0)


class GaugeCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s gauge status' % controlPanel.actorName)

        self.grid.addWidget(self.statusButton, 0, 0)
