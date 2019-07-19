__author__ = 'alefur'

from spsGUIActor.cam.xcu.cooler import CoolerPanel
from spsGUIActor.cam.xcu.gatevalve import GVPanel
from spsGUIActor.cam.xcu.gauge import GaugePanel
from spsGUIActor.cam.xcu.heaters import HeatersPanel
from spsGUIActor.cam.xcu.interlock import InterlockPanel
from spsGUIActor.cam.xcu.ionpump import IonpumpPanel
from spsGUIActor.cam.xcu.motors import MotorsPanel
from spsGUIActor.cam.xcu.pcm import PcmPanel
from spsGUIActor.cam.xcu.temps import TempsPanel
from spsGUIActor.cam.xcu.turbo import TurboPanel
from spsGUIActor.control import ControlDialog, MultiplePanel, Topbar
from spsGUIActor.modulerow import ModuleRow
from spsGUIActor.widgets import Controllers, ValueMRow


class XcuRow(ModuleRow):
    def __init__(self, camRow):
        self.camRow = camRow
        ModuleRow.__init__(self, module=camRow.module,
                           actorName='xcu_%s%i' % (camRow.arm, camRow.module.smId), actorLabel='XCU')

        self.pressure = ValueMRow(self, 'pressure', 'Pressure(Torr)', 0, '{:g}', controllerName='PCM')
        self.controllers = Controllers(self)

    @property
    def widgets(self):
        return [self.pressure]

    def setOnline(self):
        ModuleRow.setOnline(self)
        self.camRow.setOnline()

    def heartBeat(self):
        self.camRow.heartBeat()

    def createDialog(self, tabWidget):
        self.controlDialog = XcuDialog(self, tabWidget)


class XcuDialog(ControlDialog):
    def __init__(self, xcuRow, tabWidget):
        self.moduleRow = xcuRow
        self.tabWidget = tabWidget

        self.topbar = Topbar(self)
        self.topbar.insertWidget(0, self.moduleRow.actorStatus)

        self.pcmPanel = PcmPanel(self)
        self.motorsPanel = MotorsPanel(self)

        self.GVPanel = GVPanel(self)
        self.interlockPanel = InterlockPanel(self)
        self.turboPanel = TurboPanel(self)
        self.ionpumpPanel = IonpumpPanel(self)
        self.gaugePanel = GaugePanel(self)

        self.coolerPanel = CoolerPanel(self)
        self.tempsPanel = TempsPanel(self)
        self.heatersPanel = HeatersPanel(self)

        vacuumPanel = MultiplePanel(self)
        coolingPanel = MultiplePanel(self)

        vacuumPanel.addWidget(self.GVPanel, 0, 0, 1, 3)
        vacuumPanel.addWidget(self.interlockPanel, 1, 0, 1, 2)
        vacuumPanel.addWidget(self.gaugePanel, 1, 2)
        vacuumPanel.addWidget(self.turboPanel, 2, 0, 1, 3)
        vacuumPanel.addWidget(self.ionpumpPanel, 3, 0, 1, 3)

        coolingPanel.addWidget(self.coolerPanel, 0, 0, 1, 1)
        coolingPanel.addWidget(self.tempsPanel, 1, 0, 1, 1)
        coolingPanel.addWidget(self.heatersPanel, 2, 0, 1, 1)

        self.tabWidget.addTab(self.pcmPanel, 'PCM')
        self.tabWidget.addTab(self.motorsPanel, 'Motors')

        self.tabWidget.addTab(vacuumPanel, 'Pumping / Vacuum')
        self.tabWidget.addTab(coolingPanel, 'Cooling')

    @property
    def cmdBuffer(self):
        return self.moduleRow.camRow.controlDialog.cmdBuffer

    @property
    def pannels(self):
        return [self.pcmPanel, self.motorsPanel, self.GVPanel, self.interlockPanel, self.turboPanel, self.ionpumpPanel,
                self.gaugePanel, self.coolerPanel, self.tempsPanel, self.heatersPanel]
