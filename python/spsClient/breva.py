__author__ = 'alefur'

import spsClient.styles as styles
from PyQt5.QtWidgets import QGridLayout
from spsClient.common import ComboBox
from spsClient.control import ControlPanel, CommandsGB, ControlDialog
from spsClient.modulerow import ModuleRow
from spsClient.widgets import Coordinates, SwitchGB, DoubleSpinBoxGB, CustomedCmd, CmdButton, ValueMRow


class MotorState(SwitchGB):
    def __init__(self, moduleRow):
        self.moduleRow = moduleRow
        SwitchGB.__init__(self, moduleRow, key='motors_on', title='MOTORS', ind=0, fmt='{:g}', fontSize=styles.bigFont)

    def setText(self, txt):
        SwitchGB.setText(self, txt)

        try:
            self.moduleRow.controlDialog.controlPanel.commands.setMotorState()
        except AttributeError:
            pass


class CoordBoxes(QGridLayout):
    def __init__(self):
        QGridLayout.__init__(self)
        self.widgets = [DoubleSpinBoxGB('X', -10, 10, 4),
                        DoubleSpinBoxGB('Y', -10, 10, 4),
                        DoubleSpinBoxGB('Z', -10, 10, 4),
                        DoubleSpinBoxGB('U', -10, 10, 4),
                        DoubleSpinBoxGB('V', -10, 10, 4),
                        DoubleSpinBoxGB('W', -5, 10, 4)]

        for i, spinbox in enumerate(self.widgets):
            self.addWidget(spinbox, i // 3, i % 3)


class MoveCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='MOVE')

        self.combo = ComboBox()
        self.combo.addItems(['abs', 'relo', 'relu'])
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
        labels = ['x', 'y', 'z', 'rx', 'ry', 'rz']
        values = [spinbox.getValue() for spinbox in self.spinboxes]

        cmdStr = 'breva move %s ' % self.combo.currentText()
        cmdStr += (" ".join(['%s=%.4f' % (label, value) for label, value in zip(labels, values)]))

        return cmdStr


class SetRepCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SET')

        self.combo = ComboBox()
        self.combo.addItems(['REPOBJ', 'REPUTIL'])
        self.combo.currentIndexChanged.connect(self.resetCoords)

        self.addWidget(self.combo, 0, 1)

    def resetCoords(self, ind):
        for spinbox in self.spinboxes:
            spinbox.setValue(0)

    @property
    def spinboxes(self):
        return self.controlPanel.commands.coordBoxes.widgets

    def buildCmd(self):
        labels = ['x', 'y', 'z', 'rx', 'ry', 'rz']
        values = [spinbox.getValue() for spinbox in self.spinboxes]

        cmdStr = 'breva set %s ' % self.combo.currentText().lower()
        cmdStr += (" ".join(['%s=%.4f' % (label, value) for label, value in zip(labels, values)]))

        return cmdStr


class GotoCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='GO TO')

        self.comboFiber = ComboBox()
        self.comboFiber.addItems(['engtopend', 'engtopmid', 'engbotmid', 'engbotend',
                                  'scitopend', 'scitopmid', 'scibotmid', 'scibotend'])

        self.addWidget(self.comboFiber, 0, 1)

    def buildCmd(self):
        cmdStr = 'breva goto fiber=%s ' % self.comboFiber.currentText()
        return cmdStr


class BrevaRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='breva', actorLabel='BREVA')

        self.state = ValueMRow(self, 'hexaFSM', '', 0, '{:s}')
        self.substate = ValueMRow(self, 'hexaFSM', '', 1, '{:s}')
        self.motorState = MotorState(self)
        self.error = ValueMRow(self, 'error', 'ERROR', 0, '{:g}',)
        self.fiberTargeted = ValueMRow(self, 'targetedFiber', 'Fiber', 0, '{:s}')
        self.createDialog(BrevaDialog(self))

    @property
    def widgets(self):
        return [self.state, self.substate, self.motorState, self.error, self.fiberTargeted]


class BrevaDialog(ControlDialog):
    def __init__(self, brevaRow):
        ControlDialog.__init__(self, moduleRow=brevaRow)
        self.controlPanel = BrevaPanel(self)
        self.tabWidget.addTab(self.controlPanel, '')


class BrevaPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)
        self.addCommandSet(BrevaCommands(self))

    def createWidgets(self):
        self.coordinates = Coordinates(self.moduleRow, 'position', title='Position')
        self.repobj = Coordinates(self.moduleRow, 'REPOBJ', title='REPOBJ')
        self.reputil = Coordinates(self.moduleRow, 'REPUTIL', title='REPUTIL')

    def setInLayout(self):
        self.grid.addWidget(self.coordinates, 0, 0, 1, 6)
        self.grid.addWidget(self.repobj, 1, 0, 1, 6)
        self.grid.addWidget(self.reputil, 2, 0, 1, 6)


class BrevaCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS', cmdStr='breva status')
        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='breva connect controller=hexa')
        self.initButton = CmdButton(controlPanel=controlPanel, label='INIT', cmdStr='breva init')
        self.motorsOn = CmdButton(controlPanel=controlPanel, label='MOTOR ON', cmdStr='breva motor on')
        self.motorsOff = CmdButton(controlPanel=controlPanel, label='MOTOR OFF', cmdStr='breva motor off')
        self.coordBoxes = CoordBoxes()

        self.moveCmd = MoveCmd(controlPanel=controlPanel)
        self.setRepCmd = SetRepCmd(controlPanel=controlPanel)
        self.gotoCmd = GotoCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.connectButton, 0, 1)
        self.grid.addWidget(self.initButton, 1, 0)
        self.grid.addWidget(self.motorsOn, 1, 1)
        self.grid.addWidget(self.motorsOff, 1, 1)
        self.grid.addLayout(self.moveCmd, 2, 0, 1, 2)
        self.grid.addLayout(self.setRepCmd, 3, 0, 1, 2)
        self.grid.addLayout(self.coordBoxes, 2, 2, 2, 3)
        self.grid.addLayout(self.gotoCmd, 4, 0, 1, 2)

        self.setMotorState()

    def setMotorState(self):
        state = self.controlPanel.controlDialog.moduleRow.motorState.value.text()

        if state == 'ON':
            self.motorsOn.setVisible(False)
            self.motorsOff.setVisible(True)
        else:
            self.motorsOn.setVisible(True)
            self.motorsOff.setVisible(False)
