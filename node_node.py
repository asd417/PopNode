from node_graphics_node import QDMGraphicsNode, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM
from node_content_widget import QDMNodeContentWidget
from node_socket import Socket, IOTYPE_INPUT, IOTYPE_OUTPUT

DEBUG = True
class Node:
    def __init__(self, scene, title="Undefined Node", console=None):
        self.scene = scene
        self.title = title
        if console is None:
            self.console = scene.console
        else:
            self.console = console

        self.initContent()
        content = self.content
        self.inputs = content.getInputSocketTypes()
        self.outputs = content.getOutputSocketTypes()

        self.generateSockets()

        self.loadGraphics()

        if self.inputs is not None:
            self.inputValues = [None] * self.content.slotCount
        else:
            self.inputValues = None

        if self.outputs is not None:
            self.outputValues = [None] * self.content.slotCount
        else:
            self.outputValues = None

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    # Override this function to set custom content
    def initContent(self):
        self.content = QDMNodeContentWidget(self)

    def updateConnectedEdges(self):
        for socket in self.inputSockets + self.outputSockets:
            if DEBUG: self.console.log(f"checking if {socket} has Edge")
            if socket.hasEdge():
                
                socket.updateEdgePositions()
                
    def updateConnectedNodes(self):
        for socket in self.outputSockets:
            if socket.hasEdge():
                for edge in socket.edgeList:
                    if edge.end_socket.iotype == IOTYPE_INPUT:
                        edge.end_socket.node.updateThisNode()
                
    def updateInputValues(self):
        if DEBUG: self.console.log(f"updateInputValues called on {self}")
        if len(self.inputSockets) != 0:
            i = 0
            for socket in self.inputSockets:
                self.inputValues[i] = socket.loadValue()
                i += 1
    
    def updateThisNode(self):
        self.updateInputValues()
                
        self.onNodeUpdate()
                
        self.updateConnectedNodes()

    def remove(self):
        if DEBUG: self.console.log(f"Removing Node: {self}")

        # remove all connected edges
        for socket in (self.inputSockets + self.outputSockets):
            if socket.hasEdge():
                socket.clearEdgeList()
        # remove grNode
        self.scene.grScene.removeItem(self.grNode)
        # remove node from scene
        self.scene.removeNode(self)
        
    def generateSockets(self):
        self.inputSockets = []
        self.outputSockets = []

        if self.inputs is not None and len(self.inputs) > 0:
            
            # A socket is defined by Tuple as explained in node_content_widget.py therefore a variable name definitionTuple is used here
            for definitionTuple in self.inputs:
                Sindex = definitionTuple[0]
                Stype = definitionTuple[1]
                socket = Socket(node=self, index=Sindex, iotype=0, socket_gr_type=Stype)
                self.inputSockets.append(socket)

        if self.outputs is not None and len(self.outputs) > 0:
            for definitionTuple in self.outputs:
                Sindex = definitionTuple[0]
                Stype = definitionTuple[1]
                socket = Socket(node=self, index=Sindex, iotype=1, socket_gr_type=Stype)
                self.outputSockets.append(socket)

    def loadGraphics(self):
        self.grNode = QDMGraphicsNode(self)
        
        scene = self.scene
        scene.addNode(self)
        scene.grScene.addItem(self.grNode)

    @property
    def pos(self):
        return self.grNode.pos()

    def setPos(self, x, y):
        self.grNode.setPos(x, y)
        
    def onNodeUpdate(self):
        pass
        