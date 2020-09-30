__author__ = 'alefur'

from spsGUIActor.control import ControllerPanel, ControllerCmd
from spsGUIActor.widgets import ValueGB, SwitchGB, SwitchButton
from spsGUIActor.enu import EnuDeviceCmd

class AtenButton(SwitchButton):
    def __init__(self, controlPanel, key, label, safetyCheck=False):
        cmdStrOn = f'{controlPanel.actorName} power on={key}'
        cmdStrOff = f'{controlPanel.actorName} power off={key}'
        SwitchButton.__init__(self, controlPanel=controlPanel, key=key, label=label, cmdHead='', cmdStrOn=cmdStrOn,
                              cmdStrOff=cmdStrOff, safetyCheck=safetyCheck)


class AtenPanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'aten')
        self.addCommandSet(AtenCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'atenMode', '', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'atenFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'atenFSM', '', 1, '{:s}')

        self.labsphere = SwitchGB(self.moduleRow, 'labsphere', 'Labsphere', 0, '{:g}')
        self.mono = SwitchGB(self.moduleRow, 'mono', 'Monochromator', 0, '{:g}')
        self.roughpump = SwitchGB(self.moduleRow, 'roughpump', 'Roughpump', 0, '{:g}')
        self.bakeout = SwitchGB(self.moduleRow, 'bakeout', 'Bakeout', 0, '{:g}')

        self.voltage = ValueGB(self.moduleRow, 'atenVAW', 'Voltage', 0, '{:.2f}')
        self.current = ValueGB(self.moduleRow, 'atenVAW', 'Current', 1, '{:.2f}')
        self.power = ValueGB(self.moduleRow, 'atenVAW', 'Power', 2, '{:.2f}')

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.voltage, 1, 0)
        self.grid.addWidget(self.current, 1, 1)
        self.grid.addWidget(self.power, 1, 2)

        self.grid.addWidget(self.labsphere, 2, 0)
        self.grid.addWidget(self.mono, 2, 1)
        self.grid.addWidget(self.roughpump, 3, 0)
        self.grid.addWidget(self.bakeout, 3, 1)


class AtenCommands(EnuDeviceCmd):
    def __init__(self, controlPanel):
        EnuDeviceCmd.__init__(self, controlPanel)

        self.switchLabsphere = AtenButton(controlPanel=controlPanel, key='labsphere', label='Labsphere')
        self.switchMono = AtenButton(controlPanel=controlPanel, key='mono', label='Monochromator')
        self.switchRough = AtenButton(controlPanel=controlPanel, key='roughpump', label='RoughPump', safetyCheck=True)
        self.switchBakeout = AtenButton(controlPanel=controlPanel, key='bakeout', label='Bakeout', safetyCheck=True)

        self.grid.addWidget(self.switchLabsphere, 1, 0)
        self.grid.addWidget(self.switchMono, 1, 1)
        self.grid.addWidget(self.switchRough, 4, 0)
        self.grid.addWidget(self.switchBakeout, 4, 1)
