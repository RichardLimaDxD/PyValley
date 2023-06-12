import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree
from pytmx.util_pygame import load_pygame
from support import *

class Level:
	def __init__(self):

		
		self.display_surface = pygame.display.get_surface()

		
		self.all_sprites = CameraGroup()

		self.setup()
		self.overlay = Overlay(self.player)

	def setup(self):
		tmx_data = load_pygame('./setup/data/map.tmx')

		
		for layer in ['HouseFloor', 'HouseFurnitureBottom']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * tile_size,y * tile_size), surf, self.all_sprites, layers['house bottom'])

		for layer in ['HouseWalls', 'HouseFurnitureTop']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x * tile_size,y * tile_size), surf, self.all_sprites)

		
		for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
			Generic((x * tile_size,y * tile_size), surf, self.all_sprites)

		 
		water_frames = import_folder('./setup/graphics/water')
		for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x * tile_size,y * tile_size), water_frames, self.all_sprites)

		 
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree((obj.x, obj.y), obj.image, self.all_sprites, obj.name)

		 
		for obj in tmx_data.get_layer_by_name('Decoration'):
			WildFlower((obj.x, obj.y), obj.image, self.all_sprites)

		self.player = Player((640,360), self.all_sprites)
		Generic(
			pos = (0,0),
			surf = pygame.image.load('./setup/graphics/world/ground.png').convert_alpha(),
			groups = self.all_sprites,
			z = layers['ground'])

	def run(self,dt):
		self.display_surface.fill('black')
		self.all_sprites.custom_draw(self.player)
		self.all_sprites.update(dt)

		self.overlay.display()

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - screen_width / 2
		self.offset.y = player.rect.centery - screen_height / 2

		for layer in layers.values():
			for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)