from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget
from node_socket import Socket, LEFT_TOP, LEFT_BOTTOM, RIGHT_TOP, RIGHT_BOTTOM
from node_console_connector import ConsoleConnector


class Node(ConsoleConnector):
    def __init__(self, scene, title="Undefined Node", inputs=[], outputs=[]):
        self.scene = scene
        self.title = title
        self.console = scene.console

        self.content = QDMNodeContentWidget()

        self.grNode = QDMGraphicsNode(self)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)
        self.socketSpacing = 25

        # self.grNode.title = "fdadfsad"

        self.inputs = []
        self.outputs = []
        counter = 0

        for item in inputs:
            socket = Socket(node=self, index=counter, position=LEFT_BOTTOM, socket_type=item)
            self.inputs.append(socket)
            counter += 1

        counter = 0
        for item in outputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP, socket_type=item)
            self.outputs.append(socket)
            counter += 1
            
    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

    @property
    def pos(self):
        return self.grNode.pos()

    def setPos(self, x, y):
        self.grNode.setPos(x, y)
        