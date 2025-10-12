# 2D → 3D Migration Project Plan

**Project**: Complete 3D mode to feature parity with 2D mode
**Start Date**: 2025-10-12 (Fresh start after Phase 1-5 completion)
**Status**: 🚧 80% Complete - First-person mode working, UI overlay complete, polish remaining

---

## 📊 Current Status

### ✅ What's Working (Completed Phases 1-6.5)

**Phase 1-2: Foundation** ✅
- ✅ Ursina Engine integrated
- ✅ 3D rendering pipeline working
- ✅ Basic game loop functional

**Phase 3: Core Gameplay** ✅
- ✅ Dungeon rendering (walls, floors, stairs)
- ✅ Player movement (WASD controls)
- ✅ Combat system (bump-to-attack)
- ✅ Camera follow with smooth interpolation
- ✅ Level progression (stairs descent)
- ✅ 40-45 FPS performance

**Phase 4: Entity Models** ✅
- ✅ All 4 player class models
- ✅ All 6 enemy type models
- ✅ All 5 item type models
- ✅ Health bars above enemies
- ✅ Item floating/rotation animations

**Phase 5: Visual Effects** ✅
- ✅ 3D particle system with physics
- ✅ Floating damage text (billboard)
- ✅ Explosions and directional spray
- ✅ Ability visual effects (fire trails, ice, dash)
- ✅ Screen shake on impacts
- ✅ Death burst animations
- ✅ Ambient atmospheric particles

**Phase 6: UI Overlay & Input** ✅
- ✅ 3D UI overlay system (stats, abilities, combat log)
- ✅ Stats display (HP/XP bars, level, depth)
- ✅ Ability bar (cooldown indicators, hotkeys)
- ✅ Combat log (scrolling messages with color coding)
- ✅ Mouse targeting system with raycasting
- ✅ Ability input (1/2/3 keys + mouse confirmation)
- ✅ Range indicators and validation

**Phase 6.5: First-Person Camera & Performance** ✅
- ✅ First-person camera system (eye-level, 90° FOV)
- ✅ Camera rotation with smooth interpolation (arrow keys)
- ✅ Directional WASD movement (camera-relative)
- ✅ Hidden player model in first-person
- ✅ Performance optimizations:
  - ✅ Particle count limits (MAX_PARTICLES=100)
  - ✅ Conditional UI updates (only update on change)
  - ✅ Disabled ambient particles (not visible in first-person)
- ✅ UI scaling improvements (2.5x larger health bars)
- ✅ Updated targeting raycast for first-person

### ❌ What's Missing

**Critical Path (Blocking full playability):**
1. ❌ Class Selection (Phase 7)
   - 3D class selection screen
   - Character preview in 3D
   - Start game flow

**Nice to Have (Polish):**
2. ❌ FOV/Fog of War in 3D (Phase 8)
3. ❌ 3D Positional Audio (Phase 8)
4. ❌ Title/Menu Screens (Phase 7)
5. ❌ Victory/Game Over UI (Phase 7)

---

## 🎯 Migration Phases

### Phase 6: UI Overlay & Input System ✅ COMPLETED
**Duration**: 1-2 weeks (Completed 2025-10-12)
**Priority**: CRITICAL - Blocks full playability

#### Tasks

**1. UI Overlay in 3D Window**
- [x] Research Ursina UI system (Text, Button, Panel entities)
- [x] Create UI widget classes in `ui3d/` directory
- [x] Design overlay layout (corner panels, translucent backgrounds)
- [x] Implement stats panel (`ui3d/stats_display.py`):
  - [x] HP bar (current/max with visual bar)
  - [x] XP bar with level indicator
  - [x] Class name and icon
  - [x] Current level/floor number
- [x] Implement combat log (`ui3d/combat_log_3d.py`):
  - [x] Scrolling message queue (last 5 messages)
  - [x] Color-coded messages (damage, heal, info)
  - [x] Auto-fade old messages
- [x] Implement ability bar (`ui3d/ability_bar.py`):
  - [x] 3 ability slots with icons
  - [x] Cooldown overlay (grayed out when on cooldown)
  - [x] Hotkey indicators (1, 2, 3)

**2. Ability Input System**
- [x] Hook keyboard events (1/2/3 keys) in `main_3d.py`
- [x] Implement mouse position tracking in 3D world
- [x] Create targeting system (`ui3d/targeting.py`):
  - [x] Raycast from camera to world position
  - [x] Show target cursor/indicator
  - [x] Validate target range/line-of-sight
- [x] Integrate ability activation:
  - [x] Key press → ability selection
  - [x] Mouse click → target confirmation
  - [x] Execute ability via `game.py` API
- [x] Visual feedback:
  - [x] Range circle around player
  - [x] Target tile highlight
  - [x] "Out of range" indicator

