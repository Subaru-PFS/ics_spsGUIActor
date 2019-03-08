__author__ = 'alefur'
import spsClient.styles as styles
from spsClient.control import ControlPanel, CommandsGB
from spsClient.widgets import ValueGB, CmdButton, MonitorCmd, SwitchButton


class Status(ValueGB):
    def __init__(self, moduleRow):
        ValueGB.__init__(self, moduleRow, 'turboStatus', 'Status', 1, '{:s}')

    def setText(self, txt):
        ftext = [stat for stat in txt.split(',') if 'bit ' not in stat]
        self.value.setText('\n'.join(ftext))
        self.customize()


class TurboSwitch(SwitchButton):
    def __init__(self, controlPanel):
        cmdHead = '%s turbo' % controlPanel.actorName
        SwitchButton.__init__(self, controlPanel, 'turboSpeed', label='', cmdHead='',
                              cmdStrOn='%s start' % cmdHead, cmdStrOff='%s stop' % cmdHead,
                              labelOn='START', labelOff='STOP', safetyCheck=True)

        self.buttonOff.setColor(*styles.colorWidget('abort'))

    def setText(self, txt):
        try:
            speed = int(txt)
            bool = True if speed > 0 else False
        except ValueError:
            bool = False

        self.buttonOn.setVisible(not bool)
        self.buttonOff.setVisible(bool)


class TurboPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

    def createWidgets(self):
        self.speed = ValueGB(self.moduleRow, 'turboSpeed', 'Speed(RPM)', 0, '{:g}')
        self.status = Status(self.moduleRow)
        self.volt = ValueGB(self.moduleRow, 'turboVAW', 'Voltage(V)', 0, '{:g}')
        self.current = ValueGB(self.moduleRow, 'turboVAW', 'Current(A)', 1, '{:g}')
        self.power = ValueGB(self.moduleRow, 'turboVAW', 'Power(W)', 2, '{:g}')
        self.bodyTemp = ValueGB(self.moduleRow, 'turboTemps', 'bodyTemp(°C)', 0, '{:g}')
        self.controllerTemp = ValueGB(self.moduleRow, 'turboTemps', 'controllerTemp(°C)', 1, '{:g}')

    def setInLayout(self):
        self.grid.addWidget(self.speed, 0, 0)
        self.grid.addWidget(self.status, 0, 1, 2, 2)
        self.grid.addWidget(self.volt, 3, 0)
        self.grid.addWidget(self.current, 3, 1)
        self.grid.addWidget(self.power, 3, 2)
        self.grid.addWidget(self.bodyTemp, 4, 0)
        self.grid.addWidget(self.controllerTemp, 4, 1)

    def addCommandSet(self):
        self.commands = TurboCommands(self)
        self.grid.addWidget(self.commands, 0, 4, 5, 3)


class TurboCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s turbo status' % controlPanel.actorName)
        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='%s connect controller=turbo' % controlPanel.actorName)

        self.monitorCmd = MonitorCmd(controlPanel=controlPanel, controllerName='turbo')
        self.turboSwitch = TurboSwitch(controlPanel=controlPanel)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addWidget(self.connectButton, 0, 1)
        self.grid.addLayout(self.monitorCmd, 1, 0, 1, 2)
        self.grid.addWidget(self.turboSwitch.buttonOn, 2, 0)
        self.grid.addWidget(self.turboSwitch.buttonOff, 2, 0)
        self.grid.addWidget(self.emptySpace(30), 3, 0)
