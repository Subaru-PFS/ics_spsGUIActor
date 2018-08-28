__author__ = 'alefur'
from PyQt5.QtWidgets import QComboBox
from spsClient.widgets import ValueGB, ControlPanel, CmdButton, CustomedCmd, CommandsGB


class MoveCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='MOVE')

        self.combo = QComboBox()
        self.combo.addItems(['low', 'mid'])

        self.addWidget(self.combo, 0, 1)

    def buildCmd(self):
        cmdStr = '%s rexm move %s ' % (self.controlPanel.enuActor, self.combo.currentText())

        return cmdStr


class RexmCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)

        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='%s connect controller=rexm' % controlPanel.enuActor)
        self.initButton = CmdButton(controlPanel=controlPanel, label='INIT',
                                    cmdStr='%s rexm init' % controlPanel.enuActor)
        self.abortButton = CmdButton(controlPanel=controlPanel, label='ABORT',
                                     cmdStr='%s rexm abort' % controlPanel.enuActor)

        self.moveCmd = MoveCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.connectButton, 0, 0)
        self.grid.addWidget(self.initButton, 0, 1)
        self.grid.addWidget(self.abortButton, 0, 2)
        self.grid.addLayout(self.moveCmd, 1, 0, 1, 2)

    @property
    def buttons(self):
        return [self.connectButton, self.initButton, self.abortButton]


class RexmPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog, 'RDA')

        self.mode = ValueGB(self.moduleRow, 'rexmMode', 'Mode', 0, '{:s}', fontSize=9)
        self.state = ValueGB(self.moduleRow, 'rexmFSM', '', 0, '{:s}', fontSize=9)
        self.substate = ValueGB(self.moduleRow, 'rexmFSM', '', 1, '{:s}', fontSize=9)
        self.position = ValueGB(self.moduleRow, 'rexm', 'Position', 0, '{:s}', fontSize=9)

        self.switchA = ValueGB(self.moduleRow, 'rexmInfo', 'SwitchA', 0, '{:d}', fontSize=9)
        self.switchB = ValueGB(self.moduleRow, 'rexmInfo', 'switchB', 1, '{:d}', fontSize=9)
        self.speed = ValueGB(self.moduleRow, 'rexmInfo', 'Speed', 2, '{:d}', fontSize=9)
        self.steps = ValueGB(self.moduleRow, 'rexmInfo', 'Steps', 3, '{:d}', fontSize=9)

        self.commands = RexmCommands(self)

        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)
        self.grid.addWidget(self.position, 0, 3)

        self.grid.addWidget(self.switchA, 1, 0)
        self.grid.addWidget(self.switchB, 1, 1)
        self.grid.addWidget(self.speed, 1, 2)
        self.grid.addWidget(self.steps, 1, 3)

        self.grid.addWidget(self.commands, 0, 4, 2, 2)

        self.setChecked(False)
        self.showHide()

    @property
    def enuActor(self):
        return self.controlDialog.moduleRow.actorName

    @property
    def customWidgets(self):
        return [self.grid.itemAt(i).widget() for i in range(self.grid.count())] + self.commands.buttons
