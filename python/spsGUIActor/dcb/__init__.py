__author__ = 'alefur'

from spsGUIActor.control import ControlDialog
from spsGUIActor.dcb.sources import SourcesPanel
from spsGUIActor.dcbold import FiberConfig
from spsGUIActor.enu import ConnectCmd
from spsGUIActor.modulerow import ModuleRow, RowWidget
from spsGUIActor.widgets import ValueMRow, SwitchMRow, Controllers


class RowOne(RowWidget):
    def __init__(self, dcbRow):
        RowWidget.__init__(self, dcbRow)

    @property
    def widgets(self):
        dcbRow = self.moduleRow
        return [dcbRow.state, dcbRow.substate, dcbRow.qth, dcbRow.hgar, dcbRow.neon, dcbRow.krypton, dcbRow.argon]


class RowTwo(RowWidget):
    def __init__(self, dcbRow):
        RowWidget.__init__(self, dcbRow)

    @property
    def widgets(self):
        dcbRow = self.moduleRow
        return []

    @property
    def displayed(self):
        return [None, None, None] + self.widgets


class DcbRow(ModuleRow):
    def __init__(self, spsModule):
        ModuleRow.__init__(self, module=spsModule, actorName='dcb', actorLabel='DCB')

        self.state = ValueMRow(self, 'metaFSM', '', 0, '{:s}')
        self.substate = ValueMRow(self, 'metaFSM', '', 1, '{:s}')

        self.hgar = SwitchMRow(self, 'hgar', 'Hg-Ar', 0, '{:g}', controllerName='sources')
        self.neon = SwitchMRow(self, 'neon', 'Neon', 0, '{:g}', controllerName='sources')
        self.krypton = SwitchMRow(self, 'krypton', 'Krypton', 0, '{:g}', controllerName='sources')
        self.argon = SwitchMRow(self, 'argon', 'Argon', 0, '{:g}', controllerName='sources')
        self.qth = SwitchMRow(self, 'halogen', 'QTH', 0, '{:g}', controllerName='sources')

        # self.linewheel = ValueMRow(self, 'linewheel', 'Line Wheel', 1, '{:s}')
        # self.qthwheel = ValueMRow(self, 'qthwheel', 'QTH Wheel', 1, '{:s}')
        # self.adc1 = ValueMRow(self, 'adc', 'ADC 1', 0, '{:4f}')
        # self.adc2 = ValueMRow(self, 'adc', 'ADC 2', 1, '{:4f}')

        self.rows = [RowOne(self), RowTwo(self)]

        self.controllers = Controllers(self)
        self.createDialog(DcbDialog(self))

    @property
    def widgets(self):
        return sum([row.widgets for row in self.rows], [])


class DcbDialog(ControlDialog):
    def __init__(self, dcbRow):
        ControlDialog.__init__(self, moduleRow=dcbRow)
        self.fiberConfig = FiberConfig(self)
        self.connectCmd = ConnectCmd(self, ['sources'])

        self.topbar.addWidget(self.fiberConfig)
        self.topbar.addLayout(self.connectCmd)

        self.sourcesPanel = SourcesPanel(self)
        # self.filterwheelPanel = FilterwheelPanel(self)

        self.tabWidget.addTab(self.sourcesPanel, 'Sources')
        # self.tabWidget.addTab(self.filterwheelPanel, 'Filterwheels')
