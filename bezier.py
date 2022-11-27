import pygame

pygame.init()

running = True

window = pygame.display.set_mode((900, 600))

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False