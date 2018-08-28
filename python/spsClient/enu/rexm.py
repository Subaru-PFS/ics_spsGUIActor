__author__ = 'alefur'

from spsClient.widgets import ValueGB, ControlPanel


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

        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)
        self.grid.addWidget(self.position, 0, 3)

        self.grid.addWidget(self.switchA, 1, 0)
        self.grid.addWidget(self.switchB, 1, 1)
        self.grid.addWidget(self.speed, 1, 2)
        self.grid.addWidget(self.steps, 1, 3)

        self.setChecked(False)
        self.showHide()
