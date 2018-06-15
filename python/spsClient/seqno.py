__author__ = 'alefur'
from PyQt5.QtWidgets import QGridLayout, QGroupBox

from spsClient.device import Device
from spsClient.widgets import ValueGB


class Seqno(Device, QGroupBox):
    def __init__(self, aitModule):
        Device.__init__(self, mwindow=aitModule.mwindow, actorName='seqno', deviceName='SEQNO')

        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.visit = ValueGB(self.keyVarDict['visit'], 'VisitId', 0, '{:g}}')

    @property
    def customWidgets(self):
        return [self.visit]
