class ConsoleConnector:
    def __init__(self):
        pass
    def printToConsole(self,text):
        if self.console is not None:
            if self.console.lineQ.full():
                self.console.lineQ.get()
            self.console.lineQ.put(text)