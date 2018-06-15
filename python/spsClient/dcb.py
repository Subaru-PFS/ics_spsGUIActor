__author__ = 'alefur'

from spsClient.device import Device
from spsClient.widgets import ValueGB


class Dcb(Device):
    def __init__(self, aitModule):
        Device.__init__(self, mwindow=aitModule.mwindow, actorName='dcb', deviceName='DCB')

        self.state = ValueGB(self.keyVarDict['metaFSM'], '', 0, '{:s}')
        self.substate = ValueGB(self.keyVarDict['metaFSM'], '', 1, '{:s}')
        self.labsphere = ValueGB(self.keyVarDict['pow_labsphere'], 'Labsphere', 0, '{:s}')
        self.hgar = ValueGB(self.keyVarDict['hgar'], 'Hg-Ar', 0, '{:g}')
        self.neon = ValueGB(self.keyVarDict['neon'], 'Neon', 0, '{:g}')
        self.xenon = ValueGB(self.keyVarDict['xenon'], 'Xenon', 0, '{:g}')
        self.halogen = ValueGB(self.keyVarDict['halogen'], 'Halogen', 0, '{:g}')
        self.photodiode = ValueGB(self.keyVarDict['photodiode'], 'photodiode', 0, '{:g}')
        self.attenuator = ValueGB(self.keyVarDict['attenuator'], 'attenuator', 0, '{:g}')

    @property
    def customWidgets(self):
        return [self.state, self.substate, self.labsphere, self.hgar, self.neon, self.xenon, self.halogen,
                self.photodiode, self.attenuator]