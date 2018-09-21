__author__ = 'alefur'

from PyQt5.QtWidgets import QComboBox
from spsClient.widgets import ValueGB, ControlPanel, CommandsGB, CmdButton, CustomedCmd, DoubleSpinBoxGB, SwitchGB, \
    SwitchButton


class Error(ValueGB):
    def __init__(self, moduleRow):
        ValueGB.__init__(self, moduleRow, 'monoerror', 'Error', 0, '{:s}')

    def customize(self):
        text = self.value.text()
        background = 'green' if text == 'OK' else 'red'
        self.setColor(background=background)
        self.setEnabled(self.moduleRow.isOnline)


class MonoPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

        self.mode = ValueGB(self.moduleRow, 'monoMode', '', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'monoFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'monoFSM', '', 1, '{:s}')
        self.error = Error(self.moduleRow)

        self.gratingId = ValueGB(self.moduleRow, 'monograting', 'Grating', 0, '{:d}')
        self.resolution = ValueGB(self.moduleRow, 'monograting', 'Lines/mm', 1, '{:.3f}')

        self.shutter = ValueGB(self.moduleRow, 'monochromator', 'Shutter', 0, '{:s}')
        self.outport = ValueGB(self.moduleRow, 'monochromator', 'Outport', 1, '{:d}')
        self.wavelength = ValueGB(self.moduleRow, 'monochromator', 'Wavelength(nm)', 2, '{:.3f}')

        self.monoqth = SwitchGB(self.moduleRow, 'monoqth', 'QTH', 0, '{:g}')
        self.volts = ValueGB(self.moduleRow, 'monoqthVAW', 'Voltage', 0, '{:.2f}')
        self.current = ValueGB(self.moduleRow, 'monoqthVAW', 'Current', 1, '{:.2f}')
        self.power = ValueGB(self.moduleRow, 'monoqthVAW', 'Power', 2, '{:.2f}')

        self.commands = MonoCommands(self)

        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.error, 1, 0, 1, 3)

        self.grid.addWidget(self.gratingId, 2, 0)
        self.grid.addWidget(self.resolution, 2, 1)

        self.grid.addWidget(self.shutter, 3, 0)
        self.grid.addWidget(self.outport, 3, 1)
        self.grid.addWidget(self.wavelength, 3, 2)

        # self.grid.addWidget(self.monoqth, 4, 0)
        #
        # self.grid.addWidget(self.volts, 5, 0)
        # self.grid.addWidget(self.current, 5, 1)
        # self.grid.addWidget(self.power, 5, 2)

        self.grid.addWidget(self.empty, 4, 0, 1, 3)
        self.grid.addWidget(self.commands, 0, 3, 5, 3)


class ShutterCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SHUTTER')

        self.comboMove = QComboBox()
        self.comboMove.addItems(['open', 'close'])
        self.addWidget(self.comboMove, 0, 1)

    def buildCmd(self):
        cmdStr = 'dcb mono shutter %s' % self.comboMove.currentText()
        return cmdStr


class GratingCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET GRATING')
        self.combo = QComboBox()
        self.combo.addItems(['1', '2', '3'])
        self.addWidget(self.combo, 0, 1)

    def buildCmd(self):
        cmdStr = 'dcb mono set grating=%s' % self.combo.currentText()
        return cmdStr


class OutportCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET OUTPORT')
        self.combo = QComboBox()
        self.combo.addItems(['1', '2'])
        self.addWidget(self.combo, 0, 1)

    def buildCmd(self):
        cmdStr = 'dcb mono set outport=%s' % self.combo.currentText()
        return cmdStr


class WaveCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET VALUE')

        self.value = DoubleSpinBoxGB('Wavelength(nm)', 300, 1200, 3)

        self.addWidget(self.value, 0, 1)

    def buildCmd(self):
        cmdStr = 'dcb mono set wave=%.3f' % self.value.getValue()
        return cmdStr


class MonoCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='dcb status controllers=mono,monoqth')
        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='dcb connect controller=mono')

        self.gratingCmd = GratingCmd(controlPanel=controlPanel)
        self.shutterCmd = ShutterCmd(controlPanel=controlPanel)
        self.outportCmd = OutportCmd(controlPanel=controlPanel)
        self.waveCmd = WaveCmd(controlPanel=controlPanel)

        self.switchQth = SwitchButton(controlPanel=controlPanel, key='monoqth', label='QTH',
                                      cmdHead='dcb monoqth')

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.connectButton, 0, 1)

        self.grid.addLayout(self.gratingCmd, 1, 0, 1, 2)
        self.grid.addLayout(self.shutterCmd, 2, 0, 1, 2)
        self.grid.addLayout(self.outportCmd, 3, 0, 1, 2)
        self.grid.addLayout(self.waveCmd, 4, 0, 1, 2)

        # self.grid.addWidget(self.switchQth, 5, 0)

    @property
    def buttons(self):
        return [self.statusButton, self.connectButton, self.gratingCmd.button, self.shutterCmd.button,
                self.outportCmd.button, self.waveCmd.button] + self.switchQth.buttons
