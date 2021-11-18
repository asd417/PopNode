class ConsoleConnector:
    def __init__(self):
        pass
    def printToConsole(self,text):
        console = self.console
        if console is not None:
            lineQ = console.lineQ
            if lineQ.full():
                lineQ.get()
            lineQ.put(text)