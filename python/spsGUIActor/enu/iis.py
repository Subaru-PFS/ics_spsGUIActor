__author__ = 'alefur'

from spsGUIActor.control import ControllerPanel, ControllerCmd
from spsGUIActor.widgets import ValueGB, SwitchButton, SwitchGB


class ArcButton(SwitchButton):
    def __init__(self, controlPanel, arc):
        cmdStrOn = '%s iis on=%s' % (controlPanel.actorName, arc)
        cmdStrOff = '%s iis off=%s' % (controlPanel.actorName, arc)
        SwitchButton.__init__(self, controlPanel=controlPanel, key=arc, label=arc.capitalize(), cmdHead='',
                              cmdStrOn=cmdStrOn, cmdStrOff=cmdStrOff)


class IisPanel(ControllerPanel):

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'iis')
        self.addCommandSet(IisCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'iisMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'iisFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'iisFSM', '', 1, '{:s}')

        self.hgar = SwitchGB(self.moduleRow, 'hgar', 'HgAr', 0, '{:g}')

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)
        self.grid.addWidget(self.hgar, 1, 0)


class IisCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
        self.grid.addWidget(ArcButton(controlPanel, 'hgar'), 1, 0)
