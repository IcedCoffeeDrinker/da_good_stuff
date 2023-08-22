# gpt assisted (for sliders only)
#
# fix needed: size reduces strenght of offset somehow
#

from tkinter import *
from perlin_noise import PerlinNoise
from math import *
import time
import matplotlib as plt

# win settings
win_size = 500
bg_color = 'black'

# win setup
win = Tk()
win.geometry(f'{win_size}x{win_size}')
win.resizable(False, False)
win.title('b l o b')
win.config(bg=bg_color)
can = Canvas(win, width=win_size, height=win_size, bg=bg_color, highlightthickness=0)
can.place(x=0, y=0)
frameRate = Label(text="", bg='black', fg='white', font=("Consolas", 12))
frameRate.place(anchor='nw', x=0, y=0)

# settings settings - lol :)
settings_width = 500
settings_height = 550

# settings setup
settings = Tk()
settings.geometry(f'{settings_width}x{settings_height}')
settings.resizable(False, False)
settings.title('settings')
settings.config(bg='black')



class main:
    def __init__(self):
        self.resolution = 150
        self.size = 1 # ringsize in noise map
        self.scale = 150 # scale on canvas in pixels
        self.speed = .5
        self.wildness = 3
        self.offsetMultiplyer = 1
        self.slider_length = 450

        self.noise = PerlinNoise(octaves=self.wildness, seed=42)
        self.time = 0 # movement in 3th dimension
        self.neededTime = 0
        self.scale /= self.size
        self.colorMap = plt.colormaps['plasma']

        self.resolution_slider = self.create_slider("Resolution", 10, 500, self.resolution, 1)
        self.size_slider = self.create_slider("Size", 0.1, 10, self.size, 0.01)
        self.scale_slider = self.create_slider("Scale", 0, 250, self.scale, 1)
        self.speed_slider = self.create_slider("Speed", 0, 4, self.speed, 0.01)
        self.wildness_slider = self.create_slider("Wildness", 0.1, 6, self.wildness, 0.001)
        self.offset_multiplier_slider = self.create_slider("Offset Multiplier", 0.1, 10, self.offsetMultiplyer, 0.1)

        self.process()

    def create_slider(self, label_text, from_, to_, initial_value, tick_interval):
        # Create label
        label = Label(settings, text=label_text)
        label.pack(pady=10)

        # Create and configure the slider
        slider = Scale(settings, from_=from_, to=to_, orient=HORIZONTAL, length=self.slider_length, resolution=tick_interval, bg='black', fg='white', highlightthickness=0)
        slider.set(initial_value)
        slider.pack(pady=5)

        return slider

    def update_values_from_sliders(self):
        # Update values based on the sliders
        self.resolution = self.resolution_slider.get()
        self.size = self.size_slider.get()
        self.scale = self.scale_slider.get() / self.size  # Adjust for the division by size you had originally
        self.speed = self.speed_slider.get()
        self.wildness = self.wildness_slider.get()
        self.offsetMultiplyer = self.offset_multiplier_slider.get()

        # Update noise with new wildness value
        self.noise = PerlinNoise(octaves=self.wildness, seed=42)

    def process(self):
        startTime = time.time()
        self.update_values_from_sliders()

        can.delete('all')
        firstDot = None
        prevDot = None
        angleStep = 2*pi / self.resolution
        for i in range(self.resolution):
            angle = i * angleStep
            x = sin(angle) * self.size
            y = cos(angle) * -self.size
            offset = self.noise([x, y, self.time])
            color = plt.colors.to_hex(self.colorMap(offset+0.5))
            newX = sin(angle) * (self.size + offset * self.offsetMultiplyer) * self.scale + win_size/2
            newY = cos(angle) * -(self.size + offset * self.offsetMultiplyer) * self.scale + win_size/2
            if i == 0:
                firstDot = [newX, newY]
            else:
                can.create_line(prevDot[0], prevDot[1], newX, newY, fill=color, width=5)
            prevDot = [newX, newY]
        can.create_line(prevDot[0], prevDot[1], firstDot[0], firstDot[1], fill=color, width=5)
        self.time += self.speed * self.neededTime

        self.neededTime = time.time() - startTime
        try:
            frameRate.config(text=round(1/self.neededTime, 2))
        except ZeroDivisionError:
            pass
        win.after(1, self.process)

main()
win.mainloop()