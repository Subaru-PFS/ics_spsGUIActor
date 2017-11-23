__author__ = 'alefur'
from functools import partial

from spsClient.widgets import ValueGB


class Device(object):
    def __init__(self, sm, actor):
        object.__init__(self)
        self.sm = sm
        self.actor = actor
        self.mode = ValueGB('')
        self.status = ValueGB('')
        self.state = ValueGB('')

        for gb in [self.mode, self.status, self.state]:
            gb.setText('UNDEF')

        self.setMode('Operation')

        self.models['hub'].keyVarDict['actors'].addCallback(self.getStatus)

    @property
    def mwindow(self):
        return self.sm.mwindow

    @property
    def models(self):
        return self.mwindow.actor.models

    def setMode(self, mode):
        self.mode.setText(mode)

    def setStatus(self, status):
        if status == 'Offline':
            self.status.setColor('red')
        elif status == 'Online':
            self.status.setColor('green')

        self.status.setText(status)

    def setState(self, state):
        self.state.setText(state)

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

        strValue = 'nan' if value is None else fmt.format(value)
        label.setText(strValue)
        label.pimpMe()

    def getStatus(self, keyvar):
        if self.actor in keyvar.getValue():
            self.setStatus('Online')
        else:
            self.setStatus('Offline')
