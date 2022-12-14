import pygame, math
from usingMath import Bezier
import numpy as np
from numpy import array as a
import matplotlib.pyplot as plt

pygame.init()

running = True
clicked = False
pressed = False
points = [(14, 50), (40, 20)]
slopes = []
lengths = []
lerp1 = []
animate = False
neighbors = [(int(count / 5) - 2, (count % 5) - 2) for count in range(0, 25)]

step = 0
direction = 1
clock = pygame.time.Clock()

window = pygame.display.set_mode((900, 600))

def draw_lines():
	pygame.draw.lines(window, (220, 220, 220), False, points, 3)
	for point in points:
		pygame.draw.circle(window, (220, 220, 220), point, 7, 3)
	if animate:
		for lerp in lerp1:
			pygame.draw.circle(window, (220, 220, 220), lerp, 5, 2)

def draw_curve():
	points2 = a(points)
	t_points = np.arange(0, 1, 0.01)
	curve = Bezier.Curve(t_points, points2)
	for c in range(len(curve) - 1):
		pygame.draw.lines(window, (20, 20, 220), False, [curve[c], curve[c + 1]], 2)
	
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	if pygame.mouse.get_pressed()[0]:
		if not clicked:
			clicked = True
			points.append(pygame.mouse.get_pos())
			slopes = [i for i in range(len(points) - 1)]
			lengths = [i for i in range(len(points) - 1)]
			lerp1 = [list(point) for point in points[0:-1]]
			for point in range(len(points) - 1):
				slopes[point] = abs(points[point][1] - points[point + 1][1]) / abs(points[point][0] - points[point + 1][0])
				lengths[point] = math.sqrt((points[point][1] - points[point + 1][1])**2 + (points[point][0] - points[point + 1][0])**2)
		if pygame.mouse.get_pos() in points:
			pass
	else:
		clicked = False


	window.fill((30, 50, 60))
	draw_lines()
	draw_curve()
	pygame.display.update()


	clock.tick(30)


