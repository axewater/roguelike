# DNA Editor - Creature Tentacle Generator

Interactive 3D editor for designing procedural tentacle creatures using mathematical curve algorithms.

## Overview

This tool allows you to create and customize tentacle creatures in real-time using two powerful mathematical algorithms:

- **Bezier Curves**: Smooth, elegant curves with adjustable control strength
- **Fourier Series**: Organic, wave-based shapes with customizable frequency and amplitude

## Quick Start

```bash
# Run from project root
python3 dna_editor/main.py
```

## Features

- **Real-time Editing**: Adjust parameters with sliders and see instant results
- **Two Algorithms**: Switch between Bezier and Fourier curve generators
- **Thickness Controls**: Customize base thickness and taper factor
- **Preset System**: 3 built-in presets (Default, Wavy, Tight)
- **Undo/Redo**: Full history system (up to 50 steps)
- **Interactive Camera**: Orbit, zoom, and navigate the 3D scene
- **Help System**: Press H for in-app controls reference

## Controls

### Camera
- **Mouse Drag**: Orbit around creature
- **Scroll Wheel**: Zoom in/out
- **R**: Reset camera to default position

### Tentacles
- **1/2/3**: Set tentacle count (1, 2, or 3)
- **+/-**: Adjust segment count (5-20 segments)

### Algorithms
- **Q**: Switch to Bezier algorithm
- **W**: Switch to Fourier algorithm
- **Sliders**: Adjust algorithm-specific parameters

### Editing
- **Ctrl+Z**: Undo last change
- **Ctrl+Y**: Redo
- **Preset Buttons**: Load predefined configurations

### Other
- **H**: Toggle help overlay
- **ESC**: Quit application

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
2. **Wavy**: Fourier series with high wave count for organic look
3. **Tight**: Bezier curves with low control for more direct tentacles

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
- Ursina Engine
- Math (standard library)

## Architecture

The DNA Editor follows clean **separation of concerns** with a modular architecture:

### File Structure

```
dna_editor/
├── main.py                      # Entry point (60 lines)
├── core/                        # Mathematical & configuration
│   ├── curves.py               # Bezier & Fourier curve generators
│   └── constants.py            # All configuration constants
├── models/                      # 3D entity models
│   ├── tentacle.py             # Single tentacle with segments
│   └── creature.py             # Creature with body & tentacles
├── ui/                          # User interface components
│   ├── info_panel.py           # Top info display & algorithm buttons
│   ├── parameters_panel.py     # Algorithm-specific sliders
│   ├── thickness_panel.py      # Thickness & taper controls
│   ├── presets_panel.py        # Preset buttons
│   └── help_overlay.py         # Help screen overlay
├── controllers/                 # Application logic
│   ├── state_manager.py        # Undo/redo history system
│   ├── camera_controller.py    # Camera orbit & zoom logic
│   └── editor_controller.py    # Main orchestration controller
└── README.md                    # This file
```

### Design Principles

1. **Single Responsibility**: Each module has one clear purpose
2. **Separation of Concerns**: Math, models, UI, and logic are isolated
3. **Testability**: Pure functions and clear interfaces for testing
4. **Maintainability**: ~100-200 lines per file (vs. 1000 lines monolithic)
5. **Reusability**: Curve generators can be used independently

## Future Enhancements

Potential additions for future versions:
- Export tentacle DNA as JSON
- Import/save custom presets
- Multi-creature scene
- Texture/material customization
- Eye/spike/limb attachments
- Animation pattern editor

## Notes

- All graphics are procedurally generated (no external assets)
- Designed for integration with the roguelike game's creature system
- Modular architecture with clean separation of concerns
- Original monolithic version backed up as `main.py.backup`
