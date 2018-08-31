__author__ = 'alefur'

from PyQt5.QtWidgets import QPushButton, QGroupBox, QGridLayout
from spsClient import bigFont
from spsClient.cam.ccd import CcdRow
from spsClient.cam.xcu import XcuRow
from spsClient.cam.xcu.motors import MotorsPanel
from spsClient.widgets import ControlDialog


class CamStatus(QGroupBox):
    def __init__(self, cam):
        self.cam = cam
        QGroupBox.__init__(self)
        self.setTitle('Actor')
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.button = QPushButton()
        self.button.setFlat(True)
        self.setText(cam.label)
        self.grid.addWidget(self.button, 0, 0)

        self.setColor('black')

    def setStatus(self, status):
        if status == 0:
            self.setColor('red')
        if status == 1:
            self.setColor('orange')
        if status == 2:
            self.setColor('green')

    def setColor(self, background, police='white'):
        if background == "red":
            bckColor = 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0  #f43131, stop: 1 #5e1414)'

        elif background == "green":
            bckColor = 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0  #45f42e, stop: 1 #195511)'

        elif background == "orange":
            bckColor = 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0  #f4a431, stop: 1 #5e4a14)'

        else:
            bckColor = 'qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0  #dfdfdf, stop: 1 #000000)'

        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; background-color: %s ;border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " % (
                bigFont - 1, bckColor)
            + "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

        self.button.setStyleSheet(
            "QPushButton{font-size: %ipt; background: %s; color:%s; }" % (bigFont, bckColor, police))

    def setText(self, txt):
        self.button.setText(txt)


class CamRow(object):
    def __init__(self, specModule, arm):
        object.__init__(self)
        self.specModule = specModule
        self.arm = arm
        self.label = '%sCU' % arm.upper()
        self.lineNB = 0
        self.actorStatus = CamStatus(self)
        self.actorStatus.button.clicked.connect(self.showDetails)
        self.ccd = CcdRow(cam=self)
        self.xcu = XcuRow(cam=self)

    @property
    def mwindow(self):
        return self.specModule.mwindow

    @property
    def widgets(self):
        return [self.actorStatus, self.ccd.substate, self.ccd.temperature, self.xcu.pressure]

    def setOnline(self):
        self.actorStatus.setStatus(sum([self.ccd.isOnline + self.xcu.isOnline]))

    def setLine(self, lineNB):
        self.lineNB = lineNB

    def addReadRows(self):
        self.specModule.grid.addWidget(self.ccd.readRows, self.lineNB, 1)

    def showDetails(self):
        self.controlDialog = CamDialog(self)
        self.controlDialog.show()


class CamDialog(ControlDialog):
    def __init__(self, camRow):
        ControlDialog.__init__(self, moduleRow=camRow.xcu, title='%s %i' % (camRow.label, camRow.specModule.smId))

        self.motorsPanel = MotorsPanel(self)
        self.tabWidget.addTab(self.motorsPanel, 'Motors')
