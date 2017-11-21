__author__ = 'alefur'
from functools import partial

from PyQt5.QtWidgets import QLabel, QGridLayout, QGroupBox


class ValueGB(QGroupBox):
    colors = {"WIPING": ('blue', 'white'),
              "INTEGRATING": ('yellow', 'black'),
              "READING": ('orange', 'white'),
              "IDLE": ('green', 'white'),
              "NAN": ('red', 'white'),
              }
    def __init__(self, title):
        self.title = title

        QGroupBox.__init__(self)
        self.setTitle('%s' % self.title)

        self.grid = QGridLayout()
        self.value = QLabel()

        self.grid.addWidget(self.value, 0, 0)
        self.setLayout(self.grid)
        self.setColor('green')

    def setColor(self, background, police='white'):
        if background == "red":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f43131, stop: 1 #5e1414);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "green":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #45f42e, stop: 1 #195511);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "blue":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #3168f4, stop: 1 #14195e);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "yellow":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #edf431, stop: 1 #5e5b14);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")
        elif background == "orange":
            self.setStyleSheet(
                "QGroupBox {font-size: 9pt; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,stop: 0 #f4a431, stop: 1 #5e4a14);border: 1px solid gray;border-radius: 3px;margin-top: 1ex;} " +
                "QGroupBox::title {subcontrol-origin: margin;subcontrol-position: top center; padding: 0 3px;}")

        self.value.setStyleSheet("QLabel{font-size: 11pt; qproperty-alignment: AlignCenter; color:%s;}"%police)

    def setText(self, txt):
        self.value.setText(txt)

    def pimpMe(self):
        pass

class Device(object):
    def __init__(self, mwindow):
        object.__init__(self)
        self.mwindow = mwindow
        self.mode = ValueGB('')
        self.status = ValueGB('')
        self.state = ValueGB('')

        for gb in [self.mode, self.status, self.state]:
            gb.setText('UNDEF')

    @property
    def models(self):
        return self.mwindow.actor.models

    def setMode(self, mode):
        self.mode.setText(mode)

    def setStatus(self, status):
        if status == 'Offline':
            self.status.setColor('red')
        elif status == 'Online':
            self.status.setColor('green')

        self.status.setText(status)

    def setState(self, state):
        self.state.setText(state)

    def getValueGB(self, title, actorName, key, ind, fmt):
        model = self.models[actorName]
        keyvar = model.keyVarDict[key]

        valueGB = ValueGB(title)
        keyvar.addCallback(partial(self.updateVals, valueGB, ind, fmt))

        return valueGB

    def updateVals(self, label, ind, fmt, keyvar):
        values = keyvar.getValue(doRaise=False)
        values = (values,) if not isinstance(values, tuple) else values

        value = values[ind]
        strValue = 'nan' if value is None else fmt.format(value)
        label.setText(strValue)
        label.pimpMe()


class Cryostat(Device):
    def __init__(self, viscu):
        self.viscu = viscu
        Device.__init__(self, viscu.mwindow)

        self.setMode('Operation')
        self.setStatus('Offline')
        self.pressure = self.getValueGB('Pressure(Torr)', self.viscu.xcuActor, 'ionpump1', 4, '{:g}')


class Ccd(Device):

    def __init__(self, viscu):

        self.viscu = viscu
        Device.__init__(self, viscu.mwindow)

        self.setMode('Operation')
        self.setStatus('Offline')
        self.state = self.getValueGB('', self.viscu.ccdActor, 'exposureState', 0, '{:s}')
        self.temperature = self.getValueGB('Temperature(K)', self.viscu.xcuActor, 'temps', 0, '{:g}')

        setattr(self.state, 'pimpMe', partial(self.exposureState, self.state))

    def exposureState(self, state):
        label = state.value
        stateLabel = label.text().upper()
        label.setText(stateLabel)
        background, police = state.colors[stateLabel]
        state.setColor(background, police)



class Viscu(QGridLayout):
    def __init__(self, mwindow, smId, arm):
        QGridLayout.__init__(self)
        self.mwindow = mwindow
        self.smId = smId
        self.arm = arm
        self.cryostat = Cryostat(self)
        self.ccd = Ccd(self)

        self.populateLayout()

    def populateLayout(self):
        self.addWidget(QLabel('Mode'), 0, 1)
        self.addWidget(QLabel('Status'), 0, 2)
        self.addWidget(QLabel('State'), 0, 3)

        self.addWidget(QLabel('CCD_%s' % self.cam.upper()), 1, 0)
        self.addWidget(self.ccd.mode, 1, 1)
        self.addWidget(self.ccd.status, 1, 2)
        self.addWidget(self.ccd.state, 1, 3)
        self.addWidget(self.ccd.temperature, 1, 4)

        self.addWidget(QLabel('XCU_%s' % self.cam.upper()), 2, 0)
        self.addWidget(self.cryostat.mode, 2, 1)
        self.addWidget(self.cryostat.status, 2, 2)
        self.addWidget(self.cryostat.state, 2, 3)
        self.addWidget(self.cryostat.pressure, 2, 4)

    @property
    def cam(self):
        return '%s%i' % (self.arm, self.smId)

    @property
    def xcuActor(self):
        return 'xcu_%s' % self.cam

    @property
    def ccdActor(self):
        return 'ccd_%s' % self.cam