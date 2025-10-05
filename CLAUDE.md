# Dungeon Delver - Developer Guide

## 🎮 Architecture Overview

### Core Modules

- **main.py** - Entry point, initializes PyQt6 application
- **game.py** - Game state, logic, turn management
- **entities.py** - Player, Enemy, Item classes with stats
- **dungeon.py** - Procedural dungeon generation (rooms + corridors)
- **combat.py** - Damage calculation and combat resolution
- **ui.py** - PyQt6 widgets (GameWidget, StatsPanel, ClassSelectionScreen)
- **animations.py** - Visual effects (particles, floating text, screen shake)
- **abilities.py** - Ability system with cooldowns
- **constants.py** - All game configuration and constants

### Game Flow

1. **Class Selection** → Choose from 4 classes (Warrior/Mage/Rogue/Ranger)
2. **Dungeon Generation** → Procedural rooms with enemies/items
3. **Turn-Based Loop** → Player action → Enemy turn → Cooldowns tick
4. **Progression** → Level up, find loot, descend stairs

## 🏗️ Key Systems

### Class System
- Each class has unique stats (HP, ATK, DEF)
- Class-specific abilities (3 per class)
- Visual distinction with color coding

```python
CLASS_STATS = {
    CLASS_WARRIOR: {"hp": 120, "attack": 12, "defense": 8},
    CLASS_MAGE: {"hp": 70, "attack": 15, "defense": 3},
    # ...
}
```

### Equipment System
- 4 slots: Weapon, Armor, Accessory, Boots
- Automatic equipping on pickup
- Stats calculated dynamically via @property

```python
@property
def attack(self) -> int:
    bonus = 0
    if self.equipment[SLOT_WEAPON]:
        bonus += self.equipment[SLOT_WEAPON].get_stat_bonus("attack")
    return self.base_attack + bonus
```

### Rarity System
- 5 tiers: Common → Uncommon → Rare → Epic → Legendary
- Rarity multipliers: 1.0x → 1.2x → 1.5x → 2.0x → 3.0x
- Drop rates scale with dungeon level
- Visual distinction via color coding

```python
rarity_mult = {
    "common": 1.0,
    "legendary": 3.0,
}.get(self.rarity, 1.0)
return int((base_bonus + affix_bonus) * rarity_mult)
```

### Abilities System
- Cooldown-based tactical abilities
- 6 unique abilities: Fireball, Dash, Heal, Frost Nova, Whirlwind, Shadow Step
- Abilities trigger animations and effects

```python
class Fireball(Ability):
    def use(self, user, target_pos, game):
        # Deal AOE damage
        # Create animations
        # Return (success, message)
```

### Animation System
- 60 FPS update loop with delta time
- FloatingText, FlashEffect, Particle, ScreenShake classes
- AnimationManager tracks all active effects

```python
game.anim_manager.add_floating_text(x, y, "50", QColor(255, 100, 100))
game.anim_manager.add_screen_shake(5.0, 0.2)
```

## 🎨 Adding New Content

### Add a New Class
1. Add constant in `constants.py`: `CLASS_NECROMANCER = "necromancer"`
2. Define stats in `CLASS_STATS` dict
3. Add color: `COLOR_CLASS_NECROMANCER = QColor(...)`
4. Create ability set in `abilities.py`: `CLASS_ABILITIES[CLASS_NECROMANCER] = [...]`
5. Add to class selection UI in `ui.py`

### Add a New Ability
1. Create class extending `Ability` in `abilities.py`
2. Implement `use()` method with logic
3. Add animations via `game.anim_manager`
4. Add to class ability sets: `CLASS_ABILITIES[CLASS_X].append(NewAbility())`

### Add a New Item Type
1. Define constant: `ITEM_HELMET = "helmet"`
2. Add symbol: `SYMBOL_HELMET = "^"`
3. Add to `EQUIPMENT_TYPES` if equippable
4. Define effects in `ITEM_EFFECTS`
5. Update `_spawn_items()` in `game.py`
6. Add rendering logic in `ui.py`

### Add a New Enemy
1. Add constant: `ENEMY_VAMPIRE = "vampire"`
2. Define stats in `ENEMY_STATS`
3. Add symbol and color in `constants.py`
4. Implement AI in `Enemy.get_ai_action()` if custom behavior needed
5. Update spawn weights in `game._spawn_enemies()`

## 🔧 Technical Details

### Turn Management
- Player action consumes turn → `_enemy_turn()` → `_reduce_ability_cooldowns()`
- Abilities that succeed consume turn, failures don't

### Procedural Generation
- Dungeon: Rooms placed randomly, connected with corridors
- Items: Rarity scales with level (better drops deeper)
- Enemies: Level modifier increases stats: `1.0 + (level - 1) * 0.3`

### Rendering Pipeline
1. Draw tiles (floor/wall/stairs)
2. Draw entity backgrounds (colored tiles)
3. Draw entity symbols (ASCII characters)
4. Draw flash effects (damage overlay)
5. Draw particles (blood, sparkles)
6. Draw floating text (damage numbers)
7. Draw game over overlay (if dead)

### Coordinate System
- Grid: 50x30 tiles
- Tile size: 24 pixels
- Origin: Top-left (0, 0)
- Sidebar: 300px width

## 🐛 Common Pitfalls

1. **Forgetting to import** - New modules need imports in `game.py` and `ui.py`
2. **Cooldown logic** - Always call `_reduce_ability_cooldowns()` after turn
3. **Animation cleanup** - AnimationManager auto-removes dead animations
4. **Equipment stats** - Use @property decorators, recalc on equip/unequip
5. **Item rarity** - Consumables ignore rarity, equipment uses multipliers

## 📊 Performance Notes

- Animation update: O(n) where n = active animations
- Enemy AI: O(n) where n = enemy count
- Rendering: O(grid_size) + O(animations)
- 60 FPS target achievable with <100 entities

## 🎯 Future Expansion Ideas

- **Status Effects** - Poison, Burn, Stun, Freeze with visual indicators
- **Field of View** - Fog of war, stealth mechanics
- **Boss Fights** - Multi-phase bosses every 5 floors
- **Biomes** - Visual themes (dungeon, catacombs, lava, ice, void)
- **Environmental Hazards** - Traps, lava tiles, spike pits
- **Meta Progression** - Unlock new classes/abilities with currency
- **Sound** - Music and SFX via pygame.mixer or similar

## 🔑 Key Files to Modify

- **Game balance**: `constants.py` (all stats, drop rates, cooldowns)
- **New mechanics**: `game.py` (core game loop)
- **Visual effects**: `animations.py` (particles, shakes, etc.)
- **UI changes**: `ui.py` (widgets, rendering, input)
- **Combat math**: `combat.py` (damage formulas)

## 📝 Code Style

- Type hints on function parameters and returns
- Docstrings for all classes and public methods
- Constants in UPPER_CASE
- Private methods prefixed with `_`
- Color values use QColor objects
- Messages use tuple format: `(message, type)` for color coding

---

**Built with**: Python 3, PyQt6
**Architecture**: MVC pattern (Model: game.py, View: ui.py, Controller: input handling)
**License**: Your choice - have fun building!
