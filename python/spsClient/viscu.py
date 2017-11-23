__author__ = 'alefur'
from functools import partial

from PyQt5.QtWidgets import QLabel

from spsClient.device import Device


class Cryostat(Device):
    def __init__(self, viscu):
        self.viscu = viscu
        Device.__init__(self, viscu.sm, self.viscu.xcuActor)

        self.pressure = self.getValueGB('Pressure(Torr)', self.viscu.xcuActor, 'ionpump1', 4, '{:g}')

    def getStatus(self, keyvar):
        self.viscu.getStatus(keyvar)


class Ccd(Device):
    def __init__(self, viscu):
        self.viscu = viscu

        Device.__init__(self, viscu.sm, self.viscu.ccdActor)

        self.state = self.getValueGB('', self.viscu.ccdActor, 'exposureState', 0, '{:s}')
        self.temperature = self.getValueGB('Temperature(K)', self.viscu.xcuActor, 'temps', 0, '{:g}')

        setattr(self.state, 'pimpMe', partial(self.exposureState, self.state))

    def getStatus(self, keyvar):
        self.viscu.getStatus(keyvar)

    def exposureState(self, state):
        label = state.value
        stateLabel = label.text().upper()
        label.setText(stateLabel)
        background, police = state.colors[stateLabel]
        state.setColor(background, police)


class Viscu(Device):
    def __init__(self, sm, arm):
        self.arm = arm

        Device.__init__(self, sm, 'metactor')

        self.cryostat = Cryostat(self)
        self.ccd = Ccd(self)

    def getWidgets(self):
        return [QLabel(('%scu' % self.arm).upper()), self.mode, self.status, self.ccd.state, self.ccd.temperature,
                self.cryostat.pressure]

    def getStatus(self, keyvar):
        actorList = keyvar.getValue()
        if self.xcuActor in actorList and self.ccdActor in actorList:
            self.setStatus('Online')
        else:
            self.setStatus('Offline')

    @property
    def cam(self):
        return '%s%i' % (self.arm, self.sm.smId)

    @property
    def xcuActor(self):
        return 'xcu_%s' % self.cam

    @property
    def ccdActor(self):
        return 'ccd_%s' % self.cam
