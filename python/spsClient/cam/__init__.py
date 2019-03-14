__author__ = 'alefur'

import spsClient.styles as styles
from PyQt5.QtWidgets import QDialog, QGroupBox, QVBoxLayout, QGridLayout, QTabWidget, QLayout
from spsClient.cam.ccd import CcdRow
from spsClient.cam.xcu import XcuRow
from spsClient.common import PushButton
from spsClient.control import ControlDialog, ButtonBox
from spsClient.logs import CmdLogArea
from spsClient.modulerow import ActorGB


class CamStatus(ActorGB, QGroupBox):
    def __init__(self, cam):
        self.cam = cam
        self.fontSize = styles.bigFont
        QGroupBox.__init__(self)
        self.setTitle('Actor')

        self.button = PushButton()
        self.button.setFlat(True)

        self.grid = QGridLayout()
        self.grid.addWidget(self.button, 0, 0)
        self.grid.setContentsMargins(0, 0, 0, 0)
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
        self.actorStatus = CamStatus(self)
        self.actorStatus.button.clicked.connect(self.showDetails)

        self.ccd = CcdRow(self)
        self.xcu = XcuRow(self)

        self.controlDialog = CamDialog(self)

    @property
    def mwindow(self):
        return self.specModule.mwindow

    @property
    def displayed(self):
        return [self.actorStatus, self.ccd.substate, self.ccd.temperature, self.xcu.pressure]

    def setOnline(self):
        self.actorStatus.setStatus(sum([self.ccd.isOnline + self.xcu.isOnline]))

    def showDetails(self):
        self.controlDialog.setVisible(True)


class CamDialog(ControlDialog):
    def __init__(self, camRow):
        self.moduleRow = camRow
        QDialog.__init__(self, parent=camRow.mwindow.spsClient)
        self.setWindowTitle('%s %i' % (camRow.label, camRow.specModule.smId))

        self.vbox = QVBoxLayout()
        self.vbox.setSizeConstraint(QLayout.SetMinimumSize)
        self.tabWidget = QTabWidget(self)
        self.cmdBuffer = dict()

        self.moduleRow.xcu.createDialog(self.tabWidget)
        self.moduleRow.ccd.createDialog(self.tabWidget)

        self.logArea = QTabWidget(self)
        self.cmdLog = CmdLogArea()
        self.logArea.addTab(self.cmdLog, 'cmdLog')
        self.logArea.addTab(self.xcuDialog.rawLogArea(), 'xcuLog')
        self.logArea.addTab(self.ccdDialog.rawLogArea(), 'ccdLog')

        buttonBox = ButtonBox(self)

        self.vbox.addLayout(self.xcuDialog.topbar)
        self.vbox.addLayout(self.ccdDialog.topbar)
        self.vbox.addWidget(self.tabWidget)
        self.vbox.addLayout(buttonBox)
        self.vbox.addWidget(self.logArea)

        self.setLayout(self.vbox)
        self.setVisible(False)

    @property
    def ccdDialog(self):
        return self.moduleRow.ccd.controlDialog

    @property
    def xcuDialog(self):
        return self.moduleRow.xcu.controlDialog
