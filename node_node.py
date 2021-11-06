from node_graphics_node import QDMGraphicsNode, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM
from node_content_widget import QDMNodeContentWidget
from node_socket import Socket
from node_console_connector import ConsoleConnector

DEBUG = True
class Node(ConsoleConnector):
    def __init__(self, scene, title="Undefined Node"):
        self.scene = scene
        self.title = title
        self.console = scene.console

        self.initContent()
        content = self.content
        self.inputs = content.getInputs()
        self.outputs = content.getOutputs()

        self.generateSockets()
        
        self.loadGraphics()
        self.content.grNodeEdit()
        self.grNode.updateGR()

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
    
    # Override this function to set custom content
    def initContent(self):
        self.content = QDMNodeContentWidget()

    # content is a custom object that inherits QDMNodeContentWidget
    def overrideContent(self, content):
        self.content = content
        self.grNode.overrideContent(content)

    def updateConnectedEdges(self):
        for socket in self.inputSockets + self.outputSockets:
            if socket.hasEdge():
                socket.edge.updatePositions()

    def remove(self):
        if DEBUG: self.printToConsole("Removing Node" + str(self))

        # remove all connected edges
        for socket in (self.inputSockets + self.outputSockets):
            if socket.hasEdge():
                socket.edge.remove()
        # remove grNode
        self.scene.grScene.removeItem(self.grNode)
        # remove node from scene
        self.scene.removeNode(self)
        
    def generateSockets(self):
        self.inputSockets = []
        self.outputSockets = []

        if self.inputs is not None and len(self.inputs) > 0:
            counter = 0
            for item in self.inputs:
                socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_gr_type=item)
                self.inputSockets.append(socket)
                counter += 1

        if self.outputs is not None and len(self.outputs) > 0:
            counter = 0
            for item in self.outputs:
                socket = Socket(node=self, index=counter, position=RIGHT_TOP, socket_gr_type=item)
                self.outputSockets.append(socket)
                counter += 1

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
        