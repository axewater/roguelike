# DNA Creature Editor - Patch Notes

## v1.2.0 - Modern UI Overhaul (2025-10-14)

### 🎨 MAJOR UI MODERNIZATION

**Massive Button Spacing** ✅
- Button gap dramatically increased: 0.18 → **0.28** (+55%!)
- Now gives **0.21 space** between buttons (10x the original 0.02!)
- Buttons super easy to click with tons of breathing room
- No more cramped, overlapping text

**Interactive Button Feedback** ✨
- **Hover effects**: Buttons brighten when you mouse over them
- **Click feedback**: Buttons darken when pressed
- Every button now has visual interaction states
- Feels modern and responsive!

**Vibrant Color Palette** 🌈
- Replaced flat, dull colors with rich, vibrant ones
- Default buttons: Richer blue-gray (#40475A)
- Action buttons: Vibrant green (#268C59)
- Special buttons: Rich purple (#8C40A6)
- Save buttons: Bright blue (#3373B3)
- Plus/Minus: Deep red/green with better contrast

**What It Looks Like Now:**
- Hover over a button → it **brightens**
- Click a button → it **darkens** with visual feedback
- Colors are richer, more saturated, more modern
- Tons of space between all buttons
- Looks like 2024, not 2003!

**Technical Details:**
- Added 14 new color constants (7 hover + 7 pressed)
- Applied `highlight_color` and `pressed_color` to all 12+ buttons
- Button gap calculation: 0.28 gap - 0.07 button = 0.21 space per button
- Modern color theory: Base → +25% brightness for hover, -40% for pressed

**Files Modified:**
- `ui_constants.py` - 21 new/updated color constants, modernized palette
- `ui_controls.py` - Button gap 0.28, hover/press on all buttons, version v1.2
- `PATCH_NOTES.md` - This epic changelog!

**Backwards Compatibility:**
- All existing presets work perfectly
- No changes to creature logic or parameters
- Pure visual/UX improvements

## v1.0.1 - Bug Fixes (2025-10-14)

### Fixed Issues

1. **Missing `mouse` import** (NameError)
   - Added `mouse` to imports in `main.py`
   - Fixes camera orbit and zoom controls

2. **Missing primitive models** (Ursina compatibility)
   - Changed tentacles from 'cylinder' to 'cube' (stretched)
   - Changed spikes from 'cone' to 'cube' (stretched)
   - Ursina doesn't include cylinder/cone primitives by default

### Visual Changes

**Tentacles**: Now use blocky segments instead of smooth cylinders
- Creates a more stylized, retro aesthetic
- Animation still works smoothly
- Actually looks quite cool and unique!

**Spikes**: Now use thin cubes instead of cones
- Gives creatures a more angular, crystalline appearance
- Fibonacci distribution still ensures even placement

### Notes

The blocky aesthetic gives creatures a distinctive "low-poly horror" look that's actually quite appealing. If you prefer smooth cylinders/cones, you can:
- Install additional Ursina model packs
- Create custom procedural cylinder/cone meshes
- Keep the current blocky style (it's unique!)

## How to Update

Simply pull the latest code and run:

```bash
python3 dna_editor/main.py
```

All fixes are backwards compatible with existing presets.
