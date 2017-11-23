__author__ = 'alefur'

from functools import partial

from PyQt5.QtWidgets import QGridLayout, QWidget, QLabel, QHBoxLayout

from spsClient.specmodule import Specmodule


class SpsWidget(QWidget):
    def __init__(self, spsClient):
        QWidget.__init__(self)
        self.spsClient = spsClient
        self.mainLayout = QGridLayout()

        #self.mainLayout.addWidget(QLabel('Mode'), 0, 1)
        #self.mainLayout.addWidget(QLabel('Status'), 0, 2)
        #self.mainLayout.addWidget(QLabel('State'), 0, 3)


        self.mainLayout.addWidget(Specmodule(self, 1), 0, 0)

        #self.devices = {'r1': Viscu(self, smId=1, arm='r'), }

        #for name, device in self.devices.iteritems():
        #    self.mainLayout.addLayout(device, 0, 0)
        self.setLayout(self.mainLayout)

    @property
    def actor(self):
        return self.spsClient.actor
