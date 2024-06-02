from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *

class Edge:
    
    def __init__(self, start: QPoint3DF, end: QPoint3DF):
        self.start = start
        self.end = end
    
    
    def getStart(self):
        return self.start
    
    
    def getEnd(self):
        return self.end
    
    
    def changeOrientation(self):
        return Edge(self.end, self.start)
    
    
    def __eq__(self, other):
        return (self.start == other.start) and (self.end == other.end)
        
    
    
