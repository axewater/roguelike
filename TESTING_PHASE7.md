# Phase 7 Testing Guide

Quick guide for testing the Phase 7 implementation (Screens & Menus).

---

## 🚀 Quick Test Run

```bash
cd /var/www/claudelike/roguelike
python main.py --mode 3d
```

**Expected Flow**:
1. Window opens (1920x1080)
2. Class selection screen appears
3. See 4 classes with rotating models
4. Select a class (arrow keys + Enter)
5. Game starts with chosen class
6. Play normally
7. Press ESC → Pause menu appears
8. Resume or restart as needed

---

## ✅ Test Checklist

### **1. Class Selection Screen**
```bash
# Launch game
python main.py --mode 3d

# What to test:
□ Window opens without errors
□ Class selection screen appears
□ 4 class models visible (Warrior, Mage, Rogue, Ranger)
□ Models rotate smoothly (30°/sec)
□ Stats display correctly (HP, ATK, DEF)
□ Abilities list shows 3 abilities per class
□ Arrow keys / A/D navigate between classes
□ UI sounds play on navigation
□ "START GAME" button visible
□ Enter/Space/Click starts game
□ Class name voice plays on selection
```

**Expected Behavior**:
- Warrior: HP:120, ATK:12, DEF:8, Red model
- Mage: HP:70, ATK:15, DEF:3, Blue model
- Rogue: HP:85, ATK:13, DEF:4, Purple model
- Ranger: HP:90, ATK:11, DEF:5, Green model

**Common Issues**:
- Models don't appear → Check `graphics3d/players/` imports
- Stats wrong → Check `constants.py` CLASS_STATS
- No audio → Check audio system initialization

---

### **2. Game Starts Correctly**
```bash
# After selecting a class:

# What to test:
□ Game initializes without errors
□ Dungeon renders correctly
□ Player spawns at starting position
□ First-person camera active (eye level)
□ UI overlay visible (HP, XP, abilities, combat log)
□ Selected class abilities appear in ability bar
□ Movement works (WASD)
□ Camera rotation works (arrow keys)
```

**Expected Behavior**:
- Game prints initialization messages
- 3D dungeon appears
- UI overlay shows correct class info
- Combat log shows "Welcome" message
- Abilities match selected class

**Common Issues**:
- Game doesn't start → Check GameCoordinator in main_3d.py
- Wrong class → Check `game.selected_class` assignment
- No UI → Check UI3DManager initialization

---

### **3. Pause Menu**
```bash
# During gameplay:

# What to test:
□ Press ESC → Pause menu appears
□ Game freezes (no enemy movement)
□ Semi-transparent overlay visible
□ "PAUSED" title displayed
□ 5 buttons visible (Resume, Restart, Settings, Main Menu, Quit)
□ Press ESC again → Resume game
□ Click "Resume" → Resume game
□ Click "Restart" → Return to class selection
□ Click "Quit" → Exit game
```

