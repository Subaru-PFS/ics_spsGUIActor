__author__ = 'alefur'
import spsClient.styles as styles
from spsClient.control import ControllerPanel, ControllerCmd
from spsClient.widgets import ValueGB, SwitchGB, CmdButton, CustomedCmd, SpinBoxGB, SwitchButton


class AttenuatorValue(ValueGB):
    def __init__(self, moduleRow, fontSize=styles.smallFont):
        ValueGB.__init__(self, moduleRow, 'attenuator', 'attenuator', 0, '{:g}', fontSize=fontSize)
        self.controllerName = 'labsphere'

    def setText(self, txt):
        if txt == '0':
            txt = 'open'
        elif txt in ['127', '128']:
            txt = 'mid-open'
        elif txt == '255':
            txt = 'closed'

        self.value.setText(txt)
        self.customize()


class AttenuatorCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET VALUE')

        self.value = SpinBoxGB('attenuator', 0, 255)
        self.addWidget(self.value, 0, 1)

    def buildCmd(self):
        cmdStr = 'dcb labsphere attenuator=%i' % self.value.getValue()
        return cmdStr


class SwitchHalogen(SwitchButton):
    def __init__(self, controlPanel):
        SwitchButton.__init__(self, controlPanel=controlPanel, key='halogen', label='Halogen', fmt='{:s}',
                              cmdHead='dcb labsphere halogen')

    def setText(self, txt):
        bool = True if txt in ['undef', 'on'] else False

        self.buttonOn.setVisible(not bool)
        self.buttonOff.setVisible(bool)


class LabspherePanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'labsphere')
        self.addCommandSet(LabsphereCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'labsphereMode', '', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'labsphereFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'labsphereFSM', '', 1, '{:s}')

        self.halogen = SwitchGB(self.moduleRow, 'halogen', 'Halogen', 0, '{:s}')
        self.photodiode = ValueGB(self.moduleRow, 'photodiode', 'photodiode', 0, '{:g}')
        self.attenuator = AttenuatorValue(self.moduleRow)

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.halogen, 1, 0)
        self.grid.addWidget(self.photodiode, 1, 1)
        self.grid.addWidget(self.attenuator, 1, 2)


class LabsphereCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
        self.initButton = CmdButton(controlPanel=controlPanel, label='INIT', cmdStr='dcb labsphere init')
        self.attenuatorCmd = AttenuatorCmd(controlPanel=controlPanel)
        self.switchHalogen = SwitchHalogen(controlPanel=controlPanel)

        self.grid.addWidget(self.initButton, 1, 0)
        self.grid.addLayout(self.attenuatorCmd, 2, 0, 1, 2)
        self.grid.addWidget(self.switchHalogen, 3, 0)
