# Field of View / Fog of War Implementation Plan

## Overview
Implement a complete FOV/Fog of War system with three tile states (unexplored, explored, visible), enemy vision mechanics, and Rogue-specific stealth gameplay.

## Phase 1: Core FOV System (Foundation)

### 1.1 Create `fov.py` - FOV Calculation Module
**File: `fov.py` (NEW)**
- Implement **Recursive Shadowcasting algorithm** (industry standard for roguelikes)
  - `calculate_fov(dungeon, origin_x, origin_y, radius) -> set[(x, y)]`
  - Returns set of all visible tile coordinates from origin point
  - Walls block vision (use `dungeon.is_walkable()`)
  - 8 octant scanning for full 360° vision
- Helper functions:
  - `cast_light(dungeon, cx, cy, row, start_slope, end_slope, radius, octant)`
  - `get_octant_transform(octant, x, y)` for coordinate transformation

### 1.2 Create `visibility.py` - Visibility State Manager
**File: `visibility.py` (NEW)**
- `VisibilityMap` class:
  - Track 3 states per tile: `UNEXPLORED`, `EXPLORED`, `VISIBLE`
  - 2D array matching dungeon dimensions
  - `update_visibility(visible_tiles: set)` - marks visible tiles, downgrades previously visible to explored
  - `get_state(x, y) -> str` - returns tile visibility state
  - `is_visible(x, y) -> bool` - quick check for rendering
  - `is_explored(x, y) -> bool` - check if tile has been seen
  - `reveal_all()` - debug/testing function

### 1.3 Integrate into Game State
**File: `game.py`**
- Add imports: `from fov import calculate_fov` and `from visibility import VisibilityMap`
- Initialize `self.visibility_map = VisibilityMap(c.GRID_WIDTH, c.GRID_HEIGHT)` in `__init__`
- Create `update_fov()` method:
  - Calculate visible tiles using `calculate_fov()`
  - Pass to `visibility_map.update_visibility()`
  - Call after player movement and on level generation
- Reset visibility map when descending levels

### 1.4 Add Constants
**File: `constants.py`**
```python
# Field of View / Visibility
PLAYER_VISION_RADIUS = 10  # Base vision range
ROGUE_VISION_BONUS = 5     # Rogue sees +5 tiles further
ENEMY_VISION_RADIUS = 8    # Enemy detection range
ENEMY_VISION_VS_ROGUE = 6  # Reduced vision when chasing Rogue

# Visibility states
VISIBILITY_UNEXPLORED = "unexplored"
VISIBILITY_EXPLORED = "explored"
VISIBILITY_VISIBLE = "visible"

# Rendering
EXPLORED_TILE_ALPHA = 0.3  # Darkness factor for explored tiles (30% brightness)
```

---

## Phase 2: Rendering System Updates

### 2.1 Update Tile Rendering
**File: `ui/widgets/game_widget.py` - `paintEvent()` method**
- Before drawing each tile, check `self.game.visibility_map.get_state(world_x, world_y)`
- **Unexplored tiles**: Skip rendering (draw pure black or nothing)
- **Explored tiles**:
  - Draw with darkened colors (multiply RGB by `EXPLORED_TILE_ALPHA`)
  - Create helper: `_get_explored_color(base_color) -> QColor`
  - Apply to walls, floors, stairs
- **Visible tiles**: Draw normally (current behavior)

### 2.2 Update Entity Rendering
**File: `ui/widgets/game_widget.py` - `paintEvent()` entity loop**
- **Enemies**: Only render if `visibility_map.is_visible(enemy.x, enemy.y)`
- **Items**: Design choice - two options:
  - **Option A** (easier): Only show in visible tiles
  - **Option B** (memory): Show in explored tiles too (dimmed)
  - Recommend **Option A** for true fog of war tension
