__author__ = 'alefur'

from PyQt5.QtWidgets import QGridLayout, QGroupBox
from spsGUIActor.breva import BrevaRow
from spsGUIActor.cam import CamRow
from spsGUIActor.dcb import DcbRow
from spsGUIActor.enu import EnuRow
from spsGUIActor.sac import SacRow


class Module(QGroupBox):
    def __init__(self, mwindow, title):
        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setTitle(title)
        self.mwindow = mwindow

    @property
    def rows(self):
        return []

    def populateLayout(self):
        for i, row in enumerate(self.rows):
            for j, widget in enumerate(row.displayed):
                if widget is None:
                    continue
                self.grid.addWidget(widget, i, j)


class Aitmodule(Module):
    def __init__(self, mwindow):
        Module.__init__(self, mwindow=mwindow, title='AIT')

        self.dcb = DcbRow(self)
        self.sac = SacRow(self)
        self.breva = BrevaRow(self)

        self.populateLayout()
        self.adjustSize()

    @property
    def rows(self):
        return [self.dcb.rowone, self.dcb.rowtwo, self.sac, self.breva]


class Specmodule(Module):
    def __init__(self, mwindow, smId, arms=False):
        Module.__init__(self, mwindow=mwindow, title='Spectrograph Module %i' % smId)
        arms = ['b', 'r'] if not arms else arms

        self.smId = smId
        self.enu = EnuRow(self)
        self.cams = [CamRow(self, arm=arm) for arm in arms]
        self.populateLayout()
        self.adjustSize()

    @property
    def rows(self):
        return [self.enu] + self.cams
