__author__ = 'alefur'

import argparse
import os
import pwd
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from mainwindow import SpsWidget


class Spsgui(QMainWindow):
    def __init__(self, reactor, actor, cmdrName):
        QMainWindow.__init__(self)
        self.reactor = reactor
        self.actor = actor
        self.actor.connectionMade = self.connectionMade
        self.setName("%s.%s" % ("spsGUIActor", cmdrName))
        self.isConnected = False

        self.spsWidget = SpsWidget(self)
        self.setCentralWidget(self.spsWidget)

        self.setMaximumHeight(100)
        self.showMinimized()
        self.setConnected(False)

    def setConnected(self, isConnected):
        self.isConnected = isConnected
        self.spsWidget.setEnabled(isConnected)

    def connectionMade(self):
        """ For overriding. """
        self.setConnected(True)
        self.actor.cmdr.connectionLost = self.connectionLost

    def connectionLost(self, reason):
        """ For overriding. """
        self.setConnected(False)
        if not self.actor.shuttingDown:
            self.spsWidget.showError("Connection Lost", f"Connection to tron has failed : \n{reason}")

    def setName(self, name):
        self.cmdrName = name
        self.setWindowTitle(name)

    def closeEvent(self, QCloseEvent):
        self.actor.disconnectActor()
        self.reactor.callFromThread(self.reactor.stop)
        QCloseEvent.accept()


def main():
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser()

    parser.add_argument('--name', default=pwd.getpwuid(os.getuid()).pw_name, type=str, nargs='?', help='cmdr name')

    args = parser.parse_args()

    import qt5reactor

    qt5reactor.install()
    from twisted.internet import reactor

    import miniActor

    specIds = [i + 1 for i in range(12)]
    viscamNames = ['b%i' % i for i in specIds] + ['r%i' % i for i in specIds]
    nircamNames = ['n%i' % i for i in specIds]

    xcus = ['xcu_%s' % cam for cam in viscamNames + nircamNames]
    ccds = ['ccd_%s' % cam for cam in viscamNames]
    hxs = ['hx_%s' % cam for cam in nircamNames]
    enus = ['enu_sm%i' % i for i in specIds]
    lam = ['sac', 'breva']
    sps = ['dcb', 'rough1', 'rough2']

    actor = miniActor.connectActor(['hub'] + lam + sps + enus + xcus + ccds + hxs)

    try:
        ex = Spsgui(reactor, actor, args.name)
    except:
        actor.disconnectActor()
        raise

    reactor.run()
    actor.disconnectActor()


if __name__ == "__main__":
    main()
