__author__ = 'alefur'
from PyQt5.QtWidgets import QLabel, QProgressBar

from spsClient.device import Device
from functools import partial


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


class Enu(Device):
    def __init__(self, specModule):
        Device.__init__(self, mwindow=specModule.mwindow, actorName='enu_sm%i' % specModule.smId, deviceName='ENU')
        self.specModule = specModule

        self.state = self.getValueGB('', self.actorName, 'metaFSM', 0, '{:s}')
        self.substate = self.getValueGB('', self.actorName, 'metaFSM', 1, '{:s}')
        self.rexm = self.getValueGB('Red Resolution', self.actorName, 'rexm', 0, '{:s}')
        self.slit = self.getValueGB('FCA_Position', self.actorName, 'slitLocation', 0, '{:s}')
        self.shutters = self.getValueGB('SHA_Position', self.actorName, 'shutters', 0, '{:s}')
        self.bia = self.getValueGB('BIA_State', self.actorName, 'bia', 0, '{:s}')

        self.keyVarDict['integratingTime'].addCallback(self.showBar, callNow=False)
        self.updateActorStatus()

        setattr(self.rexm, 'pimpMe', partial(self.pimpDevice, self.rexm))
        setattr(self.slit, 'pimpMe', partial(self.pimpDevice, self.slit))
        setattr(self.shutters, 'pimpMe', partial(self.pimpDevice, self.shutters))
        setattr(self.bia, 'pimpMe', partial(self.pimpDevice, self.bia))

    @property
    def keyVarDict(self):
        return self.models[self.actorName].keyVarDict

    @property
    def widgets(self):
        return [self.actorStatus, self.state, self.substate, self.rexm, self.slit, self.shutters, self.bia]

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

    def pimpDevice(self, deviceGB):
        label = deviceGB.value
        background = 'red' if label.text() in ['undef', 'nan'] else 'green'
        deviceGB.setColor(background=background)

