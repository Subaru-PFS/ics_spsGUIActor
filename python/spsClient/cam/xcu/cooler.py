__author__ = 'alefur'

from spsClient.control import ControllerCmd, ControllerPanel
from spsClient.widgets import ValueGB, CmdButton, CustomedCmd, SpinBoxGB


class TempLoopCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET Temperature', safetyCheck=True)

        self.value = SpinBoxGB('setpoint(K)', 50, 250)
        self.addWidget(self.value, 0, 1)

    def buildCmd(self):
        return '%s cooler on setpoint=%d' % (self.controlPanel.actorName, self.value.getValue())


class PowerLoopCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='SET Power', safetyCheck=True)

        self.value = SpinBoxGB('setpoint(W)', 70, 250)
        self.addWidget(self.value, 0, 1)

    def buildCmd(self):
        return '%s cooler power setpoint=%d' % (self.controlPanel.actorName, self.value.getValue())


class Status(ValueGB):
    def __init__(self, moduleRow):
        ValueGB.__init__(self, moduleRow, 'coolerStatus', 'Status', 2, '{:s}')

    def setText(self, txt):
        ftext = [stat for stat in txt.split(',') if 'bit ' not in stat]
        self.value.setText('\n'.join(ftext))
        self.customize()


class CoolerPanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'cooler')
        self.addCommandSet(CoolerCommands(self))

    def createWidgets(self):
        self.status = Status(self.moduleRow)

        self.controlLoop = ValueGB(self.moduleRow, 'coolerLoop', 'controlLoop', 0, '{:s}')
        self.kP = ValueGB(self.moduleRow, 'coolerLoop', 'P', 1, '{:g}')
        self.kI = ValueGB(self.moduleRow, 'coolerLoop', 'I', 2, '{:g}')
        self.kD = ValueGB(self.moduleRow, 'coolerLoop', 'D', 3, '{:g}')

        self.setpoint = ValueGB(self.moduleRow, 'coolerTemps', 'setPoint(K)', 0, '{:g}')
        self.tip = ValueGB(self.moduleRow, 'coolerTemps', 'Tip(K)', 2, '{:g}')
        self.reject = ValueGB(self.moduleRow, 'coolerTemps', 'Reject(°C)', 1, '{:g}')

        self.minPower = ValueGB(self.moduleRow, 'coolerStatus', 'minPower(W)', 3, '{:g}')
        self.power = ValueGB(self.moduleRow, 'coolerTemps', 'Power(W)', 3, '{:g}')
        self.maxPower = ValueGB(self.moduleRow, 'coolerStatus', 'maxPower(W)', 4, '{:g}')

    def setInLayout(self):
        self.grid.addWidget(self.status, 0, 0)

        self.grid.addWidget(self.controlLoop, 0, 1)
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
        self.tempLoop = TempLoopCmd(controlPanel=controlPanel)
        self.powerLoop = PowerLoopCmd(controlPanel=controlPanel)
        self.coolerOff = CmdButton(controlPanel=controlPanel, label='COOLER OFF',
                                   cmdStr='%s cooler off' % controlPanel.actorName, safetyCheck=True)

        self.grid.addLayout(self.tempLoop, 2, 0, 1, 2)
        self.grid.addLayout(self.powerLoop, 3, 0, 1, 2)
        self.grid.addWidget(self.coolerOff, 4, 0, 1, 1)
