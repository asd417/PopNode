
from node_console_connector import ConsoleConnector
from ui_graphics import UIGraphics
from Node_Types import *

DEBUG = True
class UI(ConsoleConnector):
    def __init__(self, scene, nodetypes):
        self.scene = scene
        self.console = self.scene.console
        self.nodeTypeList = nodetypes
        self.graphics = UIGraphics(self, scene)
        self.nodeChoice = nodetypes[0]
        
    def addNode(self):
        nodeChoice = self.nodeChoice
        nodeClassName = "NT_" + nodeChoice
        nodeGenString = nodeChoice + "." + nodeClassName + "(self.scene)"
        
        if DEBUG: self.printToConsole("Creating Instance for Node Type: " + str(self.nodeChoice))
        eval(nodeGenString)
            
    def nodeChoice(self, text):
        self.nodeChoice = text