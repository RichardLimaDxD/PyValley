import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain
from random import randint


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        self.soil_layer = SoilLayer(self.all_sprites)
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)

        self.rain = Rain(self.all_sprites)
        self.raining = randint(0, 10) > 3
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()

    def setup(self):
        tmx_data = load_pygame("./setup/data/map.tmx")

        for layer in ["HouseFloor", "HouseFurnitureBottom"]:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    (x * tile_size, y * tile_size),
                    surf,
                    self.all_sprites,
                    layers["house bottom"],
                )

        for layer in ["HouseWalls", "HouseFurnitureTop"]:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * tile_size, y * tile_size), surf, self.all_sprites)

        for x, y, surf in tmx_data.get_layer_by_name("Fence").tiles():
            Generic(
                (x * tile_size, y * tile_size),
                surf,
                [self.all_sprites, self.collision_sprites],
            )

        water_frames = import_folder("./setup/graphics/water")
        for x, y, surf in tmx_data.get_layer_by_name("Water").tiles():
            Water((x * tile_size, y * tile_size), water_frames, self.all_sprites)

        for obj in tmx_data.get_layer_by_name("Trees"):
            Tree(
                pos=(obj.x, obj.y),
                surf=obj.image,
                groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],
                name=obj.name,
                player_add=self.player_add,
            )

        for obj in tmx_data.get_layer_by_name("Decoration"):
            WildFlower(
                (obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites]
            )

        for x, y, surf in tmx_data.get_layer_by_name("Collision").tiles():
            Generic(
                (x * tile_size, y * tile_size),
                pygame.Surface((tile_size, tile_size)),
                self.collision_sprites,
            )

        for obj in tmx_data.get_layer_by_name("Player"):
            if obj.name == "Start":
                self.player = Player(
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    tree_sprites=self.tree_sprites,
                    interaction=self.interaction_sprites,
                    soil_layer=self.soil_layer,
                )
            if obj.name == "Bed":
                Interaction(
                    (obj.x, obj.y),
                    (obj.width, obj.height),
                    self.interaction_sprites,
                    obj.name,
                )

        Generic(
            pos=(0, 0),
            surf=pygame.image.load("./setup/graphics/world/ground.png").convert_alpha(),
            groups=self.all_sprites,
            z=layers["ground"],
        )

    def player_add(self, item):
        self.player.item_inventory[item] += 1

    def reset(self):
        self.soil_layer.remove_water()

        self.raining = randint(0, 10) > 3
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()

        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()

    def run(self, dt):
        self.display_surface.fill("black")
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()

        if self.raining:
            self.rain.update()

        if self.player.sleep:
            self.transition.play()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - screen_width / 2
        self.offset.y = player.rect.centery - screen_height / 2

        for layer in layers.values():
            for sprite in sorted(
                self.sprites(), key=lambda sprite: sprite.rect.centery
            ):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
