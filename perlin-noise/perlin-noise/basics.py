import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise

noise1 = PerlinNoise(octaves=3)
cords = []

range = 2
accuracy = 0.01
loops = round(range/accuracy)
for i in range(5):
    y = noise1([float(i/accuracy)])
    cords.append(y)
    print(i,y)
print(cords)
plt.plot(cords)
plt.show()