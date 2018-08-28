__author__ = 'alefur'

from PyQt5.QtWidgets import QProgressBar
from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB


class ReadRows(QProgressBar):
    def __init__(self, ccdProp):
        QProgressBar.__init__(self)
        self.setRange(0, 4176)
        self.ccdProp = ccdProp
        ccdProp.keyVarDict['readRows'].addCallback(self.updateBar, callNow=False)
        ccdProp.keyVarDict['exposureState'].addCallback(self.hideBar)

    def updateBar(self, keyvar):
        try:
            val, __ = keyvar.getValue()

        except ValueError:
            val = 0

        self.setValue(val)

    def hideBar(self, keyvar):
        try:
            state = keyvar.getValue()
            if state == 'reading':
                self.show()
            else:
                raise ValueError

        except ValueError:
            self.hide()


class CcdRow(ModuleRow):
    def __init__(self, specModule, arm):
        ModuleRow.__init__(self, module=specModule, actorName='ccd_%s%i' % (arm, specModule.smId),
                           actorLabel='%sCU' % arm.upper())

        self.substate = CcdState(self)
        self.temperature = ValueGB(self, 'ccdTemps', 'Temperature(K)', 1, '{:g}')
        self.readRows = ReadRows(self)

    @property
    def customWidgets(self):
        return [self.substate, self.readRows, self.temperature]


class CcdState(ValueGB):
    def __init__(self, moduleRow):
        self.moduleRow = moduleRow
        ValueGB.__init__(self, moduleRow, 'exposureState', '', 0, '{:s}')

    def setText(self, txt):
        txt = txt.upper()

        ValueGB.setText(self, txt)
