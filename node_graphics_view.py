from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_socket import Socket, IOTYPE_INPUT, IOTYPE_OUTPUT
from node_graphics_socket import QDMGraphicsSocket
from node_graphics_edge import QDMGraphicsEdge
from node_graphics_node import QDMGraphicsNode
from node_edge import Edge, TYPE_BEZIER
from node_console_connector import ConsoleConnector

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_NODE_DRAG = 3
EDGE_DRAG_THRESHOLD = 10

DEBUG = True

class QDMGraphicsView(QGraphicsView, ConsoleConnector):
    def __init__(self, console, grscene, parent=None):
        super().__init__(parent)
        self.grScene = grscene
        self.console = console

        self.initUI()

        self.setScene(self.grScene)
        
        self.mode = MODE_NOOP

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 5
        self.zoomStep = 1
        self.zoomRange = [0, 10]

    def initUI(self):
        # QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
        self.setRenderHints(QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        
    def mouseMoveEvent(self, event):
        if self.mode == MODE_EDGE_DRAG:
            dragEdge_grEdge = self.dragEdge.grEdge
            pos = self.mapToScene(event.pos())
            dragEdge_grEdge.setDestination(pos.x(), pos.y())
            dragEdge_grEdge.update()
        
        super().mouseMoveEvent(event)
        
    def keyPressEvent(self, event):
        self.printToConsole("Pressed: " + str(event.key()))
        if event.key() == Qt.Key_Delete:
            self.deleteSelected()
        else:
            super().keyPressEvent(event)
    
    def deleteSelected(self):
        for item in self.grScene.selectedItems():
            if isinstance(item, QDMGraphicsEdge):
                item.clearEdgeList()
            if isinstance(item, QDMGraphicsNode):
                item.node.remove()

    def mousePressEvent(self, event):
        button = event.button()
        if button == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif button == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif button == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):
        button = event.button()
        if button == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif button == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif button == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.MiddleButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):
        fakeEvent = QMouseEvent(event.type(),event.localPos(), event.screenPos(),Qt.LeftButton, event.buttons() & Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonPress(self, event):
        item = self.getItemAtClick(event)
        pos = event.pos()
        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        # for socket dragging
        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                existingEdgeList = item.socket.edgeList

                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                # prevents the Node from moving when pressing part of the socket above nodes
                return
        
        if self.mode == MODE_NODE_DRAG:
            return
        
        if self.mode == MODE_NOOP:
                if DEBUG: self.printToConsole("Dragging Node")
                widgets = self.getAllWidgetsAtPos(pos)
                for widget in widgets:
                    if DEBUG: self.printToConsole(f'{widget}')
                    if widget != item and type(widget) is QDMGraphicsEdge:
                        widget.setColor("#39E9c7")
                        self.mode = MODE_NODE_DRAG
                        return

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):

        item = self.getItemAtClick(event)

        if self.mode == MODE_EDGE_DRAG:
            # End dragging edge
            self.edgeDragEnd(item)
            return

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)
        item = self.getItemAtClick(event)

        if DEBUG:
            if isinstance(item, QDMGraphicsEdge): self.printToConsole('RMB DEBUG: ' + str(item.edge) + ' connecting sockets:' + 
                                                                      str(item.edge.start_socket) + ' <--> ' + str(item.edge.end_socket))
            if type(item) is QDMGraphicsSocket: self.printToConsole('RMB DEBUG: ' + str(item.socket) + ' has' + str(len(item.socket.edgeList)) + 'edges')

            if item is None:
                self.printToConsole('SCENE:')
                self.printToConsole('  Nodes:')
                for node in self.grScene.scene.nodes: self.printToConsole('    ' + str(node))
                self.printToConsole('  Edges:')
                for edge in self.grScene.scene.edges: self.printToConsole('    ' + str(edge))

    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        # calculate zoom factor
        zoomOutFactor = 1/self.zoomInFactor

        # calculate the zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]:
            self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]:
            self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)

    def getItemAtClick(self, event):
        """Return obj of the item clicked"""
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj
    
    def edgeDragStart(self, item):
        #item type: QDMGraphicsSocket
        if DEBUG: self.printToConsole('View::edgeDragStart ~ Start dragging edge')
        if DEBUG: self.printToConsole('View::edgeDragStart ~   assign Start Socket')
        itemSocket = item.socket
        if type(item) is QDMGraphicsSocket: 
            self.dragEdgeStartingSocket = itemSocket

            self.dragEdge = Edge(self.grScene.scene, itemSocket, None, TYPE_BEZIER)

    #TODO Fix so that edge calling uses edgeList
    def edgeDragEnd(self, item):
        self.mode = MODE_NOOP
        dragEdge = self.dragEdge
        if type(item) is not QDMGraphicsSocket:
            # edge dragged to empty space 
            dragEdge.remove()
            return

        dragEdgeStartingSocket = self.dragEdgeStartingSocket
        targetEdgeEndingSocket = item.socket
        if DEBUG: self.printToConsole('View::edgeDragEnd ~ End dragging edge')
        # check if the edge creation is valid with the two given sockets
        if self.edgeLogical(dragEdgeStartingSocket, targetEdgeEndingSocket):
            if dragEdgeStartingSocket.hasEdge() and dragEdgeStartingSocket.iotype == IOTYPE_INPUT:
                dragEdgeStartingSocket.clearEdgeList()
            elif targetEdgeEndingSocket.hasEdge() and targetEdgeEndingSocket.iotype == IOTYPE_INPUT:
                targetEdgeEndingSocket.clearEdgeList()
            if DEBUG: self.printToConsole('View::edgeDragEnd ~ Edge Logical')

            if dragEdgeStartingSocket.iotype == IOTYPE_INPUT:
                # reverse the start_socket and end_socket to fix
                # end_socket of any edge should has iotype of IOTYPE_INPUT
                self.printToConsole("Edge started on Input type socket! Reversing order...")
                dragEdge.start_socket = targetEdgeEndingSocket
                dragEdge.end_socket = dragEdgeStartingSocket
            else:
                dragEdge.start_socket = dragEdgeStartingSocket
                dragEdge.end_socket = targetEdgeEndingSocket
            dragEdge.start_socket.addEdge(dragEdge)
            dragEdge.end_socket.addEdge(dragEdge)
            dragEdge.updatePositions()
        else:
            dragEdge.remove()

    def edgeLogical(self, startingSocket, endingSocket):
        if (not startingSocket is None) and (not endingSocket is None):
            if (endingSocket is not startingSocket) and (startingSocket.iotype != endingSocket.iotype) and (startingSocket.node is not endingSocket.node):
                return True
        return False

    def deltaMouseClickRelease(self, event):
        """Returns QPointF object representing the delta from click and release"""
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        deltaMouseV = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        return (deltaMouseV.x() * deltaMouseV.x()) + (deltaMouseV.y() * deltaMouseV.y())


     # Source: https://stackoverflow.com/questions/27363267/get-all-widgets-under-cursor
    def getAllWidgetsAtPos(self, pos):
        return [w for w in self.widgets_at(pos)]
    
    def widgets_at(self, pos):
        """Return ALL widgets at `pos`

        Arguments:
            pos (QPoint): Position at which to get widgets

        """

        widgets = []
        widget_at = qApp.widgetAt(pos)

        while widget_at:
            widgets.append(widget_at)

            # Make widget invisible to further enquiries
            widget_at.setAttribute(Qt.WA_TransparentForMouseEvents)
            widget_at = qApp.widgetAt(pos)

        # Restore attribute
        for widget in widgets:
            widget.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        return widgets