__author__ = 'alefur'

import spsGUIActor.styles as styles
from spsGUIActor.common import ComboBox
from spsGUIActor.control import ControllerPanel, ControllerCmd
from spsGUIActor.widgets import ValueGB, CustomedCmd, DoubleSpinBoxGB, SwitchGB, SwitchButton
from spsGUIActor.enu import EnuDeviceCmd

class Error(ValueGB):
    def __init__(self, moduleRow):
        ValueGB.__init__(self, moduleRow, 'monoerror', 'Error', 0, '{:s}')

    def customize(self):
        text = self.value.text()
        self.setColor(*styles.colorWidget('default' if text == 'OK' else 'failed'))
        self.setEnabled(self.moduleRow.isOnline)


class ShutterCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SHUTTER')

        self.comboMove = ComboBox()
        self.comboMove.addItems(['open', 'close'])
        self.addWidget(self.comboMove, 0, 1)

    def buildCmd(self):
        cmdStr = f'{self.controlPanel.actorName} mono shutter %s' % self.comboMove.currentText()
        return cmdStr


class GratingCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET GRATING')
        self.combo = ComboBox()
        self.combo.addItems(['1', '2', '3'])
        self.addWidget(self.combo, 0, 1)

    def buildCmd(self):
        cmdStr = 'dcb mono set grating=%s' % self.combo.currentText()
        return cmdStr


class OutportCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET OUTPORT')
        self.combo = ComboBox()
        self.combo.addItems(['1', '2'])
        self.addWidget(self.combo, 0, 1)

    def buildCmd(self):
        cmdStr = f'{self.controlPanel.actorName} mono set outport=%s' % self.combo.currentText()
        return cmdStr


class WaveCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET VALUE')

        self.value = DoubleSpinBoxGB('Wavelength(nm)', 300, 1200, 3)

        self.addWidget(self.value, 0, 1)

    def buildCmd(self):
        cmdStr = f'{self.controlPanel.actorName} mono set wave=%.3f' % self.value.getValue()
        return cmdStr


class MonoPanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'mono')
        self.addCommandSet(MonoCommands(self))

    def createWidgets(self):
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

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.error, 1, 0, 1, 3)

        self.grid.addWidget(self.gratingId, 2, 0)
        self.grid.addWidget(self.resolution, 2, 1)

        self.grid.addWidget(self.shutter, 3, 0)
        self.grid.addWidget(self.outport, 3, 1)
        self.grid.addWidget(self.wavelength, 3, 2)


class MonoCommands(EnuDeviceCmd):
    def __init__(self, controlPanel):
        EnuDeviceCmd.__init__(self, controlPanel)
        self.gratingCmd = GratingCmd(controlPanel=controlPanel)
        self.shutterCmd = ShutterCmd(controlPanel=controlPanel)
        self.outportCmd = OutportCmd(controlPanel=controlPanel)
        self.waveCmd = WaveCmd(controlPanel=controlPanel)

        self.switchQth = SwitchButton(controlPanel=controlPanel, key='monoqth', label='QTH',
                                      cmdHead=f'{controlPanel.actorName} monoqth')

        self.grid.addLayout(self.gratingCmd, 1, 0, 1, 2)
        self.grid.addLayout(self.shutterCmd, 2, 0, 1, 2)
        self.grid.addLayout(self.outportCmd, 3, 0, 1, 2)
        self.grid.addLayout(self.waveCmd, 4, 0, 1, 2)
