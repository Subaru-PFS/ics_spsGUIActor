__author__ = 'alefur'
from spsGUIActor.common import LineEdit, ComboBox
from spsGUIActor.control import ControllerPanel, ControllerCmd
from spsGUIActor.widgets import ValueGB, SwitchGB, ValuesRow, SwitchButton, CustomedCmd, CmdButton


class PcmButton(SwitchButton):
    def __init__(self, controlPanel, pcmPort):
        force = 'force' if pcmPort.powerName == 'bee' else ''
        cmdStrOn = '%s power on %s' % (controlPanel.actorName, pcmPort.powerName)
        cmdStrOff = '%s power off %s %s' % (controlPanel.actorName, pcmPort.powerName, force)
        safetyCheck = pcmPort.powerName == 'bee'

        SwitchButton.__init__(self, controlPanel=controlPanel, key=pcmPort.pcmPort,
                              label=pcmPort.powerName.capitalize(), ind=1, fmt='{:s}', cmdHead='',
                              cmdStrOn=cmdStrOn,
                              cmdStrOff=cmdStrOff,
                              safetyCheck=safetyCheck)


class PcmPort(ValuesRow):
    def __init__(self, moduleRow, powerName, pcmPort):
        self.powerName = powerName
        self.pcmPort = pcmPort
        widgets = [SwitchGB(moduleRow, pcmPort, 'state', 1, '{:s}'),
                   ValueGB(moduleRow, pcmPort, 'volts', 2, '{:.3f}'),
                   ValueGB(moduleRow, pcmPort, 'amps', 3, '{:.3f}'),
                   ValueGB(moduleRow, pcmPort, 'watts', 4, '{:.3f}')]

        ValuesRow.__init__(self, widgets, title=f'{powerName.capitalize()}')


class PcmPower(ValuesRow):
    def __init__(self, moduleRow):
        widgets = [ValueGB(moduleRow, 'pcmPower', 'bus1 (V)', 0, '{:.3f}'),
                   ValueGB(moduleRow, 'pcmPower', 'bus2 (V)', 1, '{:.3f}')]

        ValuesRow.__init__(self, widgets, title='Inputs')


class PcmPanel(ControllerPanel):
    ports = dict(motors=1, gauge=2, cooler=3, temps=4, bee=5, fee=6, interlock=7, heaters=8)

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'PCM')
        self.addCommandSet(PcmCommands(self))

    def createWidgets(self):
        self.pcpPower = PcmPower(self.moduleRow)
        self.pcmPorts = [PcmPort(self.moduleRow, name, f'pcmPort{portNb}') for name, portNb in self.ports.items()]

    def setInLayout(self):
        self.grid.addWidget(self.pcpPower, 0, 0, 1, 2)
        for i, pcmPort in enumerate(self.pcmPorts):
            self.grid.addWidget(pcmPort, i + 1, 0, 1, 4)


class RawCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='RAW')

        self.rawCmd = LineEdit()
        self.addWidget(self.rawCmd, 0, 1)

    def buildCmd(self):
        cmdStr = '%s pcm raw=%s' % (self.controlPanel.actorName, self.rawCmd.text())
        return cmdStr


class MaskCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='MASK')

        self.comboCmd = ComboBox()
        self.comboCmd.addItems(['GET', 'SET'])
        self.comboCmd.currentIndexChanged.connect(self.showLineEdit)

        self.combo = ComboBox()
        self.combo.addItems(['powerOn', 'lowVoltage'])

        self.linedit = LineEdit()
        self.linedit.setVisible(False)

        self.addWidget(self.comboCmd, 0, 1)
        self.addWidget(self.combo, 0, 2)
        self.addWidget(self.linedit, 0, 3)

    def buildCmd(self):
        mask = 'mask=%s' % self.linedit.text() if self.linedit.isVisible() else ''
        cmdStr = '%s pcm %sMask %s %s' % (self.controlPanel.actorName, self.comboCmd.currentText().lower(),
                                          self.combo.currentText(), mask)
        return cmdStr

    def showLineEdit(self):
        self.linedit.setVisible(self.comboCmd.currentText() == 'SET')


class ThreshCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='THRESHOLD')

        self.comboCmd = ComboBox()
        self.comboCmd.addItems(['GET', 'SET'])
        self.comboCmd.currentIndexChanged.connect(self.showLineEdit)

        self.combo = ComboBox()
        self.combo.addItems(['upsBattery', 'upsLow', 'auxLow'])

        self.linedit = LineEdit()
        self.linedit.setVisible(False)

        self.addWidget(self.comboCmd, 0, 1)
        self.addWidget(self.combo, 0, 2)
        self.addWidget(self.linedit, 0, 3)

    def buildCmd(self):
        thresh = 'v=%s' % self.linedit.text() if self.linedit.isVisible() else ''
        cmdStr = '%s pcm %sThreshold %s %s' % (self.controlPanel.actorName, self.comboCmd.currentText().lower(),
                                               self.combo.currentText(), thresh)
        return cmdStr

    def showLineEdit(self):
        self.linedit.setVisible(self.comboCmd.currentText() == 'SET')


class PcmCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
        self.statusButton = CmdButton(controlPanel=controlPanel, label='STATUS',
                                      cmdStr='%s power status' % controlPanel.actorName)

        self.rawCmd = RawCmd(controlPanel)
        self.maskCmd = MaskCmd(controlPanel)
        self.getThresh = ThreshCmd(controlPanel)

        self.grid.addWidget(self.statusButton, 0, 0)
        self.grid.addLayout(self.rawCmd, 1, 0, 1, 2)
        self.grid.addLayout(self.maskCmd, 2, 0, 1, 2)
        self.grid.addLayout(self.getThresh, 3, 0, 1, 2)

        for i, pcmPort in enumerate(controlPanel.pcmPorts):
            self.grid.addWidget(PcmButton(controlPanel, pcmPort), 4 + i, 0, 1, 2)
