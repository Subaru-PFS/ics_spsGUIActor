__author__ = 'alefur'

import spsGUIActor.styles as styles
from spsGUIActor.widgets import ValueGB


class SpecLabel(ValueGB):
    def __init__(self, spsRow, smId):
        self.smId = smId
        ValueGB.__init__(self, spsRow, 'specModules', '', 0, '{:s}', fontSize=styles.bigFont)
        self.setText(self.specName.upper())

    @property
    def specName(self):
        return f'sm{self.smId}'

    def updateVals(self, ind, fmt, keyvar):
        self.updateWidgets(keyvar.getValue(doRaise=False))

    def updateWidgets(self, specModules=None):
        specModules = self.keyvar.getValue(doRaise=False) if specModules is None else specModules
        self.setEnabled(isOnline=self.specName in specModules)

    def setEnabled(self, isOnline):
        if isOnline:
            self.setColor(*styles.colorWidget('online'))
        else:
            self.setColor(*styles.colorWidget('offline'))
