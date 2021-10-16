
from node_console_connector import ConsoleConnector
from ui_graphics import UIGraphics

class UI(ConsoleConnector):
    def __init__(self, scene):
        self.scene = scene
        self.graphics = UIGraphics(scene)