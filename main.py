import pygame
from bezier import Curve
import numpy as np

pygame.init()

#8.02m by 16.54m

running = True
clicked = False

image = pygame.image.load('2023-FRC-Field.png')
size = image.get_size()
image = pygame.transform.scale(image, (size[0] * 1.8, size[1] * 1.8))

clock = pygame.time.Clock()
window = pygame.display.set_mode(((size[0] * 1.8) + 340, (size[1] * 1.8) + 140))

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



