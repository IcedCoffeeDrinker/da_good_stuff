from tkinter import *
from math import *

# settings
window_height = 825
window_width = 500
canvas_height = 400
canvas_width = 400

win = Tk()
win.title('cube - (pointless)')
win.resizable(False, False)
win.geometry(f'{window_width}x{window_height}')
win.configure(bg='#ffffff')
can = Canvas(width=canvas_width, height=canvas_height, bg='#000000')
can.place(x=50,y=50)

# gui (without buttons)
sSpacing = 40
sWidth = 10
sYstart = canvas_height + 50 + sSpacing
sRange = [-1, 1]

sliderX = Scale(from_=sRange[0], to=sRange[1], orient=HORIZONTAL, length=canvas_width, width=sWidth,
	bg='#ffffff', highlightthickness=0, label='x rotation', resolution=0.001)
sliderX.place(x=50, y=sYstart)

sliderY = Scale(from_=sRange[0], to=sRange[1], orient=HORIZONTAL, length=canvas_width, width=sWidth,
	bg='#ffffff', highlightthickness=0, label='y rotation', resolution=0.001)
sliderY.place(x=50, y=sYstart+sSpacing+sWidth)

sliderZ = Scale(from_=sRange[0], to=sRange[1], orient=HORIZONTAL, length=canvas_width, width=sWidth,
	bg='#ffffff', highlightthickness=0, label='z rotation', resolution=0.001)
sliderZ.place(x=50, y=sYstart+(sSpacing+sWidth)*2)


