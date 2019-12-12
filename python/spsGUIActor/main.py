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
        self.setName("%s.%s" % ("spsGUIActor", cmdrName))

        self.spsWidget = SpsWidget(self)
        self.setCentralWidget(self.spsWidget)

        self.setMaximumHeight(100)
        self.showMinimized()

    def setName(self, name):
        self.cmdrName = name
        self.setWindowTitle(name)

    def closeEvent(self, QCloseEvent):
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

    specIds = [i + 1 for i in range(2)]
    allcams = ['b%i' % i for i in specIds] + ['r%i' % i for i in specIds] + ['n%i' % i for i in specIds]

    ccds = ['ccd_%s' % cam for cam in allcams]
    xcus = ['xcu_%s' % cam for cam in allcams]
    enus = ['enu_sm%i' % i for i in specIds]

    actor = miniActor.connectActor(['hub', 'dcb', 'sac', 'breva', 'seqno', 'rough1'] + enus + ccds + xcus)

    try:
        ex = Spsgui(reactor, actor, args.name)
    except:
        actor.disconnectActor()
        raise

    reactor.run()
    actor.disconnectActor()


if __name__ == "__main__":
    main()
