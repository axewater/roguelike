# Testing the 3D Mode - Quick Guide

## Prerequisites

1. **Install Dependencies**
   ```bash
   # Windows (in venv)
   venv\Scripts\activate
   pip install -r requirements.txt

   # Linux
   source venv_linux/bin/activate
   pip install -r requirements.txt
   ```

2. **Verify Installation**
   ```bash
   python -c "import ursina; print('Ursina installed!')"
   ```

---

## Running 3D Mode

### Method 1: Command Line Argument (Recommended)

```bash
# 3D Mode
python main.py --mode 3d

# 2D Mode (default)
python main.py --mode 2d
# or
python main.py
```

### Method 2: Direct Execution

```bash
# Run 3D mode directly
python main_3d.py

# Run test script
python test_ursina.py
```

---

## What You Should See

### On Launch

```
=== Claude-Like (3D Mode) ===
Launching Ursina 3D renderer...
Rendered dungeon: 1247 tiles
==================================================
CONTROLS:
  WASD / Arrow Keys - Move & Attack
  ESC - Quit
==================================================
Starting game...
Class: Warrior
Level: 1
HP: 120/120
==================================================

Player: (25, 14) | HP: 120/120 | Level: 1 | Enemies: 8
```

### 3D Window

You should see:
- **3D dungeon** with walls (cubes) and floors (planes)
- **Blue player cube** (Warrior) in the center
- **Camera** positioned behind and above player
- **Lighting** with shadows and depth
- **Stairs** as a glowing raised platform

### As You Move

- **WASD** - Player cube moves smoothly
- **Camera** - Follows player with smooth interpolation
- **Walls** - Block movement (collision detection)
- **Enemies** - Invisible in Phase 2, but combat works (check console output)

---

## Expected Behavior

### ✅ Working Features

| Feature | Expected Behavior |
|---------|-------------------|
| **Movement** | WASD moves player, ~0.15s cooldown between moves |
| **Camera** | Smoothly follows player, maintains distance |
| **Dungeon** | All rooms and corridors visible in 3D |
| **Walls** | Block movement, have collision |
| **Floors** | Walkable, different color per biome |
| **Stairs** | Glowing cube, descends level when walked on |
| **Lighting** | Three-layer lighting (ambient, sun, torch) |
| **Combat** | Bumping enemies triggers attack (console output) |
| **Level Progression** | Stairs work, new dungeon generates |

### ⏳ Not Yet Implemented (Expected)

| Feature | Status | Target Phase |
|---------|--------|--------------|
| **Enemies visible** | Not rendered | Phase 4 |
| **Items visible** | Not rendered | Phase 4 |
| **Particle effects** | No particles | Phase 5 |
| **UI overlay** | No HP bar/abilities | Phase 6 |
| **FOV/Fog of war** | All visible | Phase 6 |
| **Detailed player model** | Just a cube | Phase 4 |

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'ursina'"

**Solution:**
```bash
pip install ursina
# or
pip install -r requirements.txt
```

### Issue: Black screen or no window

**Possible causes:**
1. Graphics driver issue
2. OpenGL not supported

**Solution:**
```bash
# Check Panda3D installation
python -c "import panda3d.core; print('Panda3D OK')"

# Try test script first
python test_ursina.py
```

### Issue: "Audio warnings" on Linux

**Expected behavior:**
- Headless servers have no audio device
- Audio warnings are normal
- Game still works

**Solution:** Ignore audio warnings or test on Windows

### Issue: Very slow performance

**Possible causes:**
1. Too many entities (large dungeon)
2. Weak GPU

**Solution:**
- Close other applications
- Reduce dungeon size in constants.py (MAX_ROOMS)

### Issue: Camera clips through walls

**Status:** Known limitation for Phase 2

**Workaround:** Camera collision will be added in Phase 3

---

## Debug Mode

### Enable Ursina Debug Info

Edit `main_3d.py`:
```python
app = Ursina(
    title="Claude-Like 3D",
    development_mode=True  # Change to True
)
```

This shows:
- FPS counter
- Entity count
- Performance metrics

### Console Debug Output

The game prints debug info every 2 seconds:
```
Player: (x, y) | HP: current/max | Level: N | Enemies: count
```

### Verbose Logging

Add at top of `main_3d.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Performance Benchmarks

### Expected Performance

| System | FPS | Entity Count |
|--------|-----|--------------|
| **Desktop (GTX 1060)** | 60 | 1500 |
| **Laptop (Integrated)** | 30-60 | 1500 |
| **Old Hardware** | 15-30 | 1500 |

### If FPS < 30

1. Reduce `MAX_ROOMS` in constants.py
2. Close background applications
3. Lower window resolution (edit Ursina init)

---

## Testing Checklist

Use this checklist to verify Phase 2:

- [ ] 3D window opens
- [ ] Dungeon is visible in 3D
- [ ] Player blue cube is visible
- [ ] Can move with WASD
- [ ] Camera follows player smoothly
- [ ] Walls block movement
- [ ] Can attack enemies (console shows damage)
- [ ] Can descend stairs
- [ ] New level generates after stairs
- [ ] Lighting looks atmospheric
- [ ] No Python errors/crashes
- [ ] Can quit with ESC

---

## Screenshots & Recording

### Take Screenshots

Ursina has built-in screenshot support:
- Press **F12** to take screenshot
- Saved to project root

### Record Video

Use OBS Studio or similar to record the 3D window

### Share Results

If you encounter issues or want to share progress:
1. Screenshot the 3D window
2. Copy console output
3. Note your system specs

---

## Next Steps After Testing

### If Everything Works

Congratulations! Phase 2 is complete. Ready for:
- **Phase 3**: Enhanced 3D dungeon rendering
- **Phase 4**: 3D character and enemy models
- **Phase 5**: 3D particle effects

### If Issues Found

Please note:
1. What happened (error message or behavior)
2. When it happened (which step)
3. Your system (OS, Python version, GPU)
4. Console output

Most issues are:
- Missing dependencies (run pip install)
- Graphics driver (update drivers)
- Audio warnings (expected on Linux)

---

## Advanced: Customization

### Change Camera Settings

Edit `constants.py`:
```python
CAMERA_DISTANCE = 15.0  # Further = more zoomed out
CAMERA_HEIGHT = 8.0     # Higher = more top-down view
CAMERA_ANGLE = 45.0     # Steeper = more isometric
FOV = 60                # Wider = more fish-eye
```

### Change Player Color

Edit `graphics3d/players/__init__.py`:
```python
class_colors = {
    c.CLASS_WARRIOR: (100, 200, 255),  # Change RGB values
    # ...
}
```

### Adjust Lighting

Edit `renderer3d.py` in `setup_lighting()`:
```python
self.ambient_light = AmbientLight(color=(0.3, 0.3, 0.35, 1))  # Darker/brighter
```

---

## FAQ

**Q: Can I play the full game in 3D?**
A: Yes! Combat, items, level progression all work. Only enemies/items are invisible (Phase 4 will fix).

**Q: Can I switch between 2D and 3D?**
A: Yes, restart with `--mode 2d` or `--mode 3d`

**Q: Will my 2D save work in 3D?**
A: No saves yet, but when implemented, yes - same game logic.

**Q: Why is my player a cube?**
A: Phase 2 POC. Detailed character models come in Phase 4.

**Q: Where are the enemies?**
A: They exist (combat works), just not rendered yet. Phase 4 adds enemy models.

---

Happy testing! 🎮
