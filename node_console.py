from node_graphics_console import QDMConsole
from queue import Queue

DEBUG = True
class DebugConsole:
    def __init__(self, lineCount=10):
        self.scene = None

        self.lineCount = lineCount
        self.lineQ = Queue(maxsize=lineCount)

        self.grConsole = QDMConsole(self)
        
        if DEBUG:
            for line in range(lineCount):
                self.lineQ.put("TEST{num}".format(num=line))
        
    def setScene(self, scene):
        scene.grScene.addItem(self.grConsole)
        self.scene = scene
        