__author__ = 'alefur'
from functools import partial
from spsClient.device import Device


class Sac(Device):
    def __init__(self, aitModule):
        Device.__init__(self, mwindow=aitModule.mwindow, actorName='sac', deviceName='SAC')

        self.pentaState = self.getValueGB('Penta-Stage', self.actorName, 'lsPenta', 0, '{:s}')
        self.pentaPosition = self.getValueGB('Penta-Position', self.actorName, 'lsPenta', 1, '{:.2f}')

        self.detectorState = self.getValueGB('Detector-Stage', self.actorName, 'lsDetector', 0, '{:s}')
        self.detectorPosition = self.getValueGB('Detector-Position', self.actorName, 'lsDetector', 1, '{:.2f}')

        self.ccdState = self.getValueGB('CCD-State', self.actorName, 'ccd', 0, '{:s}')

        setattr(self.pentaPosition, 'pimpMe', partial(self.pimpValue, self.pentaPosition))
        setattr(self.detectorPosition, 'pimpMe', partial(self.pimpValue, self.detectorPosition))
        self.updateActorStatus()

    @property
    def widgets(self):
        return [self.actorStatus, self.pentaState, self.detectorState, self.ccdState,
                self.pentaPosition, self.detectorPosition]
