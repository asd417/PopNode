
LEFT_TOP = 1

IOTYPE_INPUT = 0
IOTYPE_OUTPUT = 1

DEBUG = False
class Socket:
    def __init__(self, node, index=0, iotype=0, socket_gr_type=0):
        self.node = node
        self.scene = self.node.scene
        self.console = self.scene.console
        self.index = index
        self.socket_gr_type = socket_gr_type

        self.iotype = iotype

        self.previousEdgeList = []
        self.edgeList = []
        self.grSocket = None
        
        self.value = None
        
    def __str__(self):
        return "<Socket %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
        
    def addEdge(self, edge):
        if self.iotype == IOTYPE_INPUT and len(self.edgeList) == 1:
            if DEBUG: self.console.log("Can not add more than one edge to socket with iotype 'IOTYPE_INPUT'")
            edge.remove()
        else:
            self.edgeList.append(edge)
        
        if not self.compareEdgeList():
            # If previously recorded edgelist is not the same as the current edgelist, it means there was a change in edge connections, triggering the socket to update its node
            if self.iotype == IOTYPE_INPUT:
                self.node.updateThisNode()
            self.previousEdge = self.edgeList
    
    def compareEdgeList(self):
        # returns True if both lists are the same
        prevList = self.previousEdgeList
        List = self.edgeList
        if len(prevList) != len(List):
            return False
        else:
            prevList.sort()
            List.sort()
            return prevList == List
    
    def clearEdgeList(self):
        for edge in self.edgeList:
            edge.remove()
            
    def removeEdge(self, edge):
        edge.remove()

    def hasEdge(self, edge=None):
        if edge is not None:
            # returns True if there is the specified edge in the edgeList
            return (edge in self.edgeList)
        else:
            # returns True if there is any edge in the edgeList
            return len(self.edgeList) != 0
    
    def getSocketPosition(self):
        x, y = self.node.grNode.calculateSocketPosition(self)
        return [x, y]
    
    def updateEdgePositions(self):
        for edge in self.edgeList:
            edge.updatePositions()
    
    def loadValue(self):
        if DEBUG: self.printToConsole(f"Socket in {self.node} was ordered to loadValue() ")
        if self.iotype == IOTYPE_INPUT:
            if len(self.edgeList) != 0:
                target_socket = self.edgeList[0].start_socket

                # Verify that the start_socket of the edge is in fact output socket
                if target_socket.iotype != IOTYPE_OUTPUT:
                    raise ValueError("start_socket of connected edge is not iotype=IOTYPE_OUTPUT!")
                else:
                    if DEBUG: self.console.log(f"targeting socket from socket in {self.node} to socket in {target_socket.node}")
                    return target_socket.loadValue()

        elif self.iotype == IOTYPE_OUTPUT:
            return self.node.outputValues[self.index]
        else:
            raise NotImplementedError("iotype of socket is neither 0 or 1. Possibly edited")