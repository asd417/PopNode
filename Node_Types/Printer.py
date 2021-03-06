import sys
sys.path.append("..")

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_node import Node
from node_content_widget import QDMNodeContentWidget

# https://www.pythonguis.com/tutorials/pyqt-basic-widgets/

DEBUG = False
#Node Type
class NT_Printer(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Printer")
        
    def __str__(self):
        return "<Printer Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    #Called from within the Node for loading custom content widget
    def initContent(self):
        self.content = NTW_Printer(self)
        self.printValue = 0
        
    def onNodeUpdate(self):
        if DEBUG: self.printToConsole("onNodeUpdate in " + str(self))
        inputV = self.inputValues[0]
        if inputV is None:
            self.printValue = "Invalid Input"
        else:
            self.printValue = inputV
        self.outputValues[0] = inputV
        self.content.display()

#Node Type Widget
class NTW_Printer(QDMNodeContentWidget):
    def __init__(self, node):
        super().__init__(node)
        self.inputSocketTypes = [(0,0)]
        self.outputSocketTypes = [(0,0)]
        self.height = 90

    def initUI(self):
        self.wdg_label = QLabel("No Input")
        self.addWidgetToWidgetSlot(0, self.wdg_label)
        
    def initWidgetSlots(self):
        self.slotCount = 1
        
    def display(self):
        if DEBUG: self.printToConsole("Updating Printer Node")
        try:
            text = str(self.node.printValue)
            self.wdg_label.setText(text)
        except:
            if DEBUG: self.printToConsole(str(self.node.printValue))