from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_graphics_scene import QDMGraphicsScene
from node_graphics_view import QDMGraphicsView
from node_scene import Scene
from node_node import Node
from node_edge import Edge
from node_console import ConsoleLog
from ui import UI
from random import randint

from Node_Types import *

import glob, os

DEBUG = True

class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.loadStylesheet("qss/nodestyle.qss")
        self.initUI()
        
    def initUI(self):
        self.setGeometry(0, 0, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        self.console = ConsoleLog()
        # create Graphics Scene
        self.scene = Scene(self.console)
        self.addNodes()
        # self.addUI()

        # create Graphics View
        self.view = QDMGraphicsView(self.console, self.scene.grScene, self)
        self.layout.addWidget(self.view)
        nodetypes = self._getNodeTypes()
        self.uiwidget = UI(self.scene, nodetypes)
        self.layout.addWidget(self.uiwidget.graphics)

        self.setWindowTitle("Node Editor")
        self.show()
        
    def __str__(self):
        return "NodeEditorWnd"
        
    def _getNodeTypes(self):
        os.chdir("./Node_Types")
        nodeTypeList = []
        for file in glob.glob("*.py"):
            if file != '__init__.py':
                file = file[:-3]
                nodeTypeList.append(file)
        return nodeTypeList

    # Function for testing nodes
    def addNodes(self):
        scene = self.scene
        node1 = Node(scene, "New Node 1")
        node2 = Node(scene, "New Node 2")
        node3 = Integer.NT_Integer(scene)
        node4 = Printer.NT_Printer(scene)

        node1.setPos(randint(-400, 400), randint(-400, 400))
        node2.setPos(randint(-400, 400), randint(-400, 400))
        node3.setPos(randint(-400, 400), randint(-400, 400))
        node4.setPos(randint(-400, 400), randint(-400, 400))
        
    def addDebugContent(self):
        greenBrush = QBrush(Qt.green)
        outlinePen = QPen(Qt.black)
        outlinePen.setWidth(2)
        graphicalScene = self.scene.grScene

        rect = graphicalScene.addRect(-100,-100, 80, 80, outlinePen, greenBrush)
        rect.setFlag(QGraphicsItem.ItemIsMovable)
        rect.setFlag(QGraphicsItem.ItemIsSelectable)
        
        text = graphicalScene.addText("TEXT HERE")
        text.setFlag(QGraphicsItem.ItemIsSelectable)
        text.setPos(-200, -300)
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0, 0.5))
        
        widget1 = QPushButton("Hello World")
        proxy1 = graphicalScene.addWidget(widget1)
        proxy1.setPos(0, -30)
        proxy1.setFlag(QGraphicsItem.ItemIsMovable)
        proxy1.setFlag(QGraphicsItem.ItemIsSelectable)
        
        widget2 = QTextEdit()
        proxy2 = graphicalScene.addWidget(widget2)
        proxy2.setFlag(QGraphicsItem.ItemIsMovable)
        proxy2.setFlag(QGraphicsItem.ItemIsSelectable)
        proxy2.setPos = (0, -60)
        
        line = graphicalScene.addLine(-200,-100,400,200,outlinePen)
        line.setFlag(QGraphicsItem.ItemIsMovable)
        line.setFlag(QGraphicsItem.ItemIsSelectable)
        
    def loadStylesheet(self, filename):
        print("STYLE LOADING: " + filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))
