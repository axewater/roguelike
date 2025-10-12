# Procedural Texture System Handover

**Document Version:** 1.0
**Date:** 2025-10-12
**Project:** Claude-Like Roguelike 3D
**Task:** Port procedural texture generation to PIL/Pillow for Ursina integration

---

## Executive Summary

### Goal
Port the procedural texture generation system from PyQt6's QPainter (currently used in the OpenGL title screen) to PIL/Pillow, enabling high-quality procedural graphics throughout the Ursina-based 3D game.

### Why This Matters
- The OpenGL title screen (`ui/screens/title_screen_3d.py`) has **stunning** procedural textures (moss-covered carved stone)
- The main 3D game uses Ursina Engine, which doesn't have QPainter
- PIL/Pillow provides equivalent functionality and integrates seamlessly with Ursina
- This unlocks procedural textures for dungeon walls, items, enemies, and more

### Scope
- Create modular texture generation system using PIL/Pillow
- Port existing algorithms from `title_screen_3d.py`
- Design clean API for Ursina integration
- Maintain separation of concerns (texture generation ≠ game logic)

### Time Estimate
**12-16 hours** for full implementation and integration

---

## Background

### Current State

**What Works:**
- `ui/screens/title_screen_3d.py:238-707` contains procedural texture generation using QPainter
- Generates brick patterns, moss overlays, weathering effects, carved letters
- Creates 256x256 RGBA textures uploaded to OpenGL

**The Problem:**
- This code is tied to PyQt6's `QPainter` and `QImage`
- The main 3D game uses Ursina Engine (Panda3D-based)
- Ursina accepts PIL `Image` objects via `Texture()` class
- We need the same quality textures in Ursina

**Reference Files:**
- `ui/screens/title_screen_3d.py:238-707` - Existing texture generation
- `graphics3d/utils.py` - Current Ursina utilities (may need texture helpers)

---

## Architecture

### Design Principles

1. **Separation of Concerns**
   - Texture generation = Pure image processing (no game logic)
   - Game entities = Use textures (no generation logic)
   - Cache layer = Performance optimization (separate from generation)

2. **Modularity**
   - Each texture type in its own module
   - Composable effects (bricks + moss + weathering)
   - Easy to add new generators

3. **Framework Independence**
   - Core generators work with PIL Image objects
   - Thin adapter for Ursina `Texture` wrapper
   - Could be reused in 2D mode if needed

### Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Game Layer (Ursina)                  │
│  renderer3d.py, graphics3d/tiles.py, graphics3d/items/  │
└────────────────────────┬────────────────────────────────┘
                         │ uses Texture objects
                         ▼
┌─────────────────────────────────────────────────────────┐
│              Texture Management Layer                    │
│  textures/__init__.py (Public API)                      │
│  - get_brick_texture()                                   │
│  - get_moss_stone_texture()                              │
│  - get_weathered_texture()                               │
└────────────────────────┬────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Cache Layer  │ │  Generators  │ │  Utilities   │
│              │ │              │ │              │
│ cache.py     │ │ bricks.py    │ │ generator.py │
│              │ │ organic.py   │ │ (base class) │
│ - LRU cache  │ │ weathering.py│ │              │
│ - Hash keys  │ │ carved.py    │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
                         │
                         ▼ produces
                  PIL Image objects
```

---

## File Structure

### New Directory: `textures/`

All texture generation code lives here (separate from game logic).

```
textures/
├── __init__.py           # Public API, main entry point
├── generator.py          # Base classes and common utilities
├── bricks.py             # Brick pattern generation
├── organic.py            # Moss, tendrils, organic growth
├── weathering.py         # Stains, cracks, age effects
├── carved.py             # Carved text/symbols effects
├── cache.py              # Texture caching system
└── README.md             # Usage documentation

