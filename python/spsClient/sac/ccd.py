__author__ = 'alefur'
from PyQt5.QtWidgets import QComboBox
from spsClient.widgets import ValueGB, CommandsGB, ControlPanel, DoubleSpinBoxGB, CmdButton, CustomedCmd


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

        self.combo = QComboBox()
        self.combo.addItems(['object', 'background'])

        self.exptime = DoubleSpinBoxGB('exptime', 0, 300, 2)

        self.addWidget(self.combo, 0, 1)
        self.addWidget(self.exptime, 0, 2)

    def buildCmd(self):
        exptype = 'expose' if self.combo.currentText() == 'object' else 'background'
        cmdStr = 'sac ccd %s exptime=%.2f' % (exptype, self.exptime.getValue())

        return cmdStr


class CcdCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)

        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT', cmdStr='sac ccd connect')
        self.exposeCmd = ExposeCmd(controlPanel=controlPanel)
        self.startLoop = CmdButton(controlPanel=controlPanel, label='START LOOP', cmdStr='sac ccd loop start')
        self.stopLoop = CmdButton(controlPanel=controlPanel, label='STOP LOOP', cmdStr='sac ccd loop stop')
        self.looptime = Looptime(self)

        self.grid.addWidget(self.connectButton, 0, 0)
        self.grid.addLayout(self.exposeCmd, 1, 0, 1, 3)
        self.grid.addWidget(self.startLoop, 2, 0)
        self.grid.addWidget(self.stopLoop, 2, 0)

    @property
    def buttons(self):
        return [self.connectButton, self.exposeCmd.button, self.startLoop, self.stopLoop]


class CcdPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

        self.state = ValueGB(self.moduleRow, 'ccd', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'ccd', '', 1, '{:s}')

        self.commands = CcdCommands(self)

        self.grid.addWidget(self.state, 0, 0)
        self.grid.addWidget(self.substate, 0, 1)

        self.grid.addWidget(self.commands, 0, 2, 3, 3)

    @property
    def customWidgets(self):
        return [self.grid.itemAt(i).widget() for i in range(self.grid.count())] + self.commands.buttons
