import tkinter as tk

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

# create the window
window = tk.Tk()
window.title("Settings")
#window.geometry(f"{window_width}x{window_height}")

# create the labels and entry boxes for each setting
window_height_label = tk.Label(window, text="Window Height:")
window_height_entry = tk.Entry(window, width=10)
window_height_entry.insert(0, str(window_height))

window_width_label = tk.Label(window, text="Window Width:")
window_width_entry = tk.Entry(window, width=10)
window_width_entry.insert(0, str(window_width))

tile_density_label = tk.Label(window, text="Tile Density:")
tile_density_entry = tk.Entry(window, width=10)
tile_density_entry.insert(0, str(tileDensity))

wildness_label = tk.Label(window, text="Wildness:")
wildness_entry = tk.Entry(window, width=10)
wildness_entry.insert(0, str(wildness))

zoom_label = tk.Label(window, text="Zoom:")
zoom_entry = tk.Entry(window, width=10)
zoom_entry.insert(0, str(zoom))

change_speed_label = tk.Label(window, text="Change Speed:")
change_speed_entry = tk.Entry(window, width=10)
change_speed_entry.insert(0, str(changeSpeed))

particle_amount_label = tk.Label(window, text="Particle Amount:")
particle_amount_entry = tk.Entry(window, width=10)
particle_amount_entry.insert(0, str(particleAmount))

# create the checkbox for the boolean settings
change_field_checkbox = tk.Checkbutton(window, text="Change Field", var=changeField)
show_vectors_checkbox = tk.Checkbutton(window, text="Show Vectors", var=showVectors)
animate_particles_checkbox = tk.Checkbutton(window, text="Animate Particles", var=animateParticles)

# create a function to update the settings
def update_settings():
    global tileDensity, wildness, zoom, changeSpeed, changeField, showVectors, particleAmount, animateParticles, window_height, window_width
    
    tileDensity = int(tile_density_entry.get())
    wildness = int(wildness_entry.get())
    zoom = int(zoom_entry.get())
    changeSpeed = float(change_speed_entry.get())
    changeField = bool(change_field_checkbox.get())
    showVectors = bool(show_vectors_checkbox.get())
    particleAmount = int(particle_amount_entry.get())
    animateParticles = bool(animate_particles_checkbox.get())
    window_height = int(window_height_entry.get())
    window_width = int(window_width_entry.get())
    window.geometry(f"{window_width}x{window_height}")

# create a button to apply the changes
apply_button = tk.Button(window, text="Apply", command=update_settings)

# pack all the widgets into the window
window_height_label.pack()
window_height_entry.pack()
window_width_label.pack()
window_width_entry.pack()
tile_density_label.pack()
tile_density_entry.pack()
wildness_label.pack()
wildness_entry.pack()
zoom_label.pack()
zoom_entry.pack()
change_speed_label.pack()
change_speed_entry.pack()
change_field_checkbox.pack()
show_vectors_checkbox.pack()
particle_amount_label.pack()
particle_amount_entry.pack()
animate_particles_checkbox.pack()
apply_button.pack()

# start the main loop
window.mainloop()