**Expected Behavior**:
- Game logic stops (enemies don't move)
- Camera doesn't rotate
- Pause menu overlays game (doesn't hide dungeon)
- ESC toggles pause state
- All buttons functional

**Common Issues**:
- ESC doesn't work → Check `_handle_ability_input()` logic
- Game doesn't freeze → Check `paused` state in GameController
- Menu doesn't appear → Check PauseMenu3D initialization

---

### **4. Victory Screen**
```bash
# To test victory (cheat method):

# Option A: Modify game.py temporarily
# Add after game start:
# self.current_level = 24

# Option B: Play to level 25 (will take ~30 minutes)

# What to test:
□ Victory screen appears automatically on level 25 completion
□ "VICTORY!" title visible with glow
□ Celebration particles spawn (golden/purple/pink)
□ Final stats display correctly
□ "Play Again" returns to class selection
□ "Main Menu" works (currently goes to class selection)
□ "Quit" exits game
```

**Expected Behavior**:
- Screen appears after defeating level 25 boss
- Particles fall upward with gravity
- Title pulses with golden glow
- Stats show level 25, correct XP, enemies defeated
- Audio plays victory sound

**Common Issues**:
- Screen doesn't appear → Check victory condition in GameController
- No particles → Check VictoryScreen3D particle spawning
- Wrong stats → Check stats dict in GameController

---

### **5. Game Over Screen**
```bash
# To test game over:

# Option A: Let an enemy kill you
# Option B: Modify game.py temporarily
# Add after game start:
# self.player.hp = 1

# What to test:
□ Game over screen appears automatically on death
□ "GAME OVER" title visible
□ Death reason displays (e.g., "Slain by Goblin")
□ Dark falling particles spawn
□ Final stats display correctly
□ "Try Again" returns to class selection
□ "Main Menu" works
□ "Quit" exits game
```

**Expected Behavior**:
- Screen appears immediately after death
- Particles fall downward (dark red/purple/gray)
- Title fades in over 0.8 seconds
- Death reason shows attacking enemy type
- Stats show correct level reached and XP

**Common Issues**:
- Screen doesn't appear → Check game_over condition in GameController
- No death reason → Check `game.last_attacker` tracking
- Wrong stats → Check stats dict creation

---

## 🐛 Debugging Tips

### **Check Console Output**:
```bash
# Look for these messages:
✓ Window resolution set to 1920x1080
✓ Window background set to dark blue
✓ Screen manager initialized
✓ Game coordinator initialized
✓ ClassSelection3D initialized
[ClassSelection] Selected: warrior
[GameCoordinator] Initializing game with class: warrior
✓ 3D particle system connected
✓ UI3D system initialized
[GameCoordinator] Game initialized successfully
```

### **Common Errors**:

**ImportError: No module named 'ui.screens.screen_manager_3d'**
```bash
# Fix: Make sure ui/screens/ directory exists
ls ui/screens/screen_manager_3d.py
```

**AttributeError: 'ScreenManager3D' object has no attribute 'selected_class'**
```bash
# Fix: Check class_selection_3d.py calls screen_manager.start_game_with_class()
```

**TypeError: __init__() takes X positional arguments but Y were given**
```bash
# Fix: Check GameController __init__ signature in main_3d.py
```

**Models don't appear in class selection**
```bash
# Fix: Check graphics3d/players/ imports
# Make sure all 4 model files exist:
ls graphics3d/players/warrior.py
ls graphics3d/players/mage.py
ls graphics3d/players/rogue.py
ls graphics3d/players/ranger.py
```

---

## 🔍 Manual Testing Steps

### **Full Flow Test** (15 minutes):

1. **Launch**
   ```bash
   python main.py --mode 3d
   ```

2. **Class Selection** (1 min)
   - Navigate to each class (arrow keys)
   - Check stats update correctly
   - Select Warrior (Enter)

3. **Early Game** (3 min)
   - Move around (WASD)
   - Rotate camera (arrow keys)
   - Attack an enemy (bump into it)
   - Use ability 1 (press 1, click target)
   - Check combat log shows messages

4. **Pause Menu** (1 min)
   - Press ESC
   - Check game freezes
   - Press ESC again to resume
   - Press ESC again
   - Click "Restart"

5. **New Class** (1 min)
   - Select different class (Mage)
   - Verify abilities changed
   - Start game

6. **Game Over** (3 min)
   - Let enemy kill you
   - Check game over screen
   - Check death reason
   - Click "Try Again"

7. **Final Test** (5 min)
   - Select Rogue
   - Play for a few levels
   - Press ESC → "Quit"

---

## 📊 Performance Checks

**Frame Rate**:
- Class Selection: Should be 60 FPS
- Gameplay: Should be 45-55 FPS
- Victory/Game Over: Should be 50-55 FPS (particles)
- Pause Menu: Should be 60 FPS (frozen game)

**Memory**:
- Should stay under 500MB
- No memory leaks during screen transitions

**GPU Usage**:
- Should be 30-50% on mid-range GPU
- No spikes during transitions

---

## ✅ Success Criteria

All tests pass if:
- ✅ No crashes or errors
- ✅ All screens appear correctly
- ✅ All navigation works
- ✅ All 4 classes selectable
- ✅ Pause menu functional
- ✅ Victory/game over screens work
- ✅ Performance is acceptable (45+ FPS)
- ✅ Audio plays correctly

---

## 🎉 Next Steps

If all tests pass:
1. Update MIGRATION.md (mark Phase 7 complete)
2. Update README.md (update status to 95%)
3. Update CLAUDE.md (note Phase 7 completion)
4. Commit changes with message:
   ```
   Phase 7 Complete: Screens & Menus (3D Mode)

   - Screen manager with state machine
   - 3D class selection with model previews
   - Victory and game over screens
   - Pause menu overlay
   - Complete game flow integration

   Project Status: 80% → 95% complete
   ```
5. Decide: Phase 8 (Polish) or Phase 10 (Final Review)?

---

**Testing Guide Version**: 1.0
**Date**: 2025-10-12
**Phase**: 7 - Screens & Menus
