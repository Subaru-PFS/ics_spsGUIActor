__author__ = 'alefur'

import spsClient.styles as styles
from spsClient.dcb.aten import AtenPanel
from spsClient.dcb.labsphere import LabspherePanel, AttenuatorValue
from spsClient.dcb.mono import MonoPanel
from spsClient.dcb.monoqth import MonoQthPanel
from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB, SwitchGB, EnumGB, ControlDialog


class RowOne:
    def __init__(self, dcbRow):
        self.widgets = [dcbRow.actorStatus, dcbRow.state, dcbRow.substate, dcbRow.labsphere, dcbRow.attenuator,
                        dcbRow.photodiode, dcbRow.halogen, dcbRow.neon, dcbRow.xenon]

    def setLine(self, lineNB):
        self.lineNB = lineNB


class RowTwo:
    def __init__(self, dcbRow):
        self.widgets = [None, None, None, dcbRow.mono, dcbRow.monoqth, dcbRow.monoshutter, dcbRow.wavelength,
                        dcbRow.hgar, dcbRow.krypton]

    def setLine(self, lineNB):
        self.lineNB = lineNB



class DcbRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='dcb', actorLabel='DCB')

        self.state = ValueGB(self, 'metaFSM', '', 0, '{:s}', fontSize=styles.bigFont)
        self.substate = ValueGB(self, 'metaFSM', '', 1, '{:s}', fontSize=styles.bigFont)
        self.labsphere = EnumGB(self, 'pow_labsphere', 'Labsphere', 0, '{:s}', fontSize=styles.bigFont)

        self.neon = SwitchGB(self, 'neon', 'Neon', 0, '{:g}', fontSize=styles.bigFont)
        self.xenon = SwitchGB(self, 'xenon', 'Xenon', 0, '{:g}', fontSize=styles.bigFont)
        self.hgar = SwitchGB(self, 'hgar', 'Hg-Ar', 0, '{:g}', fontSize=styles.bigFont)
        self.krypton = SwitchGB(self, 'krypton', 'Krypton', 0, '{:g}', fontSize=styles.bigFont)

        self.halogen = SwitchGB(self, 'halogen', 'Halogen', 0, '{:s}', fontSize=styles.bigFont)
        self.photodiode = ValueGB(self, 'photodiode', 'photodiode', 0, '{:g}', fontSize=styles.bigFont)
        self.attenuator = AttenuatorValue(self, fontSize=styles.bigFont)

        self.mono = SwitchGB(self, 'pow_mono', 'Monochromator', 0, '{:g}', fontSize=styles.bigFont)
        self.monoqth = SwitchGB(self, 'monoqth', 'MonoQTH', 0, '{:g}', fontSize=styles.bigFont)
        self.monoshutter = ValueGB(self, 'monochromator', 'Mono-Shutter', 0, '{:s}', fontSize=styles.bigFont)
        self.wavelength = ValueGB(self, 'monochromator', 'Wavelength(nm)', 2, '{:.3f}', fontSize=styles.bigFont)

        self.rowone = RowOne(self)
        self.rowtwo = RowTwo(self)

        self.controlDialog = DcbDialog(self)

    @property
    def customWidgets(self):
        return [self.state, self.substate, self.labsphere, self.attenuator, self.photodiode, self.halogen, self.neon,
                self.xenon, self.hgar, self.krypton, self.mono, self.monoqth, self.monoshutter, self.wavelength]


class DcbDialog(ControlDialog):
    def __init__(self, sacRow):
        ControlDialog.__init__(self, moduleRow=sacRow)

        self.atenPanel = AtenPanel(self)
        self.labspherePanel = LabspherePanel(self)
        self.monoPanel = MonoPanel(self)
        self.monoQthPanel = MonoQthPanel(self)

        self.tabWidget.addTab(self.atenPanel, 'Aten')
        self.tabWidget.addTab(self.labspherePanel, 'Labsphere')
        self.tabWidget.addTab(self.monoPanel, 'Monochromator')
        self.tabWidget.addTab(self.monoQthPanel, 'MonoQTH')

    @property
    def customWidgets(self):
        return [self.reload] + self.atenPanel.allWidgets + self.labspherePanel.allWidgets + self.monoPanel.allWidgets \
               + self.monoQthPanel.allWidgets