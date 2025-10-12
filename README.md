# Claude-Like - A 2D→3D Roguelike Journey 🎮

A feature-rich roguelike game built with Python and PyQt6, **currently migrating from 2D to 3D** using Ursina Engine. This guide helps developers understand the codebase structure and track the migration progress.

## 🚀 Migration Status: 2D → 3D

**Target:** Transform the complete 2D roguelike into a full 3D experience while preserving all gameplay mechanics.

### Current State

**🎮 Game is now FULLY PLAYABLE in 3D mode!** Run with `python main.py --mode 3d`

| System | 2D (Legacy) | 3D (New) | Status |
|--------|-------------|----------|--------|
| **Dungeon Rendering** | ✅ Complete | ✅ **Fully Visible** | **Phase 3** ✅ |
| **Player Models** | ✅ Complete | ✅ **Playable Cube** | **Phase 3** ✅ |
| **Player Movement** | ✅ Complete | ✅ **WASD Controls** | **Phase 3** ✅ |
| **Combat System** | ✅ Complete | ✅ **Bump-to-Attack** | **Phase 3** ✅ |
| **Level Progression** | ✅ Complete | ✅ **Stairs & Descent** | **Phase 3** ✅ |
| **Game Loop** | ✅ Complete | ✅ **40-45 FPS** | **Phase 3** ✅ |
| **Enemy Models** | ✅ Complete | ⏳ Not Started | Phase 4 |
| **Item Models** | ✅ Complete | ⏳ Not Started | Phase 4 |
| **Particle System** | ✅ Complete | ⏳ Not Started | Phase 5 |
| **Ability Effects** | ✅ Complete | ⏳ Not Started | Phase 5 |
| **Camera System** | ✅ 2D Camera | ✅ **Smooth Follow** | **Phase 3** ✅ |
| **Lighting** | ✅ 2D Colors | ✅ **3-Layer System** | **Phase 3** ✅ |
| **Audio** | ✅ 2D Positional | ⏳ Not Started | Phase 6 |
| **Documentation** | ✅ Updated | ✅ **Complete** | **Phase 1-3** ✅ |

### Phase Checklist

- [x] **Phase 1: Documentation & Planning** ✅ **COMPLETE**
  - [x] Update CLAUDE.md with 3D architecture
  - [x] Update README.md with migration tracker
  - [x] Create MIGRATION.md progress log
  - [x] Add Ursina to requirements
  - [x] Create graphics3d/ package structure

- [x] **Phase 2: Ursina Integration** ✅ **COMPLETE**
  - [x] Install and configure Ursina engine
  - [x] Create renderer3d.py wrapper
  - [x] Render first 3D dungeon room
  - [x] Test player movement in 3D
  - [x] Implement camera follow system
  - [x] Implement basic 3D lighting
  - [x] Create main_3d.py game loop
  - [x] Test all imports

- [x] **Phase 3: Working 3D MVP** ✅ **COMPLETE** *(1 day - Oct 12, 2025)*
  - [x] Fix grey screen rendering issue
  - [x] Set window resolution to 1920×1080
  - [x] Implement Entity-based update loop (modern Ursina pattern)
  - [x] Fix camera positioning (immediate initialization)
  - [x] Boost lighting for visibility (ambient 0.3 → 0.8)
  - [x] Brighten floor/wall tiles (×3 and ×2 respectively)
  - [x] Add comprehensive debug logging system
  - [x] Enable WASD player movement
  - [x] Verify combat system (bump-to-attack)
  - [x] Test stairs descent & level progression
  - [x] Achieve stable 40-45 FPS
  - [x] **Game fully playable in 3D!** 🎉

- [ ] **Phase 4: Entity 3D Models** *(3 weeks)*
  - [ ] Create 3D player class models
  - [ ] Create 3D enemy models
  - [ ] Create 3D item models
  - [ ] Implement basic animations

- [ ] **Phase 5: Particle System 3D** *(2 weeks)*
  - [ ] Port particle effects to 3D
  - [ ] Convert ability visuals to 3D
  - [ ] Add 3D death bursts
  - [ ] Implement floating damage text

