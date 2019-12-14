__author__ = 'alefur'
import spsGUIActor.styles as styles
from spsGUIActor.cam import CamDevice
from spsGUIActor.common import LineEdit
from spsGUIActor.control import ControllerCmd
from spsGUIActor.widgets import ValueGB, SwitchButton, CustomedCmd


class StatusString(ValueGB):
    maxNb = 2

    def __init__(self, moduleRow, key, label):
        ValueGB.__init__(self, moduleRow, key, label, 1, '{:s}')

    def setText(self, txt):
        ftext = [stat for stat in txt.split(',') if 'bit ' not in stat]
        chunks = [','.join(ftext[x:x + StatusString.maxNb]) for x in range(0, len(ftext), StatusString.maxNb)]

        self.value.setText('\n'.join(chunks))
        self.customize()


class Speed(ValueGB):
    def __init__(self, moduleRow):
        ValueGB.__init__(self, moduleRow, 'pumpSpeed', 'Speed(Hz)', 0, '{:g}')

    def customize(self):

        state = 'on' if float(self.value.text()) > 0 else 'off'
        background, police = styles.colorWidget(state)

        self.setColor(background=background, police=police)
        self.setEnabled(self.moduleRow.isOnline)


class PumpSwitch(SwitchButton):
    def __init__(self, controlPanel):
        cmdHead = '%s pump' % controlPanel.actorName
        SwitchButton.__init__(self, controlPanel, 'pumpSpeed', label='', cmdHead='',
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


class RawCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='RAW')

        self.rawCmd = LineEdit()
        self.addWidget(self.rawCmd, 0, 1)

    def buildCmd(self):
        cmdStr = '%s pump raw=%s' % (self.controlPanel.actorName, self.rawCmd.text())
        return cmdStr


class PumpPanel(CamDevice):
    def __init__(self, controlDialog):
        CamDevice.__init__(self, controlDialog, 'pump')
        self.addCommandSet(PumpCommands(self))

    def createWidgets(self):
        self.speed = Speed(self.moduleRow)
        self.status = StatusString(self.moduleRow, 'pumpStatus', 'Status')
        self.warnings = StatusString(self.moduleRow, 'pumpWarnings', 'Warnings')
        self.errors = StatusString(self.moduleRow, 'pumpErrors', 'Errors')

        self.bodyTemp = ValueGB(self.moduleRow, 'pumpTemps', 'bodyTemp(°C)', 0, '{:g}')
        self.controllerTemp = ValueGB(self.moduleRow, 'pumpTemps', 'controllerTemp(°C)', 1, '{:g}')

        self.cycleCount = ValueGB(self.moduleRow, 'pumpTimes', 'Cycle Count', 0, '{:g}')
        self.powerOnTime = ValueGB(self.moduleRow, 'pumpTimes', 'Power On time', 1, '{:g}')
        self.pumpingTime = ValueGB(self.moduleRow, 'pumpTimes', 'Pumping Time', 2, '{:g}')

        self.controllerLife = ValueGB(self.moduleRow, 'pumpLife', 'Controller Life', 0, '{:g}')
        self.tipSealLife = ValueGB(self.moduleRow, 'pumpLife', 'Tip Seal Life', 1, '{:g}')
        self.bearingLife = ValueGB(self.moduleRow, 'pumpLife', 'Bearing Life', 2, '{:g}')


    def setInLayout(self):
        self.grid.addWidget(self.speed, 0, 0, 2, 1)
        self.grid.addWidget(self.bodyTemp, 2, 0)
        self.grid.addWidget(self.controllerTemp, 3, 0)

        self.grid.addWidget(self.cycleCount, 5, 0)
        self.grid.addWidget(self.powerOnTime, 5, 1)
        self.grid.addWidget(self.pumpingTime, 5, 2)

        self.grid.addWidget(self.controllerLife, 6, 0)
        self.grid.addWidget(self.tipSealLife, 6, 1)
        self.grid.addWidget(self.bearingLife, 6, 2)

        self.grid.addWidget(self.status, 0, 1, 2, 2)
        self.grid.addWidget(self.warnings, 2, 1, 1, 2)
        self.grid.addWidget(self.errors, 3, 1, 1, 2)




class PumpCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)

        self.pumpSwitch = PumpSwitch(controlPanel=controlPanel)
        self.rawCmd = RawCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.pumpSwitch.buttonOn, 1, 0, 1, 2)
        self.grid.addWidget(self.pumpSwitch.buttonOff, 1, 0, 1, 2)
        self.grid.addLayout(self.rawCmd, 2, 0, 1, 2)
