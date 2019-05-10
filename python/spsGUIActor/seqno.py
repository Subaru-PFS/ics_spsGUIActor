__author__ = 'alefur'
from spsGUIActor.modulerow import ModuleRow
from spsGUIActor.widgets import ValueGB


class SeqnoRow(ModuleRow):
    def __init__(self, aitModule):
        ModuleRow.__init__(self, module=aitModule, actorName='seqno', actorLabel='SEQNO')

        self.visit = ValueGB(self, 'visit', 'VisitId', 0, '{:g}')

    @property
    def customWidgets(self):
        return [self.visit]
