__author__ = 'alefur'
from PyQt5.QtWidgets import QProgressBar, QGridLayout, QGroupBox, QDialog

from spsClient.device import Device
from spsClient.widgets import Coordinates, ValueGB


class DeviceGB(QGroupBox):
    def __init__(self, deviceName):
        QGroupBox.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.setTitle(deviceName)
        self.setCheckable(True)

        self.clicked.connect(self.showHide)

    @property
    def customWidgets(self):
        return [self.grid.itemAt(i).widget() for i in range(self.grid.count())]

    def showHide(self):
        bool = True if self.isChecked() else False

        for widget in self.customWidgets:
            widget.setVisible(bool)


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


class RexmWidgets(DeviceGB):
    def __init__(self, enuDevice):
        DeviceGB.__init__(self, 'RDA')

        self.mode = ValueGB(enuDevice.keyVarDict['rexmMode'], 'Mode', 0, '{:s}', fontSize=9)
        self.state = ValueGB(enuDevice.keyVarDict['rexmFSM'], '', 0, '{:s}', fontSize=9)
        self.substate = ValueGB(enuDevice.keyVarDict['rexmFSM'], '', 1, '{:s}', fontSize=9)
        self.position = ValueGB(enuDevice.keyVarDict['rexm'], 'Position', 0, '{:s}', fontSize=9)

        self.switchA = ValueGB(enuDevice.keyVarDict['rexmInfo'], 'SwitchA', 0, '{:d}', fontSize=9)
        self.switchB = ValueGB(enuDevice.keyVarDict['rexmInfo'], 'switchB', 1, '{:d}', fontSize=9)
        self.speed = ValueGB(enuDevice.keyVarDict['rexmInfo'], 'Speed', 2, '{:d}', fontSize=9)
        self.steps = ValueGB(enuDevice.keyVarDict['rexmInfo'], 'Steps', 3, '{:d}', fontSize=9)

        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)
        self.grid.addWidget(self.position, 0, 3)

        self.grid.addWidget(self.switchA, 1, 0)
        self.grid.addWidget(self.switchB, 1, 1)
        self.grid.addWidget(self.speed, 1, 2)
        self.grid.addWidget(self.steps, 1, 3)


class BshWidgets(DeviceGB):
    def __init__(self, enuDevice):
        DeviceGB.__init__(self, 'BSH')

        self.mode = ValueGB(enuDevice.keyVarDict['bshMode'], 'Mode', 0, '{:s}', fontSize=9)
        self.state = ValueGB(enuDevice.keyVarDict['bshFSM'], '', 0, '{:s}', fontSize=9)
        self.substate = ValueGB(enuDevice.keyVarDict['bshFSM'], '', 1, '{:s}', fontSize=9)

        self.shutters = ValueGB(enuDevice.keyVarDict['shutters'], 'Shutters', 0, '{:s}', fontSize=9)
        self.exptime = ValueGB(enuDevice.keyVarDict['integratingTime'], 'Exptime', 0, '{:.1f}', fontSize=9)
        self.elapsedTime = ValueGB(enuDevice.keyVarDict['elapsedTime'], 'elapsedTime', 0, '{:.1f}', fontSize=9)

        self.bia = ValueGB(enuDevice.keyVarDict['bia'], 'BIA', 0, '{:s}', fontSize=9)
        self.biaStrobe = ValueGB(enuDevice.keyVarDict['biaStrobe'], 'Strobe', 0, '{:s}', fontSize=9)
        self.biaPeriod = ValueGB(enuDevice.keyVarDict['biaConfig'], 'Bia-Period', 0, '{:.1f}', fontSize=9)
        self.biaDuty = ValueGB(enuDevice.keyVarDict['biaConfig'], 'Bia-Duty', 1, '{:.1f}', fontSize=9)

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


