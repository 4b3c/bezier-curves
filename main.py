import pygame, button, pickle, os
from bezier import Curve
import numpy as np

pygame.init()

#8.02m by 16.54m
# Constants/initialization - constants/initialization - constants/initialization - constants/initialization
clicked = False
load_file = False

image = pygame.image.load('2023-FRC-Field.png')
size = image.get_size()
image = pygame.transform.scale(image, (size[0] * 1.8, size[1] * 1.8))

clock = pygame.time.Clock()
window = pygame.display.set_mode(((size[0] * 1.8) + 340, (size[1] * 1.8) + 240))

colors = {
	0: (255, 0, 0),     # Red
	1: (0, 255, 0),     # Green
	2: (0, 0, 255),     # Blue
	3: (255, 255, 0),   # Yellow
	4: (255, 0, 255),   # Magenta
	5: (0, 255, 255),   # Cyan
	6: (128, 0, 128),   # Purple
	7: (255, 165, 0),   # Orange
	8: (139, 69, 19),   # Brown
	9: (128, 128, 128)  # Gray
}

buttons = [
			button.button(35, (1200, 70), "Add curve", 200, 80),
			button.button(35, (1200, 160), "Save", 200, 80),
			button.button(35, (1200, 250), "Load", 200, 80),
			button.button(35, (1200, 340), "Export", 200, 80)
		  ]

curves = [Curve([10, 10], colors[0])]

mode = 0
BOX_WIDTH_WIDE = 220
BOX_WIDTH = 200
BOX_HEIGHT_TALL = 50
BOX_HEIGHT = 40
BOX_X = 1100
BOX_Y = 450
BOX_PADDING = 10

# Constants/initialization - constants/initialization - constants/initialization - constants/initialization

def draw_curve_list():
	# Draw curve indicator background
	pygame.draw.rect(window, (80, 80, 80), (BOX_X, BOX_Y, BOX_WIDTH_WIDE, (BOX_HEIGHT_TALL) * len(curves) + BOX_PADDING), border_radius=3)
	for i, curve in enumerate(curves):
		box_color = (220, 220, 220) if i == mode else (100, 100, 100)
		pygame.draw.rect(window, box_color, (BOX_X + BOX_PADDING, BOX_Y + BOX_PADDING + i * (BOX_HEIGHT_TALL), BOX_WIDTH, BOX_HEIGHT), border_radius=3)
		pygame.draw.rect(window, curve.color, (BOX_X + BOX_WIDTH - (BOX_PADDING * 4), BOX_Y + (BOX_PADDING * 2) + i * (BOX_HEIGHT_TALL), BOX_PADDING * 4, BOX_PADDING * 2), border_radius=3)

		# Draw the curve number in the box
		font = pygame.font.SysFont("Arial", 20)
		text = font.render("Curve #" + str(i), True, (0, 0, 0))
		text_rect = text.get_rect(center=(BOX_X + BOX_WIDTH_WIDE / 2, BOX_Y + BOX_PADDING + i * (BOX_HEIGHT_TALL) + BOX_HEIGHT / 2))
		window.blit(text, text_rect)

def add_curve():
	curves.append(Curve(list(curves[-1].points[-1]), colors[len(curves)]))

def save():
	files = os.listdir('paths//')
	highest = 0

	for file in files:
		if int(file[-5]) > highest:
			highest = int(file[-5])

	with open('paths//path' + str(highest + 1) + '.pkl', 'wb') as f:
		pickle.dump(curves, f)

def export():
	for curve in curves:
		startx = np.transpose(curve.curve)[0][0]
		starty = np.transpose(curve.curve)[1][0]
		for x, y in zip(np.transpose(curve.curve)[0], np.transpose(curve.curve)[1]):
			print("{" + str(round((x - startx) * 30, 2)) + ", " + str(round((y - starty) * -30, 2)) + "},")

		print("END OF CURVE")

def load():
	folder_path = 'paths//'
	box_color = (220, 220, 220)
	font = pygame.font.SysFont("Arial", 40)
	file_names = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()

		mouse_pos = pygame.mouse.get_pos()
		mouse_press = pygame.mouse.get_pressed()

		pygame.draw.rect(window, (80, 80, 80), (200, 100, 300, 10 + len(file_names) * 97.5), border_radius=3)
		for i, file in enumerate(file_names):
			rect = pygame.draw.rect(window, box_color, (210, 115 + i * 95, 280, 80), border_radius=3)

			text = font.render(file[:-4], True, (0, 0, 0))
			text_rect = text.get_rect(center=(210 + 140, (115 + i * 95) + 40))
			window.blit(text, text_rect)

			if rect.collidepoint(mouse_pos) and mouse_press[0]:
				return file

		pygame.display.update()
		clock.tick(30)


while True:
	# exit loop if pygame window is closed
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()

	# Fill the background and add the image of the field
	window.fill((30, 50, 60))
	window.blit(image, (70, 70))

	# Get mouse position and clicks
	mouse_pos = pygame.mouse.get_pos()
	mouse_press = pygame.mouse.get_pressed()

	# Draw the list/selector for different curves
	draw_curve_list()

	# Draw curves:
	for curve in curves:
		curve.draw_lines(window)

	# Handle dragging points
	if curves[mode].moving != -1:
		curves[mode].move_point(curves[mode].moving, mouse_pos)
		if curves[mode].moving == len(curves[mode].points) - 1 and mode != len(curves) - 1:
			curves[mode + 1].move_point(0, mouse_pos)
			curves[mode + 1].moving = -1
		elif curves[mode].moving == 0 and mode != 0:
			curves[mode - 1].move_point(len(curves[mode - 1].points) - 1, mouse_pos)
			curves[mode - 1].moving = -1

	# Draw Buttons
	for button in buttons:
		button.draw(window, mouse_pos, mouse_press[0])

	# Handle clicking
	if mouse_press[0] and clicked == False:
		clicked = True
		# Check buttons first for being clicked
		for button in buttons:
			if button.pressed:
				if buttons[0] == button:
					add_curve()
					mode += 1
					break
				elif buttons[1] == button:
					save()
					break
				elif buttons[2] == button:
					with open("paths//" + load(), 'rb') as f:
						curves = pickle.load(f)
					break
				elif buttons[3] == button:
					export()
					break

		# Check curve list/selector second for being clicked
		else:
			for i, curve in enumerate(curves):
				box_x = BOX_X + BOX_PADDING
				box_y = BOX_Y + BOX_PADDING + i * (BOX_PADDING + BOX_HEIGHT)
				if box_x <= mouse_pos[0] <= box_x + BOX_WIDTH and box_y <= mouse_pos[1] <= box_y + BOX_HEIGHT:
					mode = i
					break

			# Handle curve points last for being clicked
			else:
				point = curves[mode].check_click(mouse_pos, False)
				if point == -1:
					if curves[mode] == curves[-1]:
						curves[mode].add_point(np.array(mouse_pos))
				elif curves[mode].moving == -1:
					curves[mode].move_point(point, mouse_pos)

	# If right click, try to delete a curve point
	elif mouse_press[2] and clicked == False:
		clicked = True

		point = curves[mode].check_click(mouse_pos, True)
		if point != -1:
			curves[mode].delete(point)

	# If the mouse isn't clicked, set clicked to false so we can't register multiple clicks for one
	elif not mouse_press[0] and not mouse_press[2]:
		clicked = False
		curves[mode].moving = -1

	# Update the screen and set the maximum fps to 30
	pygame.display.update()
	clock.tick(30)