examples/
└── texture_demo.py       # Standalone demo (saves PNGs, shows Ursina preview)
```

### File Responsibilities

#### `textures/__init__.py`
**Purpose:** Public API for the rest of the codebase

**Exports:**
```python
from textures import (
    get_brick_texture,
    get_moss_stone_texture,
    get_carved_texture,
    get_weathered_texture,
    TextureCache,
    clear_cache
)
```

**Interface:**
```python
def get_brick_texture(size=256, darkness=1.0) -> Texture:
    """Get brick texture for Ursina"""

def get_moss_stone_texture(size=256, moss_density='heavy') -> Texture:
    """Get moss-covered stone texture"""

def get_carved_texture(char, size=256, bg='moss_stone') -> Texture:
    """Get carved letter/symbol texture"""
```

---

#### `textures/generator.py`
**Purpose:** Base classes and common utilities

**Contents:**
```python
class TextureGenerator:
    """Base class for all texture generators"""

    def __init__(self, size=256):
        self.size = size
        self.image = Image.new('RGBA', (size, size))
        self.draw = ImageDraw.Draw(self.image)

    def generate(self) -> Image.Image:
        """Generate and return PIL Image"""
        raise NotImplementedError

    def to_ursina_texture(self) -> 'ursina.Texture':
        """Convert to Ursina Texture object"""
        from ursina import Texture
        return Texture(self.generate())

class RandomSeed:
    """Context manager for reproducible randomness"""
    # Allows: with RandomSeed(12345): generate_texture()

def blend_images(base, overlay, mode='multiply'):
    """Blend two PIL images (like QPainter composition modes)"""

def add_noise(image, intensity=0.1):
    """Add perlin-like noise to image"""
```

---

#### `textures/bricks.py`
**Purpose:** Brick pattern generation (port from `title_screen_3d.py:238-284`)

**Key Functions:**
```python
def generate_brick_pattern(size=256, darkness=1.0) -> Image.Image:
    """
    Generate brick pattern with mortar lines

    Args:
        size: Texture size (power of 2 recommended)
        darkness: Multiplier for brightness (0.0-1.0)

    Returns:
        PIL Image with brick pattern
    """

def _draw_single_brick(draw, x, y, width, height, base_color):
    """Draw one brick with color variation and cracks"""

def _draw_mortar_lines(draw, width, height, mortar_color):
    """Draw mortar between bricks"""
```

**Port Notes:**
- `QPainter.fillRect()` → `ImageDraw.rectangle()`
- `QPainter.drawLine()` → `ImageDraw.line()`
- `QColor` → `(R, G, B, A)` tuples
- Random variations remain identical

---

#### `textures/organic.py`
**Purpose:** Moss, tendrils, organic growth (port from `title_screen_3d.py:303-567`)

**Key Functions:**
```python
def generate_moss_overlay(base_image, density='heavy') -> Image.Image:
    """
    Add organic moss growth to existing texture

    Args:
        base_image: PIL Image to add moss to
        density: 'light', 'medium', 'heavy'
    """

def draw_moss_patch(draw, x, y, size, color, draping=False):
    """
    Draw organic moss patch with irregular edges

    Args:
        draping: If True, tendrils grow downward
    """

def draw_dense_moss_base(draw, width, height, colors):
    """Draw dense moss layer covering top of texture"""
```

**Port Notes:**
- `QPolygonF` → `ImageDraw.polygon()`
- `QPointF` → `(x, y)` tuples
- Path-based drawing → Point lists
- Same algorithms, different API

---

#### `textures/weathering.py`
**Purpose:** Stains, cracks, age effects (port from `title_screen_3d.py:285-301`)

**Key Functions:**
```python
def add_weathering(image, intensity=1.0) -> Image.Image:
    """Add age marks, stains, discoloration"""

def add_cracks(image, num_cracks=5):
    """Add hairline cracks to surface"""

def add_stains(image, num_stains=15):
    """Add dark organic stains"""
