__author__ = 'alefur'

from PyQt5.QtWidgets import QLabel, QProgressBar

from spsClient.device import Device
from functools import partial


class ReadRows(QProgressBar):
    def __init__(self, ccdWidget):
        QProgressBar.__init__(self)
        self.setRange(0, 4176)
        self.ccdWidget = ccdWidget
        ccdWidget.keyVarDict['readRows'].addCallback(partial(self.updateBar), callNow=False)
        ccdWidget.keyVarDict['exposureState'].addCallback(partial(self.hideBar))

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

        self.substate = self.getValueGB('', self.actorName, 'exposureState', 0, '{:s}')
        self.temperature = self.getValueGB('Temperature(K)', self.actorName, 'ccdTemps', 1, '{:g}')
        self.readRows = ReadRows(self)

        self.updateActorStatus()
        setattr(self.substate, 'pimpMe', partial(self.pimpExposure, self.substate))
        setattr(self.temperature, 'pimpMe', partial(self.pimpValue, self.temperature))

    @property
    def arm(self):
        return self.actorName.split('_')[1][0]

    @property
    def widgets(self):
        return [self.actorStatus, self.substate, self.readRows, self.temperature]

    @property
    def keyVarDict(self):
        return self.models[self.actorName].keyVarDict

    def pimpExposure(self, exposureGB):
        label = exposureGB.value
        text = label.text()
        exposureGB.setText(text.upper())