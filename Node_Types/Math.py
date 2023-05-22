import sys
sys.path.append("..")

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_node import Node
from node_content_widget import QDMNodeContentWidget

# https://www.pythonguis.com/tutorials/pyqt-basic-widgets/

DEBUG = False

op_list = ["+", "-", "*", "/"]

#Node Type
class NT_Math(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Math")
        
    def __str__(self):
        return "<Math Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    #Called from within the Node for loading custom content widget
    def initContent(self):
        self.content = NTW_Math(self)
        self.operator = "+"
        
    def onNodeUpdate(self):
        self.outputValues[0] = None
        input1 = self.inputValues[0]
        input2 = self.inputValues[1]
        result = self._calc(input1, input2)
        if DEBUG: self.printToConsole(f"onNodeUpdate in {self} with result as {result}")
        self.outputValues[0] = result

        self.content.display()

    def _calc(self, num1, num2):
        try:
            if self.operator == "+":
                return num1 + num2
            elif self.operator == "-":
                return num1 - num2
            elif self.operator == "*":
                return num1 * num2
            elif self.operator == "/":
                return num1 / num2
            else:
                return None
        except (TypeError, ZeroDivisionError) as e:
            if DEBUG: self.printToConsole(f"Math Node Error: {e}")
                
    def operatorChoice(self, operator):
        if DEBUG: self.printToConsole(f"Operator chosen: {self.operator}")
        self.operator = operator
        
#Node Type Widget
class NTW_Math(QDMNodeContentWidget):
    def __init__(self, node):
        super().__init__(node)
        self.inputSocketTypes = [(0,0),(2,0)]
        self.outputSocketTypes = [(1,0)]
        self.height = 120

    def initUI(self):
        self.input1_label = QLabel("Input 1")
        self.operator_comboBox = QComboBox(self)

        for operator in op_list:
            self.operator_comboBox.addItem(operator)
        
        self.operator_comboBox.activated[str].connect(self.node.operatorChoice)
             
        self.input2_label = QLabel("Input 2")

        self.addWidgetToWidgetSlot(0, self.input1_label)
        self.addWidgetToWidgetSlot(1, self.operator_comboBox)
        self.addWidgetToWidgetSlot(2, self.input2_label)

    def grNodeEdit(self, grNode):
        grNode.setHeight(60)
        
    def display(self):
        if DEBUG: self.printToConsole("Updating Math Node")