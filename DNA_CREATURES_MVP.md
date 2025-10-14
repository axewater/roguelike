# DNA Creature Editor - MVP 1.0 Development Plan

**Project**: Visual creature design tool for procedural monster creation
**Scope**: Tentacle-based creatures only (MVP)
**Timeline**: 1 week
**Status**: Planning Phase

---

## 1. Overview

### Purpose
A standalone Python application that allows designers to create and visualize tentacle-based creatures through an interactive UI. Parameters can be adjusted in real-time with immediate visual feedback.

### Goals
- ✅ Design tentacle horror creatures visually
- ✅ Adjust all creature parameters with sliders/inputs
- ✅ See changes in real-time 3D preview
- ✅ Create and save multiple creature presets
- ✅ Load and edit existing presets
- ✅ Export presets for game integration (format TBD, out of scope)

### Non-Goals (Future Versions)
- ❌ Slime creatures (MVP 2.0)
- ❌ Anemone creatures (MVP 2.0)
- ❌ Animation editing (MVP handles static preview + basic idle)
- ❌ In-game integration (separate task)
- ❌ Validation/constraints (basic only)
- ❌ Undo/redo (nice-to-have)

---

## 2. Technical Architecture

### Technology Stack

**UI Framework**: PyQt6
- Already used in the game
- Excellent widget library (sliders, spinboxes, color pickers)
- Easy layout management
- Can embed external windows

**3D Rendering**: Ursina Engine
- Already used in game's 3D mode
- Simple Entity-based API
- Runs in separate window alongside PyQt6 UI

**Data Format**: Python dictionaries → JSON export
- Human-readable
- Easy to copy/paste into game code
- Can be loaded as JSON files later

### Application Architecture

