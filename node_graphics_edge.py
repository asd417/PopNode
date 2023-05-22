from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

from node_socket import *

DRAW_DRAG = 0
DRAW_CONNECTED = 1
DEBUG = False

class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)
        
        self.edge = edge
        self.console = self.edge.console
        
        self._color = QColor("#606060")
        self._color_selected = QColor("#CCCCCC")
        self._color_hovered = QColor("#FF37a6FF")
        
        self._pen = QPen(self._color)
        self._pen.setWidthF(3.0)
        
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(3.0)
        
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashLine)
        
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(5.0)
        
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setZValue(-1)
        
        self.posSource = [0, 0]
        self.posDestination = [-200, -200]
        
        self.drawmode = DRAW_CONNECTED # default is DRAW_CONNECTED
        
        self.hovered = False
        
    def setSource(self, x, y):
        self.posSource = [x, y]
    
    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter, QStlyeOptionGraphicsItem, widget=None):
        self.updatePath()
        
        painter.setBrush(Qt.NoBrush)
        if self.hovered and self.edge.end_socket is not None:
            painter.setPen(self._pen_hovered)
            painter.drawPath(self.path())
        
        if self.edge.end_socket is None: #drag mode edge
            self.drawmode = DRAW_DRAG
            painter.setPen(self._pen_dragging)
        else:
            self.drawmode = DRAW_CONNECTED
            painter.setPen(self._pen if not self.isSelected() else self._pen_selected)
        
        painter.drawPath(self.path())
        
    def updatePath(self):
        # Handles drawings QPainterPath from Point A to Point B
        raise NotImplemented("This method has to be overwritten in a child class")
        
    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        self.hovered = False
        self.update()
        
    def shape(self):
        #raise NotImplementedError("Complete this with https://www.youtube.com/watch?v=2GOey5PnhRI")
        posSource = self.posSource
        posDestination = self.posDestination
        if self.drawmode == DRAW_DRAG:
            if self.edge.start_socket.iotype == 0:
                #reverse posSource and posDestination
                return self.calcPath(posDestination, posSource)
            else:
                return self.calcPath(posSource, posDestination)
        elif self.drawmode == DRAW_CONNECTED:
            return self.calcPath(self.posSource, posDestination)
        else:
            raise NotImplementedError("EDGE DRAWMODE UNKNOWN!!!(not DRAW_DRAG or DRAW_CONNECTED)")
            
    def boundingRect(self):
        if self.edge.start_socket is not None:
            return self.shape().boundingRect()
        else:
            return QRectF(0,0,1,1)
        
    def updatePath(self):
        path = self.shape()
        self.setPath(path)
    
    def calcPath(self, startpos, endpos):
        pass
        
    def setColor(self, color):
        self._pen = QPen(QColor(color))
        self.update()
        
class QDMGraphicsEdgeDirect(QDMGraphicsEdge):
        
    def calcPath(self, startpos, endpos):
        path = QPainterPath(QPointF(startpos[0], startpos[1]))
        path.lineTo(endpos[0], endpos[1])
        return path
    
class QDMGraphicsEdgeBezier(QDMGraphicsEdge):
        
    def calcPath(self, startpos, endpos):
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
        return path