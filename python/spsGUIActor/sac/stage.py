__author__ = 'alefur'

from spsGUIActor.common import ComboBox
from spsGUIActor.control import ControlPanel, CommandsGB
from spsGUIActor.widgets import ValueGB, DoubleSpinBoxGB, CmdButton, CustomedCmd


class MoveCmd(CustomedCmd):
    limits = dict(penta=(-450, 450),
                  detector=(0, 12))

    def __init__(self, controlPanel, stage):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='MOVE')

        self.stage = stage
        l_bound, u_bound = MoveCmd.limits[stage]

        self.combo = ComboBox()
        self.combo.addItems(['abs', 'rel'])

        self.distSpinbox = DoubleSpinBoxGB('Dist', l_bound, u_bound, 3)

        self.addWidget(self.combo, 0, 1)
        self.addWidget(self.distSpinbox, 0, 2)

    def buildCmd(self):
        reference = '' if self.combo.currentText() == 'rel' else self.combo.currentText()
        cmdStr = 'sac move %s=%.2f %s' % (self.stage, self.distSpinbox.getValue(), reference)
        return cmdStr


class StagePanel(ControlPanel):
    def __init__(self, controlDialog, stage):
        self.stage = stage
        ControlPanel.__init__(self, controlDialog)
        self.addCommandSet(StageCommands(self, stage))

    def createWidgets(self):
        label = self.stage.capitalize()
        self.state = ValueGB(self.moduleRow, 'ls%s' % label, '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'ls%s' % label, '', 1, '{:s}')
        self.position = ValueGB(self.moduleRow, 'ls%s' % label, 'Position', 2, '{:.3f}')

    def setInLayout(self):
        self.grid.addWidget(self.state, 0, 0)
        self.grid.addWidget(self.substate, 0, 1)
        self.grid.addWidget(self.position, 0, 2)


class StageCommands(CommandsGB):
    def __init__(self, controlPanel, stage):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS', cmdStr='sac stages %s status' % stage)
        self.initButton = CmdButton(controlPanel=controlPanel, label='INIT', cmdStr='sac stages %s init' % stage)

        self.moveCmd = MoveCmd(controlPanel=controlPanel, stage=stage)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.initButton, 0, 1)
        self.grid.addLayout(self.moveCmd, 1, 0, 1, 3)
