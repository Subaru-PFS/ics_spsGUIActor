__author__ = 'alefur'

from spsGUIActor.control import ControllerPanel
from spsGUIActor.enu import EnuDeviceCmd
from spsGUIActor.widgets import ValueGB, SwitchGB, SwitchButton


# class LampNames(ValueGB):
#     def __init__(self, sourcesPanel):
#         self.sourcesPanel = sourcesPanel
#         ValueGB.__init__(self, sourcesPanel.moduleRow, 'lampNames', '', 0, '{:s}')
#
#     def updateVals(self, ind, fmt, keyvar):
#         self.updateWidgets(keyvar.getValue(doRaise=False))
#
#     def updateWidgets(self, names=None):
#         names = self.keyvar.getValue(doRaise=False) if names is None else names
#         self.sourcesPanel.setLampNames(names)

class SwitchLamp(SwitchButton):
    def __init__(self, controlPanel, key, label=None, fmt='{:g}'):
        label = key.capitalize() if label is None else label
        cmdStrOn = f'{controlPanel.actorName} arc on={key}'
        cmdStrOff = f'{controlPanel.actorName} arc off={key}'
        SwitchButton.__init__(self, controlPanel=controlPanel, key=key, label=label, fmt=fmt,
                              cmdHead='', cmdStrOn=cmdStrOn, cmdStrOff=cmdStrOff)

    def setText(self, txt):
        bool = True if txt.strip() in ['0', 'nan', 'off', 'undef'] else False
        self.buttonOn.setVisible(bool)
        self.buttonOff.setVisible(not bool)


class SourcesPanel(ControllerPanel):
    lampNames = ['halogen', 'argon', 'hgar', 'neon', 'krypton']

    def __init__(self, controlDialog):
        self.addLamp = True
        ControllerPanel.__init__(self, controlDialog, 'sources')
        self.addCommandSet(SourcesCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'sourcesMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'sourcesFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'sourcesFSM', '', 1, '{:s}')

        # self.pduPorts = [PduPort(self.moduleRow, name, f'pduPort{portNb}') for name, portNb in self.ports.items()]

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        for i, lampName in enumerate(self.lampNames):
            self.grid.addWidget(SwitchGB(self.moduleRow, lampName, lampName.capitalize(), 0, '{:g}'), 1 + i, 0)


class SourcesCommands(EnuDeviceCmd):
    def __init__(self, controlPanel):
        EnuDeviceCmd.__init__(self, controlPanel)
        for i, lampName in enumerate(controlPanel.lampNames):
            self.grid.addWidget(SwitchLamp(controlPanel, lampName), i + 1, 0)
