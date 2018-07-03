__author__ = 'alefur'
from PyQt5.QtWidgets import QComboBox, QGridLayout
from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB, CommandsGB, ControlDialog, ControlPannel, DoubleSpinBoxGB, CmdButton


class SacRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='sac', actorLabel='SAC')

        self.state = ValueGB(self, 'metaFSM', '', 0, '{:s}')
        self.substate = ValueGB(self, 'metaFSM', '', 1, '{:s}')

        self.pentaPosition = ValueGB(self, 'lsPenta', 'Penta-Position', 2, '{:.2f}')
        self.detectorPosition = ValueGB(self, 'lsDetector', 'Detector-Position', 2, '{:.2f}')

    @property
    def customWidgets(self):

        widgets = [self.state, self.substate, self.pentaPosition, self.detectorPosition]

        try:
            widgets += self.controlDialog.customWidgets
        except AttributeError:
            pass

        return widgets

    def showDetails(self):
        self.controlDialog = SacDialog(self)
        self.controlDialog.show()


class MoveButton(CmdButton):
    def __init__(self, moveCmd):
        self.moveCmd = moveCmd
        CmdButton.__init__(self, controlPannel=moveCmd.controlPannel, label='MOVE')

    def getCommand(self):
        if self.isChecked():
            cmdStr = self.moveCmd.buildCmd()
            self.controlDialog.addCommand(button=self, cmdStr=cmdStr)
        else:
            self.controlDialog.clearCommand(button=self)


class MoveCmd(QGridLayout):
    limits = dict(penta=(-300, 500),
                  detector=(0, 12))

    def __init__(self, controlPannel, stage):
        QGridLayout.__init__(self)
        self.controlPannel = controlPannel
        self.stage = stage
        l_bound, u_bound = MoveCmd.limits[stage]

        self.combo = QComboBox()
        self.combo.addItems(['abs', 'rel'])

        self.button = MoveButton(self)
        self.distSpinbox = DoubleSpinBoxGB('Dist', l_bound, u_bound, 2)

        self.addWidget(self.button, 0, 0)
        self.addWidget(self.distSpinbox, 0, 1)
        self.addWidget(self.combo, 0, 2)

    def buildCmd(self):
        reference = '' if self.combo.currentText() == 'rel' else self.combo.currentText()
        cmdStr = 'sac move %s=%.2f %s' % (self.stage, self.distSpinbox.getValue(), reference)

        return cmdStr


class ExposeButton(CmdButton):
    def __init__(self, exposeCmd):
        self.exposeCmd = exposeCmd
        CmdButton.__init__(self, controlPannel=exposeCmd.controlPannel, label='EXPOSE')

    def getCommand(self):
        if self.isChecked():
            cmdStr = self.exposeCmd.buildCmd()
            self.controlDialog.addCommand(button=self, cmdStr=cmdStr)
        else:
            self.controlDialog.clearCommand(button=self)


class StartLoopButton(CmdButton):
    def __init__(self, loopCmd):
        self.loopCmd = loopCmd
        CmdButton.__init__(self, controlPannel=loopCmd.controlPannel, label='START LOOP')

    def getCommand(self):
        if self.isChecked():
            cmdStr = self.loopCmd.buildCmd(start=True)
            self.controlDialog.addCommand(button=self, cmdStr=cmdStr)
        else:
            self.controlDialog.clearCommand(button=self)


class StopLoopButton(CmdButton):
    def __init__(self, loopCmd):
        self.loopCmd = loopCmd
        CmdButton.__init__(self, controlPannel=loopCmd.controlPannel, label='STOP LOOP')

    def getCommand(self):
        if self.isChecked():
            cmdStr = self.loopCmd.buildCmd(start=False)
            self.controlDialog.addCommand(button=self, cmdStr=cmdStr)
        else:
            self.controlDialog.clearCommand(button=self)


class Looptime(ValueGB):
    def __init__(self, loopCmd):
        self.loopCmd = loopCmd
        ValueGB.__init__(self, loopCmd.controlPannel.moduleRow, 'looptime', '', 0, '{:.2f}')

    def setText(self, txt):
        if float(txt) > 0:
            self.loopCmd.stopLoop.setVisible(True)
            self.loopCmd.startLoop.setVisible(False)
        else:
            self.loopCmd.stopLoop.setVisible(False)
            self.loopCmd.startLoop.setVisible(True)


class LoopCmd(QGridLayout):
    def __init__(self, controlPannel):
        QGridLayout.__init__(self)
        self.controlPannel = controlPannel

        self.startLoop = StartLoopButton(self)
        self.stopLoop = StopLoopButton(self)

        self.looptime = Looptime(self)

        self.addWidget(self.startLoop, 0, 0)
        self.addWidget(self.stopLoop, 0, 0)

    def buildCmd(self, start):
        action = 'start' if start else 'stop'
        cmdStr = 'sac ccd loop %s' % action

        return cmdStr


