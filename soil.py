import pygame
from pygame.sprite import Group
from settings import *
from pytmx.util_pygame import load_pygame


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = layers["soil"]


class SoilLayer:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        self.soil_surf = pygame.image.load("./setup/graphics/soil/o.png")

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):
        ground = pygame.image.load("./setup/graphics/world/ground.png")
        h_tiles, v_tiles = (
            ground.get_width() // tile_size,
            ground.get_height() // tile_size,
        )

        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, _ in (
            load_pygame("./setup/data/map.tmx").get_layer_by_name("Farmable").tiles()
        ):
            self.grid[y][x].append("F")

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if "F" in cell:
                    x = index_col * tile_size
                    y = index_row * tile_size
                    rect = pygame.Rect(x, y, tile_size, tile_size)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // tile_size
                y = rect.y // tile_size

                if "F" in self.grid[y][x]:
                    self.grid[y][x].append("X")
                    self.create_soil_tiles()

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if "X" in cell:
                    SoilTile(
                        pos=(index_col * tile_size, index_row * tile_size),
                        surf=self.soil_surf,
                        groups=[self.all_sprites, self.soil_sprites],
                    )
