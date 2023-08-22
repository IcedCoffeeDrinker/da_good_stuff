from tkinter import *
from perlin_noise import PerlinNoise
import time
import matplotlib as plt
from math import *

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

# settings settings
settings_width = 500
settings_height = 600

# settings setup
settings = Tk()
settings.geometry(f'{settings_width}x{settings_height}')
settings.resizable(False, False)
settings.title('settings')
settings.config(bg='black')

class main:
    def __init__(self):
        # precompute frequently used values
        self.TWO_PI = 2 * 3.141592653589793
        self.win_size_half = win_size / 2

        self.slider_length = 450
        self.initialize_settings()

        self.noise = PerlinNoise(octaves=self.wildness, seed=42)
        self.colorMap = plt.colormaps['plasma']
        self.time = 0

        self.process()

    def initialize_settings(self):
        self.resolution = 100
        self.size = 1
        self.scale = 150 / self.size
        self.speed = .5
        self.wildness = 3
        self.offsetMultiplyer = 1

        self.resolution_slider = self.create_slider("Resolution", 10, 500, self.resolution, 10)
        self.size_slider = self.create_slider("Size", 0.1, 10, self.size, 0.1)
        self.scale_slider = self.create_slider("Scale", 0, 250, self.scale, 1)
        self.speed_slider = self.create_slider("Speed", 0, 4, self.speed, 0.01)
        self.wildness_slider = self.create_slider("Wildness", .1, 10, self.wildness, 0.1)
        self.offset_multiplier_slider = self.create_slider("Offset Multiplier", 0.1, 10, self.offsetMultiplyer, 0.1)

    def create_slider(self, label_text, from_, to_, initial_value, tick_interval):
        label = Label(settings, text=label_text)
        label.pack(pady=10)

        slider = Scale(settings, from_=from_, to=to_, orient=HORIZONTAL, length=self.slider_length, resolution=tick_interval, bg='black', fg='white')
        slider.set(initial_value)
        slider.pack(pady=5)

        return slider

    def update_values_from_sliders(self):
        self.resolution = self.resolution_slider.get()
        self.size = self.size_slider.get()
        self.scale = self.scale_slider.get() / self.size
        self.speed = self.speed_slider.get()
        self.wildness = self.wildness_slider.get()
        self.offsetMultiplyer = self.offset_multiplier_slider.get()

        # Update noise only if wildness changes
        if self.noise.octaves != self.wildness:
            self.noise = PerlinNoise(octaves=self.wildness, seed=42)

    def process(self):
        startTime = time.time()
        self.update_values_from_sliders()

        can.delete('all')
        angleStep = self.TWO_PI / self.resolution
        prevDot = [sin(angleStep) * self.size * self.scale + self.win_size_half,
                   cos(angleStep) * -self.size * self.scale + self.win_size_half]

        for i in range(1, self.resolution):
            angle = i * angleStep
            x = sin(angle) * self.size
            y = cos(angle) * -self.size
            offset = self.noise([x, y, self.time])
            color = plt.colors.to_hex(self.colorMap(offset + 0.5))
            newX = sin(angle) * (self.size + offset * self.offsetMultiplyer) * self.scale + self.win_size_half
            newY = cos(angle) * -(self.size + offset * self.offsetMultiplyer) * self.scale + self.win_size_half
            can.create_line(prevDot[0], prevDot[1], newX, newY, fill=color, width=5)
            prevDot = [newX, newY]

        self.time += self.speed

        self.neededTime = time.time() - startTime
        try:
            frameRate.config(text=round(1 / self.neededTime, 2))
        except ZeroDivisionError:
            pass
        win.after(1, self.process)

main()
win.mainloop()
