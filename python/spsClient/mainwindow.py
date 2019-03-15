__author__ = 'alefur'

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from spsClient.module import Specmodule, Aitmodule


class SpsWidget(QWidget):
    def __init__(self, spsClient):
        QWidget.__init__(self)
        self.spsClient = spsClient
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(Aitmodule(self))
        self.mainLayout.addWidget(Specmodule(self, smId=1))

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
