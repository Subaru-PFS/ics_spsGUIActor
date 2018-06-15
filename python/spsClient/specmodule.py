__author__ = 'alefur'

from PyQt5.QtWidgets import QGridLayout, QGroupBox
from spsClient.enu import Enu
from spsClient.viscu import Ccd


class Specmodule(QGroupBox):
    def __init__(self, mwindow, smId, cams=False):
        cams = ['b', 'r'] if not cams else cams
        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setTitle('Spectrograph Module %i' % smId)

        self.mwindow = mwindow
        self.smId = smId

        self.enu = Enu(self)
        self.cams = [Ccd(self, actorName='ccd_%s%i' % (cam, smId), deviceName='%sCU' % cam.upper()) for cam in cams]

        self.populateLayout()

    @property
    def devices(self):
        return [self.enu] + self.cams

    def populateLayout(self):
        for i, device in enumerate(self.devices):
            device.setLine(i)
            for j, widget in enumerate(device.widgets):
                self.grid.addWidget(widget, i, j)
