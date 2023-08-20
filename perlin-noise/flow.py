from perlin_noise import PerlinNoise
from tkinter import *
from math import *
from tqdm import tqdm

# settings
window_height = 500
window_width = 500
canvas_height = floor(window_height / 10)
canvas_width = floor(window_width / 10)
tileSize = window_height / canvas_height

# window
win = Tk()
win.title("Flow stuff")
win.resizable(False, False)
win.geometry(str(window_width) + "x" + str(window_height))
win.configure(background="#000000")
can = Canvas(win,width=window_width,height=window_height,bg="#000000",highlightthickness=0)
can.place(x=0,y=0)

# vars
flowMap = []
infMap = PerlinNoise(octaves=3) # yes, i know how to spell noise

# functions
def generateMap():
    for y in tqdm (range(canvas_height), desc="generating map..."):
        row = []
        for x in range(canvas_width):
            row.append(infMap([x + 0.5, y + 0.5]))
        flowMap.append(row)
    print(flowMap)

def draw(x,y):
    x *= tileSize
    y *= tileSize
    x1 = x + tileSize
    y1 = y + tileSize
    print(x,y,x1,y1)
    can.create_rectangle(x, y, x1, y1, fill="white", width=0)

def flow(x,y):
    touchingWall = False
    maxEturations = 1000
    eturations = 0
    xPos = x
    yPos = y 
    while not touchingWall and eturations < maxEturations:
        print(eturations, xPos, yPos)
        eturations += 1
        draw(xPos,yPos)
        direction = flowMap[yPos][xPos]
        #print(direction)
        if direction < 1 / 8: # up
            yPos -= 1
        elif direction < 1 / 8 * 2: # top-right
            xPos += 1
            yPos -= 1
        elif direction < 1 / 8 * 3: # right
            xPos += 1
        elif direction < 1 / 8 * 4: # bottom-right
            xPos += 1
            yPos += 1
        elif direction < 1 / 8 * 5: # bottom
            yPos += 1
        elif direction < 1 / 8 * 6: # bottom-left
            xPos -= 1
            yPos += 1
        elif direction < 1 / 8 * 7: # left
            xPos -= 1
        elif direction < 1 / 8 * 8: # top-left
            xPos -= 1
            yPos -= 1
        else:
            print("u fucked", direction)
        
        if not canvas_width > xPos > 0 or not canvas_height > yPos > 0:
            touchingWall = True

        

def main():
    generateMap()
    flow(25,25)
main()

win.mainloop()