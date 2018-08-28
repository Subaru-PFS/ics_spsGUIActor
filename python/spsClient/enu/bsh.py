__author__ = 'alefur'

from spsClient.widgets import ValueGB, ControlPanel


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

        self.setChecked(False)
        self.showHide()
