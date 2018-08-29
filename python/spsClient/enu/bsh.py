__author__ = 'alefur'

from PyQt5.QtWidgets import QComboBox
from spsClient.dcb.aten import SwitchButton
from spsClient.widgets import ValueGB, ControlPanel, CmdButton, CustomedCmd, CommandsGB, SwitchGB, SpinBoxGB


class ShutterCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SHUTTERS')

        self.comboMove = QComboBox()
        self.comboMove.addItems(['open', 'close'])

        self.comboShut = QComboBox()
        self.comboShut.addItems(['', 'blue', 'red'])

        self.addWidget(self.comboMove, 0, 1)
        self.addWidget(self.comboShut, 0, 2)

    def buildCmd(self):
        cmdStr = '%s shutters %s %s' % (self.controlPanel.enuActor,
                                             self.comboMove.currentText(),
                                             self.comboShut.currentText())

        return cmdStr


class BiaPeriod(ValueGB):
    def __init__(self, moduleRow):
        self.spinbox = SpinBoxGB('Period', 0, 65536)
        ValueGB.__init__(self, moduleRow, 'biaConfig', '', 0, '{:d}', fontSize=9)

    def setText(self, txt):
        if not self.spinbox.locked:
            self.spinbox.setValue(txt)

    def getValue(self):
        return self.spinbox.getValue()


class BiaDuty(ValueGB):
    def __init__(self, moduleRow):
        self.spinbox = SpinBoxGB('Duty', 0, 255)
        ValueGB.__init__(self, moduleRow, 'biaConfig', '', 1, '{:d}', fontSize=9)

    def setText(self, txt):
        if not self.spinbox.locked:
            self.spinbox.setValue(txt)

    def getValue(self):
        return self.spinbox.getValue()

class SetBiaParamCmd(CustomedCmd):
    def __init__(self, controlPanel):
        CustomedCmd.__init__(self, controlPanel=controlPanel, buttonLabel='SET PARAMETERS')

        self.period = BiaPeriod(moduleRow=self.controlPanel.moduleRow)
        self.duty = BiaDuty(moduleRow=self.controlPanel.moduleRow)

        self.addWidget(self.period.spinbox, 0, 1)
        self.addWidget(self.duty.spinbox, 0, 2)

    def buildCmd(self):
        cmdStr = '%s bia config period=%i duty=%i ' % (self.controlPanel.enuActor, self.period.getValue(),
                                                       self.duty.getValue())

        return cmdStr


class SwitchBia(SwitchButton):
    def __init__(self, controlPanel):
        SwitchButton.__init__(self, controlPanel=controlPanel, key='bia', label='BIA', fmt='{:s}',
                              cmdHead='%s bia' % controlPanel.enuActor, cmdTail=' ')

    def setText(self, txt):
        bool = True if txt in ['undef', 'on'] else False

        self.buttonOn.setVisible(not bool)
        self.buttonOff.setVisible(bool)


class BshCommands(CommandsGB):
    def __init__(self, controlPanel):
        CommandsGB.__init__(self, controlPanel)

        self.connectButton = CmdButton(controlPanel=controlPanel, label='CONNECT',
                                       cmdStr='%s connect controller=bsh' % controlPanel.enuActor)

        self.shutterCmd = ShutterCmd(controlPanel=controlPanel)
        self.switchBia = SwitchBia(controlPanel=controlPanel)

        self.switchStrobe = SwitchButton(controlPanel=controlPanel, key='biaStrobe', label='STROBE',
                                         cmdHead='%s bia strobe' % controlPanel.enuActor, cmdTail=' ')

        self.setBiaParam = SetBiaParamCmd(controlPanel=controlPanel)

        self.grid.addWidget(self.connectButton, 0, 0)
        self.grid.addLayout(self.shutterCmd, 1, 0,1,3)

        self.switchBia.setGrid(self.grid, 2, 0)
        self.switchStrobe.setGrid(self.grid, 2, 1)
        self.grid.addLayout(self.setBiaParam, 3, 0, 1, 3)

    @property
    def buttons(self):
        return [self.connectButton] + self.switchBia.buttons, self.switchStrobe.buttons


class BshPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog, 'BSH')

        self.mode = ValueGB(self.moduleRow, 'bshMode', 'Mode', 0, '{:s}', fontSize=9)
        self.state = ValueGB(self.moduleRow, 'bshFSM', '', 0, '{:s}', fontSize=9)
        self.substate = ValueGB(self.moduleRow, 'bshFSM', '', 1, '{:s}', fontSize=9)

        self.shutters = ValueGB(self.moduleRow, 'shutters', 'Shutters', 0, '{:s}', fontSize=9)
        self.exptime = ValueGB(self.moduleRow, 'integratingTime', 'Exptime', 0, '{:.1f}', fontSize=9)
        self.elapsedTime = ValueGB(self.moduleRow, 'elapsedTime', 'elapsedTime', 0, '{:.1f}', fontSize=9)

        self.bia = ValueGB(self.moduleRow, 'bia', 'BIA', 0, '{:s}', fontSize=9)
        self.biaStrobe = SwitchGB(self.moduleRow, 'biaStrobe', 'Strobe', 0, '{:g}', fontSize=9)

        self.biaPeriod = ValueGB(self.moduleRow, 'biaConfig', 'Bia-Period', 0, '{:d}', fontSize=9)
        self.biaDuty = ValueGB(self.moduleRow, 'biaConfig', 'Bia-Duty', 1, '{:d}', fontSize=9)

        self.commands = BshCommands(self)
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.shutters, 1, 0)
        self.grid.addWidget(self.exptime, 1, 1)
        self.grid.addWidget(self.elapsedTime, 1, 2)

        self.grid.addWidget(self.bia, 2, 0)
        self.grid.addWidget(self.biaStrobe, 2, 1)
        self.grid.addWidget(self.biaPeriod, 2, 2)
        self.grid.addWidget(self.biaDuty, 2, 3)

        self.grid.addWidget(self.commands, 0, 4, 3, 2)

    @property
    def enuActor(self):
        return self.controlDialog.moduleRow.actorName

    @property
    def customWidgets(self):
        return [self.grid.itemAt(i).widget() for i in range(self.grid.count())]
