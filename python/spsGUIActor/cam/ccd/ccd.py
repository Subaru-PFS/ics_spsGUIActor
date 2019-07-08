__author__ = 'alefur'
from spsGUIActor.control import CommandsGB, ControllerPanel
from spsGUIActor.widgets import ValueGB, CustomedCmd, DoubleSpinBoxGB, SpinBoxGB
from spsGUIActor.cam import CamDevice

class BiasCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='BIASES')

        self.cam = controlPanel.actorName.split('_')[1]
        self.value = SpinBoxGB('Duplicate', 1, 30)

        self.addWidget(self.value, 0, 1)

    def buildCmd(self):
        cmdStr = 'spsait bias duplicate=%d cam=%s name="Functional Test" comments="took from spsGUIActor"' % \
                 (self.value.getValue(), self.cam)
        return cmdStr


class DarksCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel, buttonLabel='DARKS')

        self.cam = controlPanel.actorName.split('_')[1]
        self.duplicate = SpinBoxGB('Duplicate', 1, 30)
        self.exptime = DoubleSpinBoxGB('Exptime', 1, 3600, 2)

        self.addWidget(self.duplicate, 0, 1)
        self.addWidget(self.exptime, 0, 2)

    def buildCmd(self):
        cmdStr = 'spsait dark exptime=%.2f duplicate=%d cam=%s name="Functional Test" comments="took from spsGUIActor"' % \
                 (self.exptime.getValue(), self.duplicate.getValue(), self.cam)

        return cmdStr


class CcdState(ValueGB):
    def __init__(self, moduleRow):
        self.moduleRow = moduleRow
        ValueGB.__init__(self, moduleRow, 'exposureState', '', 0, '{:s}')

    def setText(self, txt):
        txt = txt.upper()
        ValueGB.setText(self, txt)


class CcdPanel(CamDevice):
    def __init__(self, controlDialog):
        CamDevice.__init__(self, controlDialog, 'ccd')
        self.addCommandSet(CcdCommands(self))

    def createWidgets(self):
        self.state = CcdState(self.moduleRow, )
        self.rootDir = ValueGB(self.moduleRow, 'filepath', 'rootDir', 0, '{:s}')
        self.nightDir = ValueGB(self.moduleRow, 'filepath', 'nightDir', 1, '{:s}')
        self.filename = ValueGB(self.moduleRow, 'filepath', 'filename', 2, '{:s}')

    def setInLayout(self):
        self.grid.addWidget(self.state, 0, 0)
        self.grid.addWidget(self.rootDir, 1, 0)
        self.grid.addWidget(self.nightDir, 1, 1)
        self.grid.addWidget(self.filename, 1, 2)


class CcdCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)

        self.biasCmd = BiasCmd(controlPanel=controlPanel)
        self.darkCmd = DarksCmd(controlPanel=controlPanel)

        self.grid.addLayout(self.biasCmd, 0, 0, 1, 2)
        self.grid.addLayout(self.darkCmd, 1, 0, 1, 3)
