__author__ = 'alefur'

from spsGUIActor.control import ControllerPanel
from spsGUIActor.dcb.labsphere import SwitchArc
from spsGUIActor.enu import EnuDeviceCmd
from spsGUIActor.enu.pdu import PduPort
from spsGUIActor.widgets import ValueGB


class SourcesPanel(ControllerPanel):
    ports = dict(hgar=1, neon=2, halogen=3)

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'sources')
        self.addCommandSet(SourcesCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'sourcesMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'sourcesFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'sourcesFSM', '', 1, '{:s}')

        self.pduPorts = [PduPort(self.moduleRow, name, f'pduPort{portNb}') for name, portNb in self.ports.items()]

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        for i, pduPort in enumerate(self.pduPorts):
            self.grid.addWidget(pduPort, 1 + i, 0, 1, 4)


class SourcesCommands(EnuDeviceCmd):
    def __init__(self, controlPanel):
        EnuDeviceCmd.__init__(self, controlPanel)
        self.grid.addWidget(SwitchArc(controlPanel, 'hgar'), 1, 0)
        self.grid.addWidget(SwitchArc(controlPanel, 'neon'), 2, 0)
        self.grid.addWidget(SwitchArc(controlPanel, 'halogen'), 3, 0)
