from tkinter import *
from perlin_noise import PerlinNoise
from math import *

# settings
win_size = 500
bg_color = 'black'

# window setup
win = Tk()
win.geometry(f'{win_size}x{win_size}')
win.resizable(False, False)
win.title('b l o b')
win.config(bg=bg_color)
can = Canvas(win, width=win_size, height=win_size, bg=bg_color, highlightthickness=0)
can.place(x=0, y=0)

class main:
    def __init__(self):
        self.resolution = 20
        self.size = 1 # ringsize in noise map
        self.scale = 150 # scale on canvas
        self.speed = 0.01
        self.wildness = 3
        self.offsetMultipyer = 1

        self.noise = PerlinNoise(octaves=self.wildness)
        self.time = 0

        self.process()


    def process(self):
        can.delete('all')
        firstDot = None
        prevDot = None
        angleStep = 2*pi / self.resolution
        for i in range(self.resolution):
            angle = i * angleStep
            x = sin(angle) * self.size
            y = cos(angle) * -self.size
            offset = self.noise([x, y, self.time])
            newX = sin(angle) * (self.size + offset * self.offsetMultipyer) * self.scale + win_size/2
            newY = cos(angle) * -(self.size + offset * self.offsetMultipyer) * self.scale + win_size/2
            if i == 0:
                firstDot = [newX, newY]
            else:
                can.create_line(prevDot[0], prevDot[1], newX, newY, fill='white', width=5)
            prevDot = [newX, newY]
        can.create_line(prevDot[0], prevDot[1], firstDot[0], firstDot[1], fill='white', width=5)
        self.time += self.speed
        win.after(1, self.process)

main()
win.mainloop()