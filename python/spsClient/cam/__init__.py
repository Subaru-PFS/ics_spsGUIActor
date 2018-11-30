__author__ = 'alefur'

import spsClient.styles as styles
from PyQt5.QtWidgets import QPushButton, QDialog, QVBoxLayout, QGroupBox, QGridLayout, QTabWidget
from spsClient.cam.ccd import CcdRow, CcdGB
from spsClient.cam.xcu import XcuRow, XcuGB
from spsClient.logs import CmdLogArea, RawLogArea
from spsClient.modulerow import ActorGB
from spsClient.control import ControlDialog, ButtonBox


class CamStatus(ActorGB, QGroupBox):
    def __init__(self, cam):
        self.cam = cam
        self.fontSize = styles.bigFont
        QGroupBox.__init__(self)
        self.setTitle('Actor')

        self.button = QPushButton()
        self.button.setFlat(True)

        self.grid = QGridLayout()
        self.grid.addWidget(self.button, 0, 0)
        self.setLayout(self.grid)

        self.setColor(*styles.colorWidget('offline'))
        self.setText(cam.label)

    def setStatus(self, status):
        if status == 0:
            self.setColor(*styles.colorWidget('offline'))
        if status == 1:
            self.setColor(*styles.colorWidget('midstate'))
        if status == 2:
            self.setColor(*styles.colorWidget('online'))


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

        self.logArea = QTabWidget(self)
        self.cmdLog = CmdLogArea()
        self.rawXcuLog = RawLogArea(camRow.xcu.actorName)
        self.rawCcdLog = RawLogArea(camRow.ccd.actorName)
        self.logArea.addTab(self.cmdLog, 'cmdLog')
        self.logArea.addTab(self.rawXcuLog, 'xcuLog')
        self.logArea.addTab(self.rawCcdLog, 'ccdLog')

        buttonBox = ButtonBox(self)

        self.vbox.addLayout(self.hbox)
        self.vbox.addLayout(buttonBox)
        self.vbox.addWidget(self.logArea)

        self.setLayout(self.vbox)
        self.setWindowTitle(title)

        self.xcuGB = XcuGB(camRow.xcu)
        self.ccdGB = CcdGB(camRow.ccd)

        self.hbox.addWidget(self.xcuGB)
        self.hbox.addWidget(self.ccdGB)
