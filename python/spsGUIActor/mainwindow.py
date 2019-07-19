__author__ = 'alefur'

from PyQt5.QtWidgets import QWidget
from spsGUIActor.common import VBoxLayout
from spsGUIActor.module import Specmodule, Aitmodule


class SpsWidget(QWidget):
    def __init__(self, spsGUI):
        QWidget.__init__(self)
        self.spsGUI = spsGUI
        self.mainLayout = VBoxLayout()
        self.mainLayout.addWidget(Aitmodule(self))

        for smId in range(1, 5):
            if 'sm%d' % smId not in self.actor.config.sections():
                continue

            arms = [arm.strip() for arm in self.actor.config.get('sm%d' % smId, 'arms').split(',') if arm]
            enu = self.actor.config.getboolean('sm%d' % smId, 'enu')
            self.mainLayout.addWidget(Specmodule(self, smId=smId, enu=enu, arms=arms))

        self.setLayout(self.mainLayout)

    @property
    def actor(self):
        return self.spsGUI.actor

    def sendCommand(self, actor, cmdStr, callFunc):
        import opscore.actor.keyvar as keyvar
        self.actor.cmdr.bgCall(**dict(actor=actor,
                                      cmdStr=cmdStr,
                                      timeLim=1600,
                                      callFunc=callFunc,
                                      callCodes=keyvar.AllCodes))
