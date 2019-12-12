__author__ = 'alefur'
from spsGUIActor.cam import CamDevice
from spsGUIActor.common import LineEdit, ComboBox
from spsGUIActor.control import CommandsGB
from spsGUIActor.widgets import ValueGB, CmdButton, CustomedCmd


class RawCmd(CustomedCmd):
    cmdLogic = {0: 'raw', 1: 'getRaw', 2: 'setRaw'}

    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='RAW')

        self.comboCmd = ComboBox()
        self.comboCmd.addItems(['', 'get', 'set'])
        self.rawCmd = LineEdit()

        self.addWidget(self.comboCmd, 0, 1)
        self.addWidget(self.rawCmd, 0, 2)

    def buildCmd(self):
        cmdStr = '%s gauge %s=%s' % (self.controlPanel.actorName,
                                     self.cmdLogic[self.comboCmd.currentIndex()],
                                     self.rawCmd.text())
        return cmdStr


class GaugePanel(CamDevice):
    def __init__(self, controlDialog, controllerName=None, label=None, maxWidth=390):
        controllerName = 'PCM' if controllerName is None else controllerName
        label = 'Ion Gauge' if label is None else label
        CamDevice.__init__(self, controlDialog, controllerName, label)
        self.addCommandSet(GaugeCommands(self))
        if maxWidth:
            self.setMaximumWidth(maxWidth)

    def createWidgets(self):
        self.pressure = ValueGB(self.moduleRow, 'pressure', 'Pressure(Torr)', 0, '{:g}')

    def setInLayout(self):
        self.grid.addWidget(self.pressure, 0, 0)


class GaugeCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s gauge status' % controlPanel.actorName)

        self.rawCmd = RawCmd(controlPanel)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addLayout(self.rawCmd, 1, 0)
