__author__ = 'alefur'
import spsClient.styles as styles
from PyQt5.QtWidgets import QProgressBar
from spsClient.control import ControlDialog
from spsClient.enu.bia import BiaPanel, BiaState
from spsClient.enu.rexm import RexmPanel
from spsClient.enu.shutters import ShuttersPanel
from spsClient.enu.slit import SlitPanel
from spsClient.enu.pdu import PduPanel
from spsClient.enu.temps import TempsPanel
from spsClient.enu.iis import IisPanel
from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueMRow, Controllers


class ElapsedTime(QProgressBar):
    def __init__(self, enuRow):
        QProgressBar.__init__(self)
        self.setFormat('INTEGRATING \r\n' + '%p%')
        self.enuRow = enuRow
        self.enuRow.keyVarDict['elapsedTime'].addCallback(self.updateBar, callNow=False)
        self.enuRow.keyVarDict['integratingTime'].addCallback(self.setExptime, callNow=False)

        self.setFixedSize(90, 30)

    def setExptime(self, keyvar):
        try:
            exptime = keyvar.getValue()
        except ValueError:
            return

        self.setRange(0, exptime * 100)

    def updateBar(self, keyvar):
        try:
            val = keyvar.getValue()
        except ValueError:
            val = 0

        self.setValue(val * 100)

    def resetValue(self):
        self.hide()
        self.setValue(0)


class Substate(ValueMRow):
    def __init__(self, moduleRow):
        self.moduleRow = moduleRow
        ValueMRow.__init__(self, moduleRow, 'metaFSM', '', 1, '{:s}')
        self.elapsedTime = ElapsedTime(moduleRow)
        self.grid.addWidget(self.elapsedTime, 0, 0)

    def setText(self, txt):

        txt = txt.upper()
        if txt == 'EXPOSING':
            self.value.hide()
            self.elapsedTime.show()
            self.setMaximumSize(self.sizeHint())
        else:
            self.value.show()
            self.elapsedTime.resetValue()

        ValueMRow.setText(self, txt)


class EnuRow(ModuleRow):
    def __init__(self, specModule):
        ModuleRow.__init__(self, module=specModule, actorName='enu_sm%i' % specModule.smId, actorLabel='ENU')

        self.state = ValueMRow(self, 'metaFSM', '', 0, '{:s}')
        self.substate = Substate(self)

        self.rexm = ValueMRow(self, 'rexm', 'Red Resolution', 0, '{:s}', controllerName='rexm')
        self.slit = ValueMRow(self, 'slitLocation', 'FCA_Position', 0, '{:s}', controllerName='slit')
        self.shutters = ValueMRow(self, 'shutters', 'SHA_Position', 0, '{:s}', controllerName='bsh')
        self.bia = BiaState(self, fontSize=styles.bigFont)

        self.elapsedTime = ElapsedTime(self)
        self.controllers = Controllers(self)

        self.createDialog(EnuDialog(self))

    @property
    def widgets(self):
        return [self.state, self.substate, self.rexm, self.slit, self.shutters, self.bia]


class EnuDialog(ControlDialog):
    def __init__(self, enuRow):
        ControlDialog.__init__(self, moduleRow=enuRow, title='Entrance Unit SM%i' % enuRow.module.smId)

        self.slitPanel = SlitPanel(self)
        self.shuttersPanel = ShuttersPanel(self)
        self.biaPanel = BiaPanel(self)
        self.rexmPanel = RexmPanel(self)
        self.tempsPanel = TempsPanel(self)
        self.pduPanel = PduPanel(self)
        self.iisPanel = IisPanel(self)

        self.tabWidget.addTab(self.slitPanel, 'FCA')
        self.tabWidget.addTab(self.shuttersPanel, 'SHUTTERS')
        self.tabWidget.addTab(self.biaPanel, 'BIA')
        self.tabWidget.addTab(self.rexmPanel, 'RDA')
        self.tabWidget.addTab(self.tempsPanel, 'TEMPS')
        self.tabWidget.addTab(self.pduPanel, 'PDU')
        self.tabWidget.addTab(self.iisPanel, 'IIS')
