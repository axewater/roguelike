# DNA Editor - Parameter Guide

## What Each Parameter Does (All are now working!)

### Shape & Algorithm Section

**Tentacles (1-12)**
- Changes number of main tentacles around the body
- Distributed using Fibonacci sphere pattern

**Segments (5-20)**
- Controls smoothness of each tentacle
- More segments = smoother curves, more detail

**Algorithm**
- **Bezier**: Smooth S-curves with control points
  - *Control Strength*: How far the curve bends (0.1-0.8)
- **Fourier**: Wave-based organic shapes
  - *Wave Count*: Number of wave harmonics (1-7)
  - *Amplitude*: Intensity of wave motion (0.05-0.4)

### Appearance Section

**Base Color** (Color Picker)
- Sets the main color for body and tentacles
- Click to open color picker dialog
- Body automatically matches this color

**Color Variation (0.0-0.3)**
- How much each tentacle's color shifts
- Creates rainbow/gradient effect across tentacles
- 0.0 = all same color, 0.3 = maximum variation

**Base Thickness (0.1-0.5)**
- Starting thickness of tentacles at the base
- Affects overall chunkiness

**Taper (0.0-1.0)**
- How much tentacles thin toward the tip
- 0.0 = no taper (cylindrical), 1.0 = sharp point

**Body Size (0.5-2.0)**
- Scale of the central sphere body
- Affects tentacle anchor positions

### Branching Section

**Depth (0-3)**
- How many levels of sub-tentacles to create
- 0 = no branches, 3 = branches on branches on branches
- Exponential complexity growth!

**Count Per Level (1-3)**
- How many child tentacles spawn from each parent
- Combined with depth for fractal-like growth

**Total Segments Display**
- Shows estimated segment count across all tentacles
- Helps avoid performance issues

### Animation Section (Now affects ATTACK too!)

**Wave Speed (0.5-5.0)**
- Speed of idle wave motion
- **Also affects attack speed!** Faster = quicker whip strike
- Scales both idle undulation and attack whip wave propagation

**Wave Intensity (0.0-0.2)**
- Amplitude of idle wave motion
- **Also affects attack intensity!** Higher = more violent strike
- Scales both idle motion and attack whip amplitude

**Pulse Speed (0.5-3.0)**
- Body breathing rate
- Controls how fast the body sphere expands/contracts

**Pulse Amount (0.0-0.15)**
- How much the body expands when breathing
- 0.0 = no pulse, 0.15 = large breathing motion

### Presets & Actions

**Preset Buttons**
- Quick-load pre-configured creature designs
- Useful starting points for experimentation

**⚡ ATTACK! ⚡**
- Triggers whip-like attack animation toward camera
- All tentacles strike simultaneously
- Uses mathematical whip physics:
  - Exponential wave acceleration
  - Distance-based stretching
  - Helical curl motion
- **Now responds to Wave Speed and Wave Intensity sliders!**

**Undo / Redo**
- 50-step history for parameter changes
- Keyboard shortcuts: Ctrl+Z / Ctrl+Y

**Export JSON**
- Saves current configuration to file
- For importing into the main roguelike game

## How Parameters Interact

- **Body Size affects tentacle anchors**: Larger body = tentacles spread wider
- **Branching multiplies segments**: Total segments = tentacles × segments × branches
- **Animation parameters affect both idle and attack**: Speed/intensity sliders now control both modes
- **Color variation creates gradients**: Each tentacle shifts hue based on its index
- **Taper + Thickness = shape profile**: Control the tentacle silhouette

## Performance Tips

- High segment count (20) + high branching (3/3) = **LOTS** of spheres
- Watch the "Total Segments" counter in the Branching section
- Keep below ~500 segments for smooth 60 FPS animation
- Attack animation is computationally expensive due to complex math

## Testing Attack Animation

1. Adjust **Wave Speed** and **Wave Intensity** sliders
2. Click **⚡ ATTACK! ⚡**
3. Notice how attack speed and violence change with the sliders
4. Move camera (drag/scroll) to different positions
5. Attack again - tentacles will stretch/curl toward new camera position

Enjoy creating procedural tentacle monsters! 🐙
