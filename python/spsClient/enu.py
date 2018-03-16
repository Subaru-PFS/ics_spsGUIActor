__author__ = 'alefur'
from PyQt5.QtWidgets import QLabel

from spsClient.device import Device
from functools import partial

class Enu(Device):
    def __init__(self, specModule):
        Device.__init__(self, specModule, 'enu_sm%i' % specModule.smId)
        self.state = self.getValueGB('', self.actor, 'shutters', 0, '{:s}')
        self.rexm = self.getValueGB('Red Resolution', self.actor, 'rexm', 2, '{:s}')
        self.slit = self.getValueGB('FCA_Position', self.actor, 'slitLocation', 0, '{:s}')
        self.shutters = self.getValueGB('SHA_Position', self.actor, 'shutters', 2, '{:s}')

        setattr(self.state, 'pimpMe', partial(self.colorState, self.state))

    def getWidgets(self):
        return [QLabel('ENU'), self.mode, self.status, self.state, self.rexm, self.slit, self.shutters]

    def colorState(self, state):
        label = state.value
        stateLabel = label.text().upper()
        label.setText(stateLabel)
        background, police = state.colors[stateLabel]
        state.setColor(background, police)