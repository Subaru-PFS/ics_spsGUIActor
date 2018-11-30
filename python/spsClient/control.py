__author__ = 'alefur'
from functools import partial

import spsClient.styles as styles
from PyQt5.QtWidgets import QDialog, QGroupBox, QVBoxLayout, QGridLayout, \
    QTabWidget, QLayout
from spsClient.logs import CmdLogArea, RawLogArea
from spsClient.widgets import EmptyWidget, ReloadButton
from spsClient.common import PushButton


class CommandsGB(QGroupBox):
    def __init__(self, controlPanel, fontSize=styles.smallFont):
        self.controlPanel = controlPanel
        QGroupBox.__init__(self)
        self.grid = QGridLayout()

        self.setTitle('Commands')
        self.setLayout(self.grid)
        self.setStyleSheet(
            "QGroupBox {font-size: %ipt; border: 1px solid #d7d4d1;border-radius: 3px;margin-top: 1ex;} " % (fontSize) +
            "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

    @property
    def buttons(self):
        return []

    def emptySpace(self, height=False):
        return EmptyWidget(height=height)


class ControlPanel(QGroupBox):
    def __init__(self, controlDialog):
        QGroupBox.__init__(self)
        self.controlDialog = controlDialog
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.commands = CommandsGB(self)

    @property
    def moduleRow(self):
        return self.controlDialog.moduleRow

    @property
    def actorName(self):
        return self.controlDialog.moduleRow.actorName

    @property
    def basicWidgets(self):
        return [self.grid.itemAt(i).widget() for i in range(self.grid.count())] + self.commands.buttons

    @property
    def customWidgets(self):
        return []

    @property
    def allWidgets(self):
        return self.basicWidgets + self.customWidgets

    def emptySpace(self):
        return EmptyWidget()


class ButtonBox(QGridLayout):
    def __init__(self, controlDialog):
        QGridLayout.__init__(self)
        self.controlDialog = controlDialog
        self.apply = PushButton('Apply')
        self.apply.clicked.connect(controlDialog.sendCommands)

        self.discard = PushButton('Discard')
        self.discard.clicked.connect(controlDialog.cancelCommands)

        self.showLogs = PushButton('Show Logs')
        self.hideLogs = PushButton('Hide Logs')
        self.showLogs.clicked.connect(partial(self.show, True))
        self.hideLogs.clicked.connect(partial(self.show, False))
        self.show(False)

        self.addWidget(self.showLogs, 0, 0)
        self.addWidget(self.hideLogs, 0, 0)
        self.addWidget(EmptyWidget(), 0, 1)
        self.addWidget(self.apply, 0, 9)
        self.addWidget(self.discard, 0, 10)

    def show(self, bool):
        self.showLogs.setVisible(not bool)
        self.hideLogs.setVisible(bool)
        self.controlDialog.logArea.setVisible(bool)
        self.controlDialog.adjustSize()


class ControlDialog(QDialog):
    def __init__(self, moduleRow, title=False):
        title = moduleRow.actorLabel if not title else title
        QDialog.__init__(self, parent=moduleRow.mwindow.spsClient)
        self.vbox = QVBoxLayout()
        self.vbox.setSizeConstraint(QLayout.SetMinimumSize)
        self.tabWidget = QTabWidget(self)
        self.cmdBuffer = dict()

        self.moduleRow = moduleRow

        self.reload = ReloadButton(self)

        self.logArea = QTabWidget(self)
        self.cmdLog = CmdLogArea()
        self.rawLog = RawLogArea(moduleRow.actorName)
        self.logArea.addTab(self.cmdLog, 'cmdLog')
        self.logArea.addTab(self.rawLog, 'rawLog')

        buttonBox = ButtonBox(self)

        self.vbox.addWidget(self.reload)
        self.vbox.addWidget(self.tabWidget)
        self.vbox.addLayout(buttonBox)
        self.vbox.addWidget(self.logArea)

        self.setLayout(self.vbox)
        self.setWindowTitle(title)
        self.setVisible(False)

    def addCommand(self, button, cmdStr):
        self.cmdBuffer[button] = cmdStr

    def clearCommand(self, button):
        self.cmdBuffer.pop(button, None)

    def sendCommands(self):
        for button, fullCmd in self.cmdBuffer.items():
            [actor, cmdStr] = fullCmd.split(' ', 1)
            self.cmdLog.newLine('cmdIn=%s %s' % (actor, cmdStr))
            self.moduleRow.mwindow.sendCommand(actor=actor, cmdStr=cmdStr, callFunc=self.cmdLog.printResponse)
            button.setChecked(0)

        self.cmdBuffer.clear()

    def cancelCommands(self):
        self.cmdBuffer.clear()

    def close(self):
        self.setVisible(False)
