__author__ = 'alefur'

from spsClient.control import ControllerPanel, ControllerCmd
from spsClient.widgets import ValueGB, SwitchGB, SwitchButton


class MonoQthPanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'monoqth')
        self.addCommandSet(MonoQthCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'monoqthMode', '', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'monoqthFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'monoqthFSM', '', 1, '{:s}')

        self.monoqth = SwitchGB(self.moduleRow, 'monoqth', 'QTH', 0, '{:g}')
        self.volts = ValueGB(self.moduleRow, 'monoqthVAW', 'Voltage', 0, '{:.2f}')
        self.current = ValueGB(self.moduleRow, 'monoqthVAW', 'Current', 1, '{:.2f}')
        self.power = ValueGB(self.moduleRow, 'monoqthVAW', 'Power', 2, '{:.2f}')

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.monoqth, 1, 0)

        self.grid.addWidget(self.volts, 2, 0)
        self.grid.addWidget(self.current, 2, 1)
        self.grid.addWidget(self.power, 2, 2)


class MonoQthCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
        self.switchQth = SwitchButton(controlPanel=controlPanel, key='monoqth', label='QTH',
                                      cmdHead='dcb monoqth')
        self.grid.addWidget(self.switchQth, 1, 0)
