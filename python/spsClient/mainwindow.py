__author__ = 'alefur'

from PyQt5.QtWidgets import QGridLayout, QWidget, QVBoxLayout, QLayout
from spsClient.module import Aitmodule
from spsClient.module import Specmodule


class SpsWidget(QWidget):
    def __init__(self, spsClient):
        QWidget.__init__(self)

        self.spsClient = spsClient
        self.deviceLayout = QGridLayout()
        self.mainLayout = QVBoxLayout()

        self.deviceLayout.addWidget(Aitmodule(self), 0, 0)
        self.deviceLayout.addWidget(Specmodule(self, smId=1), 1, 0, 3, 1)
        #self.deviceLayout.addWidget(Specmodule(self, smId=2, arms=['r']), 4, 0, 2, 1)

        self.mainLayout.addLayout(self.deviceLayout)
        self.setLayout(self.mainLayout)

    @property
    def actor(self):
        return self.spsClient.actor

    def sendCommand(self, actor, cmdStr, callFunc):
        import opscore.actor.keyvar as keyvar
        self.actor.cmdr.bgCall(**dict(actor=actor,
                                      cmdStr=cmdStr,
                                      timeLim=1600,
                                      callFunc=callFunc,
                                      callCodes=keyvar.AllCodes))