__author__ = 'alefur'

from PyQt5.QtWidgets import QGroupBox, QTabWidget, QGridLayout
from spsClient import bigFont, smallFont
from spsClient.cam.xcu.motors import MotorsPanel
from spsClient.modulerow import ModuleRow
from spsClient.widgets import ControlDialog, ValueGB, ReloadButton


class XcuRow(ModuleRow):
    def __init__(self, camRow):
        self.camRow = camRow
        ModuleRow.__init__(self, module=camRow.specModule,
                           actorName='xcu_%s%i' % (camRow.arm, camRow.specModule.smId),
                           actorLabel='XCU',
                           fontSize=smallFont)

        self.pressure = ValueGB(self, 'pressure', 'Pressure(Torr)', 0, '{:g}', fontSize=bigFont)

    @property
    def customWidgets(self):
        widgets = [self.pressure]

        try:
            widgets += self.camRow.controlDialog.xcuGB.customWidgets
        except AttributeError:
            pass

        return widgets

    def setOnline(self):
        ModuleRow.setOnline(self)
        self.camRow.setOnline()


class XcuGB(QGroupBox, ControlDialog):
    def __init__(self, xcuRow):
        self.moduleRow = xcuRow
        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.tabWidget = QTabWidget(self)

        self.reload = ReloadButton(self)
        self.motorsPanel = MotorsPanel(self)

        self.tabWidget.addTab(self.motorsPanel, 'Motors')

        self.grid.addWidget(xcuRow.actorStatus, 0, 0)
        self.grid.addWidget(self.reload, 0, 1)
        self.grid.addWidget(self.tabWidget, 1, 0, 6, 6)

    @property
    def cmdBuffer(self):
        return self.moduleRow.camRow.controlDialog.cmdBuffer

    @property
    def customWidgets(self):
        return [self.reload] + self.motorsPanel.customWidgets
