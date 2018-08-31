__author__ = 'alefur'

from PyQt5.QtWidgets import QProgressBar
from spsClient import bigFont
from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB


class ReadRows(QProgressBar):
    def __init__(self, ccdRow):
        self.ccdRow = ccdRow
        QProgressBar.__init__(self)
        self.setRange(0, 4176)
        self.setFormat('READING \r\n' + '%p%')

        self.ccdRow.keyVarDict['readRows'].addCallback(self.updateBar, callNow=False)
        self.ccdRow.keyVarDict['exposureState'].addCallback(self.hideBar)
        self.setFixedSize(90, 45)

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
                self.ccdRow.substate.hide()
                self.ccdRow.cam.addReadRows()
                self.show()

            else:
                raise ValueError

        except ValueError:
            self.resetValue()

    def resetValue(self):
        self.hide()
        self.setValue(0)
        self.ccdRow.substate.show()


class CcdState(ValueGB):
    def __init__(self, moduleRow):
        self.moduleRow = moduleRow
        ValueGB.__init__(self, moduleRow, 'exposureState', '', 0, '{:s}', fontSize=bigFont)

    def setText(self, txt):
        txt = txt.upper()

        ValueGB.setText(self, txt)


class CcdRow(ModuleRow):
    def __init__(self, cam):
        self.cam = cam
        ModuleRow.__init__(self, module=cam.specModule,
                           actorName='ccd_%s%i' % (cam.arm, cam.specModule.smId),
                           actorLabel='%sCU' % cam.arm.upper())

        self.substate = CcdState(self)
        self.temperature = ValueGB(self, 'ccdTemps', 'Temperature(K)', 1, '{:g}', fontSize=bigFont)
        self.readRows = ReadRows(self)

    @property
    def customWidgets(self):
        return [self.substate, self.readRows, self.temperature]

    def setOnline(self):
        ModuleRow.setOnline(self)
        self.cam.setOnline()
