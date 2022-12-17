import pygame, math

pygame.init()

running = True
clicked = False
pressed = False
points = [(140, 50), (400, 200)]
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
	window.fill((30, 50, 60))
	pygame.draw.lines(window, (220, 220, 220), False, points, 3)
	for point in points:
		pygame.draw.circle(window, (220, 220, 220), point, 7, 3)
	if animate:
		for lerp in lerp1:
			pygame.draw.circle(window, (220, 220, 220), lerp, 5, 2)
	pygame.display.update()


	
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
			print(points, "\n\n", slopes, "\n\n", lengths, "\n\n")
		if pygame.mouse.get_pos() in points:
			pass
	else:
		clicked = False

	draw_lines()
		
	key_press = pygame.key.get_pressed()
	if key_press[pygame.K_RETURN]:
		if not pressed:
			animate = True
			pressed = True
	else:
		pressed = False

	if animate:
		step = step + direction
		print(lerp1[0])
		if step == 200 or step == 0:
			direction = -direction

		for lerp in range(len(lerp1)):
			lerp1[lerp][0] += (lengths[lerp] * step) / (slopes[lerp] * 200)
			lerp1[lerp][1] += (slopes[lerp] * lengths[lerp] * step) / 200

	clock.tick(30)


