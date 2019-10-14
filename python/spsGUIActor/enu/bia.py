__author__ = 'alefur'

from spsGUIActor.control import ControllerPanel
from spsGUIActor.dcb.aten import SwitchButton
from spsGUIActor.enu import EnuDeviceCmd
from spsGUIActor.widgets import ValueGB, CustomedCmd, SwitchGB, SpinBoxGB


class BiaPeriod(ValueGB):
    def __init__(self, moduleRow):
        self.spinbox = SpinBoxGB('Period', 0, 65536)
        ValueGB.__init__(self, moduleRow, 'biaConfig', '', 1, '{:d}')

    def setText(self, txt):
        if not self.spinbox.locked:
            self.spinbox.setValue(txt)

    def getValue(self):
        return self.spinbox.getValue()


class BiaDuty(ValueGB):
    def __init__(self, moduleRow):
        self.spinbox = SpinBoxGB('Duty', 0, 255)
        ValueGB.__init__(self, moduleRow, 'biaConfig', '', 2, '{:d}')

    def setText(self, txt):
        if not self.spinbox.locked:
            self.spinbox.setValue(txt)

    def getValue(self):
        return self.spinbox.getValue()


class SetBiaParamCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SET PARAMETERS')

        self.period = BiaPeriod(moduleRow=self.controlPanel.moduleRow)
        self.duty = BiaDuty(moduleRow=self.controlPanel.moduleRow)

        self.addWidget(self.period.spinbox, 0, 1)
        self.addWidget(self.duty.spinbox, 0, 2)

    def buildCmd(self):
        cmdStr = '%s bia period=%i duty=%i ' % (self.controlPanel.actorName, self.period.getValue(),
                                                self.duty.getValue())
        return cmdStr


class SwitchBia(SwitchButton):
    def __init__(self, controlPanel):
        SwitchButton.__init__(self, controlPanel=controlPanel, key='bia', label='BIA', fmt='{:s}',
                              cmdHead='%s bia' % controlPanel.actorName)

    def setText(self, txt):
        bool = True if txt in ['undef', 'on'] else False

        self.buttonOn.setVisible(not bool)
        self.buttonOff.setVisible(bool)


class BiaPanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'biasha')
        self.addCommandSet(BiaCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'biashaMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'biashaFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'biashaFSM', '', 1, '{:s}')

        self.bia = SwitchGB(self.moduleRow, 'bia', 'BIA', 0, '{:s}')
        self.biaStrobe = SwitchGB(self.moduleRow, 'biaConfig', 'Strobe', 0, '{:d}')
        self.biaPeriod = ValueGB(self.moduleRow, 'biaConfig', 'Bia-Period', 1, '{:d}')
        self.biaDuty = ValueGB(self.moduleRow, 'biaConfig', 'Bia-Duty', 2, '{:d}')

        self.photores1 = ValueGB(self.moduleRow, 'photores', 'PhotoRes1', 0, '{:d}')
        self.photores2 = ValueGB(self.moduleRow, 'photores', 'PhotoRes2', 1, '{:d}')

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.bia, 1, 0)
        self.grid.addWidget(self.biaStrobe, 1, 1)

        self.grid.addWidget(self.biaPeriod, 2, 0)
        self.grid.addWidget(self.biaDuty, 2, 1)

        self.grid.addWidget(self.photores1, 3, 0)
        self.grid.addWidget(self.photores2, 3, 1)


class BiaCommands(EnuDeviceCmd):
    def __init__(self, controlPanel):
        EnuDeviceCmd.__init__(self, controlPanel)
        self.switchBia = SwitchBia(controlPanel=controlPanel)
        self.switchStrobe = SwitchButton(controlPanel=controlPanel, key='biaConfig', label='STROBE',
                                         cmdHead='%s bia strobe' % controlPanel.actorName)
        self.setBiaParam = SetBiaParamCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.switchBia, 1, 0)
        self.grid.addWidget(self.switchStrobe, 1, 1)
        self.grid.addLayout(self.setBiaParam, 2, 0, 1, 3)