```

---

#### `textures/carved.py`
**Purpose:** Carved text/symbols (port from `title_screen_3d.py:592-651`)

**Key Functions:**
```python
def generate_carved_texture(char, size=256, bg='moss_stone') -> Image.Image:
    """
    Generate texture with carved character

    Args:
        char: Single character to carve
        bg: 'moss_stone', 'brick', 'plain'
    """

def _draw_carved_layers(draw, char, font_path, size):
    """Draw 3-layer carved effect (shadow, highlight, main)"""
```

**Port Notes:**
- `QFont` → `PIL.ImageFont.truetype()`
- Multi-layer text drawing remains same concept
- Offsets create depth illusion

---

#### `textures/cache.py`
**Purpose:** Performance - avoid regenerating identical textures

**Implementation:**
```python
class TextureCache:
    """LRU cache for generated textures"""

    def __init__(self, max_size=100):
        self._cache = {}  # key -> (PIL Image, Ursina Texture)
        self._lru = []    # Access order
        self.max_size = max_size

    def get(self, key) -> Optional[Texture]:
        """Get cached texture or None"""

    def put(self, key, texture):
        """Cache a texture"""

    def clear(self):
        """Clear all cached textures"""

def make_cache_key(func_name, **kwargs) -> str:
    """Create deterministic cache key from parameters"""
```

---

#### `examples/texture_demo.py`
**Purpose:** Standalone testing and visual verification

**Features:**
```python
def save_texture_samples():
    """Generate and save PNG samples of all textures"""
    textures = [
        ('brick_normal.png', get_brick_texture()),
        ('brick_dark.png', get_brick_texture(darkness=0.7)),
        ('moss_heavy.png', get_moss_stone_texture('heavy')),
        ('carved_A.png', get_carved_texture('A')),
    ]
    # Save to output/textures/

def show_ursina_preview():
    """Launch Ursina window showing textured cubes"""
    # Grid of cubes with different textures
```

**Usage:**
```bash
python examples/texture_demo.py --save
python examples/texture_demo.py --preview
```

---

## Implementation Phases

### Phase 1: Infrastructure (2-3 hours)

**Deliverables:**
- `textures/` directory structure
- `generator.py` with base class and utilities
- `cache.py` with caching system
- `__init__.py` with stub functions

**Steps:**
1. Create directory structure
2. Implement `TextureGenerator` base class
3. Implement `blend_images()`, `add_noise()` utilities
4. Implement `TextureCache` class
5. Write basic unit tests

**Acceptance Criteria:**
- Can instantiate `TextureGenerator`
- Can blend two PIL images
- Cache stores and retrieves images
- All imports work

---

### Phase 2: Brick Patterns (2-3 hours)

**Deliverables:**
- `bricks.py` fully implemented
- Matches quality of `title_screen_3d.py:238-284`

**Steps:**
1. Study reference implementation in `title_screen_3d.py:238-284`
2. Port `_draw_brick_pattern()` to PIL
3. Port `_draw_single_brick()` logic
4. Add color variation and cracks
5. Apply darkness multiplier
6. Visual comparison test (OpenGL vs PIL output)

**Acceptance Criteria:**
- Generated brick texture visually matches OpenGL version
- Darkness parameter works (0.0 = black, 1.0 = normal)
- Random seed produces consistent results
- Performance < 50ms for 256x256 texture

**Code Sample:**
```python
# Before (QPainter)
painter.fillRect(x, y, width, height, brick_color)
painter.drawLine(x, y, x + length, y + offset)

