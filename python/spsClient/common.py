__author__ = 'alefur'
import os

import spsClient

imgPath = os.path.abspath(os.path.join(os.path.dirname(spsClient.__file__), '../..', 'img'))
import spsClient.styles as styles
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QPushButton, QDoubleSpinBox, QSpinBox, QComboBox, QCheckBox


class SpinBox(QSpinBox):
    def __init__(self, *args, **kwargs):
        QSpinBox.__init__(self, *args, **kwargs)
        self.setStyleSheet("QSpinBox {font: %dpt; }" % (styles.smallFont))


class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, *args, **kwargs):
        QDoubleSpinBox.__init__(self, *args, **kwargs)
        self.setStyleSheet("QDoubleSpinBox {font: %dpt; }" % (styles.smallFont))


class PushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.setStyleSheet("QPushButton {font: %dpt; }" % (styles.smallFont))


class ComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        QComboBox.__init__(self, *args, **kwargs)
        self.setStyleSheet("QComboBox {font: %dpt; }" % (styles.smallFont))


class CheckBox(QCheckBox):
    def __init__(self, *args, **kwargs):
        QCheckBox.__init__(self, *args, **kwargs)
        self.setStyleSheet("QCheckBox {font: %dpt; }" % (styles.smallFont))


class Icon(QIcon):
    def __init__(self, filename):
        QIcon.__init__(self, Pixmap(filename))


class Pixmap(QPixmap):
    def __init__(self, filename):
        QPixmap.__init__(self)
        self.load(os.path.join(imgPath, filename))