- [ ] **Phase 6: Gameplay Integration** *(2 weeks)*
  - [ ] 3D FOV/visibility system
  - [ ] 3D ability targeting
  - [ ] Combat animations in 3D
  - [ ] 3D positional audio

- [ ] **Phase 7: Polish** *(2 weeks)*
  - [ ] Height variation in dungeons
  - [ ] Advanced lighting & shadows
  - [ ] Post-processing effects
  - [ ] Multiple camera modes

- [ ] **Phase 8: Optimization** *(2 weeks)*
  - [ ] Performance profiling
  - [ ] Optimize rendering pipeline
  - [ ] Cross-platform testing
  - [ ] Final documentation

**Progress:** 35% Complete (3 of 8 phases done)
**Estimated Completion:** 8-9 weeks remaining
**Time Saved:** 19 days ahead of schedule! (Phases 1-3 completed in 1 day instead of 3 weeks)

See `MIGRATION.md` for detailed daily progress logs.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the game in 3D mode (NEW! Fully playable)
python main.py --mode 3d

# Or run in classic 2D mode
python main.py --mode 2d
python main.py  # defaults to 2D
```

**Requirements:** Python 3.8+, PyQt6 >= 6.4.0, pygame >= 2.5.0, numpy >= 1.24.0, ursina >= 6.0.0 (for 3D)

**3D Controls:**
- **WASD / Arrow Keys** - Move and attack (bump into enemies)
- **ESC** - Quit game

## 📁 Project Structure

```
roguelike/
├── main.py                 # Application entry point
├── game.py                 # Core game state & logic
├── entities.py             # Entity classes (Player, Enemy, Item)
├── constants.py            # Game configuration & constants
├── dungeon.py              # Procedural dungeon generation
├── abilities.py            # Ability system & implementations
├── combat.py               # Combat calculation & resolution
├── animations.py           # Particle system & visual effects
├── audio.py                # Procedural audio synthesis
├── fov.py                  # Field of view calculations
├── visibility.py           # Fog of war & visibility map
├── graphics/               # ⭐ Rendering code (organized by type)
│   ├── __init__.py         # Exports all rendering functions
│   ├── utils.py            # Rendering utilities (fog, gems, runes, etc.)
│   ├── tiles.py            # Tile rendering (wall, floor, stairs)
│   ├── ability_icons.py    # Ability icon rendering
│   ├── enemies/            # Enemy rendering (one file per enemy)
│   │   ├── __init__.py     # Enemy rendering dispatcher
│   │   ├── base.py         # Shared enemy utilities (shadow, transform)
│   │   ├── goblin.py       # Goblin renderer
│   │   ├── slime.py        # Slime renderer
│   │   ├── skeleton.py     # Skeleton renderer
│   │   ├── orc.py          # Orc renderer
│   │   ├── demon.py        # Demon renderer
│   │   └── dragon.py       # Dragon renderer
│   ├── items/              # Item rendering (one file per item)
│   │   ├── __init__.py     # Item rendering dispatcher
│   │   ├── base.py         # Shared item utilities (shadow, glow)
│   │   ├── health_potion.py
│   │   ├── sword.py
│   │   ├── shield.py
│   │   ├── boots.py
│   │   └── ring.py
│   └── players/            # Player class rendering (one file per class)
│       ├── __init__.py     # Player rendering dispatcher
│       ├── base.py         # Shared player utilities (shadow, transform)
│       ├── warrior.py      # Warrior renderer
│       ├── mage.py         # Mage renderer
│       ├── rogue.py        # Rogue renderer
│       └── ranger.py       # Ranger renderer
└── ui/                     # ⭐ User interface (screens & widgets)
    ├── __init__.py         # Exports all UI components
    ├── main_window.py      # Main application window & screen manager
    ├── screens/            # Full-screen UI views
    │   ├── __init__.py
    │   ├── title_screen.py      # Animated title/splash screen
    │   ├── main_menu.py         # Main menu
    │   ├── settings_screen.py   # Settings & controls
    │   ├── class_selection.py   # Character class selection (with preview)
    │   └── victory_screen.py    # Victory/game over screen
    └── widgets/            # Reusable UI components
        ├── __init__.py
        ├── game_widget.py       # Main game rendering widget
        ├── stats_panel.py       # Player stats display
        ├── ability_button.py    # Ability button widget
        ├── ability_icon.py      # Ability icon widget
        ├── progress_bar.py      # Progress bar widget
        └── combat_log.py        # Scrolling combat log
