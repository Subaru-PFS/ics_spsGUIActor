__author__ = 'alefur'

from PyQt5.QtWidgets import QWidget
from spsGUIActor.module import Specmodule, Aitmodule
from spsGUIActor.common import VBoxLayout

class SpsWidget(QWidget):
    def __init__(self, spsGUIActor):
        QWidget.__init__(self)
        self.spsGUIActor = spsGUIActor
        self.mainLayout = VBoxLayout()
        self.mainLayout.addWidget(Aitmodule(self))
        self.mainLayout.addWidget(Specmodule(self, smId=1, ))

        self.setLayout(self.mainLayout)

    @property
    def actor(self):
        return self.spsGUIActor.actor

    def sendCommand(self, actor, cmdStr, callFunc):
        import opscore.actor.keyvar as keyvar
        self.actor.cmdr.bgCall(**dict(actor=actor,
                                      cmdStr=cmdStr,
                                      timeLim=1600,
                                      callFunc=callFunc,
                                      callCodes=keyvar.AllCodes))
