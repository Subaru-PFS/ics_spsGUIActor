__author__ = 'alefur'

import sys
import os
import pwd
import argparse

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from mainwindow import SpsWidget


class SpsClient(QMainWindow):
    def __init__(self, reactor, actor, d_width, d_height, addr, port, cmdrName, systemPath):
        QMainWindow.__init__(self)
        self.reactor = reactor
        self.actor = actor
        self.display = d_width, d_height
        self.setName("%s.%s" % ("spsClient", cmdrName))
        self.systemPath = systemPath

        self.spsWidget = SpsWidget(self)
        self.setCentralWidget(self.spsWidget)

        self.show()

    def setName(self, name):
        self.cmdrName = name
        self.setWindowTitle(name)

    def closeEvent(self, QCloseEvent):
        self.reactor.callFromThread(self.reactor.stop)
        QCloseEvent.accept()


def main():
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser()

    parser.add_argument('--host', default='localhost', type=str, nargs='?', help='tron host ip address')
    parser.add_argument('--port', default='6093', type=int, nargs='?', help='tron cmdr port')
    parser.add_argument('--name', default=pwd.getpwuid(os.getuid()).pw_name, type=str, nargs='?', help='cmdr name')
    parser.add_argument('--stretch', default=0.6, type=float, nargs='?', help='window stretching factor')

    args = parser.parse_args()

    systemPath = '%s/%s' % (os.getcwd(), sys.argv[0].split('main.py')[0])
    geometry = app.desktop().screenGeometry()
    import qt5reactor

    qt5reactor.install()
    from twisted.internet import reactor

    import miniActor

    actor = miniActor.connectActor()

    ex = SpsClient(reactor,
                   actor,
                   geometry.width() * args.stretch,
                   geometry.height() * args.stretch,
                   args.host,
                   args.port,
                   args.name,
                   systemPath)

    reactor.run()
    actor.disconnectActor()



if __name__ == "__main__":
    main()
