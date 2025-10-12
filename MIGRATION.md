# 2D → 3D Migration Project Plan

**Project**: Complete 3D mode to feature parity with 2D mode
**Start Date**: 2025-10-12 (Fresh start after Phase 1-5 completion)
**Status**: 🚧 70% Complete - Core gameplay works, UI/UX pending

---

## 📊 Current Status

### ✅ What's Working (Completed Phases 1-5)

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

### ❌ What's Missing

**Critical Path (Blocking playability):**
1. ❌ UI Overlay System (Phase 6)
   - Stats panel (HP, XP, Level)
   - Ability buttons (1/2/3 visual indicators)
   - Combat log (scrolling messages)

2. ❌ Ability Input System (Phase 6)
   - Keyboard shortcuts (1/2/3 keys)
   - Mouse targeting for abilities
   - Range/area indicators

3. ❌ Class Selection (Phase 7)
   - 3D class selection screen
   - Character preview in 3D
   - Start game flow

**Nice to Have (Polish):**
4. ❌ FOV/Fog of War in 3D (Phase 8)
5. ❌ 3D Positional Audio (Phase 8)
6. ❌ Title/Menu Screens (Phase 7)
7. ❌ Victory/Game Over UI (Phase 7)

---

## 🎯 Migration Phases

### Phase 6: UI Overlay & Input System (Current)
**Duration**: 1-2 weeks
**Priority**: CRITICAL - Blocks full playability

#### Tasks

**1. UI Overlay in 3D Window**
- [ ] Research Ursina UI system (Text, Button, Panel entities)
- [ ] Create `UI3DManager` class in new file `ui3d_manager.py`
- [ ] Design overlay layout (corner panels, translucent backgrounds)
- [ ] Implement stats panel:
  - [ ] HP bar (current/max with visual bar)
  - [ ] XP bar with level indicator
  - [ ] Class name and icon
  - [ ] Current level/floor number
- [ ] Implement combat log:
  - [ ] Scrolling message queue (last 5 messages)
  - [ ] Color-coded messages (damage, heal, info)
  - [ ] Auto-fade old messages
- [ ] Implement ability bar:
  - [ ] 3 ability slots with icons
  - [ ] Cooldown overlay (grayed out when on cooldown)
  - [ ] Hotkey indicators (1, 2, 3)

**2. Ability Input System**
- [ ] Hook keyboard events (1/2/3 keys) in `main_3d.py`
- [ ] Implement mouse position tracking in 3D world
- [ ] Create targeting system:
  - [ ] Raycast from camera to world position
  - [ ] Show target cursor/indicator
  - [ ] Validate target range/line-of-sight
- [ ] Integrate ability activation:
  - [ ] Key press → ability selection
  - [ ] Mouse click → target confirmation
  - [ ] Execute ability via `game.py` API
- [ ] Visual feedback:
  - [ ] Range circle around player
  - [ ] Target tile highlight
  - [ ] "Out of range" indicator

**3. Integration & Testing**
- [ ] Test all 6 abilities in 3D mode
- [ ] Verify cooldown display updates
- [ ] Test UI scaling on different resolutions
- [ ] Ensure UI doesn't block gameplay view

**Success Criteria:**
- ✅ Can see HP/XP bars during gameplay
- ✅ Can use abilities with 1/2/3 keys + mouse
- ✅ Combat log shows messages clearly
- ✅ Ability cooldowns visible on UI

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

| Phase | Duration | Dependencies | Priority |
|-------|----------|--------------|----------|
| Phase 6: UI & Input | 1-2 weeks | None | CRITICAL |
| Phase 7: Screens | 1 week | Phase 6 | HIGH |
| Phase 8: FOV & Audio | 1 week | Phase 6 | MEDIUM |
| Phase 9: Optimization | 1 week | Phase 6-8 | MEDIUM |
| Phase 10: Final Review | 3 days | All | HIGH |

**Total Estimated Time**: 4-6 weeks

**Critical Path**: Phase 6 → Phase 7 → Phase 10
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
*Next Review: Start of Phase 6*

**Current Phase**: Phase 6 - UI Overlay & Input System
**Next Milestone**: Playable 3D mode with full UI