```

## 🎯 Where to Find What

### Core Game Systems

| What You Need | Where to Look |
|---------------|---------------|
| **Game loop & state** | `game.py` - Main `Game` class with turn logic |
| **Player stats & inventory** | `entities.py` - `Player` class (lines 1-200) |
| **Enemy AI & behavior** | `entities.py` - `Enemy` class (lines 200-400) |
| **Items & equipment** | `entities.py` - `Item` class (lines 400+) |
| **Damage calculations** | `combat.py` - All combat formulas |
| **Ability definitions** | `abilities.py` - Each ability has its own class |
| **Dungeon generation** | `dungeon.py` - BSP room placement algorithm |
| **FOV & fog of war** | `fov.py`, `visibility.py` |

### Graphics & Rendering

| What You Need | Where to Look |
|---------------|---------------|
| **Add new enemy type** | `graphics/enemies/` - Create new file, add to `__init__.py` |
| **Add new player class** | `graphics/players/` - Create new file, add to `__init__.py` |
| **Add new item type** | `graphics/items/` - Create new file, add to `__init__.py` |
| **Modify tile appearance** | `graphics/tiles.py` |
| **Particle effects** | `animations.py` - `AnimationManager` and `Particle` classes |
| **Rendering utilities** | `graphics/utils.py` - Gems, runes, fog, gradients |
| **Ability icons** | `graphics/ability_icons.py` - Icon renderers for UI |

### User Interface

| What You Need | Where to Look |
|---------------|---------------|
| **Main game rendering** | `ui/widgets/game_widget.py` - Handles all in-game drawing |
| **HUD & stats display** | `ui/widgets/stats_panel.py` |
| **Combat log** | `ui/widgets/combat_log.py` |
| **Ability buttons** | `ui/widgets/ability_button.py` |
| **Class selection screen** | `ui/screens/class_selection.py` - Character preview + stats |
| **Menus & navigation** | `ui/screens/main_menu.py`, `title_screen.py` |
| **Settings UI** | `ui/screens/settings_screen.py` |
| **Screen management** | `ui/main_window.py` - Manages screen transitions |

### Audio & Effects

| What You Need | Where to Look |
|---------------|---------------|
| **Sound synthesis** | `audio.py` - `SoundSynthesizer` class (wave generation) |
| **Sound playback** | `audio.py` - `AudioManager` class (singleton pattern) |
| **Background music** | `audio.py` - Lines 400+ (procedural music generation) |
| **Add new sound** | `audio.py` - Add to `_generate_sounds()` method |

### Configuration

| What You Need | Where to Look |
|---------------|---------------|
| **Game constants** | `constants.py` - Grid size, tile size, viewport |
| **Biome definitions** | `constants.py` - `BIOME_COLORS` dictionary |
| **Enemy stats** | `constants.py` - `ENEMY_STATS` dictionary |
| **Class stats** | `constants.py` - `CLASS_STATS` dictionary |
| **Item rarities** | `constants.py` - Rarity constants and colors |
| **Color palette** | `constants.py` - All `COLOR_*` constants |

## 🛠️ Common Development Tasks

### Adding a New Enemy Type

1. **Define constants** in `constants.py`:
   ```python
   ENEMY_VAMPIRE = "vampire"
   ENEMY_STATS[ENEMY_VAMPIRE] = {"hp": 80, "attack": 12, "defense": 6, "xp": 50}
   COLOR_ENEMY_VAMPIRE = QColor(150, 0, 0)
   ```

2. **Create renderer** in `graphics/enemies/vampire.py`:
   ```python
   def draw_vampire(painter: QPainter, center_x: int, center_y: int,
                    tile_size: int, color: QColor, idle_time: float):
       """Draw vampire with cloak and fangs"""
       # Your rendering code here
   ```

3. **Register in dispatcher** in `graphics/enemies/__init__.py`:
   ```python
   from .vampire import draw_vampire

   def draw_enemy(...):
       # Add to dispatch logic
       elif enemy_type == c.ENEMY_VAMPIRE:
           draw_vampire(painter, center_x, center_y, tile_size, color, idle_time)
   ```

4. **Add to spawn logic** in `game.py` - Update `_spawn_enemies()` method

### Adding a New Player Class

1. **Define in `constants.py`**:
   ```python
   CLASS_NECROMANCER = "necromancer"
   CLASS_STATS[CLASS_NECROMANCER] = {
       "hp": 80, "attack": 14, "defense": 4,
       "description": "Summons undead minions"
   }
   COLOR_CLASS_NECROMANCER = QColor(100, 50, 100)
   ```

2. **Create abilities** in `abilities.py`:
   ```python
   CLASS_ABILITIES[CLASS_NECROMANCER] = [SummonUndead(), DrainLife(), DarkPact()]
   ```

3. **Create renderer** in `graphics/players/necromancer.py`:
   ```python
   def draw_necromancer(painter: QPainter, center_x: int, center_y: int,
                        tile_size: int, color: QColor, idle_time: float):
       """Draw necromancer with staff and robes"""
       # Your rendering code here
   ```

4. **Register in dispatcher** in `graphics/players/__init__.py`

5. **Add to class selection** in `ui/screens/class_selection.py`

### Adding a New Ability

Create a new class in `abilities.py`:

```python
class Teleport(Ability):
    def __init__(self):
        super().__init__("Teleport", "Instantly move to target location",
                         cooldown=8, ability_type="utility")

    def use(self, user, target_pos: Tuple[int, int], game) -> Tuple[bool, str]:
        success, msg = super().use(user, target_pos, game)
        if not success:
            return (success, msg)

        # Validate target
        tx, ty = target_pos
        if not game.dungeon.is_walkable(tx, ty):
            self.current_cooldown = 0  # Refund cooldown
            return (False, "Can't teleport there!")

        # Teleport player
        user.start_move(tx, ty)

        # Visual effects
        game.anim_manager.add_ability_trail(tx, ty, QColor(150, 50, 255), "dash")

        # Audio
        audio = get_audio_manager()
        audio.play_ability_sound('Teleport')

        return (True, f"Teleported to ({tx}, {ty})!")
