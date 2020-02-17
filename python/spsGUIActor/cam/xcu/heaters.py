__author__ = 'alefur'
from spsGUIActor.cam import CamDevice
from spsGUIActor.control import CommandsGB
from spsGUIActor.widgets import SwitchGB, ValuesRow, ValueGB, CustomedCmd, CmdButton, DoubleSpinBoxGB, SwitchButton


class HeaterState(ValuesRow):
    def __init__(self, controlPanel, name):
        heaterNb = controlPanel.heaterChannels[name]
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
        heaterNames = self.heaterNames[self.moduleRow.camRow.arm]
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


class HeaterCmd(CustomedCmd):
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

        hp, frac = self.controlPanel.heaterNames[self.controlPanel.moduleRow.camRow.arm]

        self.hPCmd = HPCmd(controlPanel, hp)
        self.heaterCmd = HeaterCmd(controlPanel, frac)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.hPCmd, 1, 0)
        self.grid.addLayout(self.heaterCmd, 2, 0)
