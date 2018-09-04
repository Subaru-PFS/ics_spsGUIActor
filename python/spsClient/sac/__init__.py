__author__ = 'alefur'
from spsClient import bigFont
from spsClient.modulerow import ModuleRow
from spsClient.sac.ccd import CcdPanel
from spsClient.sac.stage import StagePanel
from spsClient.widgets import ValueGB, ControlDialog


class SacRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='sac', actorLabel='SAC')

        self.state = ValueGB(self, 'metaFSM', '', 0, '{:s}', fontSize=bigFont)
        self.substate = ValueGB(self, 'metaFSM', '', 1, '{:s}', fontSize=bigFont)

        self.pentaPosition = ValueGB(self, 'lsPenta', 'Penta', 2, '{:.3f}', fontSize=bigFont)
        self.detectorPosition = ValueGB(self, 'lsDetector', 'Detector', 2, '{:.3f}', fontSize=bigFont)

    @property
    def customWidgets(self):

        widgets = [self.state, self.substate, self.pentaPosition, self.detectorPosition]

        try:
            widgets += self.controlDialog.customWidgets
        except AttributeError:
            pass

        return widgets

    def showDetails(self):
        self.controlDialog = SacDialog(self)
        self.controlDialog.show()


class SacDialog(ControlDialog):
    def __init__(self, sacRow):
        ControlDialog.__init__(self, moduleRow=sacRow)

        self.detectorPanel = StagePanel(self, 'detector')
        self.pentaPanel = StagePanel(self, 'penta')
        self.ccdPanel = CcdPanel(self)

        self.tabWidget.addTab(self.detectorPanel, 'Detector Stage')
        self.tabWidget.addTab(self.pentaPanel, 'Penta Stage')
        self.tabWidget.addTab(self.ccdPanel, 'CCD')

    @property
    def customWidgets(self):
        return [self.reload] + self.detectorPanel.customWidgets\
               + self.pentaPanel.customWidgets + self.ccdPanel.customWidgets
