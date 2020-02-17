__author__ = 'alefur'

import spsGUIActor.styles as styles
from PyQt5.QtWidgets import QWidget, QMessageBox, QGroupBox, QLabel, QDial
from spsGUIActor.common import GridLayout, HBoxLayout
from spsGUIActor.module import Aitmodule, Specmodule
from spsGUIActor.widgets import ValueGB


class TronDial(QDial):
    style = ''' QDial{background-color:QLinearGradient(x1: 0.177, y1: 0.004, x2: 0.831, y2: 0.911,  stop: 0 white,
    stop: 0.061 white, stop: 0.066 lightgray, stop: 0.5 #242424, stop: 0.505 #000000,stop: 0.827 #040404,
    stop: 0.966 #292929,stop: 0.983 #2e2e2e); }'''

    def __init__(self):
        QDial.__init__(self)
        self.setMinimum(0)
        self.setMaximum(10)
        self.setValue(0)
        self.setMaximumSize(30, 30)
        self.setWrapping(True)  # Smooth transition from 99 to 0
        self.setNotchesVisible(True)
        self.setStyleSheet(self.style)

    def heartBeat(self):
        value = self.value() + 1
        value = 0 if value > self.maximum() else value
        self.setValue(value)


class TronLayout(HBoxLayout):
    def __init__(self):
        HBoxLayout.__init__(self)
        self.addStretch()
        self.tronStatus = TronStatus()
        self.addWidget(self.tronStatus)

    def widget(self):
        return self.tronStatus


class TronStatus(ValueGB):
    def __init__(self, fontSize=styles.smallFont):
        self.fontSize = fontSize

        QGroupBox.__init__(self)
        self.setTitle('TRON')

        self.grid = GridLayout()
        self.grid.setContentsMargins(5, 0, 0, 0)

        self.value = QLabel()
        self.dial = TronDial()

        self.grid.addWidget(self.value, 0, 0)
        self.grid.addWidget(self.dial, 0, 1)
        self.setLayout(self.grid)

    def setEnabled(self, isOnline):
        text = 'ONLINE' if isOnline else 'OFFLINE'
        key = text if isOnline else 'failed'
        self.value.setText(text)
        self.setColor(*styles.colorWidget(key))


class SpsWidget(QWidget):
    def __init__(self, spsGUI):
        QWidget.__init__(self)
        self.spsGUI = spsGUI
        self.tronLayout = TronLayout()
        self.mainLayout = GridLayout()
        self.mainLayout.setSpacing(1)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.addLayout(self.tronLayout, 0, 0)
        self.mainLayout.addWidget(Aitmodule(self), 1, 0)

        for smId in range(1, 5):
            if 'sm%d' % smId not in self.actor.config.sections():
                continue

            arms = [arm.strip() for arm in self.actor.config.get('sm%d' % smId, 'arms').split(',') if arm]
            enu = self.actor.config.getboolean('sm%d' % smId, 'enu')
            self.mainLayout.addWidget(Specmodule(self, smId=smId, enu=enu, arms=arms), smId + 1, 0)

        self.setLayout(self.mainLayout)

    @property
    def actor(self):
        return self.spsGUI.actor

    @property
    def isConnected(self):
        return self.spsGUI.isConnected

    def sendCommand(self, actor, cmdStr, callFunc):
        import opscore.actor.keyvar as keyvar
        self.actor.cmdr.bgCall(**dict(actor=actor,
                                      cmdStr=cmdStr,
                                      timeLim=1600,
                                      callFunc=callFunc,
                                      callCodes=keyvar.AllCodes))

    def heartBeat(self):
        self.tronLayout.tronStatus.dial.heartBeat()

    def showError(self, title, error):
        reply = QMessageBox.critical(self, title, error, QMessageBox.Ok)

    def setEnabled(self, a0: bool) -> None:
        widgets = [self.mainLayout.itemAt(i).widget() for i in range(self.mainLayout.count())]

        for widget in widgets:
            widget.setEnabled(a0)
