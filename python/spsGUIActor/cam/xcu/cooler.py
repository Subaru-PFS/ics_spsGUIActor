__author__ = 'alefur'

from spsGUIActor.cam import CamDevice
from spsGUIActor.common import LineEdit
from spsGUIActor.control import ControllerCmd
from spsGUIActor.widgets import ValueGB, CmdButton, CustomedCmd, SpinBoxGB, DoubleSpinBoxGB


class TempLoopCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET Temperature', safetyCheck=True)

        self.value = DoubleSpinBoxGB('setpoint(K)', 50, 250, 2)
        self.addWidget(self.value, 0, 1)

    def buildCmd(self):
        return f'{self.controlPanel.actorName} {self.controlPanel.controllerName} on setpoint=%g' % self.value.getValue()


class PowerLoopCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET Power', safetyCheck=True)

        self.value = SpinBoxGB('setpoint(W)', 70, 250)
        self.addWidget(self.value, 0, 1)

    def buildCmd(self):
        return f'{self.controlPanel.actorName} {self.controlPanel.controllerName} power setpoint=%d' % self.value.getValue()


class RawCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='RAW')

        self.rawCmd = LineEdit()
        self.addWidget(self.rawCmd, 0, 1)

    def buildCmd(self):
        cmdStr = f'{self.controlPanel.actorName} {self.controlPanel.controllerName} raw=%s' % self.rawCmd.text()
        return cmdStr


class Status(ValueGB):
    def __init__(self, moduleRow, cooler):
        ValueGB.__init__(self, moduleRow, f'{cooler}Status', 'Status', 2, '{:s}')

    def setText(self, txt):
        ftext = '\n'.join([stat for stat in txt.split(',') if 'bit ' not in stat])
        self.value.setText(ftext)
        background = 'red' if ftext!='OK' else 'green'
        self.setColor(background=background, police='white')
        self.setEnabled(self.moduleRow.isOnline)


class CoolerPanel(CamDevice):
    def __init__(self, controlDialog, coolerName='cooler'):
        CamDevice.__init__(self, controlDialog, coolerName)
        self.addCommandSet(CoolerCommands(self))

    def createWidgets(self):
        cooler = self.controllerName
        self.status = Status(self.moduleRow, cooler)
        self.controlLoop = ValueGB(self.moduleRow, f'{cooler}Loop', 'controlLoop', 0, '{:s}')
        self.kP = ValueGB(self.moduleRow, f'{cooler}Loop', 'P', 1, '{:g}')
        self.kI = ValueGB(self.moduleRow, f'{cooler}Loop', 'I', 2, '{:g}')
        self.kD = ValueGB(self.moduleRow, f'{cooler}Loop', 'D', 3, '{:g}')

        self.setpoint = ValueGB(self.moduleRow, f'{cooler}Temps', 'setPoint(K)', 0, '{:g}')
        self.tip = ValueGB(self.moduleRow, f'{cooler}Temps', 'Tip(K)', 2, '{:g}')
        self.reject = ValueGB(self.moduleRow, f'{cooler}Temps', 'Reject(°C)', 1, '{:g}')

        self.minPower = ValueGB(self.moduleRow, f'{cooler}Status', 'minPower(W)', 3, '{:g}')
        self.power = ValueGB(self.moduleRow, f'{cooler}Temps', 'Power(W)', 3, '{:g}')
        self.maxPower = ValueGB(self.moduleRow, f'{cooler}Status', 'maxPower(W)', 4, '{:g}')

    def setInLayout(self):
        self.grid.addWidget(self.status, 0, 1, 1, 2)

        self.grid.addWidget(self.controlLoop, 0, 0)
        self.grid.addWidget(self.kP, 1, 0)
        self.grid.addWidget(self.kI, 1, 1)
        self.grid.addWidget(self.kD, 1, 2)

        self.grid.addWidget(self.setpoint, 2, 0)
        self.grid.addWidget(self.tip, 2, 1)
        self.grid.addWidget(self.reject, 2, 2)

        self.grid.addWidget(self.minPower, 3, 0)
        self.grid.addWidget(self.power, 3, 1)
        self.grid.addWidget(self.maxPower, 3, 2)


class CoolerCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
        self.connectButton.cmdStr = f'{self.controlPanel.actorName} connect controller=cooler name={self.controlPanel.controllerName}'
        self.tempLoop = TempLoopCmd(controlPanel=controlPanel)
        self.powerLoop = PowerLoopCmd(controlPanel=controlPanel)
        self.coolerOff = CmdButton(controlPanel=controlPanel, label='COOLER OFF',
                                   cmdStr=f'{self.controlPanel.actorName} {self.controlPanel.controllerName} off',
                                   safetyCheck=True)

        self.rawCmd = RawCmd(controlPanel=controlPanel)

        self.grid.addLayout(self.tempLoop, 2, 0, 1, 2)
        self.grid.addLayout(self.powerLoop, 3, 0, 1, 2)
        self.grid.addWidget(self.coolerOff, 4, 0)
        self.grid.addLayout(self.rawCmd, 5, 0, 1, 2)
