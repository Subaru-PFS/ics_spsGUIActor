__author__ = 'alefur'
from PyQt5.QtWidgets import QLabel

from spsClient.device import Device
from functools import partial


class Dcb(Device):
    def __init__(self, specModule):
        Device.__init__(self, specModule, 'dcb')
        self.state = self.getValueGB('', self.actor, 'dcbState', 0, '{:s}')
        self.hgar = self.getValueGB('Hg-Ar', self.actor, 'hgar', 0, '{:g}')
        self.neon = self.getValueGB('Neon', self.actor, 'ne', 0, '{:g}')
        self.xenon = self.getValueGB('Xenon', self.actor, 'xenon', 0, '{:g}')
        self.halogen = self.getValueGB('Halogen', self.actor, 'halogen', 0, '{:g}')
        self.photodiode = self.getValueGB('photodiode', self.actor, 'photodiode', 0, '{:g}')

        setattr(self.state, 'pimpMe', partial(self.ColorState, self.state))
        setattr(self.hgar, 'pimpMe', partial(self.switch, self.hgar))
        setattr(self.neon, 'pimpMe', partial(self.switch, self.neon))
        setattr(self.xenon, 'pimpMe', partial(self.switch, self.xenon))
        setattr(self.halogen, 'pimpMe', partial(self.switch, self.halogen))


    def getWidgets(self):
        return [QLabel('DCB'), self.mode, self.status, self.state,
                self.hgar, self.neon, self.xenon, self.halogen, self.photodiode]

    def ColorState(self, state):
        label = state.value
        stateLabel = label.text().upper()
        label.setText(stateLabel)
        background, police = state.colors[stateLabel]
        state.setColor(background, police)

    def switch(self, state):
        boolean = {'0': 'OFF', '1': 'ON', 'nan': 'NAN'}
        label = state.value
        stateLabel = boolean[label.text()]
        label.setText(stateLabel)
        background, police = state.colors[stateLabel]
        state.setColor(background, police)
