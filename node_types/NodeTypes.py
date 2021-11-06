import sys
sys.path.append("..")

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_node import Node
from node_content_widget import QDMNodeContentWidget

# https://www.pythonguis.com/tutorials/pyqt-basic-widgets/


# Why the Instance Variable of the Super Class Is Not Overridden in the Sub Class
# https://dzone.com/articles/why-instance-variable-of-super-class-is-not-overri

#Node Type
class NT_Integer(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Integer")
        self._number = 0

    def setNum(self, num):
        self._number = num
        
    def initContent(self):
        self.content = NTW_Integer(self)

#Node Type Widget
class NTW_Integer(QDMNodeContentWidget):
    def __init__(self, node):
        self.node = node
        super().__init__()
        self.inputs = None
        self.outputs = [0]

    def initUI(self):
        self.spinner = QSpinBox()
        self.spinner.setRange(-100000, 100000)
        self.spinner.valueChanged.connect(self.spinnerValueChanged)
        self.layout.addWidget(self.spinner)

    def spinnerValueChanged(self, number):
        self.node.setNum(number)
        
    def grNodeEdit(self):
        self.node.grNode.setHeight(60)
        self.node.grNode.update