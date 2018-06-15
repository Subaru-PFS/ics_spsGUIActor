__author__ = 'alefur'

from spsClient.widgets import ActorGB


class Device(object):
    def __init__(self, mwindow, actorName, deviceName):
        object.__init__(self)
        self.mwindow = mwindow
        self.actorName = actorName
        self.deviceName = deviceName

        self.actorStatus = ActorGB(self, keyvar=self.models['hub'].keyVarDict['actors'])
        self.actorStatus.button.clicked.connect(self.showDetails)
        self.line = 0

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

    def setLine(self, line):
        self.line = line

    def showDetails(self):
        pass
