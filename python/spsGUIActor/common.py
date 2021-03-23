__author__ = 'alefur'

import os

import spsGUIActor

imgPath = os.path.abspath(os.path.join(os.path.dirname(spsGUIActor.__file__), '../..', 'img'))
import spsGUIActor.styles as styles
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QPushButton, QDoubleSpinBox, QSpinBox, QComboBox, QCheckBox, QLineEdit, QGridLayout, \
    QVBoxLayout, QHBoxLayout, QTabWidget

spacing = 2


class TabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        QTabWidget.__init__(self, *args, **kwargs)
        self.setStyleSheet("QTabWidget {font: %dpt; }" % (styles.smallFont))


class SpinBox(QSpinBox):
    def __init__(self, *args, **kwargs):
        QSpinBox.__init__(self, *args, **kwargs)
        self.setStyleSheet("QSpinBox {font: %dpt; }" % (styles.smallFont))


class DoubleSpinBox(QDoubleSpinBox):
    def __init__(self, *args, **kwargs):
        QDoubleSpinBox.__init__(self, *args, **kwargs)
        self.setStyleSheet("QDoubleSpinBox {font: %dpt; }" % (styles.smallFont))


class PushButton(QPushButton):
    def __init__(self, label='', safetyCheck=False):
        self.mPixmap = None
        QPushButton.__init__(self, label)

        if safetyCheck:
            self.setPixmap(Pixmap('warning.png'))

        self.setStyleSheet("QPushButton {font: %dpt; }" % (styles.smallFont))

    def setPixmap(self, pixmap):

        pixmap = pixmap.scaledToHeight(self.sizeHint().height() - 7, mode=Qt.SmoothTransformation)
        self.mPixmap = pixmap

    def sizeHint(self):
        sizeHint = QPushButton.sizeHint(self)

        if self.mPixmap is not None:
            sizeHint = QSize(sizeHint.width() + self.mPixmap.width(), max(sizeHint.height(), self.mPixmap.height()))

        return sizeHint

    def paintEvent(self, event):
        QPushButton.paintEvent(self, event)
        if self.mPixmap is not None:
            y = (self.height() - self.mPixmap.height()) / 2
            painter = QPainter(self)
            painter.drawPixmap(5, y, self.mPixmap)


class ComboBox(QComboBox):
    def __init__(self, *args, **kwargs):
        QComboBox.__init__(self, *args, **kwargs)
        self.setStyleSheet("QComboBox {font: %dpt; }" % (styles.smallFont))


class LineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        QLineEdit.__init__(self, *args, **kwargs)
        self.setStyleSheet("QLineEdit {font: %dpt; }" % (styles.smallFont))


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


class GridLayout(QGridLayout):
    def __init__(self, *args, **kwargs):
        QGridLayout.__init__(self, *args, **kwargs)
        self.setSpacing(spacing)


class VBoxLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs):
        QVBoxLayout.__init__(self, *args, **kwargs)
        self.setSpacing(spacing)


class HBoxLayout(QHBoxLayout):
    def __init__(self, *args, **kwargs):
        QHBoxLayout.__init__(self, *args, **kwargs)
        self.setSpacing(spacing)


class GBoxGrid(QGridLayout):
    def __init__(self, *args, title='', **kwargs):
        QGridLayout.__init__(self, *args, **kwargs)
        upMargin = 1 if not title else 8
        self.setContentsMargins(0, upMargin, 0, 0)
        self.setSpacing(spacing)
