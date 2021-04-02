__author__ = 'alefur'

from spsGUIActor.control import ControllerPanel
from spsGUIActor.enu import EnuDeviceCmd
from spsGUIActor.widgets import ValueGB, SwitchGB, SwitchButton


class PduButton(SwitchButton):
    def __init__(self, controlPanel, key, label, safetyCheck=False):
        cmdStrOn = f'{controlPanel.actorName} power on={key}'
        cmdStrOff = f'{controlPanel.actorName} power off={key}'
        SwitchButton.__init__(self, controlPanel=controlPanel, key=key, label=label, cmdHead='', cmdStrOn=cmdStrOn,
                              cmdStrOff=cmdStrOff, safetyCheck=safetyCheck)


class PduPanel(ControllerPanel):
    outletsConfig = dict(channel01="neon",
                         channel02="xenon",
                         channel03="hgar",
                         channel04="krypton",
                         channel05="breva",
                         channel06="deuterium",
                         channel07="argon",
                         channel09="roughpump",
                         channel10="bakeout",
                         channel11="moxa",
                         channel12="matlamp",
                         channel13="sac",
                         channel14="mono",
                         channel15="labsphere")

    def __init__(self, controlDialog):
        ControllerPanel.__init__(self, controlDialog, 'pdu')
        self.addCommandSet(PduCommands(self))

    def createWidgets(self):
        self.mode = ValueGB(self.moduleRow, 'pduMode', '', 0, '{:s}')
        self.state = ValueGB(self.moduleRow, 'pduFSM', '', 0, '{:s}')
        self.substate = ValueGB(self.moduleRow, 'pduFSM', '', 1, '{:s}')

        self.outlets = dict([(outlet, SwitchGB(self.moduleRow, outlet, outlet.capitalize(), 0, '{:g}')) for outlet in
                             PduPanel.outletsConfig.values()])

        self.voltage = ValueGB(self.moduleRow, 'atenVAW', 'Voltage', 0, '{:.2f}')
        self.current = ValueGB(self.moduleRow, 'atenVAW', 'Current', 1, '{:.2f}')
        self.power = ValueGB(self.moduleRow, 'atenVAW', 'Power', 2, '{:.2f}')

    def setInLayout(self):
        self.grid.addWidget(self.mode, 0, 0)
        self.grid.addWidget(self.state, 0, 1)
        self.grid.addWidget(self.substate, 0, 2)

        self.grid.addWidget(self.voltage, 1, 0)
        self.grid.addWidget(self.current, 1, 1)
        self.grid.addWidget(self.power, 1, 2)

        for i, widget in enumerate(self.outlets.values()):
            self.grid.addWidget(widget, 2+i//4, i%4)



class PduCommands(EnuDeviceCmd):
    safetyCheck = ['roughpump', 'bakeout', 'sac', 'breva', 'moxa']

    def __init__(self, controlPanel):
        EnuDeviceCmd.__init__(self, controlPanel)

        for i, outlet in enumerate(controlPanel.outlets.keys()):
            switch = PduButton(controlPanel=controlPanel, key=outlet, label=outlet.capitalize(),
                               safetyCheck=outlet in PduCommands.safetyCheck)
            self.grid.addWidget(switch, 1+i//4, i%4)

