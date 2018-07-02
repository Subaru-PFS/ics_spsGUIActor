__author__ = 'alefur'

from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB


class SacRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='sac', actorLabel='SAC')

        self.state = ValueGB(self, 'metaFSM', '', 0, '{:s}')
        self.substate = ValueGB(self, 'metaFSM', '', 1, '{:s}')

        self.pentaPosition = ValueGB(self, 'lsPenta', 'Penta-Position', 2, '{:.2f}')
        self.detectorPosition = ValueGB(self, 'lsDetector', 'Detector-Position', 2, '{:.2f}')

    @property
    def customWidgets(self):
        return [self.state, self.substate, self.pentaPosition, self.detectorPosition]
