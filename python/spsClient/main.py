__author__ = 'alefur'

import sys
import os
import pwd
import argparse

from PyQt5.QtWidgets import QApplication

from mainwindow import SpsClient

if __name__ == "__main__":
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser()

    parser.add_argument('--host', default='localhost', type=str, nargs='?', help='tron host ip address')
    parser.add_argument('--port', default='6093', type=int, nargs='?', help='tron cmdr port')
    parser.add_argument('--name', default=pwd.getpwuid(os.getuid()).pw_name, type=str, nargs='?', help='cmdr name')
    parser.add_argument('--stretch', default=0.6, type=float, nargs='?', help='window stretching factor')

    args = parser.parse_args()

    systemPath = '%s/%s' % (os.getcwd(), sys.argv[0].split('main.py')[0])
    geometry = app.desktop().screenGeometry()

    ex = SpsClient(geometry.width() * args.stretch,
                   geometry.height() * args.stretch,
                   args.host,
                   args.port,
                   args.name,
                   systemPath)
