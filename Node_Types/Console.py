import sys
sys.path.append("..")

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_node import Node
from node_content_widget import QDMNodeContentWidget

# https://www.pythonguis.com/tutorials/pyqt-basic-widgets/

#Node Type
class NT_Console(Node):
    _instances = []
    def __init__(self, scene):
        super().__init__(scene, title="Console")
        self.__class__._instances.append(self)

    def __str__(self):
        return "<Console Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])
    
    def __del__(self):
        self.__class__._instances.remove(self)

    #Called from within the Node for loading custom content widget
    def initContent(self):
        self.content = NTW_Console(self)

    def update_console(self):
        log = self.console.get_log()
        if self.content is not None:
            console_view = self.content.consoleBrowser
            console_view.setText(log)
            scroll_bar = console_view.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.maximum())
            
    def clear_console(self):
        self.console.clear_log()
    

    @classmethod
    def update_all(cls):
        for instance in cls._instances:
            instance.update_console()    

#Node Type Widget
class NTW_Console(QDMNodeContentWidget):
    def __init__(self, node):
        super().__init__(node)
        self.inputSocketTypes = None
        self.outputSocketTypes = None
        self.height = 500
        self.width = 400
        
    def initUI(self):
        self.consoleBrowser = QTextBrowser()
        self.add_widget_to_widget_slot(0, self.consoleBrowser)
        self.button_clear = QPushButton()
        self.button_clear.clicked.connect(self.node.clear_console)
        
        self.button_export = QPushButton()
        horizontal_slot = QWidget()
        horizontal_slot.setLayout(QHBoxLayout())
        horizontal_slot.layout().addWidget(self.button_clear)
        horizontal_slot.layout().addWidget(self.button_export)
        
        self.add_widget_to_widget_slot(1, horizontal_slot)
        
    def initWidgetSlots(self):
        self.slotCount = 2