**3. Integration & Testing**
- [x] Test all 6 abilities in 3D mode
- [x] Verify cooldown display updates
- [x] Test UI scaling on different resolutions
- [x] Ensure UI doesn't block gameplay view

**Success Criteria:**
- ✅ Can see HP/XP bars during gameplay
- ✅ Can use abilities with 1/2/3 keys + mouse
- ✅ Combat log shows messages clearly
- ✅ Ability cooldowns visible on UI

---

### Phase 6.5: First-Person Camera & Performance ✅ COMPLETED
**Duration**: 1 week (Completed 2025-10-12)
**Priority**: HIGH - Improves immersion and performance

#### Motivation
User feedback indicated performance issues and small UI elements in third-person mode. First-person perspective offers better immersion, eliminates the need for player model development (Phase 7 simplification), and allows visibility-based optimizations.

#### Tasks

**1. First-Person Camera System**
- [x] Add first-person constants to `constants.py`:
  - [x] `USE_FIRST_PERSON = True`
  - [x] `EYE_HEIGHT = 1.4` (eye-level camera)
  - [x] `CAMERA_FOV_FPS = 90` (wider FOV)
  - [x] `CAMERA_ROTATION_SPEED = 8.0`
- [x] Update `renderer3d.py` camera system:
  - [x] Position camera at player position + eye height
  - [x] Horizontal rotation only (yaw, no pitch)
  - [x] Hide player cube (`visible=False`)
- [x] Implement camera rotation in `main_3d.py`:
  - [x] Track camera yaw (0° = North, 90° = East, etc.)
  - [x] Smooth interpolation between 90° increments
  - [x] Arrow keys rotate camera

**2. Directional Movement System**
- [x] Implement camera-relative WASD controls (`main_3d.py`):
  - [x] W/S = forward/backward relative to camera
  - [x] A/D = strafe left/right relative to camera
  - [x] Arrow Up/Down = also move forward/backward
  - [x] `_get_forward_offset()` - maps yaw to grid offsets
  - [x] `_get_left_offset()` - for strafing
- [x] Grid-based snapping (movement snaps to 90° directions)

**3. Performance Optimizations**
- [x] Particle count limiting (`animations3d.py`):
  - [x] `MAX_PARTICLES = 100` constant
  - [x] Remove oldest particles when limit exceeded
- [x] Conditional UI updates (`ui3d/*.py`):
  - [x] Cache previous values (HP, XP, level, cooldowns)
  - [x] Only update when values change
  - [x] Skip fade calculations when no messages fading
- [x] Disable unseen effects:
  - [x] `ENABLE_AMBIENT_PARTICLES_3D = False`
  - [x] Remove fog/cloud particles (not visible in first-person)

**4. UI Improvements**
- [x] Increase health bar scale:
  - [x] `HEALTH_BAR_SCALE = 2.0` (increased from 0.8)
  - [x] Better readability in first-person
- [x] Update targeting raycast (`ui3d/targeting.py`):
  - [x] Proper ray calculation using mouse cursor position
  - [x] Account for camera rotation, FOV, and aspect ratio
  - [x] Works correctly in first-person

**Success Criteria:**
- ✅ First-person camera at eye level
- ✅ Smooth camera rotation with arrow keys
- ✅ WASD movement relative to camera direction
- ✅ Performance improved (particle limits, conditional updates)
- ✅ UI elements scaled for readability
- ✅ Targeting system works in first-person

---

### Phase 7: Screens & Menus
**Duration**: 1 week
**Priority**: HIGH - Improves UX

#### Tasks

**1. Class Selection Screen (3D)**
- [ ] Create `ClassSelection3D` in `ui/screens/class_selection_3d.py`
- [ ] Display 4 class models in 3D preview:
  - [ ] Arrange in circular formation
  - [ ] Highlight selected class
  - [ ] Rotate models on hover
- [ ] Show class stats overlay (HP, Attack, Defense)
- [ ] Show ability descriptions
- [ ] "Start Game" button → transitions to 3D gameplay

**2. Title Screen (3D)**
- [ ] Update `ui/screens/title_screen_3d.py`
- [ ] 3D logo/title animation
- [ ] Menu options:
  - [ ] New Game → Class Selection 3D
  - [ ] Settings (if implemented)
  - [ ] Quit
- [ ] Background: Animated 3D dungeon fly-through

**3. Victory/Game Over Screens**
- [ ] Create `GameOverScreen3D` in `ui/screens/`
- [ ] Victory condition:
  - [ ] Show "Victory!" text
  - [ ] Display final stats (level, XP, kills)
  - [ ] "Play Again" / "Quit" buttons
