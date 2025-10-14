# DNA Creature Editor - Quick Start Guide

## Installation & Launch

```bash
# 1. Navigate to project root
cd /var/www/claudelike/roguelike

# 2. Ensure dependencies installed (if not already)
pip install -r requirements.txt

# 3. Launch editor
python3 dna_editor/main.py
```

## First Steps

1. **Browse Presets**: Click "PREV" and "NEXT" to see example creatures
2. **Experiment**: Use +/- buttons to adjust parameters
3. **Randomize**: Click "RANDOM" for instant inspiration
4. **Camera**: Drag mouse to orbit, scroll to zoom

## Key Controls

| Action | Control |
|--------|---------|
| Orbit camera | Mouse drag |
| Zoom | Mouse scroll |
| Browse presets | PREV/NEXT buttons |
| Adjust parameter | +/- buttons |
| Randomize | RANDOM button |
| Reset camera | R key |
| Toggle help | H key |
| Exit | ESC key |

## Example Workflow

### Creating a New Creature

1. Click **"NEW"** to start fresh
2. Adjust **Body Size** to 0.8
3. Change **Body Hue** to 180 (teal)
4. Set **Tentacle Count** to 10
5. Increase **Wave Speed** to 3.0
6. Add **Spikes** by incrementing to 20

### Tips

- **More segments** = smoother tentacle motion (but more entities)
- **Higher wave amplitude** = more dramatic movement
- **Eye patterns**: Try "spider" for creepy look
- **Color**: Hue 0-60 = reds, 120-180 = greens/cyans, 240-300 = blues/purples

## Parameter Quick Reference

| Parameter | Range | Effect |
|-----------|-------|--------|
| Body Size | 0.3 - 1.2 | Larger = bigger creature |
| Body Hue | 0 - 360 | Color (HSV hue) |
| Tentacle Count | 4 - 12 | More = busier |
| Length | 0.8 - 3.0 | Longer reach |
| Segments | 5 - 15 | Smoother motion |
| Wave Speed | 0.5 - 5.0 | Animation frequency |
| Wave Amplitude | 5 - 40 | Motion intensity |
| Eyes | 0 - 8 | Decorative |
| Spikes | 0 - 30 | Surface detail |

## Troubleshooting

**Can't see creature?**
- Press R to reset camera
- Scroll out to zoom out
- Check console for errors

**Laggy performance?**
- Reduce segment count to 8
- Reduce tentacle count to 6
- Reduce spike count to 10

**Want to save your design?**
- Presets auto-save in `dna_editor/presets/`
- Copy preset JSON files to share
- Edit JSON manually for fine control

## Next Steps

- Read `README.md` for full documentation
- Check `presets/examples.json` for inspiration
- Experiment with extreme parameter values!

---

Enjoy creating horrifying tentacle monsters! 🐙
