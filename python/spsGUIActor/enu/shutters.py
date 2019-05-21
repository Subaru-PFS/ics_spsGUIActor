__author__ = 'alefur'

import spsGUIActor.styles as styles
from spsGUIActor.common import ComboBox
from spsGUIActor.control import ControllerPanel, ControllerCmd
from spsGUIActor.widgets import ValueGB, CustomedCmd, DoubleSpinBoxGB, AbortButton, ValuesRow


class ShutterCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SHUTTERS')

        self.comboMove = ComboBox()
        self.comboMove.addItems(['open', 'close'])

        self.comboShut = ComboBox()
        self.comboShut.addItems(['', 'blue', 'red'])

        self.addWidget(self.comboMove, 0, 1)
        self.addWidget(self.comboShut, 0, 2)

    def buildCmd(self):
        cmdStr = '%s shutters %s %s' % (self.controlPanel.actorName,
                                        self.comboMove.currentText(),
                                        self.comboShut.currentText())
        return cmdStr


class ExposeCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='EXPOSE')

        self.exptime = DoubleSpinBoxGB('Exptime', 1, 10000, 1)

        self.comboShut = ComboBox()
        self.comboShut.addItems(['', 'blue', 'red'])

        self.addWidget(self.exptime, 0, 1)
        self.addWidget(self.comboShut, 0, 2)

    def buildCmd(self):
        cmdStr = '%s shutters expose exptime=%.1f %s' % (self.controlPanel.actorName,
                                                         self.exptime.getValue(),
                                                         self.comboShut.currentText())
        return cmdStr


class Coordinates(ValuesRow):
    posName = ['X', 'Y', 'Z', 'U', 'V', 'W']

    def __init__(self, moduleRow, key, title, fontSize=styles.smallFont):
        widgets = [ValueGB(moduleRow, key, c, i, '{:.5f}', fontSize) for i, c in enumerate(Coordinates.posName)]
        ValuesRow.__init__(self, widgets, title=title, fontSize=fontSize)


class Shutter(ValuesRow):
    shutterName = {'shb': 'Blue Shutter', 'shr': 'Red Shutter'}

    def __init__(self, moduleRow, shId):
        widgets = [ValueGB(moduleRow, shId, 'open', 0, '{:d}'),
                   ValueGB(moduleRow, shId, 'close', 1, '{:d}'),
                   ValueGB(moduleRow, shId, 'error', 2, '{:d}')]

        ValuesRow.__init__(self, widgets, title=self.shutterName[shId])



class ShuttersPanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'biasha')
        self.addCommandSet(ShuttersCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'biashaMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'biashaFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'biashaFSM', '', 1, '{:s}')

        self.shutters = ValueGB(self.moduleRow, 'shutters', 'Shutters', 0, '{:s}')
        self.exptime = ValueGB(self.moduleRow, 'integratingTime', 'Exptime', 0, '{:.1f}')
        self.elapsedTime = ValueGB(self.moduleRow, 'elapsedTime', 'elapsedTime', 0, '{:.1f}')

        self.blueShutter = Shutter(self.moduleRow, 'shb')
        self.redShutter = Shutter(self.moduleRow, 'shr')

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.shutters, 1, 0)
        self.grid.addWidget(self.exptime, 1, 1)
        self.grid.addWidget(self.elapsedTime, 1, 2)

        self.grid.addWidget(self.blueShutter, 2, 0, 1, 3)
        self.grid.addWidget(self.redShutter, 3, 0, 1, 3)


class ShuttersCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)

        self.abortButton = AbortButton(controlPanel=controlPanel,
                                       cmdStr='%s exposure finish' % controlPanel.actorName)

        self.shutterCmd = ShutterCmd(controlPanel=controlPanel)
        self.exposeCmd = ExposeCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.abortButton, 1, 0)
        self.grid.addLayout(self.shutterCmd, 2, 0, 1, 3)
        self.grid.addLayout(self.exposeCmd, 3, 0, 1, 3)