```
┌─────────────────────────────────────────┐
│  DNA Creature Editor (main.py)          │
│                                         │
│  ┌───────────────┐  ┌────────────────┐ │
│  │  PyQt6 UI     │  │  Ursina 3D     │ │
│  │  (Controls)   │◄─┤  (Preview)     │ │
│  │               │  │                │ │
│  │  - Sliders    │  │  - Entity      │ │
│  │  - Spinboxes  │  │  - Camera      │ │
│  │  - Colors     │  │  - Lighting    │ │
│  │  - Presets    │  │  - Animation   │ │
│  └───────────────┘  └────────────────┘ │
│         │                    ▲          │
│         │                    │          │
│         ▼                    │          │
│  ┌──────────────────────────┴────────┐ │
│  │  CreatureBuilder                  │ │
│  │  (Modular assembly logic)         │ │
│  └───────────────────────────────────┘ │
│         │                               │
│         ▼                               │
│  ┌───────────────────────────────────┐ │
│  │  Preset Manager                   │ │
│  │  (Save/Load/Export dictionaries)  │ │
│  └───────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

---

## 3. Feature Requirements

### 3.1 Core Parameters (Tentacle Horror)

**Body Parameters:**
- Body Size: 0.3 - 1.2 (float slider)
- Body Color Hue: 0 - 360 (color picker + slider)
- Body Shape: Sphere, Ellipsoid (dropdown) *optional for MVP*

**Tentacle Parameters:**
- Tentacle Count: 4 - 12 (integer slider/spinbox)
- Base Tentacle Length: 0.8 - 3.0 (float slider)
- Length Variation: 0% - 30% (percentage, randomizes individual tentacle lengths)
- Segments Per Tentacle: 5 - 15 (integer slider)
- Base Thickness: 0.05 - 0.20 (float slider)
- Thickness Taper: 0% - 100% (percentage, how much thinner at tip)

**Decoration Parameters:**
- Eye Count: 0 - 8 (integer spinbox)
- Eye Pattern: None, Dual, Spider, Ring (dropdown)
- Eye Size: 0.05 - 0.20 (float slider)
- Spike Count: 0 - 30 (integer slider)
- Spike Length: 0.1 - 0.5 (float slider)

**Animation Parameters:**
- Wave Speed: 0.5 - 5.0 (float slider)
- Wave Amplitude: 5 - 40 (degrees, float slider)
- Enable Idle Animation: On/Off (checkbox)

**Metadata:**
- Preset Name: Text input
- Description: Text area (optional notes)

### 3.2 UI Features

**Control Panel (Left Side, ~400px wide):**
- Collapsible sections for parameter groups
- Real-time value labels next to sliders
- "Reset to Default" button per section
- "Randomize" button (generates random valid values)
- Master "Reset All" button

**Preview Window (Right Side or separate):**
- 800x600 Ursina 3D viewport
- Orbiting camera (auto-rotate or mouse drag)
- Grid floor for scale reference
- Directional lighting
- Toggle animation on/off
- Reset camera button

**Preset Management (Bottom toolbar):**
- Preset dropdown (loads saved presets)
- "New Preset" button (clears to defaults)
- "Save Preset" button (saves current params)
- "Duplicate Preset" button (copy current)
- "Delete Preset" button
- "Export All" button (export to file)

**Status Bar:**
- Entity count display (performance indicator)
- Last saved timestamp
- Validation warnings (if any)

---

## 4. UI Layout (Detailed)

### Main Window Layout

```
┌────────────────────────────────────────────────────────────────┐
│ DNA Creature Editor v1.0 - Tentacle Horror              [_][□][X] │
├────────────────────────────────────────────────────────────────┤
│ File   Edit   View   Help                                      │
├───────────────┬────────────────────────────────────────────────┤
│               │                                                │
│  PARAMETERS   │           3D PREVIEW                           │
│               │                                                │
│ ┌───────────┐ │      [Ursina rendering window]                │
│ │  Body     │ │                                                │
│ ├───────────┤ │         OR embedded viewport                   │
│ │ Size: 0.6 │ │                                                │
│ │ [====|===]│ │      (Creature renders here)                   │
│ │           │ │                                                │
│ │ Hue: 280  │ │                                                │
│ │ [===|====]│ │      [Camera controls overlay]                 │
│ └───────────┘ │                                                │
│               │                                                │
│ ┌───────────┐ │                                                │
│ │ Tentacles │ │                                                │
│ ├───────────┤ │                                                │
│ │ Count: 8  │ │                                                │
│ │ Length:2.0│ │                                                │
│ │ Segments:10│ │                                               │
│ └───────────┘ │                                                │
│               │                                                │
│ ┌───────────┐ │                                                │
│ │Decorations│ │                                                │
│ ├───────────┤ │                                                │
│ │ Eyes: 2   │ │                                                │
│ │ Spikes: 15│ │                                                │
│ └───────────┘ │                                                │
│               │                                                │
│ ┌───────────┐ │                                                │
│ │ Animation │ │                                                │
│ ├───────────┤ │                                                │
│ │ Speed: 2.2│ │                                                │
│ │ Amp: 18   │ │                                                │
│ │ [x] Enable│ │                                                │
│ └───────────┘ │                                                │
│               │                                                │
│ [Randomize]   │                                                │
│ [Reset All]   │                                                │
│               │                                                │
├───────────────┴────────────────────────────────────────────────┤
│ Preset: [Ancient Dreadnought ▼] [New] [Save] [Duplicate] [Del]│
│ Name: [________________________]  [Export to Clipboard]        │
├────────────────────────────────────────────────────────────────┤
│ Entities: 89 | Last saved: 2 min ago | Ready                  │
└────────────────────────────────────────────────────────────────┘
```

### Alternative: Separate Windows

```
PyQt6 Control Window (400x800)        Ursina Preview (800x600)
┌──────────────────────────┐          ┌─────────────────────┐
│ [All sliders/controls]   │          │                     │
│                          │          │   3D Creature       │
│ [Parameter sections]     │   ◄──►   │   Preview           │
│                          │          │                     │
│ [Preset management]      │          │                     │
└──────────────────────────┘          └─────────────────────┘
```

---

## 5. Modular Creature Builder

### Module System (Reusable)

The editor uses the same modular system that will be in the game:

**TentacleModule:**
- Input: parent_entity, length, segments, thickness, angle, taper
- Output: List of segment entities (for animation)
- Creates cylinder chain with Ursina parent-child hierarchy

**BodyModule:**
- Input: size, color, shape_type
- Output: Body entity
- Creates sphere or ellipsoid

**EyeModule:**
- Input: parent, count, pattern, size
- Output: List of eye entities
- Places eyes in patterns (dual, spider, ring)

**SpikeModule:**
- Input: parent, count, length
- Output: List of spike entities
- Randomly distributes spikes on body surface

### CreatureBuilder Class

```
CreatureBuilder:
    - build_from_parameters(params_dict) → Creature
    - rebuild_creature(params_dict) → updates existing creature
    - clear_creature() → removes all entities
    - get_entity_count() → int
