__author__ = 'alefur'

from functools import partial

from PyQt5.QtWidgets import QGridLayout, QWidget, QLabel, QHBoxLayout

from spsClient.viscu import Viscu


class SpsWidget(QWidget):
    def __init__(self, spsClient):
        QWidget.__init__(self)
        self.spsClient = spsClient
        self.mainLayout = QGridLayout()

        self.devices = {'r1': Viscu(self, smId=1, arm='r'), }

        for name, device in self.devices.iteritems():
            self.mainLayout.addLayout(device, 0, 0)
        self.setLayout(self.mainLayout)

    @property
    def actor(self):
        return self.spsClient.actor
