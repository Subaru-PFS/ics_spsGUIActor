__author__ = 'alefur'
from spsClient.modulerow import ModuleRow
from spsClient.widgets import ValueGB


class SeqnoRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='seqno', actorLabel='SEQNO')

        self.visit = ValueGB(self, 'visit', 'VisitId', 0, '{:g}')

    @property
    def customWidgets(self):
        return [self.visit]
