import sys
from Node_Types import Console

class ConsoleLog:
    def __init__(self):
        self.logText = ""
        self.original_stdout = sys.stdout
        
    def log(self, text):
        self.logText += f"{text}\n"
        Console.NT_Console.update_all()
        
    def clear_log(self, text):
        self.logText = ""
        Console.NT_Console.update_all()
        
    def get_log(self):
        return self.logText
    
    def export_log_as_file(self):
        with open('filename.txt', 'w') as f:
            sys.stdout = f # Change the standard output to the file we created.
            print(self.logText)
            sys.stdout = self.original_stdout