__author__ = 'alefur'
from spsGUIActor.common import LineEdit
from spsGUIActor.control import CommandsGB, ControllerPanel
from spsGUIActor.widgets import ValueGB, CmdButton, CustomedCmd


class SetRawCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SET RAW')

        self.rawCmd = LineEdit()
        self.addWidget(self.rawCmd, 0, 1)

    def buildCmd(self):
        cmdStr = '%s setRaw=%s' % (self.controlPanel.actorName,
                                   self.rawCmd.text())
        return cmdStr


class GetRawCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='GET RAW')

        self.rawCmd = LineEdit()
        self.addWidget(self.rawCmd, 0, 1)

    def buildCmd(self):
        cmdStr = '%s getRaw=%s' % (self.controlPanel.actorName,
                                   self.rawCmd.text())
        return cmdStr


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

        self.getRawCmd = GetRawCmd(controlPanel)
        self.setRawCmd = SetRawCmd(controlPanel)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addLayout(self.getRawCmd, 1, 0)
        self.grid.addLayout(self.setRawCmd, 2, 0)

