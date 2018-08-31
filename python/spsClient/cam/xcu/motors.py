__author__ = 'alefur'

from spsClient.widgets import ValueGB, ControlPanel


class CcdMotor(object):
    def __init__(self, moduleRow, motorId):
        self.status = ValueGB(moduleRow, 'ccdMotor%i' % motorId, 'status', 0, '{:s}')
        self.homeSwitch = ValueGB(moduleRow, 'ccdMotor%i' % motorId, 'homeSwitch', 1, '{:d}')
        self.farSwitch = ValueGB(moduleRow, 'ccdMotor%i' % motorId, 'farSwitch', 2, '{:d}')
        self.steps = ValueGB(moduleRow, 'ccdMotor%i' % motorId, 'steps', 3, '{:g}')
        self.position = ValueGB(moduleRow, 'ccdMotor%i' % motorId, 'position', 4, '{:.2f}')

    @property
    def widgets(self):
        return [self.status, self.homeSwitch, self.farSwitch, self.steps, self.position]


class MotorsPanel(ControlPanel):
    def __init__(self, controlDialog):
        ControlPanel.__init__(self, controlDialog)

        self.motorA = CcdMotor(self.moduleRow, motorId=1)
        self.motorB = CcdMotor(self.moduleRow, motorId=2)
        self.motorC = CcdMotor(self.moduleRow, motorId=3)

        for i, motor in enumerate(self.motors):
            for j, widget in enumerate(motor.widgets):
                self.grid.addWidget(widget, i, j)

    @property
    def motors(self):
        return [self.motorA, self.motorB, self.motorC]

    @property
    def customWidgets(self):
        return [self.grid.itemAt(i).widget() for i in range(self.grid.count())]
