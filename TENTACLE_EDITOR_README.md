# Simple Tentacle Editor - Technical Documentation

## Overview

A standalone 3D tentacle creature editor featuring three novel mathematical algorithms for generating perfectly connected, organic tentacles. Built with Ursina Engine as a proof-of-concept for procedural creature generation.

**File:** `tentacle_editor_simple.py`
**Lines of Code:** ~400
**Dependencies:** Ursina 8.2.0+

---

## Quick Start

```bash
# Run the editor
python3 tentacle_editor_simple.py
```

**Controls:**
- **1/2/3** - Set tentacle count (1, 2, or 3 tentacles)
- **Q/W/E** - Switch algorithm (Catenary/Bezier/Fourier)
- **+/-** - Adjust segment count (5-20)
- **Mouse Drag** - Orbit camera
- **Scroll** - Zoom in/out
- **R** - Reset camera
- **ESC** - Quit

---

## Why This Was Created

The original DNA editor (`dna_editor/main.py`) failed because:
- Over-complicated architecture (constraint solvers, anatomy graphs, multiple modules)
- Segments were placed individually, causing disconnection issues
- Too many parameters and UI controls
- Algorithm wasn't "smart enough" mathematically

**Solution:** Generate the entire tentacle curve mathematically FIRST, then place segments along it. This guarantees perfect continuity.

---

## Three Mathematical Algorithms

### 1. Catenary Curve (Physics-Based)

**Mathematics:** `y = a * cosh(x/a)`

The catenary is the natural shape a hanging chain makes under gravity. This creates realistic drooping tentacles.

**Parameters:**
- `sag_factor` - Controls how much the tentacle sags (0.1 = tight, 1.0 = loose)

**Best For:** Realistic hanging appendages, tentacles at rest

**Implementation:** Lines 21-76

```python
# Key formula
y = a * (math.cosh(x / a) - 1)
```

---

### 2. Bezier Curve (Cubic Polynomial)

**Mathematics:** `B(t) = (1-t)³P₀ + 3(1-t)²tP₁ + 3(1-t)t²P₂ + t³P₃`

Uses four control points to create smooth S-curves. Control points are automatically calculated from anchor/target positions.

**Parameters:**
- `control_strength` - How far control points deviate from straight line

**Best For:** Elegant curves, posed tentacles, artistic control

**Implementation:** Lines 79-129

```python
# Control points create the curve shape
p1 = anchor + direction * (length * control_strength) + side * (length * 0.2)
p2 = target - direction * (length * control_strength) - side * (length * 0.2)
```

---

### 3. Fourier Series (Wave Composition)

**Mathematics:** `P(t) = base_curve(t) + Σ(Aₙ sin(nωt + φₙ))`

Combines multiple sine/cosine waves at different frequencies to create complex organic shapes.

**Parameters:**
- `num_waves` - Number of wave components (3 recommended)
- `amplitude` - Wave strength as fraction of tentacle length

**Best For:** Alien/organic appearance, undulating motion, complex curves

**Implementation:** Lines 132-189

```python
# Each wave contributes to the final shape
for n in range(1, num_waves + 1):
    wave_amp = amplitude * length / n  # Higher frequencies = smaller amplitude
    offset_x += wave_amp * math.sin(freq * t * math.pi + phase)
```

---

## Technical Architecture

### Class Structure

```
TentacleEditor (Main App)
    └── TentacleCreature
            ├── body (Entity - sphere)
            └── tentacles[] (List of Tentacle)
                    └── segments[] (List of Entity - spheres)
```

### Key Design Decisions

1. **Single File Design**
   - All code in one file for simplicity
   - No external modules or dependencies beyond Ursina
   - Easy to understand and modify

2. **Curve-First Approach**
   ```python
   # OLD WAY (failed):
   for i in range(segments):
       place_segment_at_angle(i)  # Disconnected!

   # NEW WAY (works):
   curve_points = generate_curve(anchor, target, segments)
   for i, point in enumerate(curve_points):
       place_segment_at(point)  # Guaranteed connected!
   ```

3. **Sphere Chain Segments**
   - Each segment is a sphere
   - Overlapping spheres create smooth organic appearance
   - Taper effect: base thickness × (1 - segment_index/total × 0.6)

4. **Animation System**
   - Segments store `base_position`
   - Wave animation adds sinusoidal offsets
   - Phase offset per tentacle for variety

---

## Code Organization

### Mathematical Functions (Lines 17-189)
- `catenary_curve()` - Physics-based hanging chain
- `bezier_curve()` - Cubic polynomial curves
- `fourier_curve()` - Wave composition

### Tentacle Class (Lines 192-273)
- `__init__()` - Generate curve, create segments
- `update_animation()` - Wave motion
- `destroy()` - Cleanup

### TentacleCreature Class (Lines 276-371)
- `__init__()` - Create body
- `rebuild()` - Regenerate tentacles with new parameters
- `update_animation()` - Pulse body, animate tentacles

