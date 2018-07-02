__author__ = 'alefur'

from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB


class DcbRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='dcb', actorLabel='DCB')

        self.state = ValueGB(self, 'metaFSM', '', 0, '{:s}')
        self.substate = ValueGB(self, 'metaFSM', '', 1, '{:s}')
        self.labsphere = ValueGB(self, 'pow_labsphere', 'Labsphere', 0, '{:s}')
        self.hgar = ValueGB(self, 'hgar', 'Hg-Ar', 0, '{:g}')
        self.neon = ValueGB(self, 'neon', 'Neon', 0, '{:g}')
        self.xenon = ValueGB(self, 'xenon', 'Xenon', 0, '{:g}')
        self.halogen = ValueGB(self, 'halogen', 'Halogen', 0, '{:g}')
        self.photodiode = ValueGB(self, 'photodiode', 'photodiode', 0, '{:g}')
        self.attenuator = ValueGB(self, 'attenuator', 'attenuator', 0, '{:g}')

    @property
    def customWidgets(self):
        return [self.state, self.substate, self.labsphere, self.hgar, self.neon, self.xenon, self.halogen,
                self.photodiode, self.attenuator]
