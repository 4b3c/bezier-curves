import pygame, math
from usingMath import Bezier
import numpy as np
import matplotlib.pyplot as plt

pygame.init()

#8.02m by 16.54m

running = True
clicked = False

image = pygame.image.load('2023-FRC-Field.png')
size = image.get_size()
image = pygame.transform.scale(image, (size[0] * 1.8, size[1] * 1.8))

clock = pygame.time.Clock()
window = pygame.display.set_mode(((size[0] * 1.8) + 140, (size[1] * 1.8) + 140))

class Curve:
	def __init__(self, start):
		self.points = np.array([(start)])
		self.moving = -1

	def calc_curve(self, resolution = 0.005):
		t_points = np.arange(0, 1, 0.005)
		self.curve = Bezier.Curve(t_points, self.points)

	def draw_lines(self, display):
		if len(self.points) > 1:
			now_points = [tuple(coord) for coord in self.points]
			now_curve = [tuple(coord) for coord in self.curve]
			pygame.draw.lines(display, (220, 220, 220), False, list(now_points), 3)
			pygame.draw.lines(display, (20, 20, 220), False, list(now_curve), 3)
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


main_curve = Curve([10, 10])


while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				print(main_curve.curve)

	mouse_pos = pygame.mouse.get_pos()
	mouse_press = pygame.mouse.get_pressed()

	if main_curve.moving != -1:
		main_curve.move_point(main_curve.moving, mouse_pos)

	if mouse_press[0]:
		point = main_curve.check_click(mouse_pos, False)
		if point == -1 and clicked == False:
			main_curve.add_point(np.array(mouse_pos))
			clicked = True
		elif main_curve.moving == -1:
			main_curve.move_point(point, mouse_pos)
	elif mouse_press[2] and clicked == False:
		point = main_curve.check_click(mouse_pos, True)
		if point != -1:
			main_curve.delete(point)
			clicked = True
	else:
		clicked = False
		main_curve.moving = -1

	window.fill((30, 50, 60))
	window.blit(image, (70, 70))
	main_curve.draw_lines(window)
	pygame.display.update()
	clock.tick(30)



