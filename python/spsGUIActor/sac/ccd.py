__author__ = 'alefur'

from spsGUIActor.common import ComboBox
from spsGUIActor.control import ControlPanel, CommandsGB
from spsGUIActor.widgets import ValueGB, DoubleSpinBoxGB, CmdButton, CustomedCmd


class Looptime(ValueGB):
    def __init__(self, ccdCmd):
        self.ccdCmd = ccdCmd
        ValueGB.__init__(self, ccdCmd.controlPanel.moduleRow, 'looptime', '', 0, '{:.2f}')

    def setText(self, txt):
        if float(txt) > 0:
            self.ccdCmd.stopLoop.setVisible(True)
            self.ccdCmd.startLoop.setVisible(False)
        else:
            self.ccdCmd.stopLoop.setVisible(False)
            self.ccdCmd.startLoop.setVisible(True)


class ExposeCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='EXPOSE')

        self.combo = ComboBox()
        self.combo.addItems(['object', 'background'])

        self.exptime = DoubleSpinBoxGB('exptime', 0, 3000, 2)

        self.addWidget(self.combo, 0, 1)
        self.addWidget(self.exptime, 0, 2)

    def buildCmd(self):
        exptype = 'expose' if self.combo.currentText() == 'object' else 'background'
        cmdStr = 'sac ccd %s exptime=%.2f' % (exptype, self.exptime.getValue())
        return cmdStr


class CcdPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)
        self.addCommandSet(CcdCommands(self))

    def createWidgets(self):
        self.state = ValueGB(self.moduleRow, 'ccd', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'ccd', '', 1, '{:s}')

    def setInLayout(self):
        self.grid.addWidget(self.state, 0, 0)
        self.grid.addWidget(self.substate, 0, 1)


class CcdCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS', cmdStr='sac ccd status')
        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT', cmdStr='sac ccd connect')
        self.exposeCmd = ExposeCmd(controlPanel=controlPanel)
        self.startLoop = CmdButton(controlPanel=controlPanel, label='START LOOP', cmdStr='sac ccd loop start')
        self.stopLoop = CmdButton(controlPanel=controlPanel, label='STOP LOOP', cmdStr='sac ccd loop stop')
        self.looptime = Looptime(self)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.connectButton, 0, 1)
        self.grid.addLayout(self.exposeCmd, 1, 0, 1, 3)
        self.grid.addWidget(self.startLoop, 2, 0)
        self.grid.addWidget(self.stopLoop, 2, 0)
