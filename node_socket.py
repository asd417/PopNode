from node_graphics_socket import QDMGraphicsSocket
from node_console_connector import ConsoleConnector


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4
IOTYPE_INPUT = 0
IOTYPE_OUTPUT = 1

class Socket(ConsoleConnector):
    def __init__(self, node, index=0, position=LEFT_TOP, socket_type=0):
        self.node = node
        self.scene = self.node.scene
        self.console = self.scene.console
        self.index = index
        self.position = position
        self.socket_type = socket_type
        if position == 1 or position == 2:
            self.iotype = IOTYPE_INPUT
        else:
            self.iotype = IOTYPE_OUTPUT

        self.grSocket = QDMGraphicsSocket(self, socket_type)
        
        self.grSocket.setPos(*self.calculateSocketPosition(index, position))
        
        self.edge = None
        
    def __str__(self):
        return "<Socket %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
        
    def setConnectedEdge(self, edge=None):
        self.edge = edge
        
    def getSocketPosition(self):
        x, y = self.calculateSocketPosition(self.index, self.position)
        return [x, y]
    
    def hasEdge(self):
        return self.edge is not None
    
    def calculateSocketPosition(self, index, position):
        N = self.node
        NgrN = N.grNode
        padding = N.grNode._padding
        edgeSize = N.grNode.edge_size
        socketSpacing = N.socketSpacing
        if position in (LEFT_TOP, LEFT_BOTTOM):
            x = 0
        else:
            x = N.grNode.width

        if position in (LEFT_TOP, RIGHT_TOP):
            y = NgrN.title_height + edgeSize + padding + index * socketSpacing
        else:
            y = NgrN.height - edgeSize - padding - index * socketSpacing

        return x, y