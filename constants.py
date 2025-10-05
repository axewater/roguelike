"""
Game constants and configuration for Dungeon Delver
"""
from PyQt6.QtGui import QColor

# Grid settings
GRID_WIDTH = 50
GRID_HEIGHT = 30
TILE_SIZE = 48  # pixels (2x scale for detailed sprites)

# Viewport/Camera settings
VIEWPORT_WIDTH = 25   # Tiles visible on screen
VIEWPORT_HEIGHT = 15  # Tiles visible on screen

# Window settings
SIDEBAR_WIDTH = 600
WINDOW_WIDTH = VIEWPORT_WIDTH * TILE_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = VIEWPORT_HEIGHT * TILE_SIZE

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

# Enemy health bar colors
COLOR_ENEMY_HP_BAR = QColor(220, 80, 80)
COLOR_ENEMY_HP_BAR_BG = QColor(40, 40, 40, 180)
COLOR_ENEMY_HP_BAR_BORDER = QColor(20, 20, 20)

# Sidebar section colors
COLOR_SECTION_BG = QColor(42, 42, 47)
COLOR_SECTION_BORDER = QColor(60, 60, 65)
COLOR_DIVIDER = QColor(70, 70, 75)

# Symbols for entities
SYMBOL_PLAYER = "@"
SYMBOL_GOBLIN = "g"
SYMBOL_SKELETON = "s"
SYMBOL_DRAGON = "D"
SYMBOL_POTION = "!"
SYMBOL_SWORD = "/"
SYMBOL_SHIELD = "]"
SYMBOL_BOOTS = "["
SYMBOL_RING = "o"
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

# Player class types
CLASS_WARRIOR = "warrior"
CLASS_MAGE = "mage"
CLASS_ROGUE = "rogue"
CLASS_RANGER = "ranger"

# Class stats [HP, Attack, Defense]
CLASS_STATS = {
    CLASS_WARRIOR: {"hp": 120, "attack": 12, "defense": 8, "description": "High HP tank with strong defense"},
    CLASS_MAGE: {"hp": 70, "attack": 15, "defense": 3, "description": "Glass cannon with powerful attacks"},
    CLASS_ROGUE: {"hp": 85, "attack": 13, "defense": 4, "crit_chance": 0.25, "description": "High critical hit chance and dodge"},
    CLASS_RANGER: {"hp": 90, "attack": 11, "defense": 5, "description": "Balanced fighter with ranged capabilities"},
}

# Class colors
COLOR_CLASS_WARRIOR = QColor(200, 100, 100)  # Red
COLOR_CLASS_MAGE = QColor(100, 150, 255)  # Blue
COLOR_CLASS_ROGUE = QColor(180, 100, 255)  # Purple
COLOR_CLASS_RANGER = QColor(100, 200, 100)  # Green

# Ability colors and visual settings
ABILITY_ICON_SIZE = 70  # Diameter of circular ability icons
ABILITY_ICON_SPACING = 12  # Space between icons

# Ability-specific colors
COLOR_ABILITY_FIREBALL = QColor(255, 120, 40)  # Orange-red fire
COLOR_ABILITY_FIREBALL_SECONDARY = QColor(255, 60, 0)  # Deep red
COLOR_ABILITY_DASH = QColor(120, 180, 255)  # Electric blue
COLOR_ABILITY_DASH_SECONDARY = QColor(200, 220, 255)  # Light blue
COLOR_ABILITY_HEALING = QColor(80, 220, 120)  # Vibrant green
COLOR_ABILITY_HEALING_SECONDARY = QColor(180, 255, 200)  # Light green
COLOR_ABILITY_FROST = QColor(150, 220, 255)  # Ice blue
COLOR_ABILITY_FROST_SECONDARY = QColor(200, 240, 255)  # Pale ice
COLOR_ABILITY_WHIRLWIND = QColor(255, 100, 100)  # Red
COLOR_ABILITY_WHIRLWIND_SECONDARY = QColor(255, 180, 180)  # Light red
COLOR_ABILITY_SHADOW = QColor(120, 60, 180)  # Dark purple
COLOR_ABILITY_SHADOW_SECONDARY = QColor(60, 20, 100)  # Deep shadow

# Ability icon states
COLOR_ABILITY_READY_GLOW = QColor(255, 255, 150)  # Golden glow when ready
COLOR_ABILITY_COOLDOWN_OVERLAY = QColor(20, 20, 30, 200)  # Dark overlay
COLOR_ABILITY_BORDER = QColor(80, 80, 90)  # Default border
COLOR_ABILITY_HOVER_BORDER = QColor(200, 200, 220)  # Hover border

# Enemy types
ENEMY_GOBLIN = "goblin"
ENEMY_SKELETON = "skeleton"
ENEMY_DRAGON = "dragon"

# Item types
ITEM_HEALTH_POTION = "health_potion"
ITEM_SWORD = "sword"
ITEM_SHIELD = "shield"
ITEM_BOOTS = "boots"
ITEM_RING = "ring"

# Equipment slots
SLOT_WEAPON = "weapon"
SLOT_ARMOR = "armor"
SLOT_ACCESSORY = "accessory"
SLOT_BOOTS = "boots"

# Equipment item types (can be equipped)
EQUIPMENT_TYPES = {
    ITEM_SWORD: SLOT_WEAPON,
    ITEM_SHIELD: SLOT_ARMOR,
    ITEM_BOOTS: SLOT_BOOTS,
    ITEM_RING: SLOT_ACCESSORY,
}

# Item rarities
RARITY_COMMON = "common"
RARITY_UNCOMMON = "uncommon"
RARITY_RARE = "rare"
RARITY_EPIC = "epic"
RARITY_LEGENDARY = "legendary"

# Rarity colors
COLOR_RARITY_COMMON = QColor(180, 180, 180)  # Gray
COLOR_RARITY_UNCOMMON = QColor(100, 200, 100)  # Green
COLOR_RARITY_RARE = QColor(100, 150, 255)  # Blue
COLOR_RARITY_EPIC = QColor(200, 100, 255)  # Purple
COLOR_RARITY_LEGENDARY = QColor(255, 180, 0)  # Gold

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

# Item effects (base values, modified by rarity)
ITEM_EFFECTS = {
    ITEM_HEALTH_POTION: {"heal": 30},
    ITEM_SWORD: {"attack": 5},
    ITEM_SHIELD: {"defense": 3},
    ITEM_BOOTS: {"defense": 2},
    ITEM_RING: {"attack": 2, "defense": 1},
}

# Dungeon generation
MIN_ROOM_SIZE = 4
MAX_ROOM_SIZE = 10
MAX_ROOMS = 15
ENEMIES_PER_LEVEL_BASE = 5
ITEMS_PER_LEVEL = 3

# Game mechanics
DAMAGE_VARIANCE = 0.2  # +/- 20% damage variance
