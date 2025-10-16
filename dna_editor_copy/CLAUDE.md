# DNA Editor - Developer Quickstart

A standalone 3D interactive tool for designing procedural tentacle creatures using mathematical curve algorithms.

## Quick Start

```bash
# From project root
python3 dna_editor/main.py

# Or directly from the folder
cd dna_editor
python3 main.py
```

## What It Does

Creates animated 3D tentacle creatures using two mathematical algorithms:
- **Bezier Curves** - Smooth cubic polynomial curves
- **Fourier Series** - Organic wave-based shapes

Real-time parameter adjustment with sliders, presets, and undo/redo system.

## Architecture

**Clean modular design** - each file ~100-200 lines (vs. original 1000-line monolith)

```
dna_editor/
├── main.py                      # Entry point (80 lines)
│
├── core/                        # Math & Config (no dependencies)
│   ├── curves.py               # Bezier & Fourier generators
│   └── constants.py            # All configuration values
│
├── models/                      # 3D Entities
│   ├── tentacle.py             # Single animated tentacle
│   └── creature.py             # Body + tentacles
│
├── ui/                          # UI Components
│   ├── info_panel.py           # Top bar, algorithm buttons
│   ├── parameters_panel.py     # Algorithm-specific sliders
│   ├── thickness_panel.py      # Thickness & taper controls
│   ├── presets_panel.py        # Preset buttons
│   └── help_overlay.py         # Help screen (H key)
│
└── controllers/                 # Application Logic
    ├── state_manager.py        # Undo/redo history (50 steps)
    ├── camera_controller.py    # Orbit & zoom
    └── editor_controller.py    # Main orchestrator
```

## Key Files

- **`controllers/editor_controller.py`** - Main app orchestration, keyboard input, updates
- **`core/curves.py`** - Pure mathematical curve generators (testable)
- **`models/creature.py`** - Creature entity with tentacles
- **`ui/parameters_panel.py`** - Dynamic sliders based on algorithm

## Development Notes

- **Pure math in `core/`** - No Ursina dependencies, easily testable
- **UI is modular** - Each panel is independent
- **State management** - Centralized history for undo/redo
- **No external assets** - All graphics procedurally generated

## Keyboard Controls (Developer Reference)

```
H           - Toggle help overlay
1/2/3       - Tentacle count
Q/W         - Switch algorithm (Bezier/Fourier)
+/-         - Segment count (5-20)
Ctrl+Z/Y    - Undo/Redo
R           - Reset camera
ESC         - Quit
```

## Making Changes

1. **Add a new algorithm?** → Add generator to `core/curves.py`, update `core/constants.py`
2. **Change UI layout?** → Modify specific panel in `ui/`
3. **Add new controls?** → Update `editor_controller.py` input handling
4. **Adjust animation?** → Edit `models/tentacle.py` update logic

## Dependencies

- **Ursina Engine** - 3D rendering (built on Panda3D)
- **Python 3.8+**
- **Math** (standard library)

## Integration with Roguelike

This tool is designed to generate tentacle DNA for creatures in the main roguelike game. Future: export configurations as JSON for import into `entities.py`.

---

**For user documentation:** See `README.md`
**Original monolithic version:** `main.py.backup` (archived)
