__author__ = 'alefur'

import os

import spsGUIActor.styles as styles
from PyQt5.QtWidgets import QDialog, QGroupBox, QGridLayout, QTabWidget, QLayout
from spsGUIActor.common import PushButton, imgPath, VBoxLayout
from spsGUIActor.control import ControlDialog, ButtonBox, ControllerPanel
from spsGUIActor.logs import CmdLogArea
from spsGUIActor.modulerow import ActorGB
from spsGUIActor.modulerow import ModuleRow


class CamDevice(ControllerPanel):
    def __init__(self, controlDialog, controllerName, title=None):
        title = controllerName.capitalize() if title is None else title
        ControllerPanel.__init__(self, controlDialog, controllerName)
        self.setTitle(title)
        self.setCheckable(True)

    def updateIcon(self, a0):
        filename = 'green.png' if a0 else 'orange.png'
        self.setStyleSheet("CamDevice {font-size: 10pt; font-weight:2000;border: 1px solid #000000;border-radius: 20;;margin-top: 10px;}"
                           "CamDevice::title {subcontrol-origin: margin;subcontrol-position: top left; padding: 0 10px;}"
                           "CamDevice::indicator:checked {image: url(%s);} " % os.path.join(imgPath, filename))


from spsGUIActor.cam.ccd import CcdRow
from spsGUIActor.cam.xcu import XcuRow


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


class CamRow(ModuleRow):
    def __init__(self, module, arm):
        self.module = module
        self.arm = arm
        self.label = '%sCU' % arm.upper()
        self.actorStatus = CamStatus(self)
        self.actorStatus.button.clicked.connect(self.showDetails)

        self.ccd = CcdRow(self)
        self.xcu = XcuRow(self)

        self.createDialog(CamDialog(self))

    @property
    def displayed(self):
        return [self.actorStatus, self.ccd.substate, self.ccd.temperature, self.xcu.pressure]

    def setOnline(self):
        self.actorStatus.setStatus(sum([self.ccd.isOnline + self.xcu.isOnline]))


class CamDialog(ControlDialog):
    back = dict(b='8594ff', r='e6a2a2', n='f285ff')

    def __init__(self, camRow):
        self.moduleRow = camRow
        QDialog.__init__(self, parent=camRow.mwindow.spsGUIActor)
        self.setWindowTitle('%s %i' % (camRow.label, camRow.module.smId))

        self.setStyleSheet(
            "QDialog { background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #%s, stop: 1 #efefef);}" %
            CamDialog.back[camRow.arm])

        self.vbox = VBoxLayout()
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
