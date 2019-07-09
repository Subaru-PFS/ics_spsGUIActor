__author__ = 'alefur'

from spsGUIActor.common import ComboBox, CheckBox, GridLayout
from spsGUIActor.control import ControllerPanel, ControllerCmd
from spsGUIActor.widgets import Coordinates, ValueGB, CmdButton, DoubleSpinBoxGB, CustomedCmd, AbortButton


class CoordBoxes(GridLayout):
    def __init__(self):
        GridLayout.__init__(self)
        self.widgets = [DoubleSpinBoxGB('X', -10, 10, 5),
                        DoubleSpinBoxGB('Y', -10, 10, 5),
                        DoubleSpinBoxGB('Z', -10, 10, 5),
                        DoubleSpinBoxGB('U', -2, 2, 5),
                        DoubleSpinBoxGB('V', -2, 2, 5),
                        DoubleSpinBoxGB('W', -2, 2, 5)]

        for i, spinbox in enumerate(self.widgets):
            self.addWidget(spinbox, i // 3, i % 3)

class InitCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='INIT')

        self.skipHoming = CheckBox('skipHoming')
        self.skipHoming.setChecked(False)
        self.addWidget(self.skipHoming, 0, 1)

    def buildCmd(self):
        skipHoming = 'skipHoming' if self.skipHoming.isChecked() else ''
        return '%s slit init %s' % (self.controlPanel.actorName, skipHoming)

class MoveCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='MOVE')

        self.combo = ComboBox()
        self.combo.addItems(['absolute', 'relative'])
        self.combo.currentIndexChanged.connect(self.resetCoords)

        self.addWidget(self.combo, 0, 1)

    @property
    def spinboxes(self):
        return self.controlPanel.commands.coordBoxes.widgets

    def resetCoords(self, ind):
        if ind == 0:
            vals = [float(valueGB.value.text()) for valueGB in self.controlPanel.coordinates.widgets]
        else:
            vals = 6 * [0]

        for spinbox, val in zip(self.spinboxes, vals):
            spinbox.setValue(val)

    def buildCmd(self):
        labels = ['X', 'Y', 'Z', 'U', 'V', 'W']
        values = [spinbox.getValue() for spinbox in self.spinboxes]

        cmdStr = '%s slit move %s ' % (self.controlPanel.actorName, self.combo.currentText())
        cmdStr += (" ".join(['%s=%.5f' % (label, value) for label, value in zip(labels, values)]))

        return cmdStr


class SetRepCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SET')

        self.combo = ComboBox()
        self.combo.addItems(['work', 'tool'])
        self.combo.currentIndexChanged.connect(self.resetCoords)

        self.addWidget(self.combo, 0, 1)

    def resetCoords(self, ind):
        for spinbox in self.spinboxes:
            spinbox.setValue(0)

    @property
    def spinboxes(self):
        return self.controlPanel.commands.coordBoxes.widgets

    def buildCmd(self):
        labels = ['X', 'Y', 'Z', 'U', 'V', 'W']
        values = [spinbox.getValue() for spinbox in self.spinboxes]

        cmdStr = '%s slit set %s ' % (self.controlPanel.actorName, self.combo.currentText().lower())
        cmdStr += (" ".join(['%s=%.5f' % (label, value) for label, value in zip(labels, values)]))

        return cmdStr


class SlitPanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'slit')
        self.addCommandSet(SlitCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'slitMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'slitFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'slitFSM', '', 1, '{:s}')
        self.info = ValueGB(self.moduleRow, 'hxpStatus', 'Info', 1, '{:s}')
        self.position = ValueGB(self.moduleRow, 'slitPosition', 'Position', 0, '{:s}')

        self.coordinates = Coordinates(self.moduleRow, 'slit', title='Position')
        self.work = Coordinates(self.moduleRow, 'slitWork', title='Work')
        self.tool = Coordinates(self.moduleRow, 'slitTool', title='Tool')

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)
        self.grid.addWidget(self.position, 0, 3)

        self.grid.addWidget(self.info, 1, 0, 1, 6)
        self.grid.addWidget(self.coordinates, 2, 0, 1, 6)
        self.grid.addWidget(self.work, 3, 0, 1, 6)
        self.grid.addWidget(self.tool, 4, 0, 1, 6)


class SlitCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
        self.initCmd = InitCmd(controlPanel=controlPanel)
        self.abortButton = AbortButton(controlPanel=controlPanel, cmdStr='%s slit abort' % controlPanel.actorName)
        self.goHomeButton = CmdButton(controlPanel=controlPanel, label='GO HOME',
                                      cmdStr='%s slit move home' % controlPanel.actorName)
        self.coordBoxes = CoordBoxes()

        self.moveCmd = MoveCmd(controlPanel=controlPanel)
        self.setRepCmd = SetRepCmd(controlPanel=controlPanel)

        self.grid.addLayout(self.initCmd, 1, 0, 1, 2)
        self.grid.addLayout(self.coordBoxes, 2, 0, 2, 3)
        self.grid.addLayout(self.moveCmd, 4, 0, 1, 2)
        self.grid.addWidget(self.abortButton, 4, 2)
        self.grid.addLayout(self.setRepCmd, 5, 0, 1, 2)
        self.grid.addWidget(self.goHomeButton, 6, 0, 1, 1)
