__author__ = 'alefur'

from PyQt5.QtWidgets import QProgressBar
from spsGUIActor.cam.ccd.ccd import CcdPanel
from spsGUIActor.cam.ccd.fee import FeePanel
from spsGUIActor.control import ControlDialog, MultiplePanel, Topbar
from spsGUIActor.modulerow import ModuleRow
from spsGUIActor.widgets import Controllers, ValueMRow


class ReadRows(QProgressBar):
    def __init__(self, ccdRow):
        self.ccdRow = ccdRow
        QProgressBar.__init__(self)
        self.setRange(0, 4176)
        self.setFormat('READING \r\n' + '%p%')

        self.ccdRow.keyVarDict['readRows'].addCallback(self.updateBar, callNow=False)
        self.setFixedSize(80, 30)
        self.resetValue()

    def updateBar(self, keyvar):
        try:
            val, __ = keyvar.getValue()
        except ValueError:
            val = 0

        self.setValue(val)

    def resetValue(self):
        self.hide()
        self.setValue(0)


class CcdState(ValueMRow):
    def __init__(self, moduleRow):
        self.moduleRow = moduleRow
        ValueMRow.__init__(self, moduleRow, 'exposureState', '', 0, '{:s}', controllerName='fee')
        self.readRows = ReadRows(moduleRow)
        self.grid.addWidget(self.readRows, 0, 0)

    def setText(self, txt):
        txt = txt.upper()
        if txt == 'READING':
            self.value.hide()
            self.readRows.show()
            self.setMaximumSize(self.sizeHint())
        else:
            self.value.show()
            self.readRows.resetValue()

        ValueMRow.setText(self, txt)


class CcdRow(ModuleRow):
    def __init__(self, camRow):
        self.camRow = camRow
        ModuleRow.__init__(self, module=camRow.module,
                           actorName='ccd_%s%i' % (camRow.arm, camRow.module.smId), actorLabel='CCD')

        self.substate = CcdState(self)
        self.temperature = ValueMRow(self, 'ccdTemps', 'Temperature(K)', 1, '{:g}', controllerName='fee')
        self.readRows = ReadRows(self)
        self.controllers = Controllers(self)

    @property
    def widgets(self):
        return [self.substate, self.temperature]

    def setOnline(self):
        ModuleRow.setOnline(self)
        self.camRow.setOnline()

    def heartBeat(self):
        self.camRow.heartBeat()

    def createDialog(self, tabWidget):
        self.controlDialog = CcdDialog(self, tabWidget)


class CcdDialog(ControlDialog):
    def __init__(self, ccdRow, tabWidget):
        self.moduleRow = ccdRow
        self.tabWidget = tabWidget

        self.topbar = Topbar(self)
        self.topbar.insertWidget(0, self.moduleRow.actorStatus)

        self.feePanel = FeePanel(self)
        self.ccdPanel = CcdPanel(self)

        ccdPanel = MultiplePanel(self)

        ccdPanel.addWidget(self.ccdPanel, 0, 0)
        ccdPanel.addWidget(self.feePanel, 1, 0)

        self.tabWidget.addTab(ccdPanel, 'Ccd')

    @property
    def cmdBuffer(self):
        return self.moduleRow.camRow.controlDialog.cmdBuffer

    @property
    def pannels(self):
        return [self.ccdPanel, self.feePanel]
