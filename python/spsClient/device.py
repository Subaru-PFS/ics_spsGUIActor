__author__ = 'alefur'
from functools import partial

from spsClient.widgets import ValueGB

class Device(object):
    def __init__(self, mwindow, actorName, deviceName):
        object.__init__(self)
        self.mwindow = mwindow
        self.actorName = actorName
        self.deviceName = deviceName

        self.actorStatus = ValueGB('Actor')
        self.actorStatus.setText(deviceName)
        self.line = 0
        self.mwindow.actor.models['hub'].keyVarDict['actors'].addCallback(self.updateActorStatus, callNow=False)

    @property
    def models(self):
        return self.mwindow.actor.models

    @property
    def isOnline(self):
        return self.actorName in self.mwindow.actor.models['hub'].keyVarDict['actors']

    @property
    def widgets(self):
        return [self.actorStatus]

    def getValueGB(self, title, actorName, key, ind, fmt):
        model = self.models[actorName]
        keyvar = model.keyVarDict[key]

        valueGB = ValueGB(title)
        keyvar.addCallback(partial(self.updateVals, valueGB, ind, fmt))

        return valueGB

    def updateVals(self, label, ind, fmt, keyvar):
        values = keyvar.getValue(doRaise=False)
        values = (values,) if not isinstance(values, tuple) else values

        value = values[ind]

        try:
            strValue = fmt.format(value)
        except TypeError:
            strValue = 'nan'

        label.setText(strValue)
        label.pimpMe()

    def updateActorStatus(self, keyvar=None):
        background, color = ('green', 'white') if self.isOnline else ('red', 'white')
        self.actorStatus.setColor(background, color)

        for widget in self.widgets:
            if widget in [self.actorStatus]:
                continue
            if not self.isOnline:
                try:
                    widget.setColor('black', 'white')
                except AttributeError:
                    pass

    def pimpValue(self, valueGB):

        label = valueGB.value
        if self.isOnline:
            background, color = ('red', 'white') if label.text() == 'nan' else ('green', 'white')
        else:
            background, color = ('black', 'white')

        valueGB.setColor(background, color)

    def setLine(self, line):
        self.line = line