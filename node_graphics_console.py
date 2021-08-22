from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from node_console_connector import ConsoleConnector

class QDMConsole(QGraphicsItem, ConsoleConnector):
    def __init__(self, console, parent=None):
        super().__init__(parent)

        self.console = console
        self.scene = console.scene

        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 15)
        self._font = QFont("Ubuntu", 10)

        self.lineCount = console.lineCount

        self.edge_size = 10.0
        self.title_height = 24
        self.textheight = 25
        self.width = 500
        self.height = self.textheight * self.lineCount + self.title_height + self.edge_size
        self._padding = 5.0

        self._pen_default = QPen(QColor("#7F000000"))
        self._pen_selected = QPen(QColor("#FFFFA637"))

        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_background = QBrush(QColor("#E3212121"))
        
        self.textList = []
        self.initContent()

        self.title = "Console"
        self.initTitle()

        self.initUI()
        
        self.updateText()
        
    def initContent(self):
        for i in range(self.console.lineCount):
            text = QGraphicsTextItem(self)
            text.setPos(self._padding, self.edge_size + self._padding + self.title_height + (i * self.textheight))
            text.setDefaultTextColor(self._title_color)
            text.setFont(self._font)
            self.textList.append(text)

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(self._padding, 0)
        self.title_item.setTextWidth(
            self.width - 2*self._padding
        )
        self.title_item.setPlainText(self.title)

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

    def updateText(self):
        pass

    def paint(self,painter,QStyleOptionGraphicsItem, widget= None):

        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0,0,self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height-self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width-self.edge_size, self.title_height-self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        textlist = list(self.console.lineQ.queue)
        for i in range(self.console.lineCount):
            self.textList[i].setPlainText(textlist[i])

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0,self.title_height,  self.width, self.height - self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(0,self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width-self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())