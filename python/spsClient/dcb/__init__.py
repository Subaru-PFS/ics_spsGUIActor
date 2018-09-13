__author__ = 'alefur'

from spsClient import bigFont
from spsClient.dcb.aten import AtenPanel
from spsClient.dcb.labsphere import LabspherePanel
from spsClient.dcb.mono import MonoPanel
from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB, SwitchGB, EnumGB, ControlDialog


class DcbRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='dcb', actorLabel='DCB')

        self.state = ValueGB(self, 'metaFSM', '', 0, '{:s}', fontSize=bigFont)
        self.substate = ValueGB(self, 'metaFSM', '', 1, '{:s}', fontSize=bigFont)
        self.labsphere = EnumGB(self, 'pow_labsphere', 'Labsphere', 0, '{:s}', fontSize=bigFont)
        self.hgar = SwitchGB(self, 'hgar', 'Hg-Ar', 0, '{:g}', fontSize=bigFont)
        self.neon = SwitchGB(self, 'neon', 'Neon', 0, '{:g}', fontSize=bigFont)
        self.xenon = SwitchGB(self, 'xenon', 'Xenon', 0, '{:g}', fontSize=bigFont)
        self.halogen = SwitchGB(self, 'halogen', 'Halogen', 0, '{:g}', fontSize=bigFont)
        self.photodiode = ValueGB(self, 'photodiode', 'photodiode', 0, '{:g}', fontSize=bigFont)
        self.attenuator = ValueGB(self, 'attenuator', 'attenuator', 0, '{:g}', fontSize=bigFont)

    @property
    def customWidgets(self):
        return [self.state, self.substate, self.labsphere, self.hgar, self.neon, self.xenon, self.halogen,
                self.photodiode, self.attenuator]

    def showDetails(self):
        self.controlDialog = DcbDialog(self)
        self.controlDialog.show()


class DcbDialog(ControlDialog):
    def __init__(self, sacRow):
        ControlDialog.__init__(self, moduleRow=sacRow)

        self.atenPanel = AtenPanel(self)
        self.labspherePanel = LabspherePanel(self)
        self.monoPanel = MonoPanel(self)

        self.tabWidget.addTab(self.atenPanel, 'Aten')
        self.tabWidget.addTab(self.labspherePanel, 'Labsphere')
        self.tabWidget.addTab(self.monoPanel, 'Monochromator')

    @property
    def customWidgets(self):
        return [self.reload] + self.atenPanel.allWidgets + self.labspherePanel.allWidgets + self.monoPanel.allWidgets
