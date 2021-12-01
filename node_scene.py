from node_graphics_scene import QDMGraphicsScene
DEBUG = True
class Scene:
    def __init__(self, console):
        self.nodes = []
        self.edges = []
        self.console = console

        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()

    def initUI(self):
        self.grScene = QDMGraphicsScene(self, self.console)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        try:
            self.nodes.remove(node)
        except:
            if DEBUG: self.console.log('Scene::removeNode ~ Node Already Removed')

    def removeEdge(self, edge):
        try:
            self.edges.remove(edge)
        except:
            if DEBUG: self.console.log('Scene::removeEdge ~ Edge Already Removed')