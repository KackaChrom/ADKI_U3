from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *
from edge import *
from random import *
from triangle import *
from math import *
from Settings import *


class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.points = []
        self.dt = []
        self.contours = []
        self.dtm_slope = []
        self.dtm_aspect = []
        self.drawDT = True
        self.drawContourLines = True
        self.drawSlope = True
        self.drawAspect = True
        self.dz = 0
        


    #def mousePressEvent(self, e:QMouseEvent):
        #Get cursor position
        #x = e.position().x()
        #y = e.position().y()
        
        #Generate random height
        #zmin = 150
        #zmax = 400
        #z = random() * (zmax - zmin) + zmin
        
        #Create new point
        #p = QPoint3DF(x, y, z)

        #Add point to the point cloud
        #self.points.append(p)

        #Repaint screen
        #self.repaint()
        

    def paintEvent(self,  e:QPaintEvent):
        #Draw situation
        
        #Create new object
        qp = QPainter(self)

        #Start drawing
        qp.begin(self)
        
        
        #Set graphic attributes
        #qp.setPen(Qt.GlobalColor.gray)
      
        #Draw slope
        if self.drawSlope:
            for t in self.dtm_slope:
                #Get slope
                slope = t.getSlope()
                
                #Convert slope to color
                mju = 2*255/pi
                col = int(255 - mju*slope)
                color = QColor(col, col, col)
                qp.setBrush(color)
                qp.setPen(Qt.GlobalColor.transparent)
                
                #Draw triangle
                qp.drawPolygon(t.getVertices())
            
        
        #Draw aspect
        if self.drawAspect:
            for t in self.dtm_aspect:
                #Get aspect
                aspect = t.getAspect()
                #Make from aspect full circle
                if aspect < 0:
                    aspect = pi + (pi+aspect)
                    
                #Min colors
                if aspect <= pi/3 and aspect >= 0 or aspect >= 5*pi/3 and aspect <= 2*pi:
                    r = 255
                    g = 0
                    b = 0
                elif aspect >= 1/3*pi and aspect <= pi:
                    b = 255
                    r = 0
                    g = 0
                elif aspect >= pi and aspect < 5/3*pi:
                    g = 255
                    r = 0
                    b = 0
                    
                #Colors
                if aspect > pi/3 and aspect < 2/3*pi:
                    r = int((pi/3 - aspect)*255/(pi/3))%255
                elif aspect > 2/3*pi and aspect < pi:
                    g = int((aspect-2/3*pi)*255/(pi/3))%255
                elif aspect > pi and aspect < 4/3*pi:
                    b = int((2*pi/3 - aspect)*255/(pi/3))%255
                elif aspect > 4/3*pi and aspect <5/3*pi:
                    r = int((aspect-4/3*pi)*255/(pi/3))%255
                elif aspect > 5/3*pi and aspect < 2*pi:
                    g = int((5*pi/3 - aspect)*255/(pi/3))%255
                elif aspect > 0 and aspect < pi/3:
                    b = int((aspect - pi/3)*255/(pi/3))%255    
                
                    
        
                color = QColor(r,g,b)
                qp.setBrush(color)
                qp.setPen(Qt.GlobalColor.transparent)
                
                #Draw triangle
                qp.drawPolygon(t.getVertices())
                
        
        #DRAW DT
        if self.drawDT:     
            #Set graphic attributes
            qp.setPen(Qt.GlobalColor.gray)
            qp.setBrush(Qt.GlobalColor.transparent)
            
            #Draw triangulation
            for e in self.dt:
                qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))

  



        # Draw contour lines
        if self.drawContourLines:  
            for i in range(len(self.contours)):
                #Set graphic attributs for contours and value of height
                pen = QPen(Qt.GlobalColor.darkGreen)
                pen.setWidth(1)
                qp.setPen(pen)
                qp.setBrush(Qt.GlobalColor.transparent)
                font = QFont("Arial", 8)
                qp.setFont(font)
                
                #Find start end end of line
                start_x = int(self.contours[i].getStart().x())
                start_y = int(self.contours[i].getStart().y())
                end_x = int(self.contours[i].getEnd().x())
                end_y = int(self.contours[i].getEnd().y())
                
                # Draw main contour
                if self.contours[i].getStart().getZ()%(self.dz*5) == 0:
                    #Set graphic attributs
                    pen = QPen(Qt.GlobalColor.darkGreen)
                    pen.setWidth(2)
                    qp.setPen(pen)
                    qp.setBrush(Qt.GlobalColor.transparent)
                    qp.setFont(font)
                qp.drawLine(start_x, start_y, end_x, end_y)
                # Draw value of contour
                if random() < 0.95:  
                    continue  
                
                contour_value = self.contours[i].getStart().getZ()  
                

                # Angle of contour
                angle = atan2(end_y - start_y, end_x - start_x) * 180 / pi
                
                # Random position on line
                offset = uniform(0.2, 0.8)
                text_x = start_x + offset * (end_x - start_x)
                text_y = start_y + offset * (end_y - start_y)
                
                qp.save() 
                qp.translate(text_x, text_y)
                
                # Rotate value
                qp.rotate(angle)
                
                qp.drawText(0, 0, str(contour_value))
                qp.restore()


                    
        #Set graphic attributes
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.black)

        #Draw points
        r = 2
        for p in self.points:
            qp.drawEllipse(int(p.x()-r), int(p.y()-r), 2*r, 2*r)
       
    

        #End drawing
        qp.end()
        
    
    def getPoints(self):
        # Return points
        return self.points
    
    def getDT(self):
        #Return DT
        return self.dt
    
    def clearAll(self):
        #Clear points
        self.points.clear()
        
        #Clear DT
        self.dt.clear()
        
        self.dtm_aspect.clear()
        self.dtm_slope.clear()
        self.contours.clear()
        
        #Repaint screen
        self.repaint()
        
    def clearData(self):
        # Clear results
        
        self.dt.clear()
        self.dtm_aspect.clear()
        self.dtm_slope.clear()
        self.contours.clear()
        #Repaint screen
        self.repaint()
        
        
    
    def setData(self, point):
        self.clearData()
        
        self.points = point
        
        self.repaint()    
    
    def setDT(self, dt: list[Edge]):
        self.dt = dt
        
        
    def setContours(self, contours: list[Edge]):
        self.contours = contours


    def setDTMAspect(self, dtm_aspect: list[Triangle]):
        self.dtm_aspect = dtm_aspect    
        
    
    def setDTMSlope(self, dtm_slope: list[Triangle]):
        self.dtm_slope = dtm_slope
    
    def setMinMaxDz(self, zmin:float, zmax:float, dz:float):
        self.zmin = zmin
        self.zmax = zmax
        self.dz = dz