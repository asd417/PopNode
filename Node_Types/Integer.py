import sys
sys.path.append("..")

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_node import Node
from node_content_widget import QDMNodeContentWidget

# https://www.pythonguis.com/tutorials/pyqt-basic-widgets/

#Node Type
class NT_Integer(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Integer")
        self._number = 0
        self.outputValues[0] = 0
    
    def __str__(self):
        return "<Integer Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    #Called from within the Node for loading custom content widget
    def initContent(self):
        self.content = NTW_Integer(self)
    
    def setNum(self, num):
        self._number = num
        self.updateThisNode()

    def onNodeUpdate(self):
        self.outputValues[0] = self._number

#Node Type Widget
class NTW_Integer(QDMNodeContentWidget):
    def __init__(self, node):
        super().__init__(node)
        self.inputSocketTypes = None
        self.outputSocketTypes = [(0,0)]
        self.height = 90
        
    def initUI(self):
        spinner = QSpinBox()
        spinner.setRange(-100000, 100000)
        spinner.valueChanged.connect(self.spinnerValueChanged)
        self.add_widget_to_widget_slot(0, spinner)
        
    def initWidgetSlots(self):
        self.slotCount = 1
        
    def spinnerValueChanged(self, number):
        self.node.setNum(number)