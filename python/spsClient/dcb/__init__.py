__author__ = 'alefur'

from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB, SwitchGB, EnumGB, ControlDialog, ControlPanel, CommandsGB, CmdButton, \
    CustomedCmd, SpinBoxGB, QLabel

from spsClient.dcb.aten import AtenPanel
from spsClient.dcb.labsphere import LabspherePanel


class DcbRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='dcb', actorLabel='DCB')

        self.state = ValueGB(self, 'metaFSM', '', 0, '{:s}')
        self.substate = ValueGB(self, 'metaFSM', '', 1, '{:s}')
        self.labsphere = EnumGB(self, 'pow_labsphere', 'Labsphere', 0, '{:s}')
        self.hgar = SwitchGB(self, 'hgar', 'Hg-Ar', 0, '{:g}')
        self.neon = SwitchGB(self, 'neon', 'Neon', 0, '{:g}')
        self.xenon = SwitchGB(self, 'xenon', 'Xenon', 0, '{:g}')
        self.halogen = SwitchGB(self, 'halogen', 'Halogen', 0, '{:g}')
        self.photodiode = ValueGB(self, 'photodiode', 'photodiode', 0, '{:g}')
        self.attenuator = ValueGB(self, 'attenuator', 'attenuator', 0, '{:g}')

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

        self.grid.addWidget(self.atenPanel, 0, 0)
        self.grid.addWidget(self.labspherePanel, 1, 0)

    @property
    def customWidgets(self):
        return self.atenPanel.customWidgets + self.labspherePanel.customWidgets
