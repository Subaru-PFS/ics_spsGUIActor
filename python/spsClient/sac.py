__author__ = 'alefur'
from spsClient.device import Device
from spsClient.widgets import ValueGB


class Sac(Device):
    def __init__(self, aitModule):
        Device.__init__(self, mwindow=aitModule.mwindow, actorName='sac', deviceName='SAC')

        self.state = ValueGB(self.keyVarDict['metaFSM'], '', 0, '{:s}')
        self.substate = ValueGB(self.keyVarDict['metaFSM'], '', 1, '{:s}')

        self.pentaPosition = ValueGB(self.keyVarDict['lsPenta'], 'Penta-Position', 2, '{:.2f}')
        self.detectorPosition = ValueGB(self.keyVarDict['lsDetector'], 'Detector-Position', 2, '{:.2f}')


    @property
    def customWidgets(self):
        return [self.state, self.substate, self.pentaPosition, self.detectorPosition]
