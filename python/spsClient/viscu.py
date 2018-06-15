__author__ = 'alefur'

from functools import partial

from PyQt5.QtWidgets import QProgressBar
from spsClient.device import Device
from spsClient.widgets import ValueGB


class ReadRows(QProgressBar):
    def __init__(self, ccdDevice):
        QProgressBar.__init__(self)
        self.setRange(0, 4176)
        self.ccdWidget = ccdDevice
        ccdDevice.keyVarDict['readRows'].addCallback(partial(self.updateBar), callNow=False)
        ccdDevice.keyVarDict['exposureState'].addCallback(partial(self.hideBar))

    def __del__(self):
        print('ici')

    def updateBar(self, keyvar):
        try:
            val, __ = keyvar.getValue()

        except ValueError:
            val = 0

        self.setValue(val)

    def hideBar(self, keyvar):
        try:
            state = keyvar.getValue()
            if state == 'reading':
                self.show()
            else:
                raise ValueError

        except ValueError:
            self.hide()


class Ccd(Device):
    def __init__(self, specModule, actorName, deviceName):

        Device.__init__(self, mwindow=specModule.mwindow, actorName=actorName, deviceName=deviceName)

        self.substate = ValueGB(self.keyVarDict['exposureState'], '', 0, '{:s}')
        self.temperature = ValueGB(self.keyVarDict['ccdTemps'], 'Temperature(K)', 1, '{:g}')
        self.readRows = ReadRows(self)

    @property
    def arm(self):
        return self.actorName.split('_')[1][0]

    @property
    def customWidgets(self):
        return [self.substate, self.readRows, self.temperature]

