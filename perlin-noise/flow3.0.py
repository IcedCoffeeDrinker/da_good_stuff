from perlin_noise import PerlinNoise
from tkinter import *
from math import *
import random

# settings
window_height = 500
window_width = 800
tileDensity = 15
wildness = 3
zoom = 30
changeSpeed = 0.01
changeField = True
showVectors = False

particleAmount = 30
animateParticles = True

# settings window
settings_height = 600
settings_width = 400
win2 = Tk()
win2.title("Flow stuff")
win2.resizable(False, False)
win2.geometry(str(int(settings_width)) + "x" + str(int(settings_height)))
win2.configure(background="#ffffff")

# setup
canvas_height = floor(window_height / tileDensity)
canvas_width = floor(window_width / tileDensity)
tileSize = window_height / canvas_height
window_width = floor(tileSize * canvas_width)
noise = PerlinNoise(octaves=wildness)
flowField = []
particles = []


# window
win = Tk()
win.title("Flow stuff")
win.resizable(False, False)
win.geometry(str(int(window_width)) + "x" + str(int(window_height)))
win.configure(background="#000000")
can = Canvas(win,width=window_width,height=window_height,bg="#000000",highlightthickness=0)
can.place(x=0,y=0)

# functions
class canvas:
    def __init__(self):
        self.lines = []
        self.z = 0
        self.generateFlowField()
        print("new flow field generated")

    def displayTiles(self):
        for y in range(canvas_height):
            for x in range(canvas_width):
                can.create_rectangle(x*tileSize, y*tileSize, x*tileSize+1, y*tileSize+1, fill="white", width=0)
    
    def deleteVectors(self):
        for line in self.lines:
            can.delete(line)
        self.lines = []

    def displayVectors(self):
        self.deleteVectors()
        for y in range(len(flowField)):
            for x in range(len(flowField[y])):
                vector = flowField[y][x]
                x1 = tileSize * x
                y1 = tileSize * y
                x2 = x1 + vector[0]
                y2 = y1 + vector[1]
                line = can.create_line(x1, y1, x2, y2, width=1, fill="white")
                self.lines.append(line)

    def cordConverter(self, distance, angle): # polar to cartesian
            x = distance * cos(angle)
            y = distance * sin(angle)
            return [x, y]

    def generateFlowField(self):
        global flowField
        flowField = [] # reset not setup
        for y in range(canvas_height):
            row = []
            for x in range(canvas_width):
                angle = noise([x / zoom + 0.5, y / zoom + 0.5, self.z]) * 2 * pi
                vector = self.cordConverter(tileSize,angle)
                row.append(vector)
            flowField.append(row)
        #print(flowField)

class particle:
    def __init__(self, x, y):
        self.maxVel = 100
        
        self.x = x
        self.y = y
        self.oldX = x 
        self.oldY = y
        self.v = [0,0]
    
    def draw(self):
        can.create_line(self.oldX, self.oldY, self.x, self.y, width=1, fill="white")
    
    def applyVelocity(self):
        xTile = floor(self.x / tileSize)
        yTile = floor(self.y / tileSize)
        try:
            tileVel = flowField[yTile][xTile]
        except IndexError:
            tileVel = [0,0]
            print("Error at:")
            print(xTile,yTile, self.x, self.y, self.oldX, self.oldY)
        currentVel = sqrt(self.v[0] **2 + self.v[1] **2)
        if not currentVel > self.maxVel:
            self.v[0] = tileVel[0]
            self.v[1] = tileVel[1]
    
    def updatePos(self):
        if window_width <= self.x + self.v[0]:
            self.x -= window_width
        if self.x + self.v[0] <= 0:
            self.x += window_width
        if window_height <= self.y + self.v[1]:
            self.y -= window_height
        if self.y + self.v[1] <= 0:
            self.y += window_height
        self.oldX = self.x
        self.oldY = self.y
        self.x += self.v[0]
        self.y += self.v[1]

    def update(self):
        self.draw()
        self.applyVelocity()
        self.updatePos()

def placeParticles(amount):
    for _ in range(amount):
        x = random.randint(0,window_width)
        y = random.randint(0,window_height)
        Particle = particle(x,y)
        particles.append(Particle)

def loop():
    global Canvas
    while True:
        if showVectors:
            Canvas.displayVectors()
        if animateParticles:
            for Particle in particles:        
                Particle.update()
        if changeField:
            Canvas.z += changeSpeed
            Canvas.generateFlowField()
        win.update()

def main():
    global Canvas
    Canvas = canvas()
    Canvas.generateFlowField()
    placeParticles(particleAmount)
    loop()
main()

win.mainloop()
