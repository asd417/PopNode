from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class QDMNodeContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUILayout()
        self.initUI()
        
        self.inputs = [0,1,2]
        self.outputs = [0,1,2]

    # Example UI Initialization
    def initUI(self):
        self.wdg_label = QLabel("Some title")
        self.layout.addWidget(self.wdg_label)
        self.layout.addWidget(QTextEdit("foo"))
        
    def initUILayout(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        
    def overrideUI(self):
        pass
    
    def getInputs(self):
        return self.inputs
    
    def getOutputs(self):
        return self.outputs
    
    def grNodeEdit(self):
        pass