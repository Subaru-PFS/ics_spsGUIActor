__author__ = 'alefur'

from PyQt5.QtWidgets import QGridLayout, QGroupBox

from spsClient.viscu import Ccd

class Specmodule(QGroupBox):
    def __init__(self, mwindow, smId):
        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setTitle('Spectrograph Module %i' % smId)

        self.mwindow = mwindow
        self.smId = smId

        self.rcu = Ccd(self, 'ccd_r1')
        self.bcu = Ccd(self, 'ccd_b1')

        self.populateLayout()

    @property
    def devices(self):
        return [self.rcu, self.bcu]

    def populateLayout(self):
        for i, device in enumerate(self.devices):
            for j, widget in enumerate(device.getWidgets()):
                self.grid.addWidget(widget, i, j)