- [ ] Game Over condition:
  - [ ] Show "Game Over" text
  - [ ] Show death reason
  - [ ] "Retry" / "Quit" buttons
- [ ] Integrate with `main_3d.py` game loop

**4. Menu Navigation System**
- [ ] Create screen manager for 3D mode
- [ ] Implement screen transitions (fade in/out)
- [ ] ESC key pauses game (pause menu)
- [ ] Resume/Restart/Quit options

**Success Criteria:**
- ✅ Can select class in 3D before starting
- ✅ Title screen shows on launch
- ✅ Victory/Game Over screens display properly
- ✅ Can restart game from end screens

---

### Phase 8: FOV & Audio (Polish)
**Duration**: 1 week
**Priority**: MEDIUM - Enhances immersion

#### Tasks

**1. 3D FOV/Fog of War**
- [ ] Research 3D visibility algorithms
- [ ] Port FOV system from 2D to 3D:
  - [ ] Raycast-based visibility in 3D
  - [ ] Track explored tiles in 3D space
- [ ] Visual implementation:
  - [ ] Darken/hide unexplored tiles
  - [ ] Dim tiles outside current vision
  - [ ] Brighten visible tiles
- [ ] Option: Use 3D fog/mist effect for atmosphere
- [ ] Performance: Optimize raycasting (spatial partitioning)

