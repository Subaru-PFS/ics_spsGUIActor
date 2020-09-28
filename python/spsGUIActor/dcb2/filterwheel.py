__author__ = 'alefur'

from spsGUIActor.common import ComboBox
from spsGUIActor.control import ControllerPanel
from spsGUIActor.enu import EnuDeviceCmd
from spsGUIActor.widgets import ValueGB, CustomedCmd, CmdButton


class SetFilterwheel(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SET')

        self.comboWheel = ComboBox()
        self.comboWheel.addItems(['LINEWHEEL', 'QTHWHEEL'])

        self.comboPosition = ComboBox()
        self.comboPosition.addItems([f'{i + 1}' for i in range(5)])

        self.addWidget(self.comboWheel, 0, 1)
        self.addWidget(self.comboPosition, 0, 2)

    def buildCmd(self):
        return f'{self.controlPanel.actorName} set {self.comboWheel.currentText().lower()}={self.comboPosition.currentText()}'


class InitFilterwheel(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='INIT')

        self.comboWheel = ComboBox()
        self.comboWheel.addItems(['LINEWHEEL', 'QTHWHEEL'])

        self.addWidget(self.comboWheel, 0, 1)

    def buildCmd(self):
        return f'{self.controlPanel.actorName} init {self.comboWheel.currentText().lower()}'


class FilterwheelPanel(ControllerPanel):

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'filterwheel')
        self.addCommandSet(FilterwheelCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'filterwheelMode', 'Mode', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'filterwheelFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'filterwheelFSM', '', 1, '{:s}')

        self.linewheel = ValueGB(self.moduleRow, 'linewheel', 'Line Wheel', 0, '{:d}')
        self.qthwheel = ValueGB(self.moduleRow, 'qthwheel', 'QTH Wheel', 0, '{:d}')
        self.adc1 = ValueGB(self.moduleRow, 'adc', 'ADC channel 1', 0, '{:.3f}')
        self.adc2 = ValueGB(self.moduleRow, 'adc', 'ADC channel 2', 1, '{:.3f}')

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.linewheel, 1, 0)
        self.grid.addWidget(self.qthwheel, 2, 0)

        self.grid.addWidget(self.adc1, 3, 0)
        self.grid.addWidget(self.adc2, 3, 1)


class FilterwheelCommands(EnuDeviceCmd):
    def __init__(self, controlPanel):
        EnuDeviceCmd.__init__(self, controlPanel)
        self.setFilterwheel = SetFilterwheel(controlPanel=controlPanel)
        self.initFilterwheel = InitFilterwheel(controlPanel=controlPanel)
        self.adcCalib = CmdButton(controlPanel=controlPanel, label='ADC CALIB',
                                  cmdStr=f'{controlPanel.actorName} adc calib')

        self.grid.addLayout(self.initFilterwheel, 1, 0, 1, 2)
        self.grid.addLayout(self.setFilterwheel, 2, 0, 1, 3)
        self.grid.addWidget(self.adcCalib, 3, 0,)
