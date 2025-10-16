# DNA Editor - Creature Tentacle Generator

Interactive 3D editor for designing procedural tentacle creatures using mathematical curve algorithms.

## Overview

This tool allows you to create and customize tentacle creatures in real-time using two powerful mathematical algorithms:

- **Bezier Curves**: Smooth, elegant curves with adjustable control strength
- **Fourier Series**: Organic, wave-based shapes with customizable frequency and amplitude

## Quick Start

```bash
# From project root
python3 dna_editor/main_qt.py

# Or directly from the folder
cd dna_editor
python3 main_qt.py
```

## Features

- **Real-time Editing**: Adjust parameters with sliders and see instant results
- **Two Algorithms**: Switch between Bezier and Fourier curve generators
- **Thickness Controls**: Customize base thickness and taper factor
- **Preset System**: 2 built-in presets (Default, Tight)
- **Undo/Redo**: Full history system (up to 50 steps)
- **Interactive Camera**: Orbit, zoom, and navigate the 3D scene
- **Export JSON**: Save creature configurations for use in the roguelike game
- **PyQt6 UI**: Native OS controls with familiar look and feel

## UI Layout

The editor consists of two windows:

1. **Control Panel** (PyQt6 window):
   - Tentacle count spinbox (1-3)
   - Segment count spinbox (5-20)
   - Algorithm dropdown (Bezier/Fourier)
   - Algorithm-specific parameter sliders
   - Thickness and taper sliders
   - Preset buttons
   - Undo/Redo buttons
   - Export JSON button

2. **3D Viewport** (separate Ursina window):
   - Real-time creature preview
   - Camera controls

## Controls

### Camera (in 3D Viewport Window)
- **Mouse Drag**: Orbit around creature
- **Scroll Wheel**: Zoom in/out
- **R**: Reset camera to default position

### Keyboard Shortcuts
- **Ctrl+Z**: Undo last change
- **Ctrl+Y**: Redo
- **Ctrl+E**: Export to JSON
- **Ctrl+Q**: Quit application

### UI Controls (in Control Panel)
- **Spinboxes**: Set tentacle count and segment count
- **Dropdown**: Select algorithm (Bezier or Fourier)
- **Sliders**: Adjust all parameters in real-time
- **Preset Buttons**: Load predefined configurations
- **Undo/Redo Buttons**: Navigate change history

## Algorithm Parameters

### Bezier Curves
- **Control Strength** (0.1 - 0.8): Controls how much the curve bends
  - Lower values = tighter, more direct curves
  - Higher values = looser, more S-shaped curves

### Fourier Series
- **Wave Count** (1 - 7): Number of sine waves to combine
  - More waves = more complex, organic shapes
- **Amplitude** (0.05 - 0.4): How much the waves affect the curve
  - Lower values = subtle waviness
  - Higher values = dramatic undulations

## Thickness Parameters

- **Base Thickness** (0.1 - 0.5): Starting thickness at tentacle base
- **Taper Factor** (0.0 - 1.0): How much the tentacle thins toward the tip
  - 0.0 = no taper (uniform thickness)
  - 1.0 = maximum taper (very thin tip)

## Presets

1. **Default**: Smooth Bezier curves with moderate control
2. **Tight**: Bezier curves with low control for more direct tentacles

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

This JSON can be imported into the roguelike game to create the same creature!

## Technical Details

### Mathematical Curve Generators

#### Bezier Curves
Uses cubic Bezier formula: `B(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃`
- Generates smooth, predictable curves
- Control points offset perpendicular to main direction
- Perfect for elegant, flowing tentacles

#### Fourier Series
Wave composition formula: `P(t) = base_curve(t) + Σ(Aₙ sin(nωt + φₙ))`
- Combines multiple sine waves at different frequencies
- Amplitude decreases with frequency for natural look
- Creates organic, biological-looking tentacles

### Animation System
- Tentacles animate with traveling wave motion
- Wave amplitude increases from base to tip
- Body pulses with subtle breathing effect

## Requirements

- Python 3.8+
- **PyQt6** - UI framework
- **Ursina Engine** - 3D rendering (built on Panda3D)
- Math (standard library)

## Architecture

The DNA Editor follows clean **separation of concerns** with a modular architecture:

### File Structure

```
dna_editor/
├── main_qt.py                   # Entry point
│
├── core/                        # Mathematical & configuration
│   ├── curves.py               # Bezier & Fourier curve generators
│   └── constants.py            # All configuration constants
│
├── models/                      # 3D entity models
│   ├── tentacle.py             # Single tentacle with segments
│   └── creature.py             # Creature with body & tentacles
│
├── qt_ui/                       # PyQt6 UI components
│   ├── editor_window.py        # Main window orchestrator
│   ├── control_panel.py        # Control panel with all UI widgets
│   ├── viewport_widget.py      # Ursina 3D viewport wrapper
│   └── ursina_renderer.py      # Alternative renderer (experimental)
│
├── controllers/                 # Application logic
│   └── state_manager.py        # Undo/redo history system
│
└── README.md                    # This file
```

### Design Principles

1. **Single Responsibility**: Each module has one clear purpose
2. **Separation of Concerns**: Math, models, UI, and logic are isolated
3. **Testability**: Pure functions and clear interfaces for testing
4. **Maintainability**: ~100-200 lines per file
5. **Reusability**: Curve generators can be used independently

## Integration with Roguelike

This tool is designed to generate tentacle DNA for creatures in the main roguelike game. Use the "Export JSON" feature to save configurations, which can be imported into `entities.py` to create procedural enemies or NPCs.

## Future Enhancements

Potential additions for future versions:
- Import/save custom presets
- Multi-creature scene editor
- Texture/material customization
- Eye/spike/limb attachments
- Animation pattern editor

## Notes

- All graphics are procedurally generated (no external assets)
- Designed for integration with the roguelike game's creature system
- Modular architecture with clean separation of concerns

---

**For developer documentation:** See `CLAUDE.md`
**For PyQt6 technical details:** See `PYQT6_VERSION.md`
