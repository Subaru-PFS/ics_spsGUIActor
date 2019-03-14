__author__ = 'alefur'
import spsClient.styles as styles
from spsClient.control import ControllerPanel, ControllerCmd
from spsClient.widgets import ValueGB, SwitchButton


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


class TurboPanel(ControllerPanel):
    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'turbo')
        self.addCommandSet(TurboCommands(self))

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
        self.grid.addWidget(self.volt, 2, 0)
        self.grid.addWidget(self.current, 2, 1)
        self.grid.addWidget(self.power, 2, 2)
        self.grid.addWidget(self.bodyTemp, 3, 0)
        self.grid.addWidget(self.controllerTemp, 3, 1)


class TurboCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)

        self.turboSwitch = TurboSwitch(controlPanel=controlPanel)

        self.grid.addWidget(self.turboSwitch.buttonOn, 1, 0)
        self.grid.addWidget(self.turboSwitch.buttonOff, 1, 0)
