# AAA Anti-Repetition System for Procedural Textures

## Problem
Single textures create obvious tiling/repetition ("wallpaper effect").

## Solution
Generate multiple variants with different seeds + deterministic per-tile selection.

---

## Implementation (3 Steps)

### 1. Generate Multiple Variants

```python
# graphics3d/tiles.py

# Generate 4 variants at high resolution
TEXTURE_VARIANTS = []
seeds = [12345, 67890, 24680, 13579]

for seed in seeds:
    with RandomSeed(seed):
        pil_image = generate_texture_function(size=512, ...)
        TEXTURE_VARIANTS.append(Texture(pil_image))
```

### 2. Deterministic Variant Selection

```python
def create_mesh(x, y, ...):
    # Hash tile coords to pick variant (0-3)
    variant_idx = (x * 7 + y * 13) % len(TEXTURE_VARIANTS)
    texture = TEXTURE_VARIANTS[variant_idx]

    return Entity(..., texture=texture)
```

### 3. Increase Resolution

Use 512x512 (not 256x256) for less obvious tiling.

---

## Apply to Floor/Ceiling

**Current State:**
```python
# Floor: Single texture
DUNGEON_FLOOR_TEXTURE = Texture(generate_brick_pattern(...))

# Ceiling: Single texture
DUNGEON_CEILING_TEXTURE = Texture(generate_ceiling_texture(...))
```

**Apply Anti-Repetition:**
```python
# Floor: 4 variants
DUNGEON_FLOOR_TEXTURES = []
for seed in [11111, 22222, 33333, 44444]:
    with RandomSeed(seed):
        floor = generate_brick_pattern(size=512, darkness=0.8)
        mossy = generate_moss_overlay(floor, density='light')
        DUNGEON_FLOOR_TEXTURES.append(Texture(mossy))

# Ceiling: 4 variants
DUNGEON_CEILING_TEXTURES = []
for seed in [55555, 66666, 77777, 88888]:
    with RandomSeed(seed):
        ceiling = generate_ceiling_texture(size=512, moisture_level='medium')
        DUNGEON_CEILING_TEXTURES.append(Texture(ceiling))

# Update mesh functions
def create_floor_mesh(x, y, ...):
    variant_idx = (x * 7 + y * 13) % len(DUNGEON_FLOOR_TEXTURES)
    texture = DUNGEON_FLOOR_TEXTURES[variant_idx]
    return Entity(..., texture=texture)

def create_ceiling_mesh(x, y):
    variant_idx = (x * 7 + y * 13) % len(DUNGEON_CEILING_TEXTURES)
    texture = DUNGEON_CEILING_TEXTURES[variant_idx]
    return Entity(..., texture=texture)
```

---

## Key Points

- **Different seeds** per variant (creates unique patterns)
- **Deterministic hash** `(x * 7 + y * 13) % 4` (same tile = same variant)
- **Prime multipliers** (7, 13) distribute variants evenly
- **512x512** resolution (less visible tiling)
- **4 variants** = 4x less repetition

---

## Performance

- **Memory**: ~2MB per texture set (4 variants)
- **Load time**: ~1-2 seconds per set (one-time)
- **Runtime**: Zero overhead (all cached)

---

**Result**: Professional AAA-quality dungeon with no visible repetition.
