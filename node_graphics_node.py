from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_graphics_socket import QDMGraphicsSocket


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

IOTYPE_INPUT = 0
IOTYPE_OUTPUT = 1
class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.console = self.node.console
        self.content = self.node.content

        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 15)

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))
        
        # Override if specified
        if self.content.width is not None:
            self.width = self.content.width
        else:
            self.width = 180
        if self.content.height is not None:
            self.height = self.content.height
        else:
            self.height = 240
        if self.content.edge_size is not None:
            self.edge_size = self.content.edge_size
        else:
            self.edge_size = 10.0
        if self.content.title_height is not None:
            self.title_height = self.content.title_height
        else:
            self.title_height = 24
        if self.content.padding is not None:
            self._padding = self.content.padding
        else:
            self._padding = 5.0
        

        self.socketSpacing = 25
        self.grContent = None
        
        self.widgetSlots = self.node.content.widgetSlots

        # init title
        self.initTitle()
        self.title = self.node.title

        self.initContent()
        self.initUI()
        
        # init sockets
        self.initSockets(self.node.inputSockets)
        self.initSockets(self.node.outputSockets)
        
        self.setAcceptDrops(True)

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

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
        title_item = QGraphicsTextItem(self)
        title_item.setDefaultTextColor(self._title_color)
        title_item.setFont(self._title_font)
        title_item.setPos(self._padding, 0)
        title_item.setTextWidth(
            self.width - 2*self._padding
        )
        self.title_item = title_item

    def initContent(self):
        edgeSize = self.edge_size
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(int(edgeSize), int(self.title_height + edgeSize),
                                int(self.width - 2*edgeSize),
                                int(self.height - 2*edgeSize - self.title_height)
                                )
        self.grContent.setWidget(self.content)

    def initSockets(self, socketlist):
        for socket in socketlist:
            grSocket = QDMGraphicsSocket(socket, self)
            socket.grSocket = grSocket
            grSocket.setPos(*self.calculateSocketPosition(socket))
                
    def calculateSocketPosition(self, socket):
        iotype = socket.iotype
        index = socket.index
        padding = self._padding
        edgeSize = self.edge_size
        socketSlot = self.widgetSlots[index]
        
        mappedPoint = socketSlot.mapToParent(socketSlot.rect().center())
        y = mappedPoint.y() + self.title_height + edgeSize

        if iotype == 0: # if iotype == input
            x = 0
        else:
            x = self.width
        return x, y

    
    def setHeight(self, num):
        self.height = num
        
    def setWidth(self, num):
        self.width = num

    def paint(self, painter,QStyleOptionGraphicsItem, widget= None):
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