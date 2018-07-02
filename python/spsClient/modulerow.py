__author__ = 'alefur'

from PyQt5.QtWidgets import QPushButton
from spsClient.widgets import ValueGB


class ModuleRow(object):
    def __init__(self, module, actorName, actorLabel):
        object.__init__(self)
        self.module = module
        self.actorName = actorName
        self.actorLabel = actorLabel

        self.actorStatus = ActorGB(self)
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

    def setOnline(self):

        for widget in self.customWidgets:
            try:
                if not self.isOnline:
                    widget.setColor('black', 'white')
            except AttributeError:
                pass

    def setLine(self, lineNB):
        self.lineNB = lineNB

    def showDetails(self):
        pass


class ActorGB(ValueGB):
    def __init__(self, moduleRow):
        self.moduleRow = moduleRow
        self.button = QPushButton()
        self.button.setFlat(True)
        ValueGB.__init__(self, None, None, 'ACTOR', 0, '{:s}', callNow=False,
                         keyvar=moduleRow.models['hub'].keyVarDict['actors'])

        self.grid.removeWidget(self.value)
        self.setText(moduleRow.actorLabel)
        self.grid.addWidget(self.button, 0, 0)

    def updateVals(self, ind, fmt, keyvar):
        background, color = ('green', 'white') if self.moduleRow.isOnline else ('red', 'white')
        self.setColor(background, color)
        self.moduleRow.setOnline()

    def setColor(self, background, police='white'):
        bckColor = ValueGB.setColor(self, background=background, police=police)
        self.button.setStyleSheet("QPushButton{font-size: 11pt; background: %s; color:%s; }" % (bckColor, police))

    def setText(self, txt):
        self.button.setText(txt)