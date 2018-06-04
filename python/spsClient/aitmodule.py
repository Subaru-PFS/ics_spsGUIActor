__author__ = 'alefur'

from PyQt5.QtWidgets import QGridLayout, QGroupBox

from spsClient.seqno import Seqno
from spsClient.dcb import Dcb


class Aitmodule(QGroupBox):
    def __init__(self, mwindow):
        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setTitle('AIT')

        self.mwindow = mwindow

        self.dcb = Dcb(self)
        self.seqno = Seqno(self)

        self.populateLayout()

    @property
    def devices(self):
        return [self.dcb, self.seqno]

    def populateLayout(self):
        for i, device in enumerate(self.devices):
            device.setLine(i)
            for j, widget in enumerate(device.widgets):
                self.grid.addWidget(widget, i, j)
