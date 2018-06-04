__author__ = 'alefur'
from PyQt5.QtWidgets import QLabel, QGridLayout, QGroupBox

from spsClient.device import Device
from functools import partial


class Seqno(Device, QGroupBox):
    def __init__(self, aitModule):
        Device.__init__(self, mwindow=aitModule.mwindow, actorName='seqno', deviceName='SEQNO')

        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.visit = self.getValueGB('VisitId', self.actorName, 'visit', 0, '{:g}')
        setattr(self.visit, 'pimpMe', partial(self.pimpValue, self.visit))

        self.updateActorStatus()

    @property
    def widgets(self):
        return [self.actorStatus, self.visit]

