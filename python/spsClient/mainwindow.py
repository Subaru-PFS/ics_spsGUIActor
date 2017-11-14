__author__ = 'alefur'
from PyQt5.QtWidgets import QMainWindow
from protocol import EchoClientFactory
from twisted.internet import reactor


class SpsClient(QMainWindow):
    def __init__(self, d_width, d_height, addr, port, cmdrName, systemPath):

        QMainWindow.__init__(self)
        self.display = d_width, d_height
        self.setName("%s.%s" % ("spsClient", cmdrName))
        self.systemPath = systemPath

        self.connectClient(addr, port)
        reactor.run()

    def setName(self, name):
        self.cmdrName = name
        self.setWindowTitle(name)

    def connectClient(self, addr, port):
        self.client = EchoClientFactory(self)
        reactor.connectTCP(addr, port, self.client)

    def closeEvent(self, QCloseEvent):

        reactor.callFromThread(reactor.stop)