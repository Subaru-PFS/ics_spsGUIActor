__author__ = 'alefur'

from functools import partial

from PyQt5.QtWidgets import QGridLayout, QWidget, QLabel, QHBoxLayout, QLineEdit, QPushButton

from spsClient.specmodule import Specmodule
from spsClient.widgets import LogArea

class SpsWidget(QWidget):
    def __init__(self, spsClient):
        QWidget.__init__(self)
        self.spsClient = spsClient
        self.deviceLayout = QGridLayout()
        self.mainLayout = QHBoxLayout()
        self.logLayout = QGridLayout()

        self.commandLine = QLineEdit()
        self.commandLine.returnPressed.connect(self.sendCmdLine)

        self.logArea = LogArea()
        self.logLayout.addWidget(self.logArea, 0, 0, 10, 1)
        self.logLayout.addWidget(self.commandLine, 10, 0, 1, 1)

        self.deviceLayout.addWidget(Specmodule(self, smId=1), 0, 0)

        self.mainLayout.addLayout(self.deviceLayout)
        self.mainLayout.addLayout(self.logLayout)

        self.setLayout(self.mainLayout)

    @property
    def actor(self):
        return self.spsClient.actor


    def sendCmdLine(self):
        self.sendCommand(self.commandLine.text())

    def sendCommand(self, fullCmd):
        import opscore.actor.keyvar as keyvar
        [actor, cmdStr] = fullCmd.split(' ', 1)
        self.logArea.newLine('cmdIn=%s %s' % (actor, cmdStr))
        self.actor.cmdr.bgCall(**dict(actor=actor,
                                      cmdStr=cmdStr,
                                      timeLim=600,
                                      callFunc=self.returnFunc,
                                      callCodes=keyvar.AllCodes))

    def returnFunc(self, cmdVar):
        self.logArea.newLine('cmdOut=%s' % cmdVar.replyList[0].canonical())
        for i in range(len(cmdVar.replyList) - 1):
            self.logArea.newLine(cmdVar.replyList[i + 1].canonical())