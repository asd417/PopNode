from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_console_connector import ConsoleConnector

class UIGraphics(QWidget, ConsoleConnector):
    def __init__(self, UI, scene, parent=None):
        super().__init__(parent)

        self.scene = scene
        self.UI = UI
        self.console = self.scene.console
        self.nodeTypeList = UI.nodeTypeList
        
        self.createHorizontalLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        
    
    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox("Editor")
        layout = QHBoxLayout()
        
        nodeTypeComboBox = QComboBox(self)
        for item in self.nodeTypeList:
            nodeTypeComboBox.addItem(item)
        nodeTypeComboBox.activated[str].connect(self.UI.nodeChoice)
        layout.addWidget(nodeTypeComboBox)
        
        addNode = QPushButton('Create New Node', self)
        addNode.clicked.connect(self.UI.addNode)
        layout.addWidget(addNode)
        
        buttonRed = QPushButton('Interesting Button', self)
        buttonRed.clicked.connect(self.on_click)
        layout.addWidget(buttonRed)
        
        buttonGreen = QPushButton('Useful Button', self)
        buttonGreen.clicked.connect(self.on_click)
        layout.addWidget(buttonGreen)
        
        self.horizontalGroupBox.setLayout(layout)
        
    def on_click(self):
        print('PyQt5 button click')