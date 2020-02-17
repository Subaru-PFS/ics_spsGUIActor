__author__ = 'alefur'
from spsGUIActor.cam import CamDevice
from spsGUIActor.common import LineEdit
from spsGUIActor.control import ControllerCmd
from spsGUIActor.widgets import ValueGB, CustomedCmd

from spsGUIActor.cam.xcu import addEng


class TempsPanel(CamDevice):
    visNames = ['Detector Box', 'Mangin', 'Spider', 'Thermal Spreader', 'Front Ring',
                'Channel06', 'Channel07', 'Channel08', 'Channel09', 'Channel10', 'Detector 1','Detector 2']
    nirNames = ['Mirror Cell 1', 'Mangin', 'Mirror Cell 2', 'SiC Spreader', 'Front Ring', 'Spreader Pan', 'Channel07',
                'Radiation Shield 1', 'Radiation Shield 2', 'Sidecar', 'Detector 1', 'Detector 2']
    probeNames = dict(b=visNames, r=visNames, n=nirNames)

    def __init__(self, controlDialog):
        CamDevice.__init__(self, controlDialog, 'temps')
        self.addCommandSet(TempsCommands(self))

    def createWidgets(self):
        probeNames = self.probeNames[self.moduleRow.camRow.arm]
        add = ['Channel' not in name or addEng for name in probeNames]
        self.temps = [ValueGB(self.moduleRow, 'temps', name, i, '{:.3f}') for i, name in enumerate(probeNames) if add[i]]

    def setInLayout(self):
        for i, value in enumerate(self.temps):
            self.grid.addWidget(value, i // 4, i % 4)


class RawCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='RAW')

        self.rawCmd = LineEdit()
        self.addWidget(self.rawCmd, 0, 1)

    def buildCmd(self):
        cmdStr = '%s temps raw=%s' % (self.controlPanel.actorName, self.rawCmd.text())
        return cmdStr


class TempsCommands(ControllerCmd):
    def __init__(self, controlPanel):
        ControllerCmd.__init__(self, controlPanel)
        self.rawCmd = RawCmd(controlPanel)

        self.grid.addLayout(self.rawCmd, 1, 0, 1, 2)
