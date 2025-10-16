# DNA Editor - PyQt6 Technical Guide

Technical reference for the DNA Editor's PyQt6 implementation.

## Launch

```bash
# From project root
python3 dna_editor/main_qt.py

# Or directly from the folder
cd dna_editor
python3 main_qt.py
```

## Architecture Overview

The DNA Editor uses PyQt6 for UI controls with Ursina for 3D rendering in a separate window.

### Component Breakdown

- **Control Panel**: PyQt6 window (300px fixed width) with all UI controls
- **3D Viewport**: Separate Ursina window for real-time creature preview
- **Shared Core**: Reuses `core/`, `models/`, and `controllers/state_manager.py`

## File Structure

### PyQt6 UI Components

**`main_qt.py`** (~70 lines)
- Entry point
- Creates QApplication and EditorWindow
- Sets Fusion style for consistent look

**`qt_ui/editor_window.py`** (~230 lines)
- Main window with menu bar (File/Edit/Help)
- Coordinates control panel ↔ viewport communication
- Handles undo/redo operations and JSON export
- Connects keyboard shortcuts (Ctrl+Z/Y/E/Q)

**`qt_ui/control_panel.py`** (~400 lines)
- All sliders, spinboxes, dropdowns, and buttons
- Emits signals: `creature_changed`, `undo_requested`, `redo_requested`
- Manages state synchronization
- Dynamic parameter panel switching based on algorithm

**`qt_ui/viewport_widget.py`** (~250 lines)
- Wraps Ursina 3D scene in separate window
- Creates and manages TentacleCreature instances
- Implements camera controls (mouse drag, scroll, R to reset)
- Updates creature animation every frame (~60 FPS)

**`qt_ui/ursina_renderer.py`** (~200 lines)
- Alternative/experimental renderer implementation
- Can be used instead of viewport_widget.py

### Shared Components

**`core/curves.py`** - Pure mathematical functions (Bezier & Fourier)
**`core/constants.py`** - All configuration values
**`models/tentacle.py`** - Ursina 3D tentacle model
**`models/creature.py`** - Ursina 3D creature model
**`controllers/state_manager.py`** - Undo/redo history system

## UI Controls

### Control Panel (PyQt6 Window)

**Creature Settings:**
- Tentacles: QSpinBox (1-3)
- Segments: QSpinBox (5-20)
- Algorithm: QComboBox (Bezier/Fourier)

**Algorithm Parameters:**
- **Bezier**: Control Strength QSlider (0.1-0.8)
- **Fourier**: Wave Count QSlider (1-7), Amplitude QSlider (0.05-0.4)

**Thickness:**
- Base: QSlider (0.1-0.5)
- Taper: QSlider (0.0-1.0)

**Presets:**
- Default, Wavy, Tight QPushButtons

**Actions:**
- Undo/Redo QPushButtons
- Export JSON QPushButton

### 3D Viewport (Ursina Window)

**Camera Controls:**
- Mouse drag → Rotate camera
- Scroll → Zoom in/out
- R → Reset camera to default position

### Keyboard Shortcuts (QKeySequence)

- **Ctrl+Z** - Undo
- **Ctrl+Y** - Redo
- **Ctrl+E** - Export JSON
- **Ctrl+Q** - Quit

## Export Format

The "Export JSON" feature saves configurations in this format:

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

This JSON can be imported into the roguelike game to create matching creatures.

## Technical Implementation Details

### Why Separate 3D Window?

The viewport uses a **separate Ursina window** rather than embedding:

**Advantages:**
1. **Simpler implementation** - No Qt↔Ursina rendering integration needed
2. **Fewer dependencies** - Avoids QOpenGLWidget complexity
3. **Reliable** - No context sharing or threading issues
4. **Still usable** - Users can arrange windows side-by-side

**Alternative (embedding):**
If embedding is desired in the future:
- Use `QOpenGLWidget` to host Ursina's OpenGL context
- Or use `QWindow.fromWinId()` to embed Ursina's native window handle
- Would require complex window lifecycle management and context sharing

### Signal/Slot Flow

The application uses Qt's signal/slot mechanism for communication:

