from node_graphics_console import QDMConsole
from queue import Queue
class DebugConsole:
    def __init__(self, lineCount=10):
        self.scene = None

        self.lineCount = lineCount
        self.lineQ = Queue(maxsize=lineCount)

        self.grConsole = QDMConsole(self)
        
        for line in range(lineCount):
            self.lineQ.put("TEST{num}".format(num=line))
        
    def setScene(self, scene):
        self.scene = scene
        self.scene.grScene.addItem(self.grConsole)