### TentacleEditor Class (Lines 374-566)
- `__init__()` - Setup scene, camera, UI
- `update()` - Main loop (camera, animation, input)
- UI controls and parameter management

---

## Key Parameters

### Creature-Level
- `num_tentacles` - 1-3 tentacles
- `segments_per_tentacle` - 5-20 segments (12 recommended)
- `algorithm` - 'catenary', 'bezier', or 'fourier'

### Tentacle-Level
- `anchor` - Attachment point on body (Vec3)
- `target` - Tip target position (Vec3)
- `thickness` - Base thickness (0.25, tapers to 0.1 at tip)

### Algorithm-Specific
- Catenary: `sag_factor = 0.6`
- Bezier: `control_strength = 0.4`
- Fourier: `num_waves = 3, amplitude = 0.15`

---

## Troubleshooting

### Issue: Nothing visible except debug marker

**Cause:** Entity parenting issue - `parent=None` prevents scene addition

**Solution:** Remove parent parameter (defaults to scene)
```python
# BAD:
self.root = Entity(parent=None, ...)

# GOOD:
self.root = Entity(...)  # Defaults to scene
```

### Issue: Tentacles disconnected from body

**Cause:** Segments placed individually without curve generation

**Solution:** Generate complete curve first, then place segments along it

### Issue: Camera not initialized

**Cause:** Camera only positioned in update loop

**Solution:** Set camera position in `__init__()` before first frame

---

## Performance Notes

- **Entity Count:** Body (1) + Tentacles (2) + Segments (2 × 12 = 24) = **27 entities**
- **Framerate:** 60 FPS+ on most hardware
- **Memory:** Minimal (no textures, procedural geometry only)

Scaling to more tentacles:
- 3 tentacles × 20 segments = 61 entities (still fast)
- 10 tentacles × 20 segments = 201 entities (may slow down)

---

## Future Enhancements

### Short-Term (Easy)
1. Add slider widgets for real-time parameter adjustment
2. Export creature to .obj or .json format
3. Add more body shapes (ellipsoid, cube, custom)
4. Randomize button for quick variations

### Medium-Term (Moderate)
1. Multiple tentacle layers (upper/lower body)
2. Tentacle branching (sub-tentacles)
3. Texture/material system
4. Save/load creature presets

### Long-Term (Complex)
1. Inverse kinematics for tentacles
2. Physics simulation (tentacles react to forces)
3. Animation timeline editor
4. Export to game-ready format with animations

---

## Integration with Roguelike Game

To use these tentacles in the main game (`graphics3d/enemies/`):

1. **Copy Algorithm Functions**
   ```python
   # Copy catenary_curve, bezier_curve, fourier_curve to graphics3d/utils.py
   ```

2. **Create Enemy Variant**
   ```python
   # graphics3d/enemies/tentacle_horror.py
   from graphics3d.utils import bezier_curve

   def create_tentacle_horror(parent):
       body = Entity(model='sphere', scale=1.2, parent=parent)

       for i in range(4):  # 4 tentacles
           curve = bezier_curve(anchor, target, 15)
           # Create segments along curve...
   ```

3. **Add to Enemy Pool**
   ```python
   # entities.py
   'tentacle_horror': create_tentacle_horror
   ```

---

## Mathematical Comparison

| Algorithm | Continuity | Realism | Complexity | Performance |
|-----------|------------|---------|------------|-------------|
| Catenary  | C∞         | High    | Low        | Fast        |
| Bezier    | C²         | Medium  | Low        | Fast        |
| Fourier   | C∞         | Low     | Medium     | Fast        |

**Continuity:**
- C² = Second derivative continuous (smooth but may have slight kinks)
- C∞ = Infinitely differentiable (perfectly smooth)

**Recommendation:** Use Bezier for general purpose, Catenary for realism, Fourier for alien creatures.

---

## Code Quality Notes

### Strengths
- Single file, easy to understand
- Well-commented mathematical sections
- Clear separation of concerns (math → tentacle → creature → editor)
- Comprehensive debug output

### Weaknesses
- Hard-coded parameters (could be configurable)
- No error handling (assumes valid input)
- UI is basic (could use proper widgets)
- No undo/redo system

### Recommended Improvements
1. Extract algorithms to separate module for reusability
2. Add parameter validation (min/max ranges)
3. Create proper UI panel system (Ursina's Panel widget)
4. Add keyboard shortcuts help overlay

---

## Credits

**Created:** 2025-10-15
**Purpose:** Proof-of-concept for mathematically-generated tentacle creatures
**Replaces:** `dna_editor/main.py` (overcomplicated, disconnected segments)
**Status:** Fully functional, ready for integration

---

## Summary

This tentacle editor demonstrates that **simple mathematics done right** beats complex systems. By generating curves mathematically before placing segments, we guarantee perfect continuity. The three algorithms (Catenary, Bezier, Fourier) provide different aesthetic options while maintaining the same clean architecture.

**Key Lesson:** When procedural generation fails, go back to the math. A good formula is worth a thousand constraints.