class ExposeCmd(QGridLayout):

    def __init__(self, controlPannel):
        QGridLayout.__init__(self)
        self.controlPannel = controlPannel

        self.combo = QComboBox()
        self.combo.addItems(['object', 'background'])

        self.button = ExposeButton(self)
        self.exptime = DoubleSpinBoxGB('exptime', 0, 300, 2)

        self.addWidget(self.button, 0, 0)
        self.addWidget(self.combo, 0, 1)
        self.addWidget(self.exptime, 0, 2)

    def buildCmd(self):
        exptype = 'expose' if self.combo.currentText() == 'object' else 'background'
        cmdStr = 'sac %s exptime=%.2f' % (exptype, self.exptime.getValue())

        return cmdStr


class InitButton(CmdButton):
    def __init__(self, controlPannel, stage):
        self.stage = stage
        CmdButton.__init__(self, controlPannel=controlPannel, label='INIT')

    def getCommand(self):
        if self.isChecked():
            self.controlDialog.addCommand(button=self, cmdStr='sac stages %s init' % self.stage)
        else:
            self.controlDialog.clearCommand(button=self)


class ConnectButton(CmdButton):
    def __init__(self, controlPannel):
        CmdButton.__init__(self, controlPannel=controlPannel, label='CONNECT')

    def getCommand(self):
        if self.isChecked():
            self.controlDialog.addCommand(button=self, cmdStr='sac ccd connect')
        else:
            self.controlDialog.clearCommand(button=self)


class StageCommands(CommandsGB):
    def __init__(self, controlPannel, stage):
        CommandsGB.__init__(self, controlPannel)
        self.initButton = InitButton(controlPannel=controlPannel, stage=stage)

        self.moveCmd = MoveCmd(controlPannel=controlPannel, stage=stage)

        self.grid.addWidget(self.initButton, 0, 0)
        self.grid.addLayout(self.moveCmd, 1, 0, 1, 3)

    @property
    def buttons(self):
        return [self.initButton, self.moveCmd.button]


class StagePannel(ControlPannel):
    def __init__(self, controlDialog, stage):
        label = stage.capitalize()
        ControlPannel.__init__(self, controlDialog, '%s Stage' % stage.capitalize())

        self.state = ValueGB(self.moduleRow, 'ls%s' % label, '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'ls%s' % label, '', 1, '{:s}')
        self.position = ValueGB(self.moduleRow, 'ls%s' % label, 'Position', 2, '{:.2f}')

        self.commands = StageCommands(self, stage)

        self.grid.addWidget(self.state, 0, 0)
        self.grid.addWidget(self.substate, 0, 1)
        self.grid.addWidget(self.position, 0, 2)

        self.grid.addWidget(self.commands, 0, 3, 3, 3)

    @property
    def customWidgets(self):
        return [self.grid.itemAt(i).widget() for i in range(self.grid.count())] + self.commands.buttons


class CcdCommands(CommandsGB):
    def __init__(self, controlPannel):
        CommandsGB.__init__(self, controlPannel)

        self.connectButton = ConnectButton(controlPannel=controlPannel)
        self.exposeCmd = ExposeCmd(controlPannel=controlPannel)
        self.loopCmd = LoopCmd(controlPannel=controlPannel)

        self.grid.addWidget(self.connectButton, 0, 0)
        self.grid.addLayout(self.exposeCmd, 1, 0, 1, 3)
        self.grid.addLayout(self.loopCmd, 2, 0, 1, 1)

    @property
    def buttons(self):
        return [self.connectButton, self.exposeCmd.button]


class CcdPannel(ControlPannel):
    def __init__(self, controlDialog):
        ControlPannel.__init__(self, controlDialog, 'CCD')

        self.state = ValueGB(self.moduleRow, 'ccd', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'ccd', '', 1, '{:s}')

        self.commands = CcdCommands(self)

        self.grid.addWidget(self.state, 0, 0)
        self.grid.addWidget(self.substate, 0, 1)

        self.grid.addWidget(self.commands, 0, 2, 3, 3)

    @property
    def customWidgets(self):
        return [self.grid.itemAt(i).widget() for i in range(self.grid.count())] + self.commands.buttons


class SacDialog(ControlDialog):
    def __init__(self, sacRow):
        ControlDialog.__init__(self, moduleRow=sacRow)

        self.detectorPannel = StagePannel(self, 'detector')
        self.pentaPannel = StagePannel(self, 'penta')
        self.ccdPannel = CcdPannel(self)

        self.grid.addWidget(self.detectorPannel, 0, 0)
        self.grid.addWidget(self.pentaPannel, 1, 0)
        self.grid.addWidget(self.ccdPannel, 2, 0)

    @property
    def customWidgets(self):
        return self.detectorPannel.customWidgets + self.pentaPannel.customWidgets, self.ccdPannel.customWidgets
