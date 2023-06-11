from pygame.math import Vector2

screen_width = 1280
screen_height = 720
tile_size = 64

overlay_positions = {"tool": (40, screen_height - 15), "seed": (70, screen_height - 5)}

player_tool_offset = {
    "left": Vector2(-50, 40),
    "right": Vector2(50, 40),
    "up": Vector2(0, -10),
    "down": Vector2(0, 50),
}

layers = {
    "water": 0,
    "ground": 1,
    "soil": 2,
    "soil water": 3,
    "rain floor": 4,
    "house bottom": 5,
    "ground plant": 6,
    "main": 7,
    "house top": 8,
    "fruit": 9,
    "rain drops": 10,
}

apple_pos = {
    "Small": [(18, 17), (30, 37), (12, 50), (30, 45), (20, 30), (30, 10)],
    "Large": [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)],
}

grow_speed = {"corn": 1, "tomato": 0.7}

sale_prices = {"wood": 4, "apple": 2, "corn": 10, "tomato": 20}

purchase_prices = {"corn": 4, "tomato": 5}