**2. 3D Positional Audio**
- [ ] Integrate Panda3D audio system (Ursina's backend)
- [ ] Update `audio.py` to support 3D positions:
  - [ ] `play_sound_3d(sound, position=(x, y, z))`
  - [ ] Distance-based volume attenuation
  - [ ] Stereo panning based on position
- [ ] Apply to all sound effects:
  - [ ] Combat sounds (attacks, hits)
  - [ ] Enemy death sounds
  - [ ] Item pickup sounds
  - [ ] Ability sounds
- [ ] Add 3D reverb in large rooms (optional)

**3. Additional Polish**
- [ ] Minimap in corner (top-down view)
- [ ] Death camera animation (fall/fade)
- [ ] Level transition effect (stairs descent animation)
- [ ] Particle pooling for performance

**Success Criteria:**
- ✅ Can't see through walls (FOV working)
- ✅ Explored areas remain visible but dimmed
- ✅ Sounds come from correct direction in 3D
- ✅ Audio volume scales with distance

---

### Phase 9: Optimization & Testing
**Duration**: 1 week
**Priority**: MEDIUM - Ensures quality

#### Tasks

**1. Performance Optimization**
- [ ] Profile 3D rendering (identify bottlenecks)
- [ ] Implement occlusion culling (don't render hidden walls)
- [ ] Batch similar entities (reduce draw calls)
- [ ] Optimize particle system (object pooling)
- [ ] Reduce polygon count on distant objects (LOD)
- [ ] Target: 60 FPS with 100+ entities

**2. Cross-Platform Testing**
- [ ] Test on Windows 10/11
- [ ] Test on Linux (Ubuntu, Fedora)
- [ ] Test on macOS (if available)
- [ ] Document platform-specific issues

**3. Bug Fixes & Edge Cases**
- [ ] Test all 4 classes in 3D
- [ ] Test all 6 abilities
- [ ] Test all enemy types
- [ ] Test item interactions
- [ ] Test stairs/level progression
- [ ] Test game over/victory conditions
- [ ] Fix any visual glitches

**4. Documentation Updates**
- [ ] Update `README.md` with 3D status
- [ ] Update `CLAUDE.md` with 3D completion
- [ ] Create video walkthrough/demo
- [ ] Screenshot gallery for GitHub

**Success Criteria:**
- ✅ No game-breaking bugs
- ✅ 60 FPS on target hardware
- ✅ All features work in both 2D and 3D
- ✅ Documentation complete

---

### Phase 10: Feature Parity Complete 🎉
**Duration**: Final review
**Priority**: HIGH - Project completion

#### Final Checklist

**Core Gameplay:**
- [ ] Movement, combat, items work identically in 2D and 3D
- [ ] All 4 classes playable in 3D
- [ ] All abilities functional in 3D
- [ ] Level progression works (1-25)

**UI/UX:**
- [ ] Full UI overlay in 3D
- [ ] Class selection screen
- [ ] Title/menu screens
- [ ] Victory/Game Over screens

**Visuals:**
- [ ] All entities have 3D models
- [ ] Particle effects working
- [ ] FOV/Fog of War (optional, nice-to-have)

**Audio:**
- [ ] 3D positional audio (optional, nice-to-have)

**Performance:**
- [ ] 60 FPS target met
- [ ] No memory leaks

**Decision Point:**
- [ ] Make 3D the default mode?
- [ ] Keep 2D as legacy/accessibility option?
- [ ] Update `main.py` default mode

---

## 📅 Timeline Estimate

| Phase | Duration | Status | Completed |
|-------|----------|--------|-----------|
| Phase 6: UI & Input | 1-2 weeks | ✅ DONE | 2025-10-12 |
| Phase 6.5: First-Person & Performance | 1 week | ✅ DONE | 2025-10-12 |
| Phase 7: Screens | 1 week | ⏳ NEXT | - |
| Phase 8: FOV & Audio | 1 week | ⏸️ Optional | - |
| Phase 9: Optimization | 1 week | ⏸️ Optional | - |
| Phase 10: Final Review | 3 days | ⏸️ Pending | - |

**Total Estimated Time**: ~~4-6 weeks~~ → 2-3 weeks remaining
**Completed**: 2.5 weeks (Phase 1-6.5)
**Remaining**: 1-2 weeks (Phase 7 + Final Review)

**Critical Path**: ✅ Phase 6 → ✅ Phase 6.5 → Phase 7 → Phase 10
**Optional**: Phase 8 can be deferred if time-constrained

---

## 🎯 Success Metrics

### Functional Parity
- [ ] All 2D features work in 3D
- [ ] All classes, abilities, enemies, items
- [ ] Complete game loop (start → play → end)

### Performance
- [ ] 60 FPS with <100 entities (3D)
- [ ] <500MB RAM usage
- [ ] <2 second load time per level

### Code Quality
- [ ] No breaking changes to `game.py` logic
- [ ] Clean separation: rendering vs logic
- [ ] 2D mode still works (backwards compatible)
- [ ] Well-documented 3D code

### User Experience
- [ ] Intuitive controls in 3D
- [ ] Clear UI feedback
- [ ] Smooth transitions between screens
- [ ] No visual glitches

---

## 📝 Notes & Decisions

### Architecture Decisions

**UI System Choice:**
- **Option A**: Ursina's built-in UI (Text, Button, Panel entities)
  - Pros: Native integration, 3D-aware
  - Cons: Limited styling, less flexible
- **Option B**: PyQt6 overlay on Ursina window
  - Pros: Reuse existing UI code, powerful widgets
  - Cons: Requires window composition, may have rendering conflicts
- **Decision**: Start with Option A (Ursina UI) for simplicity, fallback to B if needed

**FOV Implementation:**
- 3D raycasting may be expensive, consider:
  - Spatial partitioning (octree/grid)
  - Simplified visibility (just distance-based)
  - Optional feature (player can toggle)

**Audio Migration:**
- Panda3D (Ursina's backend) has 3D audio support
- May need to refactor `audio.py` to support both 2D and 3D
- Consider making 3D audio optional for performance

---

## 🚀 Getting Started (For Developers)

### Current State
```bash
# Play current 3D version (core gameplay only)
python main.py --mode 3d

# Play full 2D version (complete)
python main.py --mode 2d
```

### Next Steps
1. Start with **Phase 6: UI Overlay** (highest priority)
2. Create `ui3d_manager.py` module
3. Reference 2D UI in `ui/widgets/stats_panel.py` for layout
4. Test frequently in 3D mode

### Key Files to Modify
- `main_3d.py` - Add UI initialization and input handling
- `renderer3d.py` - May need to expose camera/viewport info
- New: `ui3d_manager.py` - UI overlay manager

---

## 📚 Resources

### Ursina Documentation
- UI System: https://www.ursinaengine.org/documentation.html#ui
- Input Handling: https://www.ursinaengine.org/documentation.html#input
- Text/Button/Panel: Built-in entity types

### Reference Implementation
- 2D UI: `ui/widgets/stats_panel.py`
- 2D Input: `ui/widgets/game_widget.py` (mouse/keyboard events)
- 2D Abilities: `ui/widgets/ability_button.py`

---

## ✅ Definition of Done

**3D Mode is "Complete" when:**
1. ✅ Can start game from 3D title screen
2. ✅ Can select class in 3D
3. ✅ Can play full game with UI visible
4. ✅ Can use all abilities with mouse targeting
5. ✅ Can see stats, messages, cooldowns during play
6. ✅ Can reach victory/game over screens
7. ✅ Performance is acceptable (45+ FPS)
8. ✅ No game-breaking bugs

**Stretch Goals (Optional):**
- 🎯 3D FOV/Fog of War
- 🎯 3D Positional Audio
- 🎯 Advanced camera modes (FPS, isometric)
- 🎯 Minimap overlay

---

*Last Updated: 2025-10-12*
*Next Review: Start of Phase 7*

**Current Phase**: Phase 6.5 ✅ COMPLETE
**Next Milestone**: Phase 7 - Class Selection & Menu Screens
**Status**: 3D mode now fully playable with first-person camera!
