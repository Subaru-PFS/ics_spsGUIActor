__author__ = 'alefur'
addEng = False

import numpy as np
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
from spsGUIActor.common import ComboBox, GridLayout
from spsGUIActor.control import ControlDialog, MultiplePanel, Topbar
from spsGUIActor.modulerow import ModuleRow
from spsGUIActor.widgets import Controllers, ValueMRow, CmdButton, CustomedCmd



class SetButton(CmdButton):
    def __init__(self, upperCmd):
        self.upperCmd = upperCmd
        CmdButton.__init__(self, controlPanel=None, controlDialog=upperCmd.controlDialog, label='SET cryoMode')

    def buildCmd(self):
        return self.upperCmd.buildCmd()


class SetCryoMode(CustomedCmd):
    validModes = ('offline', 'standby', 'pumpdown', 'cooldown', 'operation', 'warmup', 'bakeout')

    def __init__(self, controlDialog):
        GridLayout.__init__(self)
        self.controlDialog = controlDialog
        self.button = SetButton(self)

        self.combo = ComboBox()
        self.combo.addItems(list(SetCryoMode.validModes))

        self.addWidget(self.button, 0, 0)
        self.addWidget(self.combo, 0, 1)

    def buildCmd(self):
        cmdStr = '%s setCryoMode %s ' % (self.controlDialog.moduleRow.actorName, self.combo.currentText())
        return cmdStr


class DetectorTemp(ValueMRow):
    def __init__(self, moduleRow):
        ValueMRow.__init__(self, moduleRow, 'temps', 'Temperature(K)', 10, '{:g}', controllerName='temps')

    def updateVals(self, ind, fmt, keyvar):
        values = keyvar.getValue(doRaise=False)
        values = (values,) if not isinstance(values, tuple) else values

        temps = np.array([values[i] for i in [10, 11] if values[i] is not None])
        temps[temps >= 400] = np.nan

        try:
            value = np.nanmean(temps)
            strValue = fmt.format(value)
        except TypeError:
            strValue = 'nan'

        self.setText(strValue)
        self.moduleRow.mwindow.heartBeat()


class XcuRow(ModuleRow):
    def __init__(self, camRow):
        self.camRow = camRow
        ModuleRow.__init__(self, module=camRow.module,
                           actorName='xcu_%s%i' % (camRow.arm, camRow.module.smId), actorLabel='XCU')

        self.cryoMode = ValueMRow(self, 'cryoMode', 'cryoMode', 0, '{:s}', controllerName='')
        self.temperature = DetectorTemp(self)
        self.pressure = ValueMRow(self, 'pressure', 'Pressure(Torr)', 0, '{:g}', controllerName='PCM')
        self.controllers = Controllers(self)

    @property
    def widgets(self):
        return [self.cryoMode, self.temperature, self.pressure]

    def setOnline(self):
        ModuleRow.setOnline(self)
        self.camRow.setOnline()

    def createDialog(self, tabWidget):
        self.controlDialog = XcuDialog(self, tabWidget)


class XcuDialog(ControlDialog):
    def __init__(self, xcuRow, tabWidget):
        self.moduleRow = xcuRow
        self.tabWidget = tabWidget

        self.topbar = Topbar(self)
        self.setCryoMode = SetCryoMode(self)
        self.topbar.insertWidget(0, self.moduleRow.actorStatus)

        self.topbar.addLayout(self.setCryoMode)

        self.pcmPanel = PcmPanel(self)
        self.motorsPanel = MotorsPanel(self)

        self.GVPanel = GVPanel(self)
        self.interlockPanel = InterlockPanel(self)
        self.turboPanel = TurboPanel(self)
        self.ionpumpPanel = IonpumpPanel(self)
        self.gaugePanel = GaugePanel(self)

        self.coolerPanels = [CoolerPanel(self), CoolerPanel(self, 'cooler2')] if self.isNir else [CoolerPanel(self)]
        self.tempsPanel = TempsPanel(self)
        self.heatersPanel = HeatersPanel(self)

        vacuumPanel = MultiplePanel(self)
        coolingPanel = MultiplePanel(self)

        vacuumPanel.addWidget(self.GVPanel, 0, 0, 1, 3)
        vacuumPanel.addWidget(self.interlockPanel, 1, 0, 1, 2)
        vacuumPanel.addWidget(self.gaugePanel, 1, 2)
        vacuumPanel.addWidget(self.turboPanel, 2, 0, 1, 3)
        vacuumPanel.addWidget(self.ionpumpPanel, 3, 0, 1, 3)

        for i, cooler in enumerate(self.coolerPanels):
            coolingPanel.addWidget(cooler, i, 0)

        coolingPanel.addWidget(self.tempsPanel, i + 1, 0)
        coolingPanel.addWidget(self.heatersPanel, i + 2, 0)

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
                self.gaugePanel, self.tempsPanel, self.heatersPanel] + self.coolerPanels

    @property
    def isNir(self):
        return self.moduleRow.camRow.arm == 'n'
