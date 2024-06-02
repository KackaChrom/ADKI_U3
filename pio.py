from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QFileDialog, QWidget
from qpoint3df import *

class pio(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dia = QFileDialog(self)
        self.dia.setNameFilter("Textové soubory (*.txt)")

    def loadData(self, w, h):
        # Load data
        points = []
        if self.dia.exec():
            fileNames = self.dia.selectedFiles()
            with open(fileNames[0], 'r') as txtfile:  # Open text file
                for line in txtfile:
                    x, y, z = map(float, line.strip().split())  
                    points.append(QPoint3DF(x, y, z))  

        return self.transformPoints(points, w, h)  


    def transformPoints(self, points, w, h):
        if not points:
            return []

        # Find the bounding box of all points
        min_x = min(point.x() for point in points)
        max_x = max(point.x() for point in points)
        min_y = min(point.y() for point in points)
        max_y = max(point.y() for point in points)

        # Determine scale and offset
        scale_x = w / (max_x - min_x)
        scale_y = h / (max_y - min_y)
        scale = min(scale_x, scale_y)

        offset_x = -min_x * scale + (w - (max_x - min_x) * scale) / 2
        offset_y = -min_y * scale + (h - (max_y - min_y) * scale) / 2

        # Transform points
        transformed_points = []
        for point in points:
            x = point.x() * scale + offset_x
            y = point.y() * scale + offset_y
            z = point.getZ()
            bod = QPoint3DF(x,y,z)
            transformed_points.append(bod)
        
        return transformed_points

    