- **Player**: Always visible (it's the player!)
- Update enemy health bars to only draw for visible enemies

### 2.3 Visual Polish
**File: `graphics.py` - Add helper functions**
```python
def apply_fog_color(color: QColor, alpha: float) -> QColor:
    """Darken color for fog of war effect"""
    return QColor(
        int(color.red() * alpha),
        int(color.green() * alpha),
        int(color.blue() * alpha)
    )
```

---

## Phase 3: Enemy FOV & Intelligent AI

### 3.1 Enemy Vision System
**File: `entities.py` - `Enemy` class**
- Add fields:
  - `self.vision_radius = c.ENEMY_VISION_RADIUS`
  - `self.last_known_player_pos = None` - track where player was last seen
  - `self.turns_since_seen_player = 0` - counter for losing track

### 3.2 Enemy AI with FOV Awareness
**File: `entities.py` - `get_ai_action()` method**
- Calculate enemy FOV: `enemy_fov = calculate_fov(dungeon, self.x, self.y, self.vision_radius)`
- Check if player in FOV: `can_see_player = player_pos in enemy_fov`
- **Behavior states**:
  1. **Can see player**: Chase mode
     - Update `last_known_player_pos`
     - Reset `turns_since_seen_player = 0`
     - Move toward player
  2. **Lost sight**: Search mode
     - Move toward `last_known_player_pos`
     - Increment `turns_since_seen_player`
     - After 5 turns, return to patrol
  3. **Never seen / gave up**: Patrol mode (current behavior)

### 3.3 Enemy Vision Adjustments
**File: `game.py` - `_enemy_turn()` or `entities.py`**
- Check player class during FOV calculation
- If player is Rogue: `enemy.vision_radius = c.ENEMY_VISION_VS_ROGUE`
- Otherwise: `enemy.vision_radius = c.ENEMY_VISION_RADIUS`

---

## Phase 4: Rogue Stealth Mechanics

### 4.1 Extended Rogue Vision
**File: `game.py` - `update_fov()` method**
```python
vision_radius = c.PLAYER_VISION_RADIUS
if self.player.class_type == c.CLASS_ROGUE:
    vision_radius += c.ROGUE_VISION_BONUS
visible_tiles = calculate_fov(self.dungeon, self.player.x, self.player.y, vision_radius)
```

### 4.2 Backstab Damage Bonus
**File: `combat.py` - `player_attack_enemy()` function**
- Add parameter to detect stealth attack
- Check if enemy can see player using enemy's FOV
- If enemy CANNOT see player and player is Rogue:
  - Apply `BACKSTAB_DAMAGE_MULTIPLIER = 1.75` (75% bonus damage)
  - Return special message: `"Backstab! Critical damage!"`
- Add to constants: `BACKSTAB_DAMAGE_MULTIPLIER = 1.75`

### 4.3 Stealth UI Indicators
**File: `ui/widgets/stats_panel.py`**
- For Rogue class, add "Stealth Status" indicator:
  - **Green "HIDDEN"**: No enemies can see player
  - **Red "DETECTED"**: At least one enemy has player in FOV
  - Count enemies that can see player: `f"Detected by: {count} enemies"`

### 4.4 Stealth Audio & Visuals
**File: `game.py` - `_player_attack()` method**
- Detect backstab condition
- Play special audio: `self.audio_manager.play_stealth_kill()` (new sound)
- Add purple particle effect for backstabs
- **File: `audio.py`** - Add stealth kill sound (low whoosh + impact)

---

## Phase 5: Visual Feedback & Polish

### 5.1 Enemy Alert Indicators
**File: `animations.py`**
- Add `add_alert_particle(x, y)` - creates "!" above enemy when spotting player
- Yellow exclamation mark that bounces and fades
**File: `entities.py`**
- When enemy transitions from patrol→chase, trigger alert in game

### 5.2 Exploration Stats
**File: `ui/widgets/stats_panel.py`**
- Add exploration percentage:
  - `explored_count = visibility_map.count_explored()`
  - `total_tiles = count_floor_tiles()`
  - Display: `f"Explored: {explored/total*100:.1f}%"`

### 5.3 Minimap (Optional Enhancement)
**File: `ui/widgets/minimap.py` (NEW)**
- Small 150x150px widget showing explored areas
- Player as bright dot, enemies as red dots (if visible)
- Greyed out explored areas

### 5.4 Debug Commands (Development)
**File: `game.py`**
- Press `F1` to toggle full map reveal (testing)
- Press `F2` to show enemy FOV ranges (visual debug)
- Console output for FOV tile counts

---

## Phase 6: Balance & Testing

### 6.1 Balance Parameters to Test
- Player vision radius (10 vs 12 vs 15)
- Rogue vision bonus (3 vs 5 vs 7)
- Enemy vision radius (6 vs 8 vs 10)
- Enemy vision vs Rogue (4 vs 6 vs 8)
- Backstab multiplier (1.5x vs 1.75x vs 2.0x)
- Turns before enemy gives up search (3 vs 5 vs 8)

### 6.2 Edge Cases to Handle
- Player at dungeon edge (FOV shouldn't crash)
- Very large rooms (performance test)
- Corridors (ensure vision travels down them)
- Diagonal wall corners (shadowcasting quirks)
- Level transitions (visibility reset)
- Camera bounds with limited vision

### 6.3 Performance Optimization
- Profile FOV calculation time (should be <5ms)
- Consider caching enemy FOV if too slow
- Only recalculate enemy FOV when player moves

---

## Implementation Order

**Week 1** - Core Systems
1. Create `fov.py` with shadowcasting (1 day)
2. Create `visibility.py` with state tracking (1 day)
3. Integrate into `game.py` + update on movement (1 day)
4. Update tile rendering in `game_widget.py` (2 days)

**Week 2** - Enemy AI & Stealth
5. Enemy FOV calculation in `entities.py` (1 day)
6. Update enemy AI behavior states (2 days)
7. Rogue vision bonus + backstab damage (1 day)
8. Stealth UI indicators (1 day)

**Week 3** - Polish & Balance
9. Alert particles and visual feedback (1 day)
10. Exploration stats display (1 day)
11. Audio for stealth mechanics (1 day)
12. Balance testing + bug fixes (2 days)

---

## Testing Checklist
- [ ] FOV correctly blocks vision through walls
- [ ] Explored areas stay visible (dimmed) after leaving
- [ ] Unexplored areas are completely hidden
- [ ] Enemies only chase when player in FOV
- [ ] Enemies search last known position
- [ ] Enemies return to patrol after losing player
- [ ] Rogue has extended vision range
- [ ] Rogue receives backstab bonus
- [ ] Enemies have reduced vision vs Rogue
- [ ] Stealth indicator updates correctly
- [ ] Alert particles appear when enemy spots player
- [ ] Performance: FOV calculation <5ms
- [ ] No crashes at map boundaries

---

## Success Criteria
✅ Dungeon gradually reveals as player explores
✅ Enemies patrol rooms until spotting player
✅ Rogue class has distinct stealth advantages
✅ Tension increases from limited information
✅ Performance remains smooth (60 FPS)
✅ Clear visual feedback for stealth state
