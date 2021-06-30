__author__ = 'alefur'

import spsGUIActor.styles as styles
from spsGUIActor.aten.labsphere import LabspherePanel, AttenuatorValue
from spsGUIActor.aten.pdu import PduPanel
from spsGUIActor.control import ControlDialog
from spsGUIActor.enu import ConnectCmd
from spsGUIActor.modulerow import ModuleRow, RowWidget
from spsGUIActor.widgets import ValueMRow, SwitchMRow, Controllers


class RowOne(RowWidget):
    def __init__(self, atenRow):
        RowWidget.__init__(self, atenRow)

    @property
    def widgets(self):
        atenRow = self.moduleRow
        return [atenRow.state, atenRow.substate, atenRow.roughpump, atenRow.labsphere, atenRow.photodiode, atenRow.qth,
                atenRow.neon, atenRow.krypton]


class RowTwo(RowWidget):
    def __init__(self, atenRow):
        RowWidget.__init__(self, atenRow)

    @property
    def widgets(self):
        atenRow = self.moduleRow
        return [atenRow.roughpump2, atenRow.regenheater, atenRow.attenuator, atenRow.deuterium, atenRow.argon,
                atenRow.hgar]

    @property
    def displayed(self):
        return [None, None, None] + self.widgets


class AtenRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='aten', actorLabel='ATEN')

        self.state = ValueMRow(self, 'metaFSM', '', 0, '{:s}')
        self.substate = ValueMRow(self, 'metaFSM', '', 1, '{:s}')

        self.labsphere = SwitchMRow(self, 'labsphere', 'Labsphere', 0, '{:g}', controllerName='pdu')
        self.roughpump = SwitchMRow(self, 'roughpump', 'Rough pump', 0, '{:g}', controllerName='pdu')
        self.roughpump2 = SwitchMRow(self, 'roughpump2', 'Rough pump 2', 0, '{:g}', controllerName='pdu')
        self.regenheater = SwitchMRow(self, 'regenheater', 'Regen-Heater', 0, '{:g}', controllerName='pdu')
        self.neon = SwitchMRow(self, 'neon', 'Neon', 0, '{:g}', controllerName='aten')
        self.xenon = SwitchMRow(self, 'xenon', 'Xenon', 0, '{:g}', controllerName='aten')
        self.hgar = SwitchMRow(self, 'hgar', 'Hg-Ar', 0, '{:g}', controllerName='aten')
        self.krypton = SwitchMRow(self, 'krypton', 'Krypton', 0, '{:g}', controllerName='aten')
        self.argon = SwitchMRow(self, 'argon', 'Argon', 0, '{:g}', controllerName='aten')
        self.deuterium = SwitchMRow(self, 'deuterium', 'Deuterium', 0, '{:g}', controllerName='aten')

        self.qth = SwitchMRow(self, 'halogen', 'QTH', 0, '{:g}', controllerName='labsphere')
        self.photodiode = ValueMRow(self, 'photodiode', 'photodiode', 0, '{:g}', controllerName='labsphere')
        self.attenuator = AttenuatorValue(self, fontSize=styles.bigFont)

        self.rows = [RowOne(self), RowTwo(self)]

        self.controllers = Controllers(self)
        self.createDialog(AtenDialog(self))

    @property
    def widgets(self):
        return sum([row.widgets for row in self.rows], [])


class AtenDialog(ControlDialog):
    def __init__(self, atenRow):
        ControlDialog.__init__(self, moduleRow=atenRow)
        self.connectCmd = ConnectCmd(self, ['pdu', 'labsphere', 'sources'])

        self.topbar.addLayout(self.connectCmd)

        self.PduPanel = PduPanel(self)
        self.labspherePanel = LabspherePanel(self)

        self.tabWidget.addTab(self.PduPanel, 'Pdu')
        self.tabWidget.addTab(self.labspherePanel, 'Labsphere')
