# Dungeon Delver 🎮

A feature-rich roguelike game built with Python and PyQt6, featuring procedural dungeon generation, class-based combat, and stunning particle effects.

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Requirements
- Python 3.8+
- PyQt6

## 🎮 Gameplay

- **Choose your class**: Warrior, Mage, Rogue, or Ranger
- **Explore procedurally generated dungeons** with rooms and corridors
- **Fight enemies**: Goblins, Skeletons, and Dragons
- **Collect loot**: Equipment with rarities from Common to Legendary
- **Use abilities**: 3 unique abilities per class with cooldowns
- **Level up**: Gain XP, increase stats, descend deeper

### Controls
- **WASD/Arrows** - Move & attack (bump into enemies)
- **1/2/3** - Use abilities
- **R** - Restart
- **Q** - Quit

## 🏗️ Architecture

### Core Modules

| File | Purpose |
|------|---------|
| `main.py` | Entry point, initializes PyQt6 application |
| `game.py` | Game state, turn management, core game loop |
| `ui.py` | PyQt6 widgets (rendering, input, UI panels) |
| `entities.py` | Player, Enemy, Item classes with stats |
| `dungeon.py` | Procedural dungeon generation (BSP rooms) |
| `combat.py` | Damage calculation and combat resolution |
| `abilities.py` | Ability system with cooldowns and effects |
| `animations.py` | Visual effects (particles, trails, screen shake) |
| `graphics.py` | Geometric shape rendering for entities/tiles |
| `constants.py` | All game configuration and constants |

### Game Flow

```
Class Selection → Dungeon Generation → Turn-Based Loop → Level Up → Descend Stairs
```

## 🎨 Key Systems

### 1. Class System
Each class has unique stats and abilities:

```python
CLASS_STATS = {
    CLASS_WARRIOR: {"hp": 120, "attack": 12, "defense": 8},
    CLASS_MAGE: {"hp": 70, "attack": 15, "defense": 3},
    CLASS_ROGUE: {"hp": 85, "attack": 13, "defense": 4, "crit_chance": 0.25},
    CLASS_RANGER: {"hp": 90, "attack": 11, "defense": 5},
}
```

### 2. Equipment System
- **4 slots**: Weapon, Armor, Accessory, Boots
- **Auto-equipping** on pickup
- **Dynamic stats** via `@property` decorators
- **5 rarities**: Common → Uncommon → Rare → Epic → Legendary

### 3. Abilities System
- **Cooldown-based** tactical abilities
- **6 unique abilities**: Fireball, Dash, Heal, Frost Nova, Whirlwind, Shadow Step
- **Visual effects** with particle trails and impacts

### 4. Animation System
- **60 FPS** update loop with delta time
- **Particle types**: Directional, Trail, Ambient, Standard
- **Effects**: Floating text, screen shake, flash effects, death bursts
- **Layered rendering** for visual depth

### 5. Procedural Generation
- **Dungeon**: Random room placement with corridor connections
- **Items**: Rarity scales with dungeon level (better drops deeper)
- **Enemies**: Level modifier increases stats: `1.0 + (level - 1) * 0.3`

## 🔧 Adding New Content

### Add a New Class

```python
# 1. constants.py - Define class constant
CLASS_NECROMANCER = "necromancer"

# 2. Add stats and color
CLASS_STATS[CLASS_NECROMANCER] = {"hp": 80, "attack": 14, "defense": 4, "description": "..."}
COLOR_CLASS_NECROMANCER = QColor(100, 50, 100)

# 3. abilities.py - Create ability set
CLASS_ABILITIES[CLASS_NECROMANCER] = [SummonUndead(), DrainLife(), DarkPact()]

# 4. graphics.py - Add visual in draw_player()
elif class_type == c.CLASS_NECROMANCER:
    # Draw skull/staff shape

# 5. ui.py - Add to class selection screen
```

### Add a New Ability

```python
# abilities.py
class NewAbility(Ability):
    def __init__(self):
        super().__init__("Ability Name", "Description", cooldown=5, ability_type="damage")

    def use(self, user, target_pos, game):
        success, msg = super().use(user, target_pos, game)
        if not success:
            return (success, msg)

        # Your ability logic here
        # Add visual effects:
        # game.anim_manager.add_ability_trail(x, y, color, "ability_type")
        # game.anim_manager.add_directional_impact(...)

        return (True, "Success message!")
```

### Add a New Enemy

