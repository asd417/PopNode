from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from node_console_connector import ConsoleConnector
from node_graphics_slot import Slot

class QDMNodeContentWidget(QWidget, ConsoleConnector):
    def __init__(self, node, parent=None):
        self.console = node.console
        self.node = node
        self.widgetSlots = []
        super().__init__(parent)

        self.initUILayout()
        self.initWidgetSlots()
        
        # Example values
        # A Socket needs both index and type info. 
        # Therefore a Tuple is used to define in the simplest way.
        # example: (0,1) position: 0, type 1
        self.inputSocketTypes = [(0,1),(2,2)]
        self.outputSocketTypes = [(1,1),(2,0)]
        self.verifySlotCount()

        self.generateSlots(self.slotCount)
        self.initUI()
        
        self.width = None
        self.height = None
        self.edge_size = None
        self.title_height = None
        self.title_height = None
        self.padding = None
        
    # Override this to set the widgetslot Count
    def initWidgetSlots(self):
        self.slotCount = 3
        
    # Override this function to make changes to the grNode
    def grNodeEdit(self, grNode):
        pass
        
    # Example UI Initialization
    # Override this function to create custom node content
    # Each Slot represents a potential output or input slot
    # Sockets will be placed according to its .index property and its .iotype property
    def initUI(self):
        self.addWidgetToWidgetSlot(0, QLabel("Slot 1 Text"))

        self.addWidgetToWidgetSlot(1, QTextEdit("foo"))

        self.addWidgetToWidgetSlot(2, QLabel("Slot 3 Text"))
        
    def addWidgetToWidgetSlot(self, index, Qwidget):
        self.widgetSlots[index].layout().addWidget(Qwidget)
        
    def generateSlots(self, size):
        for i in range(size):
            slot = self.createDefaultSlotWidget(0)
            self.widgetSlots.append(slot)
        
    def createDefaultSlotWidget(self, index):
        slot = Slot(index)
        slotLayout = QVBoxLayout()
        slot.setLayout(slotLayout)
        self.layout.addWidget(slot)

        return slot
    
    def verifySlotCount(self):
        inputMax = self.getMaxSlotIndex(self.inputSocketTypes)
        outputMax = self.getMaxSlotIndex(self.outputSocketTypes)
        
        slotCount = self.slotCount
        
        if not slotCount >= inputMax and slotCount >= outputMax:
            raise Exception("Not Enough Slots for Sockets")
        
    def getMaxSlotIndex(self, socketTupleList):
        slotMaxIndex = 0
        for socketTuple in socketTupleList:
            if socketTuple[0] > slotMaxIndex:
                slotMaxIndex = socketTuple[0]
        return slotMaxIndex
        
    def initUILayout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)
        self.layout = layout
        
    def getInputSocketTypes(self):
        return self.inputSocketTypes
    
    def getOutputSocketTypes(self):
        return self.outputSocketTypes