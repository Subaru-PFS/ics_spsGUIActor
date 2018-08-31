__author__ = 'alefur'

from spsClient import bigFont
from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB


class XcuRow(ModuleRow):
    def __init__(self, cam):
        self.cam = cam
        ModuleRow.__init__(self, module=cam.specModule,
                           actorName='xcu_%s%i' % (cam.arm, cam.specModule.smId),
                           actorLabel='')

        self.pressure = ValueGB(self, 'pressure', 'Pressure(Torr)', 0, '{:g}', fontSize=bigFont)

    @property
    def customWidgets(self):
        return [self.pressure]

    def setOnline(self):
        ModuleRow.setOnline(self)
        self.cam.setOnline()
