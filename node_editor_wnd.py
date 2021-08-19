import PyQt5.QtWidgets as qtw
from node_graphics_scene import QDMGraphicsScene
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc

class NodeEditorWnd(qtw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)

        self.layout = qtw.QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        # create Graphics Scene
        self.grScene = QDMGraphicsScene()


        # create Graphics View
        self.view = qtw.QGraphicsView(self)
        self.view.setScene(self.grScene)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")
        self.show()

        self.addDebugContent()

    def addDebugContent(self):
        greenBrush = qtg.QBrush(qtc.Qt.green)
        outlinePen = qtg.QPen(qtc.Qt.black)
        outlinePen.setWidth(2)

        rect = self.grScene.addRect(-100,-100, 80, 80, outlinePen, greenBrush)
        rect.setFlag(qtw.QGraphicsItem.ItemIsMovable)
        
        text = self.grScene.addText("TEXT HERE")
        text.setFlag(qtw.QGraphicsItem.ItemIsSelectable)
        text.setFlag(qtw.QGraphicsItem.ItemIsMovable)

