__author__ = 'alefur'

from PyQt5.QtWidgets import QGridLayout, QGroupBox
from spsClient.breva import BrevaRow
from spsClient.dcb import DcbRow
from spsClient.enu import EnuRow
from spsClient.sac import SacRow
from spsClient.seqno import SeqnoRow
from spsClient.viscu import CcdRow


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
            row.setLine(i)
            for j, widget in enumerate(row.widgets):
                self.grid.addWidget(widget, i, j)


class Aitmodule(Module):
    def __init__(self, mwindow):
        Module.__init__(self, mwindow=mwindow, title='AIT')

        self.dcb = DcbRow(self)
        self.seqno = SeqnoRow(self)
        self.sac = SacRow(self)
        self.breva = BrevaRow(self)

        self.populateLayout()

    @property
    def rows(self):
        return [self.dcb, self.sac, self.breva]


class Specmodule(Module):
    def __init__(self, mwindow, smId, arms=False):
        Module.__init__(self, mwindow=mwindow, title='Spectrograph Module %i' % smId)
        arms = ['b', 'r'] if not arms else arms

        self.smId = smId

        self.enu = EnuRow(self)
        self.cams = [CcdRow(self, arm=arm) for arm in arms]

        self.populateLayout()

    @property
    def rows(self):
        return [self.enu] + self.cams