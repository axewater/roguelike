# Claude-Like Roguelike 🎮

A Python roguelike game migrating from 2D (PyQt6) to 3D (Ursina Engine).

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run in 2D mode (complete, legacy)
python main.py --mode 2d

# Run in 3D mode (in development)
python main.py --mode 3d
```

## Project Structure

### Core Game Files
- **`game.py`** - Main game logic (turn-based, combat, dungeon management)
- **`entities.py`** - Player, Enemy, Item classes
- **`dungeon.py`** - Procedural dungeon generation
- **`abilities.py`** - Class abilities and cooldown system
- **`combat.py`** - Damage calculations
- **`constants.py`** - All configuration and game constants

### 2D Rendering (Complete)
- **`ui/`** - PyQt6 UI (screens, widgets, menus)
- **`graphics/`** - 2D geometric shape rendering
- **`animations.py`** - 2D particle effects

### 3D Rendering (In Development)
- **`main_3d.py`** - 3D mode entry point
- **`renderer3d.py`** - Ursina 3D rendering manager
- **`graphics3d/`** - 3D models (procedurally generated)
- **`animations3d.py`** - 3D particle effects

### Support Systems
- **`audio.py`** - Procedural sound synthesis (no audio files needed!)
- **`fov.py`** / **`visibility.py`** - Field of view and fog of war

## Documentation

- **`README.md`** - Complete feature documentation and file reference
- **`MIGRATION.md`** - 3D migration project plan and roadmap
- **`docs_archive_2025-10-12/`** - Archived phase summaries and old docs

## Current Status

**2D Mode**: ✅ Complete - Fully playable with all features
**3D Mode**: 🚧 70% Complete - Core gameplay works, UI pending

### What Works in 3D
- ✅ Dungeon rendering (walls, floors, stairs)
- ✅ Player movement (WASD)
- ✅ Combat system (bump-to-attack)
- ✅ Enemy AI and 3D models
- ✅ Item models with animations
- ✅ Particle effects (explosions, trails, text)
- ✅ Camera follow system
- ✅ Level progression

### What's Missing in 3D
- ❌ UI overlay (stats, abilities, combat log)
- ❌ FOV/Fog of War in 3D
- ❌ Ability targeting system
- ❌ Class selection screen
- ❌ Title/Victory screens
- ❌ 3D positional audio

See `MIGRATION.md` for the complete development roadmap.

## Architecture Notes

### Dual Rendering
The game supports both 2D and 3D rendering:
- **Game logic** (`game.py`) is renderer-agnostic
- **2D mode** uses PyQt6 widgets
- **3D mode** uses Ursina Entity system
- Mode selection via `--mode` flag in `main.py`

### Particle System Bridging
The `AnimationManager3DProxy` in `main_3d.py` converts 2D particle calls to 3D:
- Converts PyQt6 `QColor` to RGB tuples
- Translates pixel coords to 3D world space
- Allows `game.py` to remain unchanged

### No External Assets
- **Graphics**: All 3D models procedurally generated (no .obj files)
- **Audio**: All sounds procedurally synthesized (no .wav files)
- **Textures**: Ursina primitive shapes with color/materials

## Development Workflow

1. **2D is the reference** - All features work in 2D
2. **3D mirrors 2D** - Porting features from 2D to 3D
3. **Game logic unchanged** - Only rendering layer modified
4. **Test both modes** - Ensure 2D doesn't break

## Key Technologies

- **Python 3.8+**
- **PyQt6** - 2D UI and rendering
- **Ursina Engine** - 3D rendering (built on Panda3D)
- **pygame** - Audio playback
- **numpy** - Sound wave synthesis

---

**For detailed feature documentation:** See `README.md`
**For migration progress:** See `MIGRATION.md`
