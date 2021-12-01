from node_graphics_edge import *

TYPE_DIRECT = 1
TYPE_BEZIER = 2

IOTYPE_INPUT = 0
IOTYPE_OUTPUT = 1

DEBUG = True
class Edge:
    def __init__(self, scene, start_socket, end_socket, type=1):
        self.scene = scene
        self.console = self.scene.console
        
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.grEdge = QDMGraphicsEdgeDirect(self) if type == TYPE_DIRECT else QDMGraphicsEdgeBezier(self)

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self
        
        self.updatePositions()
        
        self.scene.grScene.addItem(self.grEdge)
        self.scene.addEdge(self)
        
    def __str__(self):
        return "<Edge %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
    
    def __lt__(self, other):
        return id(self) < id(other)
        
    def updatePositions(self):
        
        if self.start_socket is self.end_socket:
            self.remove()
        else:
            source_pos = self.start_socket.getSocketPosition()
            source_pos[0] += self.start_socket.node.grNode.pos().x()
            source_pos[1] += self.start_socket.node.grNode.pos().y()
            self.grEdge.setSource(*source_pos)
            if self.end_socket is not None:
                end_pos = self.end_socket.getSocketPosition()
                end_pos[0] += self.end_socket.node.grNode.pos().x()
                end_pos[1] += self.end_socket.node.grNode.pos().y()
                self.grEdge.setDestination(*end_pos)
            else:
                self.grEdge.setDestination(*source_pos)
            self.grEdge.update()
            
        
    def remove_from_socket(self):
        if DEBUG: self.printToConsole("Edge::remove_from_socket()")
        try:
            if self.start_socket is not None:
                self.start_socket.edgeList.remove(self)
            if self.end_socket is not None:
                self.end_socket.edgeList.remove(self)
        except:
            if DEBUG: self.printToConsole(f"Attempted to remove edge {self} but this edge is already removed")
        
    def remove(self):
        self.remove_from_socket()
        self.scene.grScene.removeItem(self.grEdge)
        self.scene.removeEdge(self)