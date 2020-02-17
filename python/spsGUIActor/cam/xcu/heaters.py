__author__ = 'alefur'

from spsGUIActor.cam import CamDevice
from spsGUIActor.control import CommandsGB
from spsGUIActor.widgets import SwitchGB, ValuesRow, ValueGB, CustomedCmd, CmdButton, DoubleSpinBoxGB, SwitchButton
from spsGUIActor.cam.xcu import addEng

class HeaterState(ValuesRow):
    def __init__(self, controlPanel, name):
        heaterNb = controlPanel.heaterChannels[name]
        self.name = name
        widgets = [SwitchGB(controlPanel.moduleRow, 'heaters', 'enabled', heaterNb, '{:g}'),
                   ValueGB(controlPanel.moduleRow, 'heaters', 'fraction', heaterNb + 2, '{:.2f}')]

        ValuesRow.__init__(self, widgets, title=name.capitalize())


class HeatersPanel(CamDevice):
    visNames = ['spreader', 'ccd']
    nirNames = ['shield', 'asic']
    heaterNames = dict(b=visNames, r=visNames, n=nirNames)
    heaterChannels = dict(ccd=4, spreader=5, asic=0, shield=1)

    def __init__(self, controlDialog):
        CamDevice.__init__(self, controlDialog, 'temps', 'Heaters')
        self.addCommandSet(HeatersCommands(self))

    def createWidgets(self):
        sortedChannels = dict(sorted(self.heaterChannels.items(), key=lambda kv: kv[1])).keys()
        heaterNames = sortedChannels if addEng else self.heaterNames[self.moduleRow.camRow.arm]
        self.heaters = [HeaterState(self, name) for name in heaterNames]

    def setInLayout(self):
        for i, value in enumerate(self.heaters):
            self.grid.addWidget(value, i, 0)


class HPCmd(SwitchButton):

    def __init__(self, controlPanel, name):
        cmdStrOn = '%s HPheaters on %s' % (controlPanel.actorName, name)
        cmdStrOff = '%s HPheaters off %s' % (controlPanel.actorName, name)
        SwitchButton.__init__(self, controlPanel=controlPanel, key='heaters', label=name.capitalize(),
                              ind=controlPanel.heaterChannels[name], cmdHead='', cmdStrOn=cmdStrOn, cmdStrOff=cmdStrOff)

    def setText(self, txt):
        bool = True if txt.strip() in ['0', 'nan', 'off', 'undef'] else False
        self.buttonOn.setVisible(bool)
        self.buttonOff.setVisible(not bool)


class FracCmd(CustomedCmd):
    def __init__(self, controlPanel, name):
        self.name = name
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET %s' % name.upper())

        self.value = DoubleSpinBoxGB('Power(percent)', vmin=0, vmax=100, decimals=2)
        self.addWidget(self.value, 0, 1)

    def buildCmd(self):
        return '%s heaters %s power=%d' % (self.controlPanel.actorName, self.name, self.value.getValue())


class HeatersCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s heaters status' % controlPanel.actorName)
        self.grid.addWidget(self.statusButton, 0, 0)

        for i, heater in enumerate(controlPanel.heaters):
            name = heater.name
            if name in ['spreader', 'shield']:
                self.grid.addWidget(HPCmd(controlPanel, name), 1 + i, 0)
            else:
                self.grid.addLayout(FracCmd(controlPanel, name), 1 + i, 0)