# After (PIL)
draw.rectangle([x, y, x+width, y+height], fill=brick_color)
draw.line([x, y, x+length, y+offset], fill=crack_color, width=1)
```

---

### Phase 3: Organic Effects (3-4 hours)

**Deliverables:**
- `organic.py` fully implemented
- `weathering.py` fully implemented
- Moss generation matches OpenGL quality

**Steps:**
1. Port `_draw_organic_moss_patch()` (lines 303-415)
2. Port `_draw_dense_moss_base()` (lines 417-491)
3. Port `_generate_moss_overlay()` (lines 493-567)
4. Port weathering effects (lines 285-301)
5. Implement draping tendril logic
6. Test composition: brick + moss + weathering

**Acceptance Criteria:**
- Moss patches have irregular organic edges
- Draping tendrils grow downward
- Dense moss base covers top with wavy edge
- Weathering adds convincing age effects
- Layering order matches OpenGL version

**Tricky Parts:**
- `QPolygonF` → need point lists for `ImageDraw.polygon()`
- Irregular edges require careful point generation
- Tendrils are iterative (circles getting smaller)

---

### Phase 4: Carved Effects (2-3 hours)

**Deliverables:**
- `carved.py` fully implemented
- Can generate carved letter textures

**Steps:**
1. Port `_generate_letter_textures()` logic (lines 592-651)
2. Handle font loading (TrueType font needed)
3. Implement 3-layer effect (shadow, highlight, main)
4. Support custom background textures
5. Test with all uppercase letters and numbers

**Acceptance Criteria:**
- Carved letters have depth illusion
- Works with moss_stone background
- Font rendering is clean
- Shadow/highlight offsets create 3D effect

**Font Handling:**
```python
from PIL import ImageFont

# Try common font paths
font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "/System/Library/Fonts/Helvetica.ttc"
]

for path in font_paths:
    if os.path.exists(path):
        font = ImageFont.truetype(path, size=180)
        break
```

---

### Phase 5: Ursina Integration (2-3 hours)

**Deliverables:**
- Public API in `__init__.py`
- Integration with existing graphics3d modules
- Example usage in dungeon rendering

**Steps:**
1. Implement clean API functions in `__init__.py`
2. Add Ursina `Texture` wrapper functions
3. Update `graphics3d/tiles.py` to use procedural textures
4. Update `graphics3d/items/base.py` to support textured items
5. Add texture variety to dungeon walls
6. Test in-game performance

**Integration Points:**

**`graphics3d/tiles.py`** (dungeon walls):
```python
from textures import get_brick_texture, get_moss_stone_texture

class DungeonWall(Entity):
    def __init__(self, x, y):
        texture = get_moss_stone_texture(size=256, moss_density='medium')
        super().__init__(
            model='cube',
            texture=texture,
            position=(x, 0, y)
        )
```

**`graphics3d/items/base.py`** (item textures):
```python
from textures import get_weathered_texture

class Item3D(Entity):
    def __init__(self, color):
        # Add procedural wear to items
        texture = get_weathered_texture(base_color=color, intensity=0.5)
        super().__init__(model='cube', texture=texture)
