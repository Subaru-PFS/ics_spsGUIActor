__author__ = 'alefur'
from PyQt5.QtWidgets import QLabel, QGridLayout, QGroupBox

from spsClient.device import Device
from functools import partial


class Dcb(Device):
    def __init__(self, aitModule):
        Device.__init__(self, mwindow=aitModule.mwindow, actorName='dcb', deviceName='DCB')

        self.state = self.getValueGB('', self.actorName, 'metaFSM', 0, '{:s}')
        self.substate = self.getValueGB('', self.actorName, 'metaFSM', 1, '{:s}')
        self.labsphere = self.getValueGB('Labsphere', self.actorName, 'pow_labsphere', 0, '{:s}')
        self.hgar = self.getValueGB('Hg-Ar', self.actorName, 'hgar', 0, '{:g}')
        self.neon = self.getValueGB('Neon', self.actorName, 'neon', 0, '{:g}')
        self.xenon = self.getValueGB('Xenon', self.actorName, 'xenon', 0, '{:g}')
        self.halogen = self.getValueGB('Halogen', self.actorName, 'halogen', 0, '{:g}')
        self.photodiode = self.getValueGB('photodiode', self.actorName, 'photodiode', 0, '{:g}')
        self.attenuator = self.getValueGB('attenuator', self.actorName, 'attenuator', 0, '{:g}')

        setattr(self.labsphere, 'pimpMe', partial(self.pimpLabsphere, self.labsphere))

        setattr(self.hgar, 'pimpMe', partial(self.pimpSwitch, self.hgar))
        setattr(self.neon, 'pimpMe', partial(self.pimpSwitch, self.neon))
        setattr(self.xenon, 'pimpMe', partial(self.pimpSwitch, self.xenon))
        setattr(self.halogen, 'pimpMe', partial(self.pimpSwitch, self.halogen))

        setattr(self.photodiode, 'pimpMe', partial(self.pimpValue, self.photodiode))
        setattr(self.attenuator, 'pimpMe', partial(self.pimpValue, self.attenuator))

        self.updateActorStatus()

    @property
    def widgets(self):
        return [self.actorStatus, self.state, self.substate, self.labsphere, self.hgar, self.neon,
                self.xenon, self.halogen, self.photodiode, self.attenuator]

    def pimpLabsphere(self, labsphereGB):
        label = labsphereGB.value
        text = label.text()
        labsphereGB.setText(text.upper())

    def pimpSwitch(self, switchGB):
        boolean = {'0': 'OFF', '1': 'ON', 'nan': 'NAN'}
        label = switchGB.value

        stateLabel = boolean[label.text()]
        switchGB.setText(stateLabel)
