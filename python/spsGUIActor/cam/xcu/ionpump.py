__author__ = 'alefur'

from spsGUIActor.cam import CamDevice
from spsGUIActor.common import ComboBox, LineEdit
from spsGUIActor.control import ControllerCmd
from spsGUIActor.widgets import SwitchGB, ValuesRow, ValueGB, CustomedCmd


class Status(ValueGB):
    def __init__(self, moduleRow, pumpId):
        ValueGB.__init__(self, moduleRow, f'ionpump{pumpId}Errors', 'status', 2, '{:s}')

    def setText(self, txt):
        ftext = '\n'.join([stat for stat in txt.split(',') if 'bit ' not in stat])
        self.value.setText(ftext)
        background = 'red' if ftext != 'OK' else 'green'
        self.setColor(background=background, police='white')
        self.setEnabled(self.moduleRow.isOnline)


class Ionpump(ValuesRow):
    def __init__(self, moduleRow, pumpId):
        widgets = [SwitchGB(moduleRow, f'ionpump{pumpId}', 'state', 0, '{:g}'),
                   ValueGB(moduleRow, f'ionpump{pumpId}', 'volts', 1, '{:g}'),
                   ValueGB(moduleRow, f'ionpump{pumpId}', 'amps', 2, '{:g}'),
                   ValueGB(moduleRow, f'ionpump{pumpId}', 'temp', 3, '{:g}'),
                   ValueGB(moduleRow, f'ionpump{pumpId}', 'pressure', 4, '{:g}')]

        ValuesRow.__init__(self, widgets, title=f'ionpump{pumpId}'.capitalize())

        self.grid.addWidget(ValueGB(moduleRow, f'ionpump{pumpId}Errors', 'errorMask', 0, '{:02X}'), 1, 0)
        self.grid.addWidget(Status(moduleRow, pumpId), 1, 1, 1, 4)


class IonpumpPanel(CamDevice):
    def __init__(self, controlDialog):
        CamDevice.__init__(self, controlDialog, 'ionpump', 'Ion pumps')
        self.addCommandSet(IonpumpCommands(self))

    def createWidgets(self):
        self.ionpump1 = Ionpump(self.moduleRow, 1)
        self.ionpump2 = Ionpump(self.moduleRow, 2)

    def setInLayout(self):
        self.grid.addWidget(self.ionpump1, 0, 0)
        self.grid.addWidget(self.ionpump2, 1, 0)


class PumpCmd(CustomedCmd):
    pumpName = {0: '', 1: 'pump1', 2: 'pump2'}

    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='IONPUMP', safetyCheck=True)

        self.comboSwitch = ComboBox()
        self.comboSwitch.addItems(['ON', 'OFF'])

        self.comboPump = ComboBox()
        self.comboPump.addItems(['default (1-2)', 'pump1', 'pump2'])

        self.addWidget(self.comboSwitch, 0, 1)
        self.addWidget(self.comboPump, 0, 2)

    def buildCmd(self):
        cmdStr = '%s ionpump %s %s' % (self.controlPanel.actorName,
                                       self.comboSwitch.currentText().lower(),
                                       self.pumpName[self.comboPump.currentIndex()])
        return cmdStr


class RawCmd(CustomedCmd):
    cmdLogic = {0: 'ionpump', 1: 'ionpumpRead', 2: 'ionpumpWrite'}

    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='RAW')

        self.comboCmd = ComboBox()
        self.comboCmd.addItems(['', 'read', 'write'])
        self.rawCmd = LineEdit()

        self.addWidget(self.comboCmd, 0, 1)
        self.addWidget(self.rawCmd, 0, 2)

    def buildCmd(self):
        cmdStr = '%s %s raw=%s' % (self.controlPanel.actorName,
                                   self.cmdLogic[self.comboCmd.currentIndex()],
                                   self.rawCmd.text())
        return cmdStr


class IonpumpCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)

        self.pumpCmd = PumpCmd(controlPanel)
        self.rawCmd = RawCmd(controlPanel)

        self.grid.addLayout(self.pumpCmd, 1, 0, 1, 2)
        self.grid.addLayout(self.rawCmd, 2, 0, 1, 2)

#
# class PumpSwitch(SwitchButton):
#     def __init__(self, metaSwitch, pumpId):
#         self.metaSwitch = metaSwitch
#         self.pumpId = pumpId
#         cmdHead = '%s ionpump' % metaSwitch.controlPanel.actorName
#         SwitchButton.__init__(self, metaSwitch.controlPanel, f'ionpump{pumpId}', label='', cmdHead='',
#                               cmdStrOn=f'{cmdHead} on pump{pumpId}', cmdStrOff=f'{cmdHead} off pump{pumpId}',
#                               labelOn=f'START PUMP{pumpId}', labelOff=f'STOP PUMP{pumpId}', safetyCheck=True)
#
#         self.buttonOff.setColor(*styles.colorWidget('abort'))
#
#     def setText(self, txt):
#         SwitchButton.setText(self, txt)
#         if txt != 'nan':
#             self.metaSwitch.setState(self.pumpId, int(txt))
#
#
# class MetaSwitch(CustomedCmd):
#     def __init__(self, controlPanel):
#         self.controlPanel = controlPanel
#         self.state = {1: 0, 2: 0}
#         CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='START', safetyCheck=True)
#         self.buttonStop = InnerButton(self, label='STOP', safetyCheck=True)
#         self.buttonStop.setColor(*styles.colorWidget('abort'))
#
#         self.pumpSwitch1 = PumpSwitch(self, pumpId=1)
#         self.pumpSwitch2 = PumpSwitch(self, pumpId=2)
#
#         self.addWidget(self.buttonStop, 0, 0)
#         self.addWidget(self.pumpSwitch1, 0, 0)
#         self.addWidget(self.pumpSwitch2, 1, 0)
#
#     @property
#     def buttonStart(self):
#         return self.button
#
#     def setState(self, pumpId, state):
#         self.state[pumpId] = state
#         metaState = sum(self.state.values())
#         if metaState == 0:
#             self.buttonStart.setVisible(True)
#             self.buttonStop.setVisible(False)
#             self.pumpSwitch1.setVisible(False)
#             self.pumpSwitch2.setVisible(False)
#
#         elif metaState == 2:
#             self.buttonStart.setVisible(False)
#             self.buttonStop.setVisible(True)
#             self.pumpSwitch1.setVisible(False)
#             self.pumpSwitch2.setVisible(False)
#         else:
#             self.buttonStart.setVisible(False)
#             self.buttonStop.setVisible(False)
#             self.pumpSwitch1.setVisible(True)
#             self.pumpSwitch2.setVisible(True)
#
#     def buildCmd(self):
#         state = 'on' if self.buttonStart.isVisible() else 'off'
#         return '%s ionpump %s' % (self.controlPanel.actorName, state)
