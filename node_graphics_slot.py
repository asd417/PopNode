from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Slot(QWidget):
    def __init__(self, index):
        super().__init__()
        self.index = index
        self.slot = None
        
    def setLayout(self, layout):
        super().setLayout(layout)
        self.slot = layout