```

Then add to a class's ability list in `CLASS_ABILITIES` dictionary.

### Adding a New UI Screen

1. **Create screen file** in `ui/screens/your_screen.py`:
   ```python
   from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

   class YourScreen(QWidget):
       def __init__(self):
           super().__init__()
           layout = QVBoxLayout()
           # Build your UI
           self.setLayout(layout)
   ```

2. **Export in `ui/screens/__init__.py`**:
   ```python
   from ui.screens.your_screen import YourScreen
   __all__ = [..., 'YourScreen']
   ```

3. **Add to main window** in `ui/main_window.py`:
   ```python
   self.your_screen = YourScreen()
   self.stacked_widget.addWidget(self.your_screen)
   ```

4. **Create navigation method**:
   ```python
   def show_your_screen(self):
       self.stacked_widget.setCurrentWidget(self.your_screen)
   ```

### Adding a New Sound Effect

In `audio.py`, add to `AudioManager._generate_sounds()`:

```python
# Create the sound using wave synthesis
my_sound = synth.combine_waves(
    synth.generate_sweep(800, 400, 0.2, 0.5),  # Whoosh
    synth.generate_noise(0.1, 0.3)              # Impact
)
self.sounds['my_sound'] = synth.array_to_sound(my_sound)
```

Add a helper method:

```python
def play_my_sound(self):
    """Play my custom sound"""
    self.play_sound('my_sound', volume=0.8, pitch_variation=0.1)
