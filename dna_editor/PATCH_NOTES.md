# DNA Creature Editor - Patch Notes

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
