__author__ = 'alefur'
from functools import partial

from spsGUIActor.common import CheckBox, LineEdit
from spsGUIActor.control import ControllerPanel, ControllerCmd
from spsGUIActor.widgets import ValueGB, CmdButton, CustomedCmd


class Status(ValueGB):
    def __init__(self, moduleRow):
        ValueGB.__init__(self, moduleRow, 'interlock', 'Status', 1, '{:s}')

    def setText(self, txt):
        ftext = [stat for stat in txt.split(',') if 'bit ' not in stat]
        self.value.setText('\n'.join(ftext))
        self.customize()

class InterlockPanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'interlock')
        self.addCommandSet(InterlockCommands(self))

    def createWidgets(self):
        self.pCryostat = ValueGB(self.moduleRow, 'interlockPressures', 'pCryostat(Torr)', 0, '{:g}')
        self.pRoughing = ValueGB(self.moduleRow, 'interlockPressures', 'pRoughing(Torr)', 1, '{:g}')
        self.status = Status(self.moduleRow)

    def setInLayout(self):
        self.grid.addWidget(self.pCryostat, 0, 0)
        self.grid.addWidget(self.pRoughing, 0, 1)
        self.grid.addWidget(self.status, 1, 0, 3, 2)


class RawCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='RAW')

        self.rawCmd = LineEdit()
        self.addWidget(self.rawCmd, 0, 1)

    def buildCmd(self):
        cmdStr = '%s interlock raw=%s' % (self.controlPanel.actorName, self.rawCmd.text())
        return cmdStr



class InterlockCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
        self.rawCmd = RawCmd(controlPanel=controlPanel)
        self.grid.addLayout(self.rawCmd, 1, 0, 1, 2)

