import pygame, math
from usingMath import Bezier
import numpy as np
from numpy import array as a
import matplotlib.pyplot as plt

pygame.init()

#8.02m by 16.54m

running = True
clicked = False
pressed = False
points = []
slopes = []
lengths = []
lerp1 = []
animate = False
neighbors = [(int(count / 5) - 2, (count % 5) - 2) for count in range(0, 25)]

image = pygame.image.load('2023-FRC-Field.png')
size = image.get_size()
print(size)
image = pygame.transform.scale(image, (size[0] * 1.8, size[1] * 1.8))

step = 0
direction = 1
clock = pygame.time.Clock()

window = pygame.display.set_mode(((size[0] * 1.8) + 140, (size[1] * 1.8) + 140))

def draw_lines():
	pygame.draw.lines(window, (220, 220, 220), False, points, 3)

def draw_circles():
	for point in points:
		pygame.draw.circle(window, (220, 220, 220), point, 7, 3)

def draw_curve():
	points2 = a(points)
	t_points = np.arange(0, 1, 0.005)
	curve = Bezier.Curve(t_points, points2)
	for c in range(len(curve) - 1):
		pygame.draw.lines(window, (20, 20, 220), False, [curve[c], curve[c + 1]], 5)
	
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				print(Bezier.Curve(np.arange(0, 1, 0.005), a(points)))

	mouse_pos = pygame.mouse.get_pos()

	if pygame.mouse.get_pressed()[0]:
		for point in range(len(points)):
			if abs(mouse_pos[0] - points[point][0]) < 15 and abs(mouse_pos[1] - points[point][1]) < 15:
				clicked_index = point
				break

		if clicked_index != 0:
			points[clicked_index] = mouse_pos

		if not clicked:
			clicked = True
			if clicked_index == 0:
				points.append(mouse_pos)

			if len(points) > 1:
				slopes = [i for i in range(len(points) - 1)]
				lengths = [i for i in range(len(points) - 1)]

				for point in range(len(points) - 1):
					slopes[point] = abs(points[point][1] - points[point + 1][1]) / abs(points[point][0] - points[point + 1][0])
					lengths[point] = math.sqrt((points[point][1] - points[point + 1][1])**2 + (points[point][0] - points[point + 1][0])**2)
	else:
		clicked = False
		clicked_index = 0

	if pygame.mouse.get_pressed()[2]:
		for point in range(len(points)):
			if abs(mouse_pos[0] - points[point][0]) < 15 and abs(mouse_pos[1] - points[point][1]) < 15:
				points.remove(points[point])
				break


	window.fill((30, 50, 60))
	window.blit(image, (70, 70))
	if len(points) > 0:
		draw_circles()
	if len(points) > 1:
		draw_lines()
		draw_curve()
	pygame.display.update()


	clock.tick(30)


