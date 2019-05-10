__author__ = 'alefur'

import spsGUIActor.styles as styles
from PyQt5.QtWidgets import QLineEdit
from spsGUIActor.control import ControlDialog
from spsGUIActor.dcb.aten import AtenPanel
from spsGUIActor.dcb.labsphere import LabspherePanel, AttenuatorValue
from spsGUIActor.dcb.mono import MonoPanel
from spsGUIActor.dcb.monoqth import MonoQthPanel
from spsGUIActor.modulerow import ModuleRow
from spsGUIActor.widgets import ValueGB, ValueMRow, SwitchMRow, EnumMRow, Controllers


class RowOne:
    def __init__(self, dcbRow):
        self.dcbRow = dcbRow

    @property
    def widgets(self):
        dcbRow = self.dcbRow
        return [dcbRow.state, dcbRow.substate, dcbRow.labsphere, dcbRow.attenuator,
                dcbRow.photodiode, dcbRow.halogen, dcbRow.neon, dcbRow.krypton, dcbRow.hgar]

    @property
    def displayed(self):
        return [self.dcbRow.actorStatus] + self.widgets


class RowTwo:
    def __init__(self, dcbRow):
        self.dcbRow = dcbRow

    @property
    def widgets(self):
        dcbRow = self.dcbRow
        return [dcbRow.mono, dcbRow.monoqth, dcbRow.monoshutter, dcbRow.wavelength,
                dcbRow.xenon, dcbRow.deuterium, dcbRow.argon]

    @property
    def displayed(self):
        return [None, None, None] + self.widgets


class FiberConfig(ValueGB):
    def __init__(self, controlDialog, key='fiberConfig', title='fiberConfig', fmt='{:s}', fontSize=styles.smallFont):
        self.controlDialog = controlDialog
        ValueGB.__init__(self, controlDialog.moduleRow, key=key, title=title, ind=0, fmt=fmt, fontSize=fontSize)

        self.fibers = QLineEdit()
        self.fibers.editingFinished.connect(self.newConfig)
        self.grid.removeWidget(self.value)

        self.grid.addWidget(self.fibers, 0, 0)

    def setText(self, txt):
        txt = ','.join(txt.split(';'))
        self.fibers.setText(txt)

    def newConfig(self):
        cmdStr = 'config fibers=%s' % ','.join([fib.strip() for fib in self.fibers.text().split(',')])
        self.controlDialog.moduleRow.mwindow.sendCommand(actor='dcb',
                                                         cmdStr=cmdStr,
                                                         callFunc=self.controlDialog.cmdLog.printResponse)


class DcbRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='dcb', actorLabel='DCB')

        self.state = ValueMRow(self, 'metaFSM', '', 0, '{:s}')
        self.substate = ValueMRow(self, 'metaFSM', '', 1, '{:s}')
        self.labsphere = SwitchMRow(self, 'pow_labsphere', 'Labsphere', 0, '{:g}', controllerName='aten')

        self.neon = SwitchMRow(self, 'neon', 'Neon', 0, '{:g}', controllerName='aten')
        self.xenon = SwitchMRow(self, 'xenon', 'Xenon', 0, '{:g}', controllerName='aten')
        self.hgar = SwitchMRow(self, 'hgar', 'Hg-Ar', 0, '{:g}', controllerName='aten')
        self.krypton = SwitchMRow(self, 'krypton', 'Krypton', 0, '{:g}', controllerName='aten')
        self.argon = SwitchMRow(self, 'argon', 'Argon', 0, '{:g}', controllerName='aten')
        self.deuterium = SwitchMRow(self, 'deuterium', 'Deuterium', 0, '{:g}', controllerName='aten')

        self.halogen = SwitchMRow(self, 'halogen', 'Halogen', 0, '{:s}', controllerName='labsphere')
        self.photodiode = ValueMRow(self, 'photodiode', 'photodiode', 0, '{:g}', controllerName='labsphere')
        self.attenuator = AttenuatorValue(self, fontSize=styles.bigFont)

        self.mono = SwitchMRow(self, 'pow_mono', 'Monochromator', 0, '{:g}', controllerName='aten')
        self.monoqth = SwitchMRow(self, 'monoqth', 'MonoQTH', 0, '{:g}', controllerName='monoqth')
        self.monoshutter = ValueMRow(self, 'monochromator', 'Mono-Shutter', 0, '{:s}', controllerName='mono')
        self.wavelength = ValueMRow(self, 'monochromator', 'Wavelength(nm)', 2, '{:.3f}', controllerName='mono')

        self.rowone = RowOne(self)
        self.rowtwo = RowTwo(self)

        self.controllers = Controllers(self)
        self.createDialog(DcbDialog(self))

    @property
    def widgets(self):
        return self.rowone.widgets + self.rowtwo.widgets


class DcbDialog(ControlDialog):
    def __init__(self, dcbRow):
        ControlDialog.__init__(self, moduleRow=dcbRow)
        self.fiberConfig = FiberConfig(self)
        self.topbar.addWidget(self.fiberConfig)

        self.atenPanel = AtenPanel(self)
        self.labspherePanel = LabspherePanel(self)
        self.monoPanel = MonoPanel(self)
        self.monoQthPanel = MonoQthPanel(self)

        self.tabWidget.addTab(self.atenPanel, 'Aten')
        self.tabWidget.addTab(self.labspherePanel, 'Labsphere')
        self.tabWidget.addTab(self.monoPanel, 'Monochromator')
        self.tabWidget.addTab(self.monoQthPanel, 'MonoQTH')
