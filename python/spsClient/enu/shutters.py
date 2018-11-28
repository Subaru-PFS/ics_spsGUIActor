__author__ = 'alefur'

from PyQt5.QtWidgets import QComboBox, QGroupBox, QGridLayout
import spsClient.styles as styles
from spsClient.widgets import ValueGB, ControlPanel, CmdButton, CustomedCmd, CommandsGB, DoubleSpinBoxGB, AbortButton


class ShutterCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SHUTTERS')

        self.comboMove = QComboBox()
        self.comboMove.addItems(['open', 'close'])

        self.comboShut = QComboBox()
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

        self.comboShut = QComboBox()
        self.comboShut.addItems(['', 'blue', 'red'])

        self.addWidget(self.exptime, 0, 1)
        self.addWidget(self.comboShut, 0, 2)

    def buildCmd(self):
        cmdStr = '%s shutters expose exptime=%.1f %s' % (self.controlPanel.actorName,
                                                         self.exptime.getValue(),
                                                         self.comboShut.currentText())
        return cmdStr


class Shutter(QGroupBox):
    shutterName = {'shb': 'Blue Shutter', 'shr': 'Red Shutter'}

    def __init__(self, moduleRow, shId):
        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setTitle(self.shutterName[shId])
        self.open = ValueGB(moduleRow, shId, 'open', 0, '{:d}')
        self.close = ValueGB(moduleRow, shId, 'close', 1, '{:d}')
        self.error = ValueGB(moduleRow, shId, 'error', 2, '{:d}')

        for j, widget in enumerate(self.widgets):
            self.grid.addWidget(widget, 0, j)

        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; border: 1px solid #d7d4d1;border-radius: 3px;margin-top: 1ex;} " % (
                styles.smallFont) +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

    @property
    def widgets(self):
        return [self.open, self.close, self.error]


class ShuttersCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s bsh status' % controlPanel.actorName)
        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='%s connect controller=bsh' % controlPanel.actorName)

        self.abortButton = AbortButton(controlPanel=controlPanel,
                                       cmdStr='%s shutters close force' % controlPanel.actorName)

        self.shutterCmd = ShutterCmd(controlPanel=controlPanel)
        self.exposeCmd = ExposeCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.connectButton, 0, 1)
        self.grid.addWidget(self.abortButton, 1, 0)
        self.grid.addLayout(self.shutterCmd, 2, 0, 1, 3)
        self.grid.addLayout(self.exposeCmd, 3, 0, 1, 3)
        #self.grid.addWidget(self.empty, 4, 0, 1, 3)

    @property
    def buttons(self):
        return [self.statusButton, self.connectButton, self.shutterCmd.button, self.exposeCmd.button]


class ShuttersPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

        self.mode = ValueGB(self.moduleRow, 'bshMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'bshFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'bshFSM', '', 1, '{:s}')

        self.shutters = ValueGB(self.moduleRow, 'shutters', 'Shutters', 0, '{:s}')
        self.exptime = ValueGB(self.moduleRow, 'integratingTime', 'Exptime', 0, '{:.1f}')
        self.elapsedTime = ValueGB(self.moduleRow, 'elapsedTime', 'elapsedTime', 0, '{:.1f}')

        self.blueShutter = Shutter(self.moduleRow, 'shb')
        self.redShutter = Shutter(self.moduleRow, 'shr')

        self.commands = ShuttersCommands(self)
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.shutters, 1, 0)
        self.grid.addWidget(self.exptime, 1, 1)
        self.grid.addWidget(self.elapsedTime, 1, 2)

        self.grid.addWidget(self.blueShutter, 2, 0, 1, 3)
        self.grid.addWidget(self.redShutter, 3, 0, 1, 3)

        self.grid.addWidget(self.empty, 4, 0, 1, 3)
        self.grid.addWidget(self.commands, 0, 4, 4, 3)

    @property
    def customWidgets(self):
        return self.blueShutter.widgets + self.redShutter.widgets
