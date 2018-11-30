__author__ = 'alefur'

from functools import partial

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import  QGroupBox, QGridLayout
import spsClient.styles as styles
from spsClient.widgets import ValueGB
from spsClient.common import PushButton

class ModuleRow(object):
    def __init__(self, module, actorName, actorLabel, fontSize=styles.bigFont):
        object.__init__(self)
        self.module = module
        self.actorName = actorName
        self.actorLabel = actorLabel

        self.actorStatus = ActorGB(self, fontSize=fontSize)
        self.actorStatus.button.clicked.connect(self.showDetails)
        self.lineNB = 0

    @property
    def mwindow(self):
        return self.module.mwindow

    @property
    def models(self):
        return self.mwindow.actor.models

    @property
    def keyVarDict(self):
        return self.models[self.actorName].keyVarDict

    @property
    def isOnline(self):
        return self.actorName in self.models['hub'].keyVarDict['actors']

    @property
    def widgets(self):
        return [self.actorStatus] + self.customWidgets

    @property
    def allWidgets(self):
        return self.customWidgets + self.controlDialog.customWidgets

    def setOnline(self, isOnline=None):
        isOnline = isOnline if isOnline is not None else self.isOnline

        self.actorStatus.setOnline(isOnline=isOnline)

        for widget in self.allWidgets:
            widget.setEnabled(isOnline)

    def setLine(self, lineNB):
        self.lineNB = lineNB

    def showDetails(self):
        self.controlDialog.setVisible(True)


class ActorGB(ValueGB, QGroupBox):
    def __init__(self, moduleRow, fontSize=styles.bigFont):
        self.moduleRow = moduleRow
        self.keyvar = moduleRow.models['hub'].keyVarDict['actors']
        self.fontSize = fontSize

        QGroupBox.__init__(self)
        self.setTitle('Actor')

        self.button = PushButton()
        self.button.setFlat(True)
        self.setText(moduleRow.actorLabel)

        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.grid)
        self.grid.addWidget(self.button, 0, 0)

        QTimer.singleShot(1000, self.attachCallback)

    def attachCallback(self):
        self.cb = partial(self.newConnection)
        self.keyvar.addCallback(self.cb, callNow=True)

    def newConnection(self, keyvar):
        self.moduleRow.setOnline()

    def setOnline(self, isOnline):
        self.setColor(*styles.colorWidget('online' if isOnline else 'offline'))

    def setColor(self, background, police='white'):
        bckColor = ValueGB.setBackground(self, background=background)
        self.button.setStyleSheet(
            "QPushButton{font-size: %ipt; background: %s; color:%s; }" % (self.fontSize, bckColor, police))

    def setText(self, txt):
        self.button.setText(txt)