class SlitWidgets(DeviceGB):
    def __init__(self, enuDevice):
        DeviceGB.__init__(self, 'FCA')

        self.mode = ValueGB(enuDevice.keyVarDict['slitMode'], 'Mode', 0, '{:s}', fontSize=9)
        self.state = ValueGB(enuDevice.keyVarDict['slitFSM'], '', 0, '{:s}', fontSize=9)
        self.substate = ValueGB(enuDevice.keyVarDict['slitFSM'], '', 1, '{:s}', fontSize=9)
        self.info = ValueGB(enuDevice.keyVarDict['slitInfo'], 'Info', 0, '{:s}', fontSize=9)
        self.location = ValueGB(enuDevice.keyVarDict['slitLocation'], 'Location', 0, '{:s}', fontSize=9)

        self.coordinates = Coordinates(enuDevice.keyVarDict['slit'], title='Position', fontSize=9)
        self.home = Coordinates(enuDevice.keyVarDict['slitHome'], title='Home', fontSize=9)
        self.tool = Coordinates(enuDevice.keyVarDict['slitTool'], title='Tool', fontSize=9)

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


class EnuDetail(QDialog):
    def __init__(self, enuDevice):
        QDialog.__init__(self, parent=enuDevice.specModule.mwindow.spsClient)

        self.enuDevice = enuDevice
        self.grid = QGridLayout()
        self.textForHuman = ValueGB(enuDevice.keyVarDict['text'], 'Text', 0, '{:s}')

        self.slitWidgets = SlitWidgets(enuDevice=enuDevice)
        self.bshWidgets = BshWidgets(enuDevice=enuDevice)
        self.rexmWidgets = RexmWidgets(enuDevice=enuDevice)

        self.grid.addWidget(self.textForHuman, 0, 0, 1, 2)
        self.grid.addWidget(self.slitWidgets, 1, 0, 5, 1)
        self.grid.addWidget(self.bshWidgets, 1, 1, 3, 1)
        self.grid.addWidget(self.rexmWidgets, 4, 1, 2, 1)
        self.setLayout(self.grid)

        self.setVisible(True)

        self.setWindowTitle('Entrance Unit SM%i' % enuDevice.specModule.smId)

    @property
    def customWidgets(self):
        return self.slitWidgets.customWidgets + self.bshWidgets.customWidgets + self.rexmWidgets.customWidgets


class Enu(Device):
    def __init__(self, specModule):
        Device.__init__(self, mwindow=specModule.mwindow, actorName='enu_sm%i' % specModule.smId, deviceName='ENU')
        self.specModule = specModule

        self.state = ValueGB(self.keyVarDict['metaFSM'], '', 0, '{:s}')
        self.substate = ValueGB(self.keyVarDict['metaFSM'], '', 1, '{:s}')

        self.rexm = ValueGB(self.keyVarDict['rexm'], 'Red Resolution', 0, '{:s}')
        self.slit = ValueGB(self.keyVarDict['slitLocation'], 'FCA_Position', 0, '{:s}')
        self.shutters = ValueGB(self.keyVarDict['shutters'], 'SHA_Position', 0, '{:s}')
        self.bia = ValueGB(self.keyVarDict['bia'], 'BIA_State', 0, '{:s}')

        self.keyVarDict['integratingTime'].addCallback(self.showBar, callNow=False)

    @property
    def customWidgets(self):
        widgets = [self.state, self.substate, self.rexm, self.slit, self.shutters, self.bia]

        try:
            widgets += self.enuDetail.customWidgets
        except AttributeError:
            pass

        return widgets

    def showBar(self, keyvar):
        try:
            exptime = keyvar.getValue()
        except ValueError:
            return

        elapsedTime = ElapsedTime(self, exptime=exptime)
        self.specModule.grid.addWidget(elapsedTime, self.line, len(self.widgets))

    def removeWidget(self, widget):
        self.state.show()
        self.specModule.grid.removeWidget(widget)
        widget.deleteLater()

    def showDetails(self):
        self.enuDetail = EnuDetail(self)
        self.enuDetail.show()
