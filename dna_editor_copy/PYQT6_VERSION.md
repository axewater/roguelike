# PyQt6 DNA Editor - Quick Reference

## Launch

```bash
python3 dna_editor_copy/main_qt.py
```

## What's Different from Ursina UI Version

### Advantages
✅ **Better UI control** - No coordinate positioning issues
✅ **Native widgets** - OS-standard sliders, spinboxes, buttons
✅ **Menu bar** - File/Edit/Help menus with keyboard shortcuts
✅ **Familiar UX** - Looks like a normal desktop app
✅ **Export built-in** - Ctrl+E to export JSON

### Architecture
- **Left panel**: PyQt6 control panel (300px fixed width)
- **Right area**: 3D viewport (separate Ursina window)
- **Shared code**: Reuses `core/`, `models/`, and `controllers/state_manager.py`

## File Overview

### New Files (PyQt6 specific)

**`main_qt.py`** (60 lines)
- Entry point
- Creates QApplication and EditorWindow

**`qt_ui/editor_window.py`** (230 lines)
- Main window with menu bar
- Coordinates control panel ↔ viewport
- Handles undo/redo, export JSON

**`qt_ui/control_panel.py`** (400 lines)
- All sliders, spinboxes, dropdowns
- Emits signals: `creature_changed`, `undo_requested`, `redo_requested`
- Manages state synchronization

**`qt_ui/viewport_widget.py`** (230 lines)
- Wraps Ursina 3D scene
- Creates creature, manages animation
- Camera controls (mouse drag, scroll, R to reset)

### Reused Files (unchanged)

**`core/curves.py`** - Pure math (Bezier & Fourier)
**`core/constants.py`** - All config values
**`models/tentacle.py`** - Ursina tentacle model
**`models/creature.py`** - Ursina creature model
**`controllers/state_manager.py`** - Undo/redo logic

## Controls

### In PyQt6 Control Panel

**Creature Settings:**
- Tentacles: Spinbox (1-3)
- Segments: Spinbox (5-20)
- Algorithm: Dropdown (Bezier/Fourier)

**Algorithm Parameters:**
- **Bezier**: Control Strength slider (0.1-0.8)
- **Fourier**: Wave Count (1-7), Amplitude (0.05-0.4)

**Thickness:**
- Base: Slider (0.1-0.5)
- Taper: Slider (0.0-1.0)

**Presets:**
- Default, Wavy, Tight buttons

**Actions:**
- Undo/Redo buttons
- Export JSON button

### In 3D Viewport Window

**Camera:**
- Mouse drag → Rotate camera
- Scroll → Zoom in/out
- R → Reset camera

### Keyboard Shortcuts

- **Ctrl+Z** - Undo
- **Ctrl+Y** - Redo
- **Ctrl+E** - Export JSON
- **Ctrl+Q** - Quit

## Export Format

The "Export JSON" button saves a file like this:

```json
{
  "num_tentacles": 2,
  "segments_per_tentacle": 12,
  "algorithm": "bezier",
  "algorithm_params": {
    "control_strength": 0.4
  },
  "thickness_base": 0.25,
  "taper_factor": 0.6
}
```

This JSON can be loaded into the roguelike game to create the same creature!

## Technical Notes

### Why Separate 3D Window?

The viewport uses a **separate Ursina window** rather than embedding because:
1. **Simpler implementation** - No Qt↔Ursina rendering integration needed
2. **Fewer dependencies** - Avoids QOpenGLWidget complexity
3. **Still works well** - User can arrange windows side-by-side

### Future Enhancement Ideas

If embedding is desired:
- Use `QOpenGLWidget` to host Ursina's OpenGL context
- Or use `QWindow.fromWinId()` to embed Ursina's native window handle
- Would require more complex window lifecycle management

### Signal Flow

```
User adjusts slider
  → ControlPanel emits creature_changed signal
  → EditorWindow receives signal
  → EditorWindow saves state (undo/redo)
  → EditorWindow calls viewport.rebuild_creature()
  → ViewportWidget destroys old creature
  → ViewportWidget creates new TentacleCreature with new params
  → Ursina renders updated creature
```

## Comparison Table

| Feature | Ursina UI Version | PyQt6 Version |
|---------|------------------|---------------|
| UI Framework | Ursina Text/Button | PyQt6 QWidget |
| Windows | Single | Two (control + 3D) |
| Coordinate System | Normalized (-0.9 to 0.9) | Pixel-based |
| Sliders | Ursina Slider | QSlider |
| Layout | Manual positioning | QVBoxLayout/QHBoxLayout |
| Menu Bar | No | Yes (File/Edit/Help) |
| Keyboard Shortcuts | Custom held_keys | QKeySequence |
| Export JSON | Via preset system | Built-in File menu |

## Troubleshooting

**"Separate window doesn't appear"**
- Check console for Ursina errors
- Make sure Ursina is installed: `pip install ursina`

**"Controls don't update creature"**
- Verify signal connections in console output
- Check for Python errors

**"Undo/Redo buttons disabled"**
- Normal on first launch (no history yet)
- Make a change, then undo should enable

**"Export does nothing"**
- Check file dialog appeared
- Verify write permissions in target directory

## Development

Want to modify the PyQt6 version?

**Add a new slider:**
1. Edit `qt_ui/control_panel.py`
2. Add slider widget in appropriate group
3. Connect `valueChanged` signal to emit `creature_changed`
4. Update `get_state()` to include new value

**Change layout:**
1. Edit `qt_ui/control_panel.py` or `editor_window.py`
2. Modify `QVBoxLayout`/`QHBoxLayout` structures
3. PyQt6 layouts are much more predictable than Ursina positioning!

**Embed 3D viewport:**
1. Edit `qt_ui/viewport_widget.py`
2. Replace placeholder label with `QOpenGLWidget`
3. Initialize Ursina with custom window handle
4. Requires Ursina internals knowledge
