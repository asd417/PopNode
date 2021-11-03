from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

from node_socket import *
from node_console_connector import ConsoleConnector

DRAW_DRAG = 0
DRAW_CONNECTED = 1

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
        
        self.drawmode = DRAW_CONNECTED # default is DRAW_CONNECTED
        
    def setSource(self, x, y):
        self.posSource = [x, y]
    
    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter, QStlyeOptionGraphicsItem, widget=None):
        self.updatePath()
        
        if self.edge.end_socket is None: #drag mode edge
            self.drawmode = DRAW_DRAG
            painter.setPen(self._pen_dragging)
        else:
            self.drawmode = DRAW_CONNECTED
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
        posSource = self.posSource
        posDestination = self.posDestination
        if self.drawmode == DRAW_DRAG:
            if self.edge.start_socket.iotype == 0:
                #reverse posSource and posDestination
                self.drawGeneric(posDestination, posSource)
            else:
                self.drawGeneric(posSource, posDestination)
        elif self.drawmode == DRAW_CONNECTED:
            self.drawGeneric(self.posSource, posDestination)
        
        else:
            raise NotImplemented("EDGE DRAWMODE UNKNOWN!!!(not DRAW_DRAG or DRAW_CONNECTED)")
    
    def drawGeneric(self, startpos, endpos):
        path = QPainterPath(QPointF(startpos[0], startpos[1]))
        
        deltax = abs(startpos[0] - endpos[0])
        deltay = abs(startpos[1] - endpos[1])

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
            startpos[0] + deltax, startpos[1],
            endpos[0] - deltax, endpos[1],
            endpos[0], endpos[1])
        self.setPath(path)