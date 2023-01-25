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
print(size)
image = pygame.transform.scale(image, (size[0] * 1.8, size[1] * 1.8))

clock = pygame.time.Clock()
window = pygame.display.set_mode(((size[0] * 1.8) + 140, (size[1] * 1.8) + 140))

class Curve:
	def __init__(self, start):
		self.points = np.array([(start)])

	def calc_curve(self, resolution = 0.005):
		points = np.array(self.points)
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
				if right:
					self.points.remove(self.points[point])
					self.calc_curve()
					return
				break
		point += 1
		if not right:
			if point == len(self.points):
				self.new_point(coord)


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

	if mouse_press[0] == True and clicked == False:
		main_curve.check_click(mouse_pos, False)
		clicked = True

	elif mouse_press[2] == True and clicked == False:
		main_curve.check_click(mouse_pos, True)
		clicked = True

	elif mouse_press[0] == False and mouse_press[2] == False:
		clicked = False

	window.fill((30, 50, 60))
	window.blit(image, (70, 70))
	main_curve.draw_lines(window)
	pygame.display.update()
	clock.tick(30)


