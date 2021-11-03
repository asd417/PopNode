from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_graphics_socket import QDMGraphicsSocket
from node_graphics_edge import QDMGraphicsEdge
from node_graphics_node import QDMGraphicsNode
from node_edge import Edge, TYPE_BEZIER
from node_console_connector import ConsoleConnector

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
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
                item.edge.remove()
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

        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        # for socket dragging
        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                # prevents the Node from moving when pressing part of the socket above nodes
                return

        if self.mode == MODE_EDGE_DRAG:
            if self.edgeDragEnd(item):
                # end dragging since item was pressed but mode was dragging
                return

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):

        item = self.getItemAtClick(event)

        magSQdeltaMV = self.deltaMouseClickRelease(event)

        if self.mode == MODE_EDGE_DRAG:
            # End draggin edge
            # Magnitude SQuared of delta mouse vector
            if magSQdeltaMV > EDGE_DRAG_THRESHOLD*EDGE_DRAG_THRESHOLD:
                if self.edgeDragEnd(item):
                    # Mouse Not Moved Enough
                    return

        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        super().mousePressEvent(event)
        item = self.getItemAtClick(event)

        if DEBUG:
            if isinstance(item, QDMGraphicsEdge): self.printToConsole('RMB DEBUG: ' + str(item.edge) + ' connecting sockets:' + 
                                                                      str(item.edge.start_socket) + ' <--> ' + str(item.edge.end_socket))
            if type(item) is QDMGraphicsSocket: self.printToConsole('RMB DEBUG: ' + str(item.socket) + ' has edge: ' + str(item.socket.edge))

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
        if DEBUG: self.printToConsole('View::edgeDragStart ~ Start dragging edge')
        if DEBUG: self.printToConsole('View::edgeDragStart ~   assign Start Socket')
        self.last_start_socket = item.socket
        self.previousEdge = item.socket.edge
        self.dragEdge = Edge(self.grScene.scene, item.socket, None, TYPE_BEZIER)

    def edgeDragEnd(self, item):
        """ Return true to skip rest of the code"""
        dragEdge = self.dragEdge
        prevEdge = self.previousEdge
        last_start_socket = self.last_start_socket
        self.mode = MODE_NOOP
        if DEBUG: self.printToConsole('View::edgeDragEnd ~ End dragging edge')
        if self.edgeLogical(item):
            #assign end socket
            if item.socket.hasEdge() and item.socket.edge is not dragEdge:
                item.socket.edge.remove()
            
            if prevEdge is not None: prevEdge.remove()
            if last_start_socket.iotype == 0: #if last_start_socket is input type
                # reverse the start_socket and end_socket to fix
                self.printToConsole("Edge started on Input type socket! Reversing order...")
                dragEdge.start_socket = item.socket
                dragEdge.end_socket = last_start_socket
            else:
                dragEdge.start_socket = last_start_socket
                dragEdge.end_socket = item.socket
            dragEdge.start_socket.setConnectedEdge(dragEdge)
            dragEdge.end_socket.setConnectedEdge(dragEdge)
            dragEdge.updatePositions()
            return True
        
        dragEdge.remove()
        dragEdge = None
        if prevEdge is not None:
            prevEdge.start_socket.edge = prevEdge

        return False
    
    def edgeLogical(self, item):
        lastStartSocket = self.last_start_socket
        if type(item) is QDMGraphicsSocket: 
            itemSocket = item.socket
            if itemSocket is not lastStartSocket:
                if lastStartSocket.iotype != itemSocket.iotype:
                    if lastStartSocket.node is not itemSocket.node:
                        return True
        return False

    def deltaMouseClickRelease(self, event):
        """Returns QPointF object representing the delta from click and release"""
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        deltaMouseV = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        return (deltaMouseV.x() * deltaMouseV.x()) + (deltaMouseV.y() * deltaMouseV.y())