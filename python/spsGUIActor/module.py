__author__ = 'alefur'

import spsGUIActor.dcb as dcb
import spsGUIActor.dcb2 as dcb2
import spsGUIActor.dcbold as dcbold
from PyQt5.QtWidgets import QGroupBox
from spsGUIActor.breva import BrevaRow
from spsGUIActor.cam import CamRow
from spsGUIActor.common import GridLayout
from spsGUIActor.enu import EnuRow
from spsGUIActor.rough import RoughRow
from spsGUIActor.sac import SacRow
import spsGUIActor.styles as styles

class Module(QGroupBox):
    def __init__(self, mwindow, title):
        QGroupBox.__init__(self)
        self.grid = GridLayout()
        self.setLayout(self.grid)
        self.setTitle(title)
        self.mwindow = mwindow
        self.setStyleSheet()

    @property
    def rows(self):
        return []

    def populateLayout(self):
        for i, row in enumerate(self.rows):
            for j, widget in enumerate(row.displayed):
                if widget is None:
                    continue
                self.grid.addWidget(widget, i, j)

    def setEnabled(self, a0: bool) -> None:
        for row in self.rows:
            row.setOnline(a0)

        QGroupBox.setEnabled(self, a0)

    def setStyleSheet(self, styleSheet=None):
        styleSheet = "QGroupBox {font-size: %ipt;border: 1px solid lightgray;border-radius: 3px;margin-top: 6px;} "%styles.bigFont \
                     + "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top left; padding: 0 0px;}"
        QGroupBox.setStyleSheet(self, styleSheet)


class Aitmodule(Module):
    def __init__(self, mwindow):
        Module.__init__(self, mwindow=mwindow, title='AIT')
        actors = [actor.strip() for actor in mwindow.actor.config.get('ait', 'actors').split(',')]

        self.dcbs = []

        if 'dcbold' in actors:
            self.dcbs += dcbold.DcbRow(self).rows
        if 'dcb' in actors:
            self.dcbs += dcb.DcbRow(self).rows
        if 'dcb2' in actors:
            self.dcbs += dcb2.DcbRow(self).rows

        self.sac = [SacRow(self)] if 'sac' in actors else []
        self.breva = [BrevaRow(self)] if 'breva' in actors else []
        roughs = ['rough1'] if 'rough1' in actors else []
        roughs += (['rough2'] if 'rough2' in actors else [])

        self.roughs = [RoughRow(self, rough) for rough in roughs]

        self.populateLayout()
        self.adjustSize()

    @property
    def rows(self):
        return self.dcbs + self.sac + self.breva + self.roughs


class Specmodule(Module):
    def __init__(self, mwindow, smId, enu=True, arms=None):
        Module.__init__(self, mwindow=mwindow, title='Spectrograph Module %i' % smId)
        arms = ['b', 'r', 'n'] if arms is None else arms

        self.smId = smId
        self.enu = [EnuRow(self)] if enu else []
        self.cams = [CamRow(self, arm=arm) for arm in arms]
        self.populateLayout()
        self.adjustSize()

    @property
    def rows(self):
        return self.enu + self.cams
