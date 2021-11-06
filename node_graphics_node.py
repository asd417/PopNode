from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_console_connector import ConsoleConnector
from node_graphics_socket import QDMGraphicsSocket


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4
class QDMGraphicsNode(QGraphicsItem, ConsoleConnector):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.console = self.node.console
        self.content = self.node.content

        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 15)

        self.width = 180
        self.height = 240
        self.edge_size = 10.0
        self.title_height = 24
        self._padding = 5.0

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))
        
        self.socketSpacing = 25
        self.grContent = None
        
        self.initSockets(self.node.inputSockets)
        self.initSockets(self.node.outputSockets)

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def calculateSocketPosition(self, index, position):
        padding = self._padding
        edgeSize = self.edge_size
        socketSpacing = self.socketSpacing
        if position in (LEFT_TOP, LEFT_BOTTOM):
            x = 0
        else:
            x = self.width

        if position in (LEFT_TOP, RIGHT_TOP):
            y = self.title_height + edgeSize + padding + index * socketSpacing
        else:
            y = self.height - edgeSize - padding - index * socketSpacing

        return x, y

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        for item in self.scene().scene.grScene.selectedItems():
            if isinstance(item, QDMGraphicsNode):
                item.node.updateConnectedEdges()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(
            self.width - 2*self._padding
        )

    def initContent(self):
        edgeSize = self.edge_size
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(edgeSize, self.title_height + edgeSize,
                                self.width - 2*edgeSize,
                                self.height - 2*edgeSize - self.title_height
                                )
        self.grContent.setWidget(self.content)

    def initSockets(self, socketlist):
        for socket in socketlist:
            self.grSocket = QDMGraphicsSocket(socket, self, socket.socket_gr_type)
            self.grSocket.setPos(*self.calculateSocketPosition(socket.index, socket.position))
    
    def setHeight(self, num):
        self.height = num
        
    def setWidth(self, num):
        self.width = num

    def overrideContent(self, content):
        self.content = content
        self.updateGR()
        
    def updateGR(self):
        # Clears original QGraphicsProxyWidget
        if self.grContent is not None:
            self.grContent.setParent(None)
            del self.grContent
            
        # init title
        self.initTitle()
        self.title = self.node.title

        # init sockets
        self.initSockets(self.node.inputSockets)
        self.initSockets(self.node.outputSockets)
        
        # init content
        self.initContent()

        self.initUI()

    def paint(self,painter,QStyleOptionGraphicsItem, widget= None):
        height = self.height
        width = self.width
        title_height = self.title_height
        edge_size = self.edge_size

        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0,0,width, title_height, edge_size, edge_size)
        path_title.addRect(0, title_height-edge_size, edge_size, edge_size)
        path_title.addRect(width-edge_size, title_height-edge_size, edge_size, edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0,title_height, width, height - title_height, edge_size, edge_size)
        path_content.addRect(0,title_height, edge_size, edge_size)
        path_content.addRect(width-edge_size, title_height, edge_size, edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, width, height, edge_size, edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())