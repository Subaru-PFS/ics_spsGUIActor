__author__ = 'alefur'
from functools import partial
from spsClient.device import Device


class Sac(Device):
    def __init__(self, aitModule):
        Device.__init__(self, mwindow=aitModule.mwindow, actorName='sac', deviceName='SAC')

        self.state = self.getValueGB('', self.actorName, 'metaFSM', 0, '{:s}')
        self.substate = self.getValueGB('', self.actorName, 'metaFSM', 1, '{:s}')

        self.pentaPosition = self.getValueGB('Penta-Position', self.actorName, 'lsPenta', 1, '{:.2f}')
        self.detectorPosition = self.getValueGB('Detector-Position', self.actorName, 'lsDetector', 1, '{:.2f}')

        setattr(self.pentaPosition, 'pimpMe', partial(self.pimpValue, self.pentaPosition))
        setattr(self.detectorPosition, 'pimpMe', partial(self.pimpValue, self.detectorPosition))
        self.updateActorStatus()

    @property
    def widgets(self):
        return [self.actorStatus, self.state, self.substate, self.pentaPosition, self.detectorPosition]