```
User adjusts slider in ControlPanel
  → ControlPanel emits creature_changed(params) signal
  → EditorWindow receives signal via slot
  → EditorWindow saves state to StateManager (undo/redo)
  → EditorWindow calls viewport.rebuild_creature(params)
  → ViewportWidget destroys old TentacleCreature
  → ViewportWidget creates new TentacleCreature with new params
  → Ursina renders updated creature
```

### Animation Loop

The viewport uses a QTimer to step Ursina forward without blocking Qt:

```python
# In ViewportWidget._update_animation() (called every 16ms ≈ 60 FPS)
self.ursina_app.step()  # Render one Ursina frame
self.animation_time += ursina_time.dt
if self.creature:
    self.creature.update_animation(self.animation_time)
self._handle_camera_controls()
```

This allows both Qt and Ursina event loops to run concurrently.

### State Management

Undo/redo is handled by `StateManager`:
- Stores up to 50 states in memory
- Each state is a dict snapshot of all parameters
- EditorWindow coordinates state saving/restoration
- Undo/redo buttons enable/disable based on history availability

## Troubleshooting

**"Separate window doesn't appear"**
- Check console for Ursina errors
- Ensure Ursina is installed: `pip install ursina`
- Verify Panda3D (Ursina's backend) is working

**"Controls don't update creature"**
- Check console for signal connection messages
- Look for Python exceptions during rebuild
- Verify import paths are correct (`dna_editor` vs `dna_editor_copy`)

**"Undo/Redo buttons disabled"**
- Normal on first launch (no history yet)
- Make a change, then undo should enable
- Check console for StateManager debug output

**"Export does nothing"**
- Verify QFileDialog appears
- Check write permissions in target directory
- Look for exceptions in console

**"Animation is choppy"**
- QTimer interval may be too high (default 16ms)
- Ursina scene may be too complex
- Check system GPU/CPU usage

## Development Guide

### Adding a New UI Control

1. Edit `qt_ui/control_panel.py`
2. Create QWidget (QSlider, QSpinBox, etc.)
3. Add to appropriate QGroupBox
4. Connect `valueChanged` signal to `_on_param_changed` slot
5. Update `get_state()` to include new parameter value
6. Emit `creature_changed` signal with updated state

Example:
```python
# In ControlPanel.__init__
self.my_slider = QSlider(Qt.Orientation.Horizontal)
self.my_slider.setRange(0, 100)
self.my_slider.valueChanged.connect(self._on_param_changed)
some_layout.addWidget(self.my_slider)

# In get_state()
state['my_param'] = self.my_slider.value() / 100.0
```

### Changing UI Layout

1. Edit `qt_ui/control_panel.py` or `qt_ui/editor_window.py`
2. Modify QVBoxLayout/QHBoxLayout/QGridLayout structures
3. Use `.addWidget()`, `.addLayout()`, `.addStretch()` for positioning
4. PyQt6 layouts are declarative and predictable

### Modifying 3D Rendering

1. Edit `qt_ui/viewport_widget.py`
2. Modify `_create_scene()` for scene setup (lighting, ground, sky)
3. Modify `rebuild_creature()` for creature instantiation
4. Modify `_update_animation()` for per-frame updates
5. Modify `_handle_camera_controls()` for camera behavior

### Adding a New Algorithm

1. Add generator function to `core/curves.py`
2. Add constants to `core/constants.py`
3. Update `qt_ui/control_panel.py` to add algorithm to dropdown
4. Update `_update_algorithm_params()` to show/hide relevant sliders
5. Test with creature creation in viewport

## Dependencies

- **Python 3.8+**
- **PyQt6** - `pip install PyQt6`
- **Ursina Engine** - `pip install ursina`
- **Panda3D** (installed automatically with Ursina)

## Performance Considerations

- **State snapshots**: Each undo state stores ~1KB (negligible)
- **Creature rebuild**: ~0.01-0.05s depending on segment count
- **Animation loop**: Runs at 60 FPS (~16ms per frame)
- **Memory**: Single creature uses ~5-10MB (Ursina meshes)

## Future Enhancements

Possible improvements:
- **Embed viewport**: Use QOpenGLWidget to embed Ursina in Qt window
- **Custom presets**: Allow users to save/load their own preset files
- **Multi-creature scene**: Edit multiple creatures simultaneously
- **Material editor**: Add texture/shader customization
- **Export formats**: Add .obj export in addition to JSON

---

**For user documentation:** See `README.md`
**For developer quickstart:** See `CLAUDE.md`
