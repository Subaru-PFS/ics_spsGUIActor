__author__ = 'alefur'
import os
import subprocess
from datetime import datetime as dt

import spsGUIActor.styles as styles
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import QPlainTextEdit


class CmdLogArea(QPlainTextEdit):
    printLevels = {'D': 0, '>': 0,
                   'I': 1, ':': 1,
                   'W': 2,
                   'F': 3, '!': 4}
    colorCode = {'d': 'regular',
                 '>': 'regular',
                 'i': 'regular',
                 ':': 'success',
                 'w': 'warning',
                 'f': 'failed',
                 '!': 'failed'}

    def __init__(self):
        QPlainTextEdit.__init__(self)
        self.setMinimumSize(720, 180)
        self.printLevel = CmdLogArea.printLevels['I']
        self.setMaximumBlockCount(10000)
        self.setReadOnly(True)

        self.setStyleSheet("background-color: black;color:white;")
        self.setFont(QFont("Monospace", 8))

    def newLine(self, newLine, code=None):
        code = 'i' if code is None else code
        color, __ = styles.colorWidget(CmdLogArea.colorCode[code])
        self.appendHtml('\n<font color="%s">%s  %s</font>' % (color, dt.now().strftime('%Y-%m-%d %H:%M:%S'), newLine))

        self.moveCursor(QTextCursor.End)
        self.ensureCursorVisible()

    def formatResponse(self, actor, code, keywords):
        color, __ = styles.colorWidget(CmdLogArea.colorCode[code])
        return '<font color="%s">%s %s %s</font>' % (color, actor, code, keywords)

    def printResponse(self, resp):
        reply = resp.replyList[-1]
        code = resp.lastCode

        if CmdLogArea.printLevels[code] >= self.printLevel:
            self.newLine(newLine='%s %s %s ' % (reply.header.actor,
                                                reply.header.code.lower(),
                                                reply.keywords.canonical(delimiter=';')),
                         code=reply.header.code.lower())


class RawLogArea(QPlainTextEdit):
    colorCode = {'i': 'regular', 'w': 'warning', 'f': 'failed', ':': 'success'}
    refresh = 60
    maxBlockCount = 20000
    maxBytes = 100000

    def __init__(self, actor):
        QPlainTextEdit.__init__(self)
        self.setMinimumSize(400, 180)
        self.actor = actor

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.parseLog)
        self.timer.setInterval(RawLogArea.refresh * 1000)
        self.timer.start()

        self.setMaximumBlockCount(RawLogArea.maxBlockCount)
        self.setReadOnly(True)

        self.setStyleSheet("background-color: black;color:white;")
        self.setFont(QFont("Monospace", 8))

        self.logs = ''
        self.parseLog(nbline=2000)

    def newLine(self, newLine):
        try:
            code = RawLogArea.colorCode[newLine.split(' ', 21)[20]]
        except (KeyError, IndexError):
            code = 'regular'

        color, __ = styles.colorWidget(code)
        self.appendHtml('\n<font color="%s">%s</font>' % (color, newLine))

    def parseLog(self, nbline=1000):
        try:
            logs = self.tail(actor=self.actor, nbline=nbline)

        except FileExistsError:
            return

        ind = logs.find(self.logs[-100:])
        newLog = logs[ind + 100:]
        self.logs += newLog
        self.logs = self.logs[-RawLogArea.maxBytes:]

        for line in (newLog.split('\n')):
            if line:
                self.newLine(newLine=line)

        self.moveCursor(QTextCursor.End)
        self.ensureCursorVisible()

    def tail(self, actor, nbline=1000):
        logfile = os.path.expandvars('$ICS_MHS_LOGS_ROOT/actors/%s/current.log' % actor)
        if not (os.path.isfile(logfile)):
            raise FileExistsError
        args = ['tail', '-n', '%d' % nbline, logfile]
        output = subprocess.check_output(args)
        return output.decode('utf8')
