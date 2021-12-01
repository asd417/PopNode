from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

DEBUG = False

class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, parent):
        self.socket = socket
        #parent
        super().__init__(parent)
        self.console = self.socket.console

        self.radius = 6.0
        self.outline_width = 1.0
        self._colors = [
            QColor("#FFFF7700"),
            QColor("#FF52e220"),
            QColor("#FF0056a6"),
            QColor("#FFa86db1"),
            QColor("#FFb54747"),
            QColor("#FFdbe220"),
        ]

        self._color_background = self._colors[socket.socket_gr_type]
        self._color_outline = QColor("#FF000000")

        self._pen = QPen(self._color_outline)
        self._debugpen = QPen(QColor("#FF00EE"))
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        r = self.radius
        painter.setBrush(self._brush)
        if DEBUG and len(self.socket.edgeList) != 0:
            painter.setPen(self._debugpen)
        else:
            painter.setPen(self._pen)
        painter.drawEllipse(-r, -r, 2*r, 2*r)

    def boundingRect(self):
        olw = self.outline_width
        r = self.radius
        return QRectF(
            -r - olw,
            -r - olw,
            2*(r + olw),
            2*(r + olw)
        )