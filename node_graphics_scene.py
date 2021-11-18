from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

from node_console_connector import ConsoleConnector

class QDMGraphicsScene(QGraphicsScene, ConsoleConnector):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene
        self.console = self.scene.console

        # settings
        self.gridSize = 20
        self.gridSquares = 5
        self.gridPenWidth = 1

        self._color_background = QColor("#393939")

        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#242424")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(self.gridPenWidth)

        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(self.gridPenWidth)

        self.setBackgroundBrush(self._color_background)


    def setGrScene(self, width, height):
        self.setSceneRect(-width//2, -height//2, width, height)

    def drawBackground(self, painter, rect):
        gridSize = self.gridSize
        super().drawBackground(painter, rect)

        # create grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))
        
        first_left = left - (left % gridSize)
        first_top = top - (top % gridSize)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, gridSize):
            if x % (self.gridSquares * gridSize) == 0:
                lines_dark.append(QLine(x, top, x, bottom))
            else:
                lines_light.append(QLine(x, top, x, bottom))
        for y in range(first_top, bottom, gridSize):
            if y % (self.gridSquares * gridSize) == 0:
                lines_dark.append(QLine(right, y, left, y))
            else:
                lines_light.append(QLine(right, y, left, y))

        # draw the lines
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)
        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)