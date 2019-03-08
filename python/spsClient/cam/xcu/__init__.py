__author__ = 'alefur'

import spsClient.styles as styles
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout
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


class XcuGB(ControlDialog):
    def __init__(self, xcuRow):
        self.moduleRow = xcuRow

        self.topbar = QHBoxLayout()
        self.topbar.setAlignment(Qt.AlignLeft)
        self.reload = ReloadButton(self)

        self.topbar.addWidget(xcuRow.actorStatus)
        self.topbar.addWidget(self.reload)

        self.GVPanel = GVPanel(self)
        self.turboPanel = TurboPanel(self)
        self.gaugePanel = GaugePanel(self)
        self.coolerPanel = CoolerPanel(self)
        self.motorsPanel = MotorsPanel(self)

    @property
    def cmdBuffer(self):
        return self.moduleRow.camRow.controlDialog.cmdBuffer

    @property
    def virtualTabs(self):
        return dict(Gatevalve=self.GVPanel, Turbo=self.turboPanel, Cooler=self.coolerPanel, Gauge=self.gaugePanel,
                    Motors=self.motorsPanel)

    @property
    def customWidgets(self):
        topbar = [self.topbar.itemAt(i).widget() for i in range(self.topbar.count())]
        pannels = sum([tab.allWidgets for tab in self.virtualTabs.values()], [])

        return topbar + pannels
