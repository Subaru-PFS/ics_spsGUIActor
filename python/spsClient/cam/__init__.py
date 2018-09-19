__author__ = 'alefur'

from PyQt5.QtWidgets import QPushButton, QDialog, QVBoxLayout, QDialogButtonBox, QGroupBox, QGridLayout

from spsClient import bigFont
from spsClient.cam.ccd import CcdRow, CcdGB
from spsClient.cam.xcu import XcuRow, XcuGB
from spsClient.modulerow import ActorGB
from spsClient.widgets import ControlDialog


class CamStatus(ActorGB, QGroupBox):
    def __init__(self, cam):
        self.cam = cam
        self.fontSize = bigFont
        QGroupBox.__init__(self)
        self.setTitle('Actor')

        self.button = QPushButton()
        self.button.setFlat(True)

        self.grid = QGridLayout()
        self.grid.addWidget(self.button, 0, 0)
        self.setLayout(self.grid)

        self.setColor('black')
        self.setText(cam.label)

    def setStatus(self, status):
        if status == 0:
            self.setColor('red')
        if status == 1:
            self.setColor('orange')
        if status == 2:
            self.setColor('green')


class CamRow(object):
    def __init__(self, specModule, arm):
        object.__init__(self)
        self.specModule = specModule
        self.arm = arm
        self.label = '%sCU' % arm.upper()
        self.lineNB = 0
        self.actorStatus = CamStatus(self)
        self.actorStatus.button.clicked.connect(self.showDetails)
        self.ccd = CcdRow(camRow=self)
        self.xcu = XcuRow(camRow=self)

        self.controlDialog = CamDialog(self)

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
        self.controlDialog.setVisible(True)


class CamDialog(ControlDialog):
    def __init__(self, camRow):
        title = '%s %i' % (camRow.label, camRow.specModule.smId)
        QDialog.__init__(self, parent=camRow.mwindow.spsClient)

        self.vbox = QVBoxLayout()
        self.hbox = QVBoxLayout()
        self.cmdBuffer = dict()
        self.moduleRow = camRow

        buttonBox = QDialogButtonBox(QDialogButtonBox.Apply | QDialogButtonBox.Discard)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.sendCommands)
        buttonBox.button(QDialogButtonBox.Discard).clicked.connect(self.cancelCommands)

        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(buttonBox)

        self.setLayout(self.vbox)
        self.setWindowTitle(title)

        self.xcuGB = XcuGB(camRow.xcu)
        self.ccdGB = CcdGB(camRow.ccd)

        self.hbox.addWidget(self.xcuGB)
        self.hbox.addWidget(self.ccdGB)
