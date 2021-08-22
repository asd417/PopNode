from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

from node_socket import *
from node_console_connector import ConsoleConnector

class QDMGraphicsEdge(QGraphicsPathItem, ConsoleConnector):
    def __init__(self, edge, parent=None):
        super().__init__(parent)
        
        self.edge = edge
        self.console = self.edge.console
        
        self._color = QColor("#606060")
        self._color_selected = QColor("#CCCCCC")
        
        self._pen = QPen(self._color)
        self._pen.setWidth(3.0)
        
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidth(3.0)
        
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashLine)
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setZValue(-1)
        
        self.posSource = [0, 0]
        self.posDestination = [-200, -200]
        
    def setSource(self, x, y):
        self.posSource = [x, y]
    
    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter, QStlyeOptionGraphicsItem, widget=None):
        self.updatePath()
        
        if self.edge.end_socket is None:
            painter.setPen(self._pen_dragging)
        else:
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())
        
    def updatePath(self):
        # Handles drawings QPainterPath from Point A to Point B
        raise NotImplemented("This method has to be overwritten in a child class")
        
        
class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        self.setPath(path)
    
class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
    def updatePath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        
        deltax = abs(self.posSource[0] - self.posDestination[0])
        deltay = abs(self.posSource[1] - self.posDestination[1])

        if deltax < 150:
            if deltax <= 75:
                deltax = deltax * 2
            else:
                deltax = 150
        elif deltax > 250:
            deltax = 250
        deltax -= 1000/(deltay+1)
        if deltax < 0:
            deltax = 0

        path.cubicTo(
            self.posSource[0] + deltax, self.posSource[1],
            self.posDestination[0] - deltax, self.posDestination[1],
            self.posDestination[0], self.posDestination[1])
        self.setPath(path)