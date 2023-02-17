import pygame, button
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
window = pygame.display.set_mode(((size[0] * 1.8) + 340, (size[1] * 1.8) + 240))

curves = [Curve([10, 10], (20, 20, 220))]
mode = 0

buttons = [
			button.button(35, (1200, 70), "Add curve", 200, 80),
			button.button(35, (1200, 160), "Save", 200, 80),
			button.button(35, (1200, 250), "Load", 200, 80),
			button.button(35, (1200, 340), "Export", 200, 80)
		  ]

BOX_WIDTH = 200
BOX_HEIGHT = 40
BOX_X = 1100
BOX_Y = 450
BOX_PADDING = 10

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	window.fill((30, 50, 60))
	window.blit(image, (70, 70))

	mouse_pos = pygame.mouse.get_pos()
	mouse_press = pygame.mouse.get_pressed()

	# Draw curve indicator background
	pygame.draw.rect(window, (80, 80, 80), (BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT * len(curves)), border_radius=3)
	for i, curve in enumerate(curves):
		box_color = (220, 220, 220) if i == mode else (100, 100, 100)
		pygame.draw.rect(window, box_color, (BOX_X + BOX_PADDING, BOX_Y + BOX_PADDING + i * (BOX_PADDING + BOX_HEIGHT), BOX_WIDTH, BOX_HEIGHT), border_radius=3)

		# Draw the curve number in the box
		font = pygame.font.SysFont("Arial", 20)
		text = font.render("Curve #" + str(i), True, (0, 0, 0))
		text_rect = text.get_rect(center=(BOX_X + BOX_PADDING + BOX_WIDTH / 2, BOX_Y + BOX_PADDING + i * (BOX_PADDING + BOX_HEIGHT) + BOX_HEIGHT / 2))
		window.blit(text, text_rect)

	# Check for button presses, if none are pressed but mouse is still pressed, manipulate curves
	for button in buttons:
		button.draw(window, mouse_pos, mouse_press[0])

		if button.pressed:
			if buttons[0] == button:
				curves.append(Curve(list(curves[-1].points[-1]), (220, 20, 20)))
			elif buttons[1] == button:
				pass
			elif buttons[2] == button:
				pass
			elif buttons[3] == button:
				for curve in curves:
					startx = np.transpose(curve.curve)[0][0]
					starty = np.transpose(curve.curve)[1][0]
					for x, y in zip(np.transpose(curve.curve)[0], np.transpose(curve.curve)[1]):
						print("{" + str(round((x - startx) * 30, 2)) + ", " + str(round((y - starty) * -30, 2)) + "},")

					print("END OF CURVE")
			break
		else:
			# Check if the user clicked on a curve selection box
			if mouse_press[0]:
				for i, curve in enumerate(curves):
					if BOX_X + BOX_PADDING + i * (BOX_PADDING + BOX_HEIGHT) <= mouse_pos[0] <= BOX_X + BOX_PADDING + (i+1) * (BOX_PADDING + BOX_HEIGHT) and BOX_Y + BOX_PADDING <= mouse_pos[1] <= BOX_Y + BOX_PADDING + BOX_HEIGHT:
						mode = i
						break

	else:
		for curve in curves:
			if curve.moving != -1:
				curve.move_point(curve.moving, mouse_pos)

			if mouse_press[0] and clicked == False:
				point = curve.check_click(mouse_pos, False)
				if point == -1 and clicked == False:
					curve.add_point(np.array(mouse_pos))
					clicked = True
				elif curve.moving == -1:
					curve.move_point(point, mouse_pos)
			elif mouse_press[2] and clicked == False:
				point = curve.check_click(mouse_pos, True)
				if point != -1:
					curve.delete(point)
					clicked = True
			else:
				clicked = False
				curve.moving = -1


	for curve in curves:
		curve.draw_lines(window)
				
	pygame.display.update()
	clock.tick(30)
