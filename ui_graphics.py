from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_console_connector import ConsoleConnector

class UIGraphics(QWidget, ConsoleConnector):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene
        self.console = self.scene.console