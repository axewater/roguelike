"""
Game constants and configuration for Dungeon Delver
"""
from PyQt6.QtGui import QColor

# Grid settings
GRID_WIDTH = 50
GRID_HEIGHT = 30
TILE_SIZE = 20  # pixels

# Window settings
SIDEBAR_WIDTH = 250
WINDOW_WIDTH = GRID_WIDTH * TILE_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT * TILE_SIZE

# Colors
COLOR_FLOOR = QColor(240, 240, 240)
COLOR_WALL = QColor(60, 60, 60)
COLOR_PLAYER = QColor(50, 150, 255)
COLOR_ENEMY_GOBLIN = QColor(150, 255, 100)
COLOR_ENEMY_SKELETON = QColor(200, 200, 200)
COLOR_ENEMY_DRAGON = QColor(255, 50, 50)
COLOR_ITEM_POTION = QColor(255, 100, 255)
COLOR_ITEM_WEAPON = QColor(255, 200, 50)
COLOR_ITEM_ARMOR = QColor(150, 150, 255)
COLOR_STAIRS = QColor(100, 100, 255)

# Tile types
TILE_FLOOR = 0
TILE_WALL = 1
TILE_STAIRS = 2

# Entity types
ENTITY_PLAYER = "player"
ENTITY_ENEMY = "enemy"
ENTITY_ITEM = "item"

# Enemy types
ENEMY_GOBLIN = "goblin"
ENEMY_SKELETON = "skeleton"
ENEMY_DRAGON = "dragon"

# Item types
ITEM_HEALTH_POTION = "health_potion"
ITEM_SWORD = "sword"
ITEM_SHIELD = "shield"

# Player starting stats
PLAYER_START_HP = 100
PLAYER_START_MAX_HP = 100
PLAYER_START_ATTACK = 10
PLAYER_START_DEFENSE = 5

# Enemy stats [HP, Attack, Defense]
ENEMY_STATS = {
    ENEMY_GOBLIN: {"hp": 30, "attack": 5, "defense": 2, "xp": 10},
    ENEMY_SKELETON: {"hp": 50, "attack": 8, "defense": 4, "xp": 20},
    ENEMY_DRAGON: {"hp": 150, "attack": 20, "defense": 10, "xp": 100},
}

# Item effects
ITEM_EFFECTS = {
    ITEM_HEALTH_POTION: {"heal": 30},
    ITEM_SWORD: {"attack": 5},
    ITEM_SHIELD: {"defense": 3},
}

# Dungeon generation
MIN_ROOM_SIZE = 4
MAX_ROOM_SIZE = 10
MAX_ROOMS = 15
ENEMIES_PER_LEVEL_BASE = 5
ITEMS_PER_LEVEL = 3

# Game mechanics
DAMAGE_VARIANCE = 0.2  # +/- 20% damage variance
