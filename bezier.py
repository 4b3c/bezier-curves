from usingMath import Bezier
import numpy as np
import pygame, math

def dist_between_points(coords1, coords2):
	distx = coords2[0] - coords1[0]
	disty = coords2[1] - coords1[1]
	return math.sqrt(distx * distx + disty * disty);

def calculate_length(points):
	length = 0
	for i in range(len(points) - 1):
		length += dist_between_points(points[i], points[i + 1])

	return length

def calc_curve(points, resolution = 0.05):
	t_points = np.arange(0, 1, resolution)
	return Bezier.Curve(t_points, points)

class Curve:
	def __init__(self, start, color, points = [[None]]):
		if points[0][0] == None:
			self.points = np.array([(start)])
			self.moving = -1
			self.color = color
		else:
			self.points = points
			curve_points = calc_curve(self.points)
			self.length = calculate_length(curve_points)
			

	def calc_curve(self, resolution = 0.05):
		t_points = np.arange(0, 1, resolution)
		self.curve = Bezier.Curve(t_points, self.points)

	def draw_lines(self, display):
		if len(self.points) > 1:
			now_points = [tuple(coord) for coord in self.points]
			now_curve = [tuple(coord) for coord in self.curve]
			pygame.draw.lines(display, (220, 220, 220), False, list(now_points), 3)
			pygame.draw.lines(display, self.color, False, list(now_curve), 3)
		for point in self.points:
			pygame.draw.circle(display, (220, 220, 220), point, 7, 3)

	def new_point(self, coord):
		self.points = np.append(self.points, np.array([coord]), 0)
		self.calc_curve()

	def check_click(self, coord, right):
		for point in range(len(self.points)):
			if abs(coord[0] - self.points[point][0]) < 15 and abs(coord[1] - self.points[point][1]) < 15:
				return point
		return -1

	def delete(self, point):
		placeholder = list(self.points)
		placeholder.pop(point)
		self.points = np.array(placeholder)
		self.calc_curve()

	def add_point(self, coord):
		self.points = np.append(self.points, np.array([coord]), 0)
		self.calc_curve()

	def move_point(self, point, coord):
		self.moving = point
		self.points[point] = np.array([coord])
		self.calc_curve()