"""
Game constants and configuration for Dungeon Delver
"""
from PyQt6.QtGui import QColor

# Grid settings
GRID_WIDTH = 50
GRID_HEIGHT = 30
TILE_SIZE = 24  # pixels (increased for better visibility)

# Window settings
SIDEBAR_WIDTH = 300
WINDOW_WIDTH = GRID_WIDTH * TILE_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT * TILE_SIZE

# Colors - Improved palette
COLOR_FLOOR = QColor(45, 45, 48)  # Dark floor
COLOR_WALL = QColor(30, 30, 35)  # Darker walls
COLOR_PLAYER = QColor(100, 200, 255)  # Bright blue
COLOR_PLAYER_BORDER = QColor(50, 100, 200)
COLOR_ENEMY_GOBLIN = QColor(100, 220, 80)  # Green
COLOR_ENEMY_SKELETON = QColor(220, 220, 220)  # White
COLOR_ENEMY_DRAGON = QColor(255, 80, 60)  # Red
COLOR_ITEM_POTION = QColor(255, 50, 200)  # Magenta
COLOR_ITEM_WEAPON = QColor(255, 215, 0)  # Gold
COLOR_ITEM_ARMOR = QColor(150, 180, 255)  # Light blue
COLOR_STAIRS = QColor(150, 100, 255)  # Purple

# Text colors
COLOR_TEXT_LIGHT = QColor(220, 220, 220)
COLOR_TEXT_DARK = QColor(20, 20, 25)

# Message colors
COLOR_MSG_DAMAGE = "#ff6b6b"
COLOR_MSG_HEAL = "#51cf66"
COLOR_MSG_ITEM = "#ffd43b"
COLOR_MSG_EVENT = "#74c0fc"
COLOR_MSG_DEATH = "#ff4444"
COLOR_MSG_LEVELUP = "#a9e34b"

# UI colors
COLOR_PANEL_BG = QColor(35, 35, 40)
COLOR_HP_BAR_FULL = QColor(80, 200, 120)
COLOR_HP_BAR_MID = QColor(255, 193, 7)
COLOR_HP_BAR_LOW = QColor(244, 67, 54)
COLOR_HP_BAR_BG = QColor(50, 50, 55)
COLOR_XP_BAR = QColor(138, 43, 226)
COLOR_XP_BAR_BG = QColor(50, 50, 55)

# Symbols for entities
SYMBOL_PLAYER = "@"
SYMBOL_GOBLIN = "g"
SYMBOL_SKELETON = "s"
SYMBOL_DRAGON = "D"
SYMBOL_POTION = "!"
SYMBOL_SWORD = "/"
SYMBOL_SHIELD = "]"
SYMBOL_STAIRS = ">"
SYMBOL_WALL = "#"
SYMBOL_FLOOR = "."

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
