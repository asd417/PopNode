from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import math

class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, console, parent=None):
        super().__init__(parent)

        self.scene = scene
        self.console = console
        # settings
        self.gridSize = 20
        self.gridSquares = 5
        self.gridPenWidth = 1

        self._color_background = QColor("#333333")

        self._color_light = QColor("#3E3E3E")
        self._color_dark = QColor("#2E2E2E")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(self.gridPenWidth)

        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(self.gridPenWidth)

        self.setBackgroundBrush(self._color_background)
    
    def __str__(self):
        return "QDMGraphicsScene"

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
        lines_smallgrid, lines_lggrid = [], []
        for x in range(first_left, right, gridSize):
            if x % (self.gridSquares * gridSize) == 0:
                lines_lggrid.append(QLine(x, top, x, bottom))
            else:
                lines_smallgrid.append(QLine(x, top, x, bottom))
        for y in range(first_top, bottom, gridSize):
            if y % (self.gridSquares * gridSize) == 0:
                lines_lggrid.append(QLine(right, y, left, y))
            else:
                lines_smallgrid.append(QLine(right, y, left, y))

        # draw the lines

        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_smallgrid)
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_lggrid)