```python
# constants.py
ENEMY_VAMPIRE = "vampire"
ENEMY_STATS[ENEMY_VAMPIRE] = {"hp": 80, "attack": 12, "defense": 6, "xp": 50}
COLOR_ENEMY_VAMPIRE = QColor(150, 0, 0)

# graphics.py - Add to draw_enemy()
elif enemy_type == c.ENEMY_VAMPIRE:
    # Draw bat/vampire shape with fangs

# game.py - Update spawn weights in _spawn_enemies()
```

### Add a New Item Type

```python
# constants.py
ITEM_HELMET = "helmet"
SYMBOL_HELMET = "^"
EQUIPMENT_TYPES[ITEM_HELMET] = SLOT_HEAD  # If equippable
ITEM_EFFECTS[ITEM_HELMET] = {"defense": 4}

# graphics.py - Add to draw_item()
elif item_type == c.ITEM_HELMET:
    # Draw helmet shape

# game.py - Add to _spawn_items() item_types list
```

## 🎨 Graphics & Visuals

### Particle Effects
The game features a sophisticated particle system with multiple layers:

**Directional Particles** - Spray away from impacts with friction
```python
game.anim_manager.add_directional_impact(x, y, from_x, from_y, color, count=10)
```

**Ability Trails** - Unique visual signatures per ability
```python
game.anim_manager.add_ability_trail(x, y, color, "fireball")  # Fire trail
game.anim_manager.add_ability_trail(x, y, color, "ice")       # Ice crystals
game.anim_manager.add_ability_trail(x, y, color, "dash")      # Speed lines
```

**Death Bursts** - Enemy-specific particle explosions
```python
game.anim_manager.add_death_burst(x, y, enemy_type)
```

**Ambient Atmosphere** - Floating dust particles for immersion

### Rendering Pipeline
1. Draw tiles (floor/wall/stairs)
2. Draw entities with geometric shapes
3. Draw enemy health bars
4. Draw flash effects (damage overlay)
5. Draw ambient particles (background)
6. Draw trail effects
7. Draw regular particles
8. Draw directional impact particles
9. Draw floating damage text
10. Draw game over overlay

## ⚡ Performance Tips

- Animation update: **O(n)** where n = active animations
- Enemy AI: **O(n)** where n = enemy count
- Rendering: **O(grid_size)** + O(animations)
- Target: **60 FPS** achievable with <100 entities
- Ambient particles auto-spawn every 0.5s (2-4 particles)

## 🎯 Balancing

### Key Constants (constants.py)
```python
DAMAGE_VARIANCE = 0.2           # +/- 20% damage variance
ENEMIES_PER_LEVEL_BASE = 5      # Base enemy count
ITEMS_PER_LEVEL = 3             # Items per level
MAX_ROOMS = 15                  # Dungeon room count
```

### Rarity Drop Rates
- **Common**: 60% → 20% (scales with level)
- **Uncommon**: 30% → 40%
- **Rare**: 8% → 28%
- **Epic**: 2% → 10%
- **Legendary**: 0% → 2%

## 🐛 Common Pitfalls

1. **Importing**: New modules need imports in `game.py` and `ui.py`
2. **Cooldowns**: Always call `_reduce_ability_cooldowns()` after turns
3. **Animation cleanup**: AnimationManager auto-removes dead animations
4. **Equipment stats**: Use `@property` decorators for dynamic calculation
5. **Turn consumption**: Abilities that fail should NOT consume turn (refund cooldown)

## 📝 Code Style

- Type hints on parameters and returns
- Docstrings for all classes and public methods
- Constants in `UPPER_CASE`
- Private methods prefixed with `_`
- Color values use `QColor` objects
- Messages use tuple format: `(message, type)` for color coding

## 🔮 Future Ideas

- **Status Effects**: Poison, Burn, Stun with visual indicators
- **Field of View**: Fog of war, stealth mechanics
- **Boss Fights**: Multi-phase bosses every 5 floors
- **Biomes**: Different dungeon themes (catacombs, lava, ice)
- **Environmental Hazards**: Traps, spike pits, lava tiles
- **Meta Progression**: Unlock new classes/abilities between runs
- **Sound & Music**: Audio feedback for actions

## 📄 License

Your choice - have fun building!

## 🤝 Contributing

Feel free to fork, modify, and expand this game. The architecture is designed to be modular and extensible.

---

**Built with**: Python 3, PyQt6
**Architecture**: MVC pattern (Model: game.py, View: ui.py, Controller: input handling)
**Graphics**: Geometric shapes with particle effects (no sprites needed!)
