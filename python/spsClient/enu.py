__author__ = 'alefur'
from PyQt5.QtWidgets import QProgressBar

from spsClient.modulerow import ModuleRow
from spsClient.widgets import Coordinates, ValueGB, ControlDialog, ControlPannel


class ElapsedTime(QProgressBar):
    def __init__(self, enuWidget, exptime):
        QProgressBar.__init__(self)
        self.setRange(0, exptime)
        self.enuWidget = enuWidget
        enuWidget.keyVarDict['elapsedTime'].addCallback(self.updateBar)
        enuWidget.keyVarDict['exptime'].addCallback(self.hideBar, callNow=False)

    def updateBar(self, keyvar):
        try:
            val = keyvar.getValue()
        except ValueError:
            val = 0

        self.setValue(val)

    def hideBar(self, keyvar):
        self.enuWidget.keyVarDict['elapsedTime'].removeCallback(self.updateBar)
        self.enuWidget.keyVarDict['exptime'].removeCallback(self.hideBar)
        self.enuWidget.removeWidget(self)


class RexmPannel(ControlPannel):
    def __init__(self, controlDialog):
        ControlPannel.__init__(self, controlDialog, 'RDA')

        self.mode = ValueGB(self.moduleRow, 'rexmMode', 'Mode', 0, '{:s}', fontSize=9)
        self.state = ValueGB(self.moduleRow, 'rexmFSM', '', 0, '{:s}', fontSize=9)
        self.substate = ValueGB(self.moduleRow, 'rexmFSM', '', 1, '{:s}', fontSize=9)
        self.position = ValueGB(self.moduleRow, 'rexm', 'Position', 0, '{:s}', fontSize=9)

        self.switchA = ValueGB(self.moduleRow, 'rexmInfo', 'SwitchA', 0, '{:d}', fontSize=9)
        self.switchB = ValueGB(self.moduleRow, 'rexmInfo', 'switchB', 1, '{:d}', fontSize=9)
        self.speed = ValueGB(self.moduleRow, 'rexmInfo', 'Speed', 2, '{:d}', fontSize=9)
        self.steps = ValueGB(self.moduleRow, 'rexmInfo', 'Steps', 3, '{:d}', fontSize=9)

        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)
        self.grid.addWidget(self.position, 0, 3)

        self.grid.addWidget(self.switchA, 1, 0)
        self.grid.addWidget(self.switchB, 1, 1)
        self.grid.addWidget(self.speed, 1, 2)
        self.grid.addWidget(self.steps, 1, 3)


class BshPannel(ControlPannel):
    def __init__(self, controlDialog):
        ControlPannel.__init__(self, controlDialog, 'BSH')

        self.mode = ValueGB(self.moduleRow, 'bshMode', 'Mode', 0, '{:s}', fontSize=9)
        self.state = ValueGB(self.moduleRow, 'bshFSM', '', 0, '{:s}', fontSize=9)
        self.substate = ValueGB(self.moduleRow, 'bshFSM', '', 1, '{:s}', fontSize=9)

        self.shutters = ValueGB(self.moduleRow, 'shutters', 'Shutters', 0, '{:s}', fontSize=9)
        self.exptime = ValueGB(self.moduleRow, 'integratingTime', 'Exptime', 0, '{:.1f}', fontSize=9)
        self.elapsedTime = ValueGB(self.moduleRow, 'elapsedTime', 'elapsedTime', 0, '{:.1f}', fontSize=9)

        self.bia = ValueGB(self.moduleRow, 'bia', 'BIA', 0, '{:s}', fontSize=9)
        self.biaStrobe = ValueGB(self.moduleRow, 'biaStrobe', 'Strobe', 0, '{:s}', fontSize=9)
        self.biaPeriod = ValueGB(self.moduleRow, 'biaConfig', 'Bia-Period', 0, '{:.1f}', fontSize=9)
        self.biaDuty = ValueGB(self.moduleRow, 'biaConfig', 'Bia-Duty', 1, '{:.1f}', fontSize=9)

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


