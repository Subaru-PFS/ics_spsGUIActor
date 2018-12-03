__author__ = 'alefur'

import spsClient.styles as styles
from PyQt5.QtWidgets import QGroupBox, QTabWidget, QGridLayout
from spsClient.cam.xcu.cooler import CoolerPanel
from spsClient.cam.xcu.gatevalve import GVPanel
from spsClient.cam.xcu.gauge import GaugePanel
from spsClient.cam.xcu.motors import MotorsPanel
from spsClient.cam.xcu.turbo import TurboPanel
from spsClient.control import ControlDialog
from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB, ReloadButton


class XcuRow(ModuleRow):
    def __init__(self, camRow):
        self.camRow = camRow
        ModuleRow.__init__(self, module=camRow.specModule,
                           actorName='xcu_%s%i' % (camRow.arm, camRow.specModule.smId),
                           actorLabel='XCU',
                           fontSize=styles.smallFont)

        self.pressure = ValueGB(self, 'pressure', 'Pressure(Torr)', 0, '{:g}', fontSize=styles.bigFont)

    @property
    def customWidgets(self):
        return [self.pressure]

    @property
    def allWidgets(self):
        widgets = self.customWidgets
        try:
            widgets += self.camRow.controlDialog.xcuGB.customWidgets
        except AttributeError:
            pass
        return widgets

    def setOnline(self):
        ModuleRow.setOnline(self)
        self.camRow.setOnline()

    def showDetails(self):
        pass


class XcuGB(QGroupBox, ControlDialog):
    def __init__(self, xcuRow):
        self.moduleRow = xcuRow
        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.tabWidget = QTabWidget(self)

        self.reload = ReloadButton(self)
        self.GVPanel = GVPanel(self)
        self.turboPanel = TurboPanel(self)
        self.gaugePanel = GaugePanel(self)
        self.coolerPanel = CoolerPanel(self)
        self.motorsPanel = MotorsPanel(self)

        self.tabWidget.addTab(self.GVPanel, 'Gatevalve')
        self.tabWidget.addTab(self.turboPanel, 'Turbo')
        self.tabWidget.addTab(self.coolerPanel, 'Cooler')
        self.tabWidget.addTab(self.gaugePanel, 'Gauge')
        self.tabWidget.addTab(self.motorsPanel, 'Motors')

        self.grid.addWidget(xcuRow.actorStatus, 0, 0)
        self.grid.addWidget(self.reload, 0, 1)
        self.grid.addWidget(self.tabWidget, 1, 0, 6, 6)

    @property
    def cmdBuffer(self):
        return self.moduleRow.camRow.controlDialog.cmdBuffer

    @property
    def customWidgets(self):
        return [self.reload] + self.motorsPanel.allWidgets + self.gaugePanel.allWidgets + self.turboPanel.allWidgets + \
               self.GVPanel.allWidgets + self.coolerPanel.allWidgets
