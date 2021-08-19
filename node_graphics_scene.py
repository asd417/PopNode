import PyQt5.QtWidgets as pyqt
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import math

class QDMGraphicsScene(pyqt.QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)

        # settings
        self.gridSize = 20
        self.gridSquares = 5
        self.gridPenWidth = 1

        self._color_background = qtg.QColor("#393939")

        self._color_light = qtg.QColor("#2f2f2f")
        self._color_dark = qtg.QColor("#242424")

        self._pen_light = qtg.QPen(self._color_light)
        self._pen_light.setWidth(self.gridPenWidth)

        self._pen_dark = qtg.QPen(self._color_dark)
        self._pen_dark.setWidth(self.gridPenWidth)

        self.scene_width, self.scene_height = 64000, 64000
        self.setSceneRect(-self.scene_width//2, -self.scene_height//2, self.scene_width, self.scene_height)

        self.setBackgroundBrush(self._color_background)


    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # create grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))
        
        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.gridSize):
            if x % (self.gridSquares * self.gridSize) == 0:
                lines_dark.append(qtc.QLine(x, top, x, bottom))
            else:
                lines_light.append(qtc.QLine(x, top, x, bottom))
        for y in range(first_top, bottom, self.gridSize):
            if y % (self.gridSquares * self.gridSize) == 0:
                lines_dark.append(qtc.QLine(right, y, left, y))
            else:
                lines_light.append(qtc.QLine(right, y, left, y))

        # draw the lines
        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)
        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)