class SlitPannel(ControlPannel):
    def __init__(self, controlDialog):
        ControlPannel.__init__(self, controlDialog, 'FCA')

        self.mode = ValueGB(self.moduleRow, 'slitMode', 'Mode', 0, '{:s}', fontSize=9)
        self.state = ValueGB(self.moduleRow, 'slitFSM', '', 0, '{:s}', fontSize=9)
        self.substate = ValueGB(self.moduleRow, 'slitFSM', '', 1, '{:s}', fontSize=9)
        self.info = ValueGB(self.moduleRow, 'slitInfo', 'Info', 0, '{:s}', fontSize=9)
        self.location = ValueGB(self.moduleRow, 'slitLocation', 'Location', 0, '{:s}', fontSize=9)

        self.coordinates = Coordinates(self.moduleRow, 'slit', title='Position', fontSize=9)
        self.home = Coordinates(self.moduleRow, 'slitHome', title='Home', fontSize=9)
        self.tool = Coordinates(self.moduleRow, 'slitTool', title='Tool', fontSize=9)

        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)
        self.grid.addWidget(self.location, 0, 3)

        self.grid.addWidget(self.info, 1, 0, 1, 6)
        self.grid.addWidget(self.coordinates, 2, 0, 1, 6)
        self.grid.addWidget(self.home, 3, 0, 1, 6)
        self.grid.addWidget(self.tool, 4, 0, 1, 6)

    @property
    def customWidgets(self):
        return [self.grid.itemAt(i).widget() for i in range(self.grid.count())] + self.coordinates.widgets + \
               self.home.widgets + self.tool.widgets


class EnuDialog(ControlDialog):
    def __init__(self, enuRow):
        ControlDialog.__init__(self, moduleRow=enuRow, title='Entrance Unit SM%i' % enuRow.module.smId)

        # self.textForHuman = ValueGB(enuDevice.keyVarDict['text'], 'Text', 0, '{:s}')

        self.slitPannel = SlitPannel(self)
        self.bshPannel = BshPannel(self)
        self.rexmPannel = RexmPannel(self)

        # self.grid.addWidget(self.textForHuman, 0, 0, 1, 2)
        self.grid.addWidget(self.slitPannel, 1, 0, 5, 1)
        self.grid.addWidget(self.bshPannel, 1, 1, 3, 1)
        self.grid.addWidget(self.rexmPannel, 4, 1, 2, 1)

    @property
    def customWidgets(self):
        return self.slitPannel.customWidgets + self.bshPannel.customWidgets + self.rexmPannel.customWidgets


class EnuRow(ModuleRow):
    def __init__(self, specModule):
        ModuleRow.__init__(self, module=specModule, actorName='enu_sm%i' % specModule.smId, actorLabel='ENU')

        self.state = ValueGB(self, 'metaFSM', '', 0, '{:s}')
        self.substate = ValueGB(self, 'metaFSM', '', 1, '{:s}')

        self.rexm = ValueGB(self, 'rexm', 'Red Resolution', 0, '{:s}')
        self.slit = ValueGB(self, 'slitLocation', 'FCA_Position', 0, '{:s}')
        self.shutters = ValueGB(self, 'shutters', 'SHA_Position', 0, '{:s}')
        self.bia = ValueGB(self, 'bia', 'BIA_State', 0, '{:s}')

        self.keyVarDict['integratingTime'].addCallback(self.showBar, callNow=False)

    @property
    def customWidgets(self):
        widgets = [self.state, self.substate, self.rexm, self.slit, self.shutters, self.bia]

        try:
            widgets += self.enuDialog.customWidgets
        except AttributeError:
            pass

        return widgets

    def showBar(self, keyvar):
        try:
            exptime = keyvar.getValue()
        except ValueError:
            return

        elapsedTime = ElapsedTime(self, exptime=exptime)
        self.module.grid.addWidget(elapsedTime, self.lineNB, len(self.widgets))

    def removeWidget(self, widget):
        self.state.show()
        self.module.grid.removeWidget(widget)
        widget.deleteLater()

    def showDetails(self):
        self.enuDialog = EnuDialog(self)
        self.enuDialog.show()
