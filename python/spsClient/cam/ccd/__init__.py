__author__ = 'alefur'

import spsClient.styles as styles
from PyQt5.QtWidgets import QProgressBar, QTabWidget, QGridLayout, QGroupBox
from spsClient.cam.ccd.ccd import CcdPanel
from spsClient.cam.ccd.fee import FeePanel
from spsClient.control import ControlDialog
from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB, ReloadButton


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
                self.ccdRow.camRow.addReadRows()
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
        ValueGB.__init__(self, moduleRow, 'exposureState', '', 0, '{:s}', fontSize=styles.bigFont)

    def setText(self, txt):
        txt = txt.upper()
        ValueGB.setText(self, txt)


class CcdRow(ModuleRow):
    def __init__(self, camRow):
        self.camRow = camRow
        ModuleRow.__init__(self, module=camRow.specModule,
                           actorName='ccd_%s%i' % (camRow.arm, camRow.specModule.smId),
                           actorLabel='CCD',
                           fontSize=styles.smallFont)

        self.substate = CcdState(self)
        self.temperature = ValueGB(self, 'ccdTemps', 'Temperature(K)', 1, '{:g}', fontSize=styles.bigFont)
        self.readRows = ReadRows(self)

    @property
    def customWidgets(self):
        return [self.substate, self.readRows, self.temperature]

    @property
    def allWidgets(self):
        widgets = self.customWidgets
        try:
            widgets += self.camRow.controlDialog.ccdGB.customWidgets
        except AttributeError:
            pass
        return widgets

    def setOnline(self):
        ModuleRow.setOnline(self)
        self.camRow.setOnline()

    def showDetails(self):
        pass


class CcdGB(QGroupBox, ControlDialog):
    def __init__(self, ccdRow):
        self.moduleRow = ccdRow
        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.tabWidget = QTabWidget(self)
        self.reload = ReloadButton(self)

        self.feePanel = FeePanel(self)
        self.ccdPanel = CcdPanel(self)

        self.tabWidget.addTab(self.feePanel, 'Fee')
        self.tabWidget.addTab(self.ccdPanel, 'Ccd')

        self.grid.addWidget(ccdRow.actorStatus, 0, 0)
        self.grid.addWidget(self.reload, 0, 1)

        self.grid.addWidget(self.tabWidget, 1, 0, 6, 6)

    @property
    def cmdBuffer(self):
        return self.moduleRow.camRow.controlDialog.cmdBuffer
