__author__ = 'alefur'

from PyQt5.QtWidgets import QGridLayout, QWidget, QHBoxLayout
from spsClient.aitmodule import Aitmodule
from spsClient.specmodule import Specmodule


class SpsWidget(QWidget):
    def __init__(self, spsClient):
        self.printLevels = {'D': 0, '>': 0,
                            'I': 1, ':': 1,
                            'W': 2,
                            'F': 3, '!': 4}
        self.printLevel = self.printLevels['I']

        QWidget.__init__(self)

        self.spsClient = spsClient
        self.deviceLayout = QGridLayout()
        self.mainLayout = QHBoxLayout()
        self.logLayout = QGridLayout()

        self.deviceLayout.addWidget(Aitmodule(self), 0, 0)
        self.deviceLayout.addWidget(Specmodule(self, smId=1), 1, 0, 3, 1)
        self.deviceLayout.addWidget(Specmodule(self, smId=2, cams=['r']), 4, 0, 2, 1)

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
                                      callFunc=self.printResponse,
                                      callCodes=keyvar.AllCodes))

    def printResponse(self, resp):
        reply = resp.replyList[-1]
        code = resp.lastCode

        if self.printLevels[code] >= self.printLevel:
            self.logArea.newLine("%s %s %s" % (reply.header.actor,
                                               reply.header.code.lower(),
                                               reply.keywords.canonical(delimiter=';')))