class cube:
	def __init__(self):
		self.size = 100
		self.rotation = [0, 0, 0]
		self.vertexSize = 5
		self.projectionMode = 'ortographic'

		# display settings
		self.showVertecies = verteciesVar
		self.showLines = linesVar
		self.showFaces = facesVar

		# perspective settings
		self.fov = 10 # in degrees
		self.zOffset = 10

		self.S = 1 / tan(self.fov / 2 * pi / 180)
		self.n = 1 # far and near plane
		self.f = 10

		self.vertecies = [
			[-1, -1 , -1],
			[-1, -1, 1],
			[-1, 1, -1],
			[-1, 1, 1],
			[1, -1, -1],
			[1, -1, 1],
			[1, 1, -1],
			[1, 1, 1]
		]
		self.backup = self.vertecies.copy()
		self.lines = [
			[0, 1],
			[0, 2],
			[0, 4],
			[7, 6],
			[7, 3],
			[7, 5],
			[1, 3],
			[1, 5],
			[2, 3],
			[2, 6],
			[4, 5],
			[4, 6]
		]
		self.faces = [
			[0, 2, 6, 4, '#FFB7B2'], # v0, v1, v2, v3, color
			[0, 1, 3, 2, '#FF9AA2'],
			[0, 1, 5, 4, '#FFDAC1'],
			[7, 6, 4, 5, '#E2F0CB'],
			[7, 6, 2, 3, '#B5EAD7'],
			[7, 3, 1, 5, '#C7CEEA'],
		]
		self.ortographicMatrix = [
		[1, 0, 0],
		[0, 1, 0],
		[0, 0, 0]
		]
		self.perspectiveMatrix = [
			[self.S, 0, 0, 0],
			[0, self.S, 0, 0],
			[0, 0, self.f / (self.f - self.n), 1],
			[0, 0, self.f * self.n / (self.f - self.n), 0]
		]
		self.loop()

	def matrixMultiplier(self, matrix, vertex):
		final_vertex = []
		for row in range(len(matrix)):
			sum = 0
			for column in range(len(vertex)):
				sum += matrix[row][column] * vertex[column]
			final_vertex.append(sum)
		return final_vertex

	def project(self, object):
		projection = []
		if self.projectionMode == 'ortographic':
			for vertex in object:
				newVertex = self.matrixMultiplier(self.ortographicMatrix, vertex)
				projection.append(newVertex)
		else:
			for vertex in object:
				copyVertex = vertex.copy()
				copyVertex.append(1)
				copyVertex[2] += self.zOffset
				copyVertex = self.matrixMultiplier(self.perspectiveMatrix, copyVertex)
				copyVertex = [copyVertex[0] / copyVertex[3], copyVertex[1] / copyVertex[3], copyVertex[2] / copyVertex[3]]
				projection.append(copyVertex)
		return projection

	def translate(self, projection):
		final_projection = []
		for vertex in projection:
			vertex[0] *= self.size
			vertex[1] *= self.size
			vertex[0] += canvas_width / 2
			vertex[1] += canvas_width / 2
			final_projection.append(vertex)
		return final_projection

	def rotate(self, object):
		rotationX = [
		[1, 0, 0],
		[0, cos(self.rotation[0]), -sin(self.rotation[0])],
		[0, sin(self.rotation[0]), cos(self.rotation[0])]
		]
		rotationY = [
		[cos(self.rotation[1]), 0, sin(self.rotation[1])],
		[0, 1, 0],
		[-sin(self.rotation[1]), 0, cos(self.rotation[1])]
		]
		rotationZ = [
		[cos(self.rotation[2]), -sin(self.rotation[2]), 0],
		[sin(self.rotation[2]), cos(self.rotation[2]), 0],
		[0, 0, 1]
		]
		new_object = []
		for vertex in object:
			new_vertex = self.matrixMultiplier(rotationX, vertex)
			new_vertex = self.matrixMultiplier(rotationY, new_vertex)
			new_vertex = self.matrixMultiplier(rotationZ, new_vertex)
			new_object.append(new_vertex)
		return new_object

	def draw(self, projection):
		can.delete('all')
		if self.showVertecies.get():
			for vertex in projection:
				x = vertex[0] - self.vertexSize
				y = vertex[1] - self.vertexSize
				x1 = vertex[0] + self.vertexSize
				y1 = vertex[1] + self.vertexSize
				can.create_oval(x, y, x1, y1, fill='white', width=0)

		if self.showLines.get():
			for line in self.lines:
				point = projection[line[0]]
				point1 = projection[line[1]]
				can.create_line(point[0], point[1], point1[0], point1[1], fill='white')

		if self.showFaces.get():
			facesWithCenter = []											#	calculate center of every face
			for face in self.faces:											#
				relV0 = self.vertecies[face[0]] # diagonal to relV2			#
				relV2 = self.vertecies[face[2]]								#
				centerZ = (relV0[2] + relV2[2]) / 2							#
				newFace = face.copy()										#
				newFace.append(centerZ)										#
				facesWithCenter.append(newFace)								#

			facesWithCenter.sort(key=lambda x: x[5], reverse=True)	#	sorting faces from back to front
			facesWithCenter = facesWithCenter[3:7] 					#

			for face in facesWithCenter:																		#	apply face order to projected cube,
				v0 = projection[face[0]]																		#	then draw it.
				v1 = projection[face[1]]																		#
				v2 = projection[face[2]]																		#
				v3 = projection[face[3]]																		#
				can.create_polygon(v0[0], v0[1],  v1[0], v1[1],  v2[0], v2[1],  v3[0], v3[1], fill=face[4])		#

	def update(self):
		self.rotation = [sliderX.get()/100, sliderY.get()/100, sliderZ.get()/100]

	def reset(self):
		self.rotation = [0, 0, 0]
		sliderX.set(0)
		sliderY.set(0)
		sliderZ.set(0)
		self.vertecies = self.backup

	def modeChanger(self):
		if self.projectionMode == 'ortographic':
			self.projectionMode = 'perspective'
			buttonProjection.config(text='ortographic')
		else:
			self.projectionMode = 'ortographic'
			buttonProjection.config(text='perspective')

	def loop(self):
		self.update()
		self.vertecies = self.rotate(self.vertecies)
		projection = self.project(self.vertecies)
		projection = self.translate(projection)
		self.draw(projection)
		win.after(1, self.loop)

# gui checkboxes
verteciesVar = IntVar(value=True)
verteciesCheck = Checkbutton(text='dots', font=('Arial', 12), bg='white', variable=verteciesVar)
verteciesCheck.place(x=50, anchor=SW, y=window_height-50)

linesVar = IntVar(value=True)
linesCheck = Checkbutton(text='lines', font=('Arial', 12), bg='white', variable=linesVar)
linesCheck.place(relx=0.5, anchor=S, y=window_height-50)

facesVar = IntVar()
facesCheck = Checkbutton(text='faces', font=('Arial', 12), bg='white', variable=facesVar)
facesCheck.place(x=window_width-50, anchor=SE, y=window_height-50)


# start
Cube = cube()


# buttons
buttonReset = Button(text='reset', font=('Arial', 20), command=Cube.reset)
buttonReset.place(x=50, anchor=W, y=window_height-125)

buttonProjection = Button(text='perspective', font=('Arial', 20), command=Cube.modeChanger)
buttonProjection.place(x=window_width-50, anchor=E, y=window_height-125)


win.mainloop()
