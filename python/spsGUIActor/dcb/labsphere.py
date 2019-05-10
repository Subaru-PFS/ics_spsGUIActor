__author__ = 'alefur'
import spsGUIActor.styles as styles
from spsGUIActor.control import ControllerPanel, ControllerCmd
from spsGUIActor.widgets import ValueGB, SwitchGB, CustomedCmd, SpinBoxGB, SwitchButton


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


class SwitchArc(SwitchButton):
    def __init__(self, controlPanel, key, label, fmt='{:g}'):
        cmdStrOn = 'dcb arc on=%s' % key
        cmdStrOff = 'dcb arc off=%s' % key
        SwitchButton.__init__(self, controlPanel=controlPanel, key=key, label=label, fmt=fmt,
                              cmdHead='', cmdStrOn=cmdStrOn, cmdStrOff=cmdStrOff)

    def setText(self, txt):
        bool = True if txt.strip() in ['0', 'nan', 'off', 'undef'] else False
        self.buttonOn.setVisible(bool)
        self.buttonOff.setVisible(not bool)


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

        self.neon = SwitchGB(self.moduleRow, 'neon', 'Neon', 0, '{:g}')
        self.xenon = SwitchGB(self.moduleRow, 'xenon', 'Xenon', 0, '{:g}')
        self.hgar = SwitchGB(self.moduleRow, 'hgar', 'HgAr', 0, '{:g}')
        self.krypton = SwitchGB(self.moduleRow, 'krypton', 'Krypton', 0, '{:g}')
        self.argon = SwitchGB(self.moduleRow, 'argon', 'Argon', 0, '{:g}')
        self.deuterium = SwitchGB(self.moduleRow, 'deuterium', 'Deuterium', 0, '{:g}')

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.halogen, 1, 0)
        self.grid.addWidget(self.photodiode, 1, 1)
        self.grid.addWidget(self.attenuator, 1, 2)

        self.grid.addWidget(self.neon, 2, 0)
        self.grid.addWidget(self.xenon, 2, 1)
        self.grid.addWidget(self.krypton, 2, 2)

        self.grid.addWidget(self.hgar, 3, 0)
        self.grid.addWidget(self.argon, 3, 1)
        self.grid.addWidget(self.deuterium, 3, 2)


class LabsphereCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
        self.attenuatorCmd = AttenuatorCmd(controlPanel=controlPanel)
        self.switchHalogen = SwitchArc(controlPanel=controlPanel, key='halogen', label='Halogen', fmt='{:s}')
        self.switchNeon = SwitchArc(controlPanel=controlPanel, key='neon', label='Neon')
        self.switchXenon = SwitchArc(controlPanel=controlPanel, key='xenon', label='Xenon')
        self.switchHgar = SwitchArc(controlPanel=controlPanel, key='hgar', label='HgAr')
        self.switchKrypton = SwitchArc(controlPanel=controlPanel, key='krypton', label='Krypton')
        self.switchArgon = SwitchArc(controlPanel=controlPanel, key='argon', label='Argon')
        self.switchDeuterium = SwitchArc(controlPanel=controlPanel, key='deuterium', label='Deuterium')

        self.grid.addLayout(self.attenuatorCmd, 1, 0, 1, 2)
        self.grid.addWidget(self.switchHalogen, 2, 0)

        self.grid.addWidget(self.switchNeon, 3, 0)
        self.grid.addWidget(self.switchXenon, 3, 1)
        self.grid.addWidget(self.switchHgar, 3, 2)

        self.grid.addWidget(self.switchKrypton, 4, 0)
        self.grid.addWidget(self.switchArgon, 4, 1)
        self.grid.addWidget(self.switchDeuterium, 4, 2)