```

Use in game code:

```python
audio = get_audio_manager()
audio.play_my_sound()
```

## 🏗️ Architecture Patterns

### Module Organization

- **Package-based refactoring**: Large modules (`graphics.py`, `ui.py`) have been split into packages with submodules
- **Dispatcher pattern**: `graphics/enemies/__init__.py`, `graphics/players/__init__.py`, `graphics/items/__init__.py` dispatch to specific renderers
- **Backward compatibility**: All packages export symbols to maintain imports from original single-file structure
- **Separation of concerns**: Rendering (graphics/), logic (game.py), data (entities.py), config (constants.py)

### Key Design Patterns

- **Singleton**: `AudioManager` uses singleton pattern via `get_audio_manager()`
- **Entity Component**: Base `Entity` class with `Player`, `Enemy`, `Item` subclasses
- **Observer**: PyQt signals for UI events (`ability_clicked`, etc.)
- **State Machine**: `MainWindow` manages screen transitions with `QStackedWidget`
- **Strategy**: Ability system with polymorphic `use()` method

### Animation System

All entities inherit from `Entity` class in `entities.py`:

- **Smooth movement**: Interpolated display position separate from grid position
- **Idle animations**: `idle_time` parameter drives breathing/bobbing
- **Facing direction**: `facing_direction` tuple for character orientation
- **Bob offset**: Vertical offset for walk cycles

Managed by `AnimationManager` in `animations.py`:

- **Particle types**: Standard, Directional, Trail, Ambient
- **Effect helpers**: `add_death_burst()`, `add_ability_trail()`, `add_directional_impact()`
- **Auto-cleanup**: Dead particles automatically removed

### Rendering Pipeline

From `ui/widgets/game_widget.py` - `paintEvent()`:

1. Draw tiles (floor/wall/stairs)
2. Draw entities (players, enemies, items) with geometric shapes
3. Draw health bars
4. Draw flash effects (damage overlay)
5. Draw ambient particles (background layer)
6. Draw trail particles
7. Draw standard particles
8. Draw directional impact particles
9. Draw floating damage text
10. Draw game over overlay

## 🎨 Graphics System

### Geometric Rendering

All graphics are **procedurally drawn** using PyQt6's `QPainter` - no image files needed!

**Techniques used:**
- `QLinearGradient`, `QRadialGradient` for lighting/shading
- `drawPolygon()` for complex shapes
- `drawEllipse()`, `drawRect()` for basic primitives
- Layered rendering for depth
- Color variations for detail (warts, scars, armor plates)

**Shared utilities** in `graphics/utils.py`:
- `draw_gem()` - Faceted gems with different cuts
- `draw_rune()` - Glowing magical symbols
- `draw_metallic_gradient()` - Realistic metal shading
- `draw_sparkle()` - Star sparkle effects
- `apply_fog_color()` - Fog of war tinting

### Rarity System (Items)

Items support 5 rarity tiers, each with visual enhancements:

- **Common** (60% drop): Basic appearance
- **Uncommon** (30%): Better materials, brass accents
- **Rare** (8%): Silver/chrome, small gems
- **Epic** (2%): Gold trim, glowing runes, large gems
- **Legendary** (<1%): Particle effects, sparkles, star-cut gems

See `graphics/items/sword.py` for complete example.

### Biome System

The game features 5 biomes that change every 5 levels:

- **Dungeon** (1-5): Classic stone corridors
- **Catacombs** (6-10): Dusty bone crypts
- **Caves** (11-15): Earthy natural caverns
- **Hell** (16-20): Charred lava landscapes
- **Abyss** (21-25): Void-touched dimensions

Biome data in `constants.py` - `BIOME_COLORS` dictionary. Rendering in `graphics/tiles.py`.

## 🔊 Audio System

**100% procedural** - no audio files needed! Uses numpy for wave synthesis.

### Wave Types

In `audio.py` - `SoundSynthesizer` class:

- `generate_sine_wave()` - Pure tone (musical notes)
- `generate_square_wave()` - Retro/harsh sounds
- `generate_sweep()` - Frequency slides (whooshes)
- `generate_noise()` - White noise (impact, texture)
- `combine_waves()` - Mix multiple waveforms

### Sound Categories

All sounds generated in `AudioManager._generate_sounds()`:

- **Combat**: Attack swings, hits, crits, enemy deaths
- **Abilities**: 6 unique ability sounds
- **Movement**: Footsteps with pitch variation
- **Items**: Pickup, drink, equip sounds
- **UI**: Menu clicks, selections
- **Events**: Level up, stairs, game over
- **Voice**: TTS-based procedural voice lines

### Background Music

Adaptive layered music system:

- **Intensity levels**: Calm (exploration) → Tense (combat)
- **Music ducking**: SFX louder during combat
- **Smooth transitions**: Interpolated intensity changes
- **Looping**: Seamless 10-second loops

## 🧪 Testing & Debugging

### Useful Debug Tricks

**Print entity positions:**
```python
print(f"Player: {game.player.x}, {game.player.y}")
print(f"Enemies: {[(e.x, e.y) for e in game.enemies]}")
```

**Test abilities without cooldown:**
```python
player.abilities[0].current_cooldown = 0  # Force ready
```

**Spawn specific enemy:**
```python
from entities import Enemy
import constants as c
game.enemies.append(Enemy(10, 10, c.ENEMY_DRAGON, c.ENEMY_STATS[c.ENEMY_DRAGON]))
```

**Toggle fog of war:**
```python
game.visibility_map.reveal_all()  # See entire dungeon
```

**God mode:**
```python
game.player.hp = 999999
game.player.max_hp = 999999
```

### Performance Monitoring

The game targets **60 FPS**. Performance bottlenecks:

- Animation update: O(n) particles
- Enemy AI: O(n) enemies
- Rendering: O(grid_size) + O(animations)
- FOV calculation: O(visible_tiles)

Typical performance with <100 entities: 60 FPS stable.

## 📚 Code Style & Conventions

- **Type hints** on all function parameters and returns
- **Docstrings** for all classes and public methods
- **Constants** in `UPPER_CASE` (defined in `constants.py`)
- **Private methods** prefixed with `_`
- **Colors** use `QColor` objects from PyQt6
- **Messages** use tuple format: `(message_text, message_type)` for color coding
- **File organization**: One class/system per file where possible

## 🐛 Troubleshooting

### Import Errors

If you get import errors after refactoring:
- Check `__init__.py` files export the right symbols
- Verify `__all__` lists are complete
- Ensure backward compatibility imports are present

### Graphics Not Showing

- Check `paintEvent()` is called (add print statement)
- Verify entity positions are within viewport bounds
- Ensure colors have sufficient contrast with background

### Audio Issues

- Verify pygame mixer initialized: `pygame.mixer.get_init()`
- Check volume settings: `audio.set_sfx_volume(0.7)`
- Reduce buffer size if experiencing lag: `pygame.mixer.pre_init(22050, -16, 2, 512)`

### Animation Glitches

- Ensure `dt` (delta time) is being passed correctly
- Check `update()` is called every frame
- Verify `move_duration` is reasonable (0.1-0.3s)

## 🎯 Next Steps

Want to extend the game? Check out `CLAUDE.md` for:
- Detailed gameplay mechanics
- Balance constants and formulas
- Adding new content (enemies, abilities, items)
- Future feature ideas
- Audio synthesis guide

## 🤝 Contributing

This codebase is designed to be modular and extensible. When adding features:

1. Follow existing patterns (dispatcher, base classes)
2. Add constants to `constants.py` first
3. Create rendering code in appropriate `graphics/` submodule
4. Update `__init__.py` exports for new modules
5. Test with different biomes and difficulty levels

Happy coding! 🎮
