__author__ = 'alefur'
from PyQt5.QtWidgets import QProgressBar
from spsClient.enu.bsh import BshPanel
from spsClient.enu.rexm import RexmPanel
from spsClient.enu.slit import SlitPanel
from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB, ControlDialog
from spsClient import bigFont

class ElapsedTime(QProgressBar):
    def __init__(self, enuWidget, exptime):
        QProgressBar.__init__(self)
        self.setRange(0, exptime)
        self.enuWidget = enuWidget
        enuWidget.keyVarDict['elapsedTime'].addCallback(self.updateBar)
        enuWidget.keyVarDict['exptime'].addCallback(self.hideBar, callNow=False)

    def updateBar(self, keyvar):
        try:
            val = keyvar.getValue()
        except ValueError:
            val = 0

        self.setValue(val)

    def hideBar(self, keyvar):
        self.enuWidget.keyVarDict['elapsedTime'].removeCallback(self.updateBar)
        self.enuWidget.keyVarDict['exptime'].removeCallback(self.hideBar)
        self.enuWidget.removeWidget(self)


class EnuDialog(ControlDialog):
    def __init__(self, enuRow):
        ControlDialog.__init__(self, moduleRow=enuRow, title='Entrance Unit SM%i' % enuRow.module.smId)

        # self.textForHuman = ValueGB(enuDevice.keyVarDict['text'], 'Text', 0, '{:s}')

        self.slitPanel = SlitPanel(self)
        self.bshPanel = BshPanel(self)
        self.rexmPanel = RexmPanel(self)

        # self.grid.addWidget(self.textForHuman, 0, 0, 1, 2)
        self.grid.addWidget(self.slitPanel, 1, 0, 5, 1)
        self.grid.addWidget(self.bshPanel, 1, 1, 3, 1)
        self.grid.addWidget(self.rexmPanel, 4, 1, 2, 1)

    @property
    def customWidgets(self):
        return self.slitPanel.customWidgets + self.bshPanel.customWidgets + self.rexmPanel.customWidgets


class EnuRow(ModuleRow):
    def __init__(self, specModule):
        ModuleRow.__init__(self, module=specModule, actorName='enu_sm%i' % specModule.smId, actorLabel='ENU')

        self.state = ValueGB(self, 'metaFSM', '', 0, '{:s}', fontSize=bigFont)
        self.substate = ValueGB(self, 'metaFSM', '', 1, '{:s}', fontSize=bigFont)

        self.rexm = ValueGB(self, 'rexm', 'Red Resolution', 0, '{:s}', fontSize=bigFont)
        self.slit = ValueGB(self, 'slitLocation', 'FCA_Position', 0, '{:s}', fontSize=bigFont)
        self.shutters = ValueGB(self, 'shutters', 'SHA_Position', 0, '{:s}', fontSize=bigFont)
        self.bia = ValueGB(self, 'bia', 'BIA_State', 0, '{:s}', fontSize=bigFont)

        self.keyVarDict['integratingTime'].addCallback(self.showBar, callNow=False)

    @property
    def customWidgets(self):
        widgets = [self.state, self.substate, self.rexm, self.slit, self.shutters, self.bia]

        try:
            widgets += self.controlDialog.customWidgets
        except AttributeError:
            pass

        return widgets

    def showBar(self, keyvar):
        try:
            exptime = keyvar.getValue()
        except ValueError:
            return

        elapsedTime = ElapsedTime(self, exptime=exptime)
        self.module.grid.addWidget(elapsedTime, self.lineNB, len(self.widgets))

    def removeWidget(self, widget):
        self.state.show()
        self.module.grid.removeWidget(widget)
        widget.deleteLater()

    def showDetails(self):
        self.controlDialog = EnuDialog(self)
        self.controlDialog.show()
