import math as m
import numpy as np
from asciimatics.screen import Screen


class donut:
    def __init__(self, screen):
        self.screen = screen
        
        # torus settings
        self.torusCircleResolution = 30
        self.torusResolution = 30
        self.torusCircleRadius = 0.3
        self.torusRadius = .6
        self.rotationSpeed = [0.1, 0.1, 0.1] # x, y, z

        # light settings
        self.lightPos = [1, 2 , -2] # relative to donut

        # ascii settings
        self.zoom = 0.5
        self.screenSize = self.screen.height
        self.characters = '.,-~:;=!*#$@'

        # camera settings
        self.fov = 10 # in degrees
        self.zOffset = 10

        self.S = 1 / m.tan(self.fov / 2 * m.pi / 180)
        self.n = 1 # far and near plane
        self.f = 10

        self.perspectiveMatrix = [
			[self.S, 0, 0, 0],
			[0, self.S, 0, 0],
			[0, 0, self.f / (self.f - self.n), 1],
			[0, 0, self.f * self.n / (self.f - self.n), 0]
		]
        
        self.torus = self.generateDonut()
        self.torusLighting = []
        self.loop()

    def matrixMultiplier(self, matrix, vertex):
        final_vertex = []
        for row in range(len(matrix)):
            sum = 0
            for column in range(len(vertex)):
                sum += matrix[row][column] * vertex[column]
            final_vertex.append(sum)
        return final_vertex
    
    def rotate(self, vertex, axis, angle):
        if axis =='x':
            matrix = [[1, 0, 0],
                      [0, m.cos(angle), -m.sin(angle)],
                      [0, m.sin(angle), m.cos(angle)]]
        elif axis == 'y':
            matrix = [[m.cos(angle), 0, m.sin(angle)],
                      [0, 1, 0],
                      [-m.sin(angle), 0, m.cos(angle)]]
        elif axis == 'z':
            matrix = [[m.cos(angle), -m.sin(angle), 0],
                      [m.sin(angle), m.cos(angle), 0],
                      [0, 0, 1]]
        return self.matrixMultiplier(matrix, vertex)
            
    def generateDonut(self):
        circleStepSize = 2 * m.pi / self.torusCircleResolution
        circle = []
        for i in range(self.torusCircleResolution):
            vertex = [self.torusRadius+self.torusCircleRadius*m.cos(circleStepSize*i),
                      self.torusCircleRadius*m.sin(circleStepSize*i),
                      0]
            circle.append(vertex)
        torusStepSize = 2 * m.pi / self.torusResolution
        torus = []
        for i in range(self.torusResolution):
            newCircle = [self.rotate(circle[ii], 'y', torusStepSize*i) for ii in range(self.torusCircleResolution)]
            torus += newCircle
        print('donut generated')
        return torus
    
    def rotateTorus(self):
        for i in range(len(self.torus)):
            self.torus[i] = self.rotate(self.torus[i], 'x', self.rotationSpeed[0])
            self.torus[i] = self.rotate(self.torus[i], 'y', self.rotationSpeed[1])
            self.torus[i] = self.rotate(self.torus[i], 'z', self.rotationSpeed[2])

    def project(self):
        projection = []
        for vertex in self.torus:
            copyVertex = vertex.copy()
            copyVertex.append(1)
            copyVertex[2] += self.zOffset
            copyVertex = self.matrixMultiplier(self.perspectiveMatrix, copyVertex)
            copyVertex = [copyVertex[0] / copyVertex[3], copyVertex[1] / copyVertex[3], copyVertex[2] / copyVertex[3]]
            projection.append(copyVertex)
        projection.sort(key=lambda x: x[2], reverse=True)
        return projection
    
    def light(self):
        brightness = []
        max = 0
        min = 9999
        for vertex in self.torus:
            distance  = m.sqrt((vertex[0]-self.lightPos[0])**2 + (vertex[1]-self.lightPos[1])**2 + (vertex[2]-self.lightPos[2])**2)
            if distance < min: min = distance
            if distance > max: max = distance
            brightness.append(distance)
        for i in range(len(brightness)):
            brightness[i] = (brightness[i] - min) / (max - min)
        return brightness            

    def ascii(self, projection, brightness):
        stepSize = 1 / len(self.characters)
        self.screen.clear()
        for i in range(len(projection)):
            vertex = projection[i]
            pixel = [int(round(vertex[ii]* self.screenSize * self.zoom + self.screenSize / 2)) for ii in range(2)]
            character = self.characters[round(brightness[i] / stepSize)-1]
            self.screen.print_at(character, pixel[0], pixel[1])
        self.screen.refresh()

        

    def loop(self):
        while True:
            brightness = self.light()
            projection = self.project()
            self.ascii(projection, brightness)
            self.rotateTorus()

Screen.wrapper(donut)