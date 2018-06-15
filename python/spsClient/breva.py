__author__ = 'alefur'

from spsClient.device import Device
from spsClient.widgets import Coordinates


class Breva(Device):
    def __init__(self, aitModule):
        Device.__init__(self, mwindow=aitModule.mwindow, actorName='breva', deviceName='BREVA')

        self.coordinates = Coordinates(self.keyVarDict['position'], title='Position')

    @property
    def customWidgets(self):
        return self.coordinates.widgets