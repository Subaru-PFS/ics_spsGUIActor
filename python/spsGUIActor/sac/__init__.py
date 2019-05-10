__author__ = 'alefur'

from spsGUIActor.control import ControlDialog
from spsGUIActor.modulerow import ModuleRow
from spsGUIActor.sac.ccd import CcdPanel
from spsGUIActor.sac.stage import StagePanel
from spsGUIActor.widgets import ValueMRow


class SacRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='sac', actorLabel='SAC')

        self.state = ValueMRow(self, 'metaFSM', '', 0, '{:s}')
        self.substate = ValueMRow(self, 'metaFSM', '', 1, '{:s}')

        self.pentaPosition = ValueMRow(self, 'lsPenta', 'Penta', 2, '{:.3f}')
        self.detectorPosition = ValueMRow(self, 'lsDetector', 'Detector', 2, '{:.3f}')
        self.createDialog(SacDialog(self))

    @property
    def widgets(self):
        return [self.state, self.substate, self.pentaPosition, self.detectorPosition]


class SacDialog(ControlDialog):
    def __init__(self, sacRow):
        ControlDialog.__init__(self, moduleRow=sacRow)

        self.detectorPanel = StagePanel(self, 'detector')
        self.pentaPanel = StagePanel(self, 'penta')
        self.ccdPanel = CcdPanel(self)

        self.tabWidget.addTab(self.detectorPanel, 'Detector Stage')
        self.tabWidget.addTab(self.pentaPanel, 'Penta Stage')
        self.tabWidget.addTab(self.ccdPanel, 'CCD')
