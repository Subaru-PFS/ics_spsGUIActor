__author__ = 'alefur'

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel


class SpsWidget(QWidget):
    def __init__(self, spsClient):
        QWidget.__init__(self)
        self.spsClient = spsClient
        self.mainLayout = QVBoxLayout()

        self.setLayout(self.mainLayout)
