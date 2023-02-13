import pygame

class button():

	def __init__(self, text_size, pos, text, side_size = 1.6, top_size = 1.4):
		self.text = text
		self.pos = list(pos)
		self.high_pos = list(pos[:])
		self.text_size = text_size
		self.font = pygame.font.SysFont("Monokai", self.text_size, True)
		self.size = self.font.size(text)
		self.surf_size = (self.size[0] * side_size, self.size[1] * top_size)
		self.high_size = (self.surf_size[0] * 1.05, self.surf_size[1])
		self.pressed = False
		self.highlighted = False

		# normal button surface
		self.surf = pygame.Surface(self.surf_size)
		self.surf.fill((20, 20, 20))
		text_surf = self.font.render(self.text, False, (200, 200, 200))
		self.surf.blit(text_surf, ((self.surf_size[0] - self.size[0]) / 2, text_size / 2))
		pygame.draw.rect(self.surf, ((50, 50, 50)), ((0, 0) + self.surf_size), int(text_size / 6))


		# highlighted button surface
		self.high_surf = pygame.Surface(self.high_size)
		self.high_surf.fill((20, 20, 20))
		text_surf = self.font.render(self.text, False, (200, 200, 200))
		self.high_surf.blit(text_surf, ((self.high_size[0] - self.size[0]) / 2, text_size / 2))
		pygame.draw.rect(self.high_surf, ((50, 50, 50)), ((0, 0) + self.high_size), int(text_size / 6))

		self.pos[0] = (self.pos[0]  - (self.surf_size[0] / 2))
		self.high_pos[0] = (self.high_pos[0]  - (self.high_size[0] / 2))

	def draw(self, window, mouse_pos, mouse_press, off_y = 0):
		self.pressed = False
		if mouse_pos[0] < self.pos[0] or mouse_pos[0] > self.pos[0] + self.surf_size[0]:
			window.blit(self.surf, (self.pos[0], self.pos[1] + off_y))
			self.highlighted = False
		elif mouse_pos[1] < self.pos[1] or mouse_pos[1] > self.pos[1] + self.surf_size[1]:
			window.blit(self.surf, (self.pos[0], self.pos[1] + off_y))
			self.highlighted = False
		else:
			window.blit(self.high_surf, (self.high_pos[0], self.high_pos[1] + off_y))
			self.highlighted = True
			if mouse_press:
				self.pressed = True
