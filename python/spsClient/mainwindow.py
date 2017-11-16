__author__ = 'alefur'

from functools import partial

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QHBoxLayout


class SpsWidget(QWidget):
    def __init__(self, spsClient):
        QWidget.__init__(self)
        self.spsClient = spsClient
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.addLabels('xcu_r1', 'pressure'))
        self.mainLayout.addLayout(self.addLabels('xcu_r1', 'coolerTemps'))
        self.mainLayout.addLayout(self.addLabels('xcu_r1', 'temps'))
        self.mainLayout.addLayout(self.addLabels('xcu_r1', 'roughPressure1'))
        self.mainLayout.addLayout(self.addLabels('xcu_r1', 'turboSpeed'))

        self.setLayout(self.mainLayout)

    @property
    def actor(self):
        return self.spsClient.actor

    def addLabels(self, actorName, key):
        model = self.actor.models[actorName]
        keyvar = model.keyVarDict[key]
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel('%s : ' % key))
        labels = []

        for i in range(keyvar.key.typedValues.maxVals):
            label = QLabel('nan')
            hbox.addWidget(label)
            labels.append(label)

        keyvar.addCallback(partial(self.updateVals, labels))

        return hbox

    def updateVals(self, labels, keyvar):
        values = keyvar.getValue(doRaise=False)
        values = [values] if len(labels) == 1 else values

        for i, label in enumerate(labels):
            value = values[i]
            strValue = 'nan' if value is None else '%g' % value
            label.setText(strValue)
