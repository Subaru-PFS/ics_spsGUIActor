__author__ = 'alefur'
from spsGUIActor.control import ControllerPanel, CommandsGB
from spsGUIActor.widgets import SwitchGB, ValuesRow, ValueGB, CustomedCmd, CmdButton, DoubleSpinBoxGB, SwitchButton
from spsGUIActor.cam import CamDevice

class HeaterState(ValuesRow):
    heaters = dict(ccd=0, spreader=1, asic=4, shield=5)

    def __init__(self, moduleRow, name):
        heaterNb = self.heaters[name]
        widgets = [SwitchGB(moduleRow, 'heaters', 'enabled', heaterNb, '{:g}'),
                   ValueGB(moduleRow, 'heaters', 'fraction', heaterNb + 2, '{:.2f}')]

        ValuesRow.__init__(self, widgets, title=name.capitalize())


class HeatersPanel(CamDevice):
    visNames = ['ccd', 'spreader']
    nirNames = ['asic', 'shield']
    heaterNames = dict(b=visNames, r=visNames, n=nirNames)

    def __init__(self, controlDialog):
        CamDevice.__init__(self, controlDialog, 'temps', 'Heaters')
        self.addCommandSet(HeatersCommands(self))

    def createWidgets(self):
        heaterNames = self.heaterNames[self.moduleRow.camRow.arm]
        self.heaters = [HeaterState(self.moduleRow, name) for name in heaterNames]

    def setInLayout(self):
        for i, value in enumerate(self.heaters):
            self.grid.addWidget(value, i, 0)


class HPCmd(SwitchButton):
    heaters = dict(ccd=0, spreader=1, asic=4, shield=5)

    def __init__(self, controlPanel, name):
        cmdStrOn = '%s HPheaters on %s' % (controlPanel.actorName, name)
        cmdStrOff = '%s HPheaters off %s' % (controlPanel.actorName, name)
        SwitchButton.__init__(self, controlPanel=controlPanel, key='heaters', label=name.capitalize(),
                              ind=self.heaters[name], cmdHead='', cmdStrOn=cmdStrOn, cmdStrOff=cmdStrOff)

    def setText(self, txt):
        bool = True if txt.strip() in ['0', 'nan', 'off', 'undef'] else False
        self.buttonOn.setVisible(bool)
        self.buttonOff.setVisible(not bool)


class HeaterCmd(CustomedCmd):
    def __init__(self, controlPanel, name):
        self.name = name
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET %s' % name.upper())

        self.value = DoubleSpinBoxGB('Power(frac)', vmin=0, vmax=1, decimals=2)
        self.addWidget(self.value, 0, 1)

    def buildCmd(self):
        return '%s heaters %s power=%d' % (self.controlPanel.actorName, self.name, self.value.getValue())


class HeatersCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s heaters status' % controlPanel.actorName)

        frac, hp = self.controlPanel.heaterNames[self.controlPanel.moduleRow.camRow.arm]

        self.hPCmd = HPCmd(controlPanel, hp)
        self.heaterCmd = HeaterCmd(controlPanel, frac)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.hPCmd, 1, 0)
        self.grid.addLayout(self.heaterCmd, 2, 0)
