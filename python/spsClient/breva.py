__author__ = 'alefur'

from spsClient.device import Device


class Breva(Device):
    def __init__(self, aitModule):
        Device.__init__(self, mwindow=aitModule.mwindow, actorName='breva', deviceName='BREVA')

        self.posX = self.getValueGB('X', self.actorName, 'position', 0, '{:.5f}')
        self.posY = self.getValueGB('Y', self.actorName, 'position', 1, '{:.5f}')
        self.posZ = self.getValueGB('Z', self.actorName, 'position', 2, '{:.5f}')
        self.posU = self.getValueGB('U', self.actorName, 'position', 3, '{:.5f}')
        self.posV = self.getValueGB('V', self.actorName, 'position', 4, '{:.5f}')
        self.posW = self.getValueGB('W', self.actorName, 'position', 5, '{:.5f}')

        self.updateActorStatus()

    @property
    def widgets(self):
        return [self.actorStatus, self.posX, self.posY, self.posZ, self.posU, self.posV, self.posW]
