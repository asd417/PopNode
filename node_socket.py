from node_console_connector import ConsoleConnector


LEFT_TOP = 1

IOTYPE_INPUT = 0
IOTYPE_OUTPUT = 1

class Socket(ConsoleConnector):
    def __init__(self, node, index=0, position=LEFT_TOP, socket_gr_type=0):
        self.node = node
        self.scene = self.node.scene
        self.console = self.scene.console
        self.index = index
        self.position = position
        self.socket_gr_type = socket_gr_type
        if position == 1 or position == 2:
            self.iotype = IOTYPE_INPUT
        else:
            self.iotype = IOTYPE_OUTPUT
        
        self.edge = None
        
    def __str__(self):
        return "<Socket %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
        
    def setConnectedEdge(self, edge=None):
        self.edge = edge
    
    def hasEdge(self):
        return self.edge is not None
    
    def getSocketPosition(self):
        x, y = self.node.grNode.calculateSocketPosition(self.index, self.position)
        return [x, y]