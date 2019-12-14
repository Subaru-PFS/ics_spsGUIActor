__author__ = 'alefur'

from spsGUIActor.control import ControlDialog
from spsGUIActor.dcb import FiberConfig
from spsGUIActor.dcb2.sources import SourcesPanel
from spsGUIActor.enu import ConnectCmd
from spsGUIActor.modulerow import ModuleRow
from spsGUIActor.widgets import ValueMRow, SwitchMRow, Controllers


class Dcb2Row(ModuleRow):
    def __init__(self, spsModule):
        ModuleRow.__init__(self, module=spsModule, actorName='dcb', actorLabel='DCB')

        self.state = ValueMRow(self, 'metaFSM', '', 0, '{:s}')
        self.substate = ValueMRow(self, 'metaFSM', '', 1, '{:s}')

        self.hgar = SwitchMRow(self, 'hgar', 'Hg-Ar', 0, '{:g}', controllerName='sources')
        self.neon = SwitchMRow(self, 'neon', 'Neon', 0, '{:g}', controllerName='sources')
        self.krypton = SwitchMRow(self, 'krypton', 'Krypton', 0, '{:g}', controllerName='sources')
        self.halogen = SwitchMRow(self, 'halogen', 'Halogen', 0, '{:g}', controllerName='sources')

        self.controllers = Controllers(self)
        self.createDialog(DcbDialog(self))

    @property
    def widgets(self):
        return [self.state, self.substate, self.halogen, self.hgar, self.neon, self.krypton]


class DcbDialog(ControlDialog):
    def __init__(self, dcbRow):
        ControlDialog.__init__(self, moduleRow=dcbRow)
        self.fiberConfig = FiberConfig(self)
        self.connectCmd = ConnectCmd(self, ['pdu', 'sources'])

        self.topbar.addWidget(self.fiberConfig)
        self.topbar.addLayout(self.connectCmd)

        self.sourcesPanel = SourcesPanel(self)

        self.tabWidget.addTab(self.sourcesPanel, 'Sources')
