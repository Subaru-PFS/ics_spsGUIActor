__author__ = 'alefur'

from PyQt5.QtWidgets import QGridLayout, QGroupBox

from spsClient.viscu import Viscu


class Specmodule(QGroupBox):
    def __init__(self, mwindow, smId):
        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setTitle('Spectrograph Module %i' % smId)

        self.mwindow = mwindow
        self.smId = smId

        self.rcu = Viscu(self, 'r')
        self.bcu = Viscu(self, 'r')
        self.ncu = Viscu(self, 'r')

        self.populateLayout()

    @property
    def devices(self):
        return [self.enu, self.rcu, self.bcu, self.ncu]

    def populateLayout(self):
        for i, device in enumerate(self.devices):
            for j, widget in enumerate(device.getWidgets()):
                self.grid.addWidget(widget, i, j)