```

**Acceptance Criteria:**
- Dungeon walls use procedural brick textures
- No FPS drop (cache is effective)
- Textures look good from all angles
- Memory usage is reasonable (< 50MB for textures)

---

### Phase 6: Polish & Examples (1-2 hours)

**Deliverables:**
- `examples/texture_demo.py` working
- `textures/README.md` with usage guide
- Performance benchmarks

**Steps:**
1. Create demo script that saves PNGs
2. Create Ursina preview window
3. Write README with API examples
4. Run performance benchmarks
5. Add type hints to all functions
6. Add docstrings with examples

**README Should Include:**
- Quick start example
- API reference
- Parameter explanations
- Performance tips
- Extending with new generators

---

## Code Samples

### Example 1: Basic Brick Texture

**Before (QPainter in title_screen_3d.py:238-276)**
```python
def _draw_brick_pattern(self, painter: QPainter, width: int, height: int):
    brick_base = QColor(65, 60, 55)
    mortar = QColor(95, 90, 85)
    painter.fillRect(0, 0, width, height, mortar)

    brick_height = height // 4
    brick_width = width // 3
    mortar_size = 3

    for row in range(4):
        y = row * brick_height
        offset = (brick_width // 2) if row % 2 == 1 else 0

        for col in range(-1, 4):
            x = col * brick_width + offset
            variation = random.randint(-8, 8)
            brick_color = QColor(
                brick_base.red() + variation,
                brick_base.green() + variation,
                brick_base.blue() + variation
            )
            brick_rect = (
                x + mortar_size,
                y + mortar_size,
                brick_width - mortar_size * 2,
                brick_height - mortar_size * 2
            )
            painter.fillRect(*brick_rect, brick_color)
```

**After (PIL in textures/bricks.py)**
```python
def generate_brick_pattern(size=256, darkness=1.0):
    brick_base = (65, 60, 55)
    mortar = (95, 90, 85)

    image = Image.new('RGBA', (size, size), color=mortar + (255,))
    draw = ImageDraw.Draw(image)

    brick_height = size // 4
    brick_width = size // 3
    mortar_size = 3

    for row in range(4):
        y = row * brick_height
        offset = (brick_width // 2) if row % 2 == 1 else 0

        for col in range(-1, 4):
            x = col * brick_width + offset
            variation = random.randint(-8, 8)
            brick_color = (
                brick_base[0] + variation,
                brick_base[1] + variation,
                brick_base[2] + variation,
                255
            )
            brick_rect = [
                x + mortar_size,
                y + mortar_size,
                x + brick_width - mortar_size,
                y + brick_height - mortar_size
            ]
            draw.rectangle(brick_rect, fill=brick_color)

    # Apply darkness
    if darkness != 1.0:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(darkness)

    return image
```

---

### Example 2: Moss Overlay

**Before (QPainter - lines 303-416)**
```python
def _draw_organic_moss_patch(self, painter: QPainter, x: float, y: float,
                             size: float, moss_color: QColor, draping: bool = False):
    from PyQt6.QtGui import QPolygonF
    from PyQt6.QtCore import QPointF

    num_points = random.randint(8, 16)
    points = []
    for i in range(num_points):
        angle = (2 * math.pi * i) / num_points
        radius_var = random.uniform(0.5, 1.0)
        radius = size * radius_var
        angle_wobble = random.uniform(-0.3, 0.3)
        px = x + radius * math.cos(angle + angle_wobble)
        py = y + radius * math.sin(angle + angle_wobble)
        points.append(QPointF(px, py))

    polygon = QPolygonF(points)
    painter.setBrush(moss_color)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawPolygon(polygon)
```

**After (PIL - textures/organic.py)**
```python
def draw_moss_patch(draw, x, y, size, moss_color, draping=False):
    """Draw organic moss patch with irregular edges"""
    num_points = random.randint(8, 16)
    points = []
    for i in range(num_points):
        angle = (2 * math.pi * i) / num_points
        radius_var = random.uniform(0.5, 1.0)
        radius = size * radius_var
        angle_wobble = random.uniform(-0.3, 0.3)
        px = x + radius * math.cos(angle + angle_wobble)
        py = y + radius * math.sin(angle + angle_wobble)
        points.append((px, py))

    draw.polygon(points, fill=moss_color, outline=None)
```

**Key Differences:**
- `QPointF(x, y)` → `(x, y)` tuple
- `QPolygonF(points)` → just `points` list
- `painter.drawPolygon()` → `draw.polygon()`
- Same logic, simpler API

---

### Example 3: Ursina Integration

```python
# In graphics3d/tiles.py
from textures import get_moss_stone_texture
from ursina import Entity

class WallTile(Entity):
    def __init__(self, x, z, wall_type='dungeon'):
        # Get procedural texture (cached automatically)
        if wall_type == 'dungeon':
            texture = get_moss_stone_texture(size=256, moss_density='heavy')
        elif wall_type == 'brick':
            texture = get_brick_texture(size=256, darkness=0.8)
        else:
            texture = get_weathered_texture(size=256)

        super().__init__(
            model='cube',
            texture=texture,
            position=(x, 0, z),
            scale=(1, 2, 1)  # Tall wall
        )
```

---

## Testing Strategy

### Unit Tests

**File:** `tests/test_textures.py`

```python
import unittest
from PIL import Image
from textures import *

class TestBrickGeneration(unittest.TestCase):
    def test_brick_texture_size(self):
        img = generate_brick_pattern(size=256)
        self.assertEqual(img.size, (256, 256))

    def test_brick_darkness(self):
        img_normal = generate_brick_pattern(darkness=1.0)
        img_dark = generate_brick_pattern(darkness=0.5)
        # Dark version should have lower average brightness
        avg_normal = sum(img_normal.getdata()) / (256*256)
        avg_dark = sum(img_dark.getdata()) / (256*256)
        self.assertLess(avg_dark, avg_normal)

    def test_deterministic_with_seed(self):
        with RandomSeed(12345):
            img1 = generate_brick_pattern()
        with RandomSeed(12345):
            img2 = generate_brick_pattern()
        # Should be identical
        self.assertEqual(list(img1.getdata()), list(img2.getdata()))

class TestMossGeneration(unittest.TestCase):
    def test_moss_overlay_adds_green(self):
        base = generate_brick_pattern()
        mossy = generate_moss_overlay(base, density='heavy')
        # Mossy version should have more green channel
        # (test color distribution)

class TestCache(unittest.TestCase):
    def test_cache_hit(self):
        cache = TextureCache()
        key = "brick_256_1.0"
        img = generate_brick_pattern()
        cache.put(key, img)
        cached = cache.get(key)
        self.assertIsNotNone(cached)
```

---

### Visual Regression Tests

**File:** `tests/test_visual_regression.py`

```python
def test_compare_to_opengl_reference():
    """Compare PIL output to saved OpenGL reference images"""
    # Reference images saved from title_screen_3d.py
    reference_dir = "tests/reference_textures/"

    tests = [
        ("brick_normal.png", lambda: generate_brick_pattern()),
        ("moss_heavy.png", lambda: generate_moss_stone_texture('heavy')),
        ("carved_A.png", lambda: generate_carved_texture('A')),
    ]

    for filename, generator_func in tests:
        reference = Image.open(reference_dir + filename)
        generated = generator_func()

        # Calculate perceptual difference (SSIM or MSE)
        similarity = calculate_similarity(reference, generated)

        # Should be > 95% similar
        assert similarity > 0.95, f"{filename} differs too much: {similarity}"
```

---

### Performance Benchmarks

**File:** `tests/benchmark_textures.py`

```python
import time

def benchmark_generation():
    """Measure texture generation performance"""
    iterations = 100

    start = time.time()
    for _ in range(iterations):
        img = generate_brick_pattern(size=256)
    elapsed = time.time() - start

    avg_time = elapsed / iterations
    print(f"Brick 256x256: {avg_time*1000:.2f}ms per texture")

    # Should be < 50ms per texture
    assert avg_time < 0.05

def benchmark_cache():
    """Measure cache effectiveness"""
    cache = TextureCache()

    # First generation (cache miss)
    start = time.time()
    tex1 = get_brick_texture()
    miss_time = time.time() - start

    # Second generation (cache hit)
    start = time.time()
    tex2 = get_brick_texture()
    hit_time = time.time() - start

    print(f"Cache miss: {miss_time*1000:.2f}ms")
    print(f"Cache hit: {hit_time*1000:.2f}ms")
    print(f"Speedup: {miss_time/hit_time:.1f}x")

    # Cache should be >10x faster
    assert hit_time < miss_time / 10
```

---

## Integration Points

### 1. Dungeon Walls (`graphics3d/tiles.py`)

**Current:**
```python
class WallTile(Entity):
    def __init__(self, x, z):
        super().__init__(
            model='cube',
            color=color.gray,  # Flat color
            position=(x, 0, z)
        )
```

**After Integration:**
```python
from textures import get_moss_stone_texture

class WallTile(Entity):
    def __init__(self, x, z, texture_variant=0):
        # Multiple texture variants for variety
        densities = ['light', 'medium', 'heavy']
        moss = densities[texture_variant % 3]

        texture = get_moss_stone_texture(size=256, moss_density=moss)

        super().__init__(
            model='cube',
            texture=texture,
            position=(x, 0, z)
        )
```

---

### 2. Items (`graphics3d/items/base.py`)

**Current:**
```python
class Item3D(Entity):
    def __init__(self, item_type, color):
        super().__init__(
            model='sphere',
            color=color,  # Flat color
            scale=0.3
        )
```

**After Integration:**
```python
from textures import get_weathered_texture

class Item3D(Entity):
    def __init__(self, item_type, base_color):
        # Add weathering to make items look aged/used
        texture = get_weathered_texture(
            base_color=base_color,
            intensity=0.6
        )

        super().__init__(
            model='sphere',
            texture=texture,
            scale=0.3
        )
```

---

### 3. Enemies (`graphics3d/enemies/base.py`)

**Potential Enhancement:**
```python
from textures import generate_skin_texture  # Future enhancement

class Enemy3D(Entity):
    def __init__(self, enemy_type):
        # Could add procedural skin/scales/fur textures
        if enemy_type == 'dragon':
            texture = generate_scale_texture(color=color.red)
        elif enemy_type == 'orc':
            texture = generate_skin_texture(color=color.green, roughness=0.8)

        super().__init__(model='cube', texture=texture)
```

---

### 4. Renderer (`renderer3d.py`)

**Preload Common Textures:**
```python
class Renderer3D:
    def __init__(self):
        # Preload common textures during initialization
        from textures import get_brick_texture, get_moss_stone_texture

        self.common_textures = {
            'wall_normal': get_moss_stone_texture('medium'),
            'wall_dark': get_brick_texture(darkness=0.6),
            'floor': get_brick_texture(darkness=0.8),
        }
```

---

## Success Criteria

### Functional Requirements

- [ ] All texture generators produce valid PIL Images
- [ ] Brick patterns match OpenGL reference quality
- [ ] Moss overlays have organic appearance
- [ ] Carved textures have depth illusion
- [ ] Weathering effects look convincing
- [ ] Cache prevents redundant generation
- [ ] API is clean and well-documented

### Performance Requirements

- [ ] 256x256 texture generation < 50ms
- [ ] Cache hit retrieval < 1ms
- [ ] No FPS drop in-game (maintain 60 FPS)
- [ ] Memory usage < 50MB for texture cache
- [ ] 100 unique textures can be generated without lag

### Quality Requirements

- [ ] Visual similarity to OpenGL version > 95%
- [ ] Textures look good from all angles in Ursina
- [ ] No visible seams or artifacts
- [ ] Random variations are convincing
- [ ] Color palette matches game aesthetic

### Code Quality Requirements

- [ ] All functions have type hints
- [ ] All functions have docstrings with examples
- [ ] Unit test coverage > 80%
- [ ] No circular dependencies
- [ ] Follows PEP 8 style guide
- [ ] Passes mypy static type checking

---

## Deliverables Checklist

### Code Files
- [ ] `textures/__init__.py` - Public API
- [ ] `textures/generator.py` - Base classes
- [ ] `textures/bricks.py` - Brick generation
- [ ] `textures/organic.py` - Moss generation
- [ ] `textures/weathering.py` - Weathering effects
- [ ] `textures/carved.py` - Carved text
- [ ] `textures/cache.py` - Caching system
- [ ] `examples/texture_demo.py` - Demo script

### Documentation
- [ ] `textures/README.md` - Usage guide
- [ ] API reference in docstrings
- [ ] Code comments for complex algorithms
- [ ] This HANDOVER.md updated with "COMPLETE" status

### Tests
- [ ] `tests/test_textures.py` - Unit tests
- [ ] `tests/test_visual_regression.py` - Visual tests
- [ ] `tests/benchmark_textures.py` - Performance tests
- [ ] Reference images saved in `tests/reference_textures/`

### Integration
- [ ] `graphics3d/tiles.py` uses procedural textures
- [ ] `graphics3d/items/base.py` supports textured items
- [ ] `renderer3d.py` preloads common textures
- [ ] Game runs without errors
- [ ] Visual improvement is noticeable

---

## Dependencies

### Required Python Packages

Add to `requirements.txt`:
```
Pillow>=10.0.0  # PIL fork, image processing
```

Install:
```bash
pip install Pillow
```

### Optional Packages

For advanced features:
```
scikit-image  # For perceptual similarity metrics (SSIM)
numpy         # Already required, useful for noise generation
```

---

## FAQ / Troubleshooting

### Q: Why not use Perlin noise for textures?
**A:** The existing OpenGL textures don't use Perlin noise - they use geometric patterns (bricks) and organic shapes (moss). Perlin noise could be a future enhancement for natural surfaces.

### Q: Should we support texture sizes other than 256x256?
**A:** Yes, the system should support any power-of-2 size (128, 256, 512, 1024). Pass `size` parameter to all generators.

### Q: How do we handle font availability across platforms?
**A:** Try multiple font paths in order (Linux, Windows, macOS). Fall back to default font if none found. See Phase 4 code sample.

### Q: What if cache grows too large?
**A:** `TextureCache` uses LRU eviction - oldest unused textures are removed when `max_size` is reached (default 100 textures = ~25MB).

### Q: Can this work in 2D mode too?
**A:** Yes! The generators produce PIL Images which can be converted to PyQt6 `QPixmap` for 2D rendering. The core generators are framework-agnostic.

---

## Timeline

| Phase | Task | Time | Dependencies |
|-------|------|------|--------------|
| 1 | Infrastructure | 2-3h | None |
| 2 | Brick Patterns | 2-3h | Phase 1 |
| 3 | Organic Effects | 3-4h | Phase 1, 2 |
| 4 | Carved Effects | 2-3h | Phase 1, 2, 3 |
| 5 | Ursina Integration | 2-3h | Phase 1-4 |
| 6 | Polish & Examples | 1-2h | Phase 1-5 |
| **TOTAL** | | **12-18h** | |

---

## Contacts & Questions

**Primary Contact:** [Your Name/Team]
**Codebase:** `/var/www/claudelike/roguelike/`
**Reference Implementation:** `ui/screens/title_screen_3d.py:238-707`

**Questions During Implementation:**
- Ambiguities in porting logic → Check reference code first
- Performance issues → Profile and optimize bottleneck
- Visual differences → Compare side-by-side with OpenGL output
- Integration problems → Check Ursina's `Texture` documentation

---

## Appendix: QPainter to PIL Cheat Sheet

| QPainter | PIL Equivalent |
|----------|----------------|
| `QImage(w, h, Format_RGBA8888)` | `Image.new('RGBA', (w, h))` |
| `QPainter(image)` | `ImageDraw.Draw(image)` |
| `painter.fillRect(x, y, w, h, color)` | `draw.rectangle([x, y, x+w, y+h], fill=color)` |
| `painter.drawLine(x1, y1, x2, y2)` | `draw.line([x1, y1, x2, y2])` |
| `painter.drawEllipse(x, y, w, h)` | `draw.ellipse([x, y, x+w, y+h])` |
| `painter.drawPolygon(QPolygonF(...))` | `draw.polygon([(x1,y1), (x2,y2), ...])` |
| `painter.setBrush(QColor(...))` | Pass `fill=(r,g,b,a)` to draw calls |
| `painter.setPen(QColor(...))` | Pass `outline=(r,g,b,a)` to draw calls |
| `QColor(r, g, b, a)` | `(r, g, b, a)` tuple |
| `painter.setCompositionMode(Multiply)` | `ImageChops.multiply(img1, img2)` |
| `image.mirrored(False, True)` | `image.transpose(Image.FLIP_TOP_BOTTOM)` |

---

**END OF HANDOVER DOCUMENT**

*This document should contain everything needed to implement the procedural texture system independently. Update this document with "COMPLETE" status and any lessons learned when finished.*