```

**Rebuild Strategy:**
When a parameter changes:
1. Destroy all existing entities
2. Rebuild from scratch with new parameters
3. Reset camera/animation state

*(Incremental updates possible in future, but overkill for MVP)*

---

## 6. Parameter → Entity Mapping

### How Parameters Drive Generation

**Example Flow:**

```
User sets:
  - tentacle_count = 8
  - base_length = 2.0
  - length_variation = 20%
  - segments = 10
  - thickness = 0.1
  - taper = 50%

Builder calculates:
  - angle_step = 360 / 8 = 45°
  - For each tentacle:
      - length = 2.0 * random(0.8, 1.2) [20% variation]
      - Tentacle 0: angle=0°, length=2.15
      - Tentacle 1: angle=45°, length=1.93
      - Tentacle 2: angle=90°, length=2.08
      - ... etc

  - For each tentacle, build chain:
      - 10 segments
      - segment_length = length / 10
      - thickness at base = 0.1
      - thickness at tip = 0.1 * 0.5 = 0.05 (taper)
      - Each segment thickness interpolates
```

### Deterministic Randomness

Use seed for "Randomize" button and variations:
```
seed = hash(preset_name + timestamp)
rng = random.Random(seed)
```

For "length_variation", use preset's name as seed so same preset generates same variation pattern.

---

## 7. Implementation Phases

### Phase 1: Foundation (Day 1-2)

**Day 1: Project Setup + Basic UI**
- Create `dna_creature_editor.py` main file
- Set up PyQt6 main window
- Create basic layout (left panel, right panel)
- Add placeholder widgets (sliders, labels)
- Test PyQt6 window launches

**Day 2: Ursina Integration**
- Set up Ursina in separate window OR embedded
- Create basic scene (camera, lighting, grid floor)
- Test Ursina + PyQt6 running simultaneously
- Implement camera orbit/controls
- Test entity creation (spawn a test sphere)

**Deliverable:** UI launches with 3D preview window

---

### Phase 2: Core Builder (Day 3)

**Morning: Module Implementation**
- Implement `TentacleModule.build()`
- Implement `BodyModule.build()`
- Test tentacle generation with hardcoded params

**Afternoon: CreatureBuilder Class**
- Implement `CreatureBuilder.build_from_parameters()`
- Implement `CreatureBuilder.rebuild_creature()`
- Test rebuilding with different parameters

**Deliverable:** Can generate tentacle creature from parameter dict

---

### Phase 3: Parameter Controls (Day 4)

**Morning: Body + Tentacle Controls**
- Wire body size slider → rebuild
- Wire color picker → rebuild
- Wire tentacle count → rebuild
- Wire tentacle length slider → rebuild
- Wire segments slider → rebuild

**Afternoon: All Remaining Controls**
- Thickness, taper sliders
- Length variation slider
- Test all parameters update creature

**Deliverable:** All core parameters control creature appearance

---

### Phase 4: Decorations + Animation (Day 5)

**Morning: Eye + Spike Modules**
- Implement `EyeModule.build()`
- Implement `SpikeModule.build()`
- Wire eye count, pattern controls
- Wire spike count, length controls

**Afternoon: Animation System**
- Implement wave animation in Ursina update loop
- Wire animation speed/amplitude sliders
- Wire enable/disable checkbox
- Test animation with various parameters

**Deliverable:** Full creature with decorations and animation

---