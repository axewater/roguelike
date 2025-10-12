# DNA-Based Procedural Monster Generation System

**Status**: Design Document
**Priority**: Future Enhancement
**Goal**: Generate infinite unique monster variations from code-only DNA patterns

---

## 1. Overview

This document describes a system for procedurally generating graphically diverse monsters from **DNA-based genomes** mixed with the **game's random seed**. All geometry is generated from code - no external assets.

### Key Features:
- **Archetype-based**: Define monster types (Spider, Tentacle Horror, Dragon, etc.)
- **DNA genomes**: Each archetype has parametric ranges (leg count, tentacle length, etc.)
- **Seed-driven variation**: Same seed = same creature (deterministic)
- **Skeleton system**: DNA → Skeleton → 3D Entities
- **Procedural animation**: Rule-based movement (wave tentacles, walk cycles)
- **100% code-generated**: No .obj files, no external models

---

## 2. Core Concept

### The Generation Pipeline:

```
Game Seed + Monster Index
         ↓
   Generate DNA (from Genome)
         ↓
   Build Skeleton (from DNA)
         ↓
   Spawn 3D Entities (from Skeleton)
         ↓
   Setup Animation Rules (from DNA traits)
```

### Example Flow:

```python
# 1. Define what a "Tentacle Horror" can look like
GENOME_TENTACLE_HORROR = {
    'tentacles': (4, 12),           # 4-12 tentacles
    'tentacle_segments': (5, 15),   # How bendy (5-15 segments)
    'tentacle_length': (1.0, 3.0),  # Length in world units
    'body_size': (0.5, 1.2),        # Core body size
    'eye_count': (0, 3),            # 0-3 eyes
}

# 2. Generate unique creature from seed
creature = ProceduralCreature(GENOME_TENTACLE_HORROR, seed=42)

# Result: 8 tentacles, each 2.1 units long, 11 segments, 1 eye
```

---

## 3. Architecture

### Class Structure:

```
ProceduralCreature
    ├── DNA (dict of trait values)
    ├── Skeleton (bone hierarchy)
    ├── Entities (list of Ursina Entity objects)
    └── Animation Rules (behavior functions)

Skeleton
    └── Bones (list)
          ├── name: str
          ├── parent: Bone | None
          ├── position: Vec3
          ├── rotation: Vec3
          ├── length: float
          ├── entity: Entity (3D geometry attached)
          └── children: list[Bone]

Bone
    ├── get_world_position()
    ├── get_world_rotation()
    ├── set_local_rotation(angle)
    └── update_transform()
```

---

## 4. Genome Definitions

### Format:

```python
GENOME_NAME = {
    'trait_name': (min_value, max_value),  # Range for numeric traits
    'boolean_trait': (True, True),         # Fixed boolean
    'color_hue': (0, 360),                 # Hue range (degrees)
}
```

### Example Archetypes:

#### Spider Archetype

```python
GENOME_SPIDER = {
    'body_segments': (2, 4),       # 2-4 body segments
    'legs_per_segment': (4, 8),    # 4-8 legs per segment
    'leg_length': (0.5, 1.5),      # Leg length range
    'leg_thickness': (0.05, 0.15), # Leg diameter
    'body_width': (0.3, 0.6),      # Body width
    'eye_count': (6, 12),          # Spider eyes
    'mandibles': (True, True),     # Always has mandibles
    'color_hue': (0, 30),          # Red-orange range
}
```

#### Tentacle Horror Archetype

```python
GENOME_TENTACLE_HORROR = {
    'body_segments': (1, 1),       # Single core body
    'tentacles': (4, 12),          # 4-12 tentacles
    'tentacle_segments': (5, 15),  # Bendy-ness
    'tentacle_length': (1.0, 3.0), # Length in units
    'body_size': (0.5, 1.2),       # Core size
    'eye_count': (0, 3),           # 0-3 eyes (alien)
    'spikes': (0, 20),             # Random spikes
    'color_hue': (270, 310),       # Purple range
}
```

#### Dragon Archetype

```python
GENOME_DRAGON = {
    'body_length': (2.0, 4.0),     # Long serpentine body
    'neck_length': (0.5, 2.0),     # Neck length
    'wings': (True, True),         # Always has wings
    'wing_span': (1.5, 3.0),       # Wing size
    'legs': (4, 4),                # Always 4 legs
    'tail_segments': (8, 15),      # Long tail
    'horns': (2, 6),               # Horn count
    'scales_density': (0.5, 1.0),  # Visual detail
    'color_hue': (0, 360),         # Any color
}
```

---

## 5. Implementation Details

### 5.1 ProceduralCreature Class

```python
class ProceduralCreature:
    """
    A procedurally generated monster from DNA + seed.

    Attributes:
        genome (dict): Archetype genome defining trait ranges
        seed (int): Random seed for generation
        dna (dict): Actual trait values (rolled from genome)
        skeleton (Skeleton): Bone hierarchy
        entities (list): Ursina Entity objects
        animation_mode (str): Animation behavior name
    """

    def __init__(self, archetype_genome, seed):
        self.genome = archetype_genome
        self.seed = seed
        self.rng = random.Random(seed)

        # Step 1: Generate DNA from genome
        self.dna = self.generate_dna()

        # Step 2: Build skeleton from DNA
        self.skeleton = self.build_skeleton()

        # Step 3: Generate 3D entities from skeleton
        self.entities = self.spawn_geometry()

        # Step 4: Set up animation behaviors
        self.setup_animation_rules()

    def generate_dna(self):
        """
        Roll DNA values from genome ranges using RNG.

        Returns:
            dict: DNA with concrete values for each trait
        """
        dna = {}
        for gene, (min_val, max_val) in self.genome.items():
            if isinstance(min_val, bool):
                # Fixed boolean trait
                dna[gene] = min_val
            elif isinstance(min_val, int):
                # Integer range
                dna[gene] = self.rng.randint(min_val, max_val)
            else:
                # Float range
                dna[gene] = self.rng.uniform(min_val, max_val)
        return dna

    def build_skeleton(self):
        """
        Create bone hierarchy from DNA.
        Different logic for different archetype types.

        Returns:
            Skeleton: Hierarchical bone structure
        """
        skeleton = Skeleton()

        # Example: Tentacle Horror
        if 'tentacles' in self.dna:
            # Add body bone (root)
            skeleton.add_bone('body', position=(0, 0, 0))

            # Add tentacle chains radiating from body
            tentacle_count = self.dna['tentacles']
            angle_step = 360 / tentacle_count

            for i in range(tentacle_count):
                angle = angle_step * i
                segment_count = self.dna['tentacle_segments']
                segment_length = self.dna['tentacle_length'] / segment_count

                # Create tentacle chain
                for seg in range(segment_count):
                    bone_name = f'tentacle_{i}_{seg}'
                    parent_name = 'body' if seg == 0 else f'tentacle_{i}_{seg-1}'

                    skeleton.add_bone(
                        bone_name,
                        parent=parent_name,
                        length=segment_length,
                        angle=angle if seg == 0 else 0,
                        bone_type='tentacle'
                    )

        # Example: Spider
        elif 'legs_per_segment' in self.dna:
            # Add body segments
            body_segments = self.dna['body_segments']
            for i in range(body_segments):
                segment_name = f'body_{i}'
                parent_name = f'body_{i-1}' if i > 0 else None
                skeleton.add_bone(segment_name, parent=parent_name)

                # Add legs to this segment
                legs = self.dna['legs_per_segment']
                for j in range(legs):
                    angle = (360 / legs) * j
                    leg_name = f'leg_{i}_{j}'
                    skeleton.add_bone(
                        leg_name,
                        parent=segment_name,
                        length=self.dna['leg_length'],
                        angle=angle,
                        bone_type='leg'
                    )

        return skeleton

    def spawn_geometry(self):
        """
        Create Ursina entities along skeleton bones.

        Returns:
            list: Ursina Entity objects
        """
        entities = []
        color = self.get_color_from_dna()

        for bone in self.skeleton.bones:
            # Different geometry for different bone types
            if bone.bone_type == 'tentacle':
                entity = Entity(
                    model='cylinder',
                    scale=(0.1, bone.length, 0.1),
                    color=color,
                    position=bone.get_world_position(),
                    rotation=bone.get_world_rotation()
                )
            elif bone.bone_type == 'leg':
                entity = Entity(
                    model='cylinder',
                    scale=(self.dna['leg_thickness'], bone.length, self.dna['leg_thickness']),
                    color=color,
                    position=bone.get_world_position(),
                    rotation=bone.get_world_rotation()
                )
            elif bone.bone_type == 'body':
                entity = Entity(
                    model='sphere',
                    scale=self.dna.get('body_size', 0.5),
                    color=color,
                    position=bone.get_world_position()
                )
            else:
                continue

            entities.append(entity)
            bone.entity = entity  # Link entity to bone

        return entities

    def get_color_from_dna(self):
        """
        Generate color from DNA hue range.

        Returns:
            color.rgb: Ursina color object
        """
        if 'color_hue' in self.dna:
            hue = self.dna['color_hue']
            # Convert hue to RGB (simplified)
            from ursina import color
            return color.hsv(hue, 0.7, 0.6)
        return color.gray

    def setup_animation_rules(self):
        """
        Define how this creature animates based on DNA.
        """
        if 'tentacles' in self.dna:
            self.animation_mode = 'wave_tentacles'
            self.wave_speed = self.rng.uniform(1.0, 3.0)
            self.wave_amplitude = self.rng.uniform(10, 30)
        elif 'legs_per_segment' in self.dna:
            self.animation_mode = 'walk_cycle'
            self.walk_speed = self.rng.uniform(2.0, 4.0)

    def animate(self, time, dt):
        """
        Update animation every frame.

        Args:
            time (float): Current game time
            dt (float): Delta time since last frame
        """
        if self.animation_mode == 'wave_tentacles':
            # Wave motion through tentacles
            for bone in self.skeleton.bones:
                if bone.bone_type == 'tentacle':
                    # Sine wave along tentacle chain
                    depth = bone.get_depth()  # Distance from root
                    phase = (time * self.wave_speed) + (depth * 0.3)
                    rotation = math.sin(phase) * self.wave_amplitude

                    bone.set_local_rotation(rotation)
                    if bone.entity:
                        bone.entity.rotation = bone.get_world_rotation()

        elif self.animation_mode == 'walk_cycle':
            # Legs move in walking pattern
            for bone in self.skeleton.bones:
                if bone.bone_type == 'leg':
                    leg_index = bone.get_sibling_index()
                    phase = (time * self.walk_speed) + (leg_index * math.pi / 4)
                    swing = math.sin(phase) * 30  # 30 degree swing

                    bone.set_local_rotation(swing)
                    if bone.entity:
                        bone.entity.rotation = bone.get_world_rotation()
```

### 5.2 Skeleton Class

```python
class Skeleton:
    """
    Hierarchical bone structure for a creature.
    """

    def __init__(self):
        self.bones = []
        self.bone_map = {}  # name -> Bone lookup

    def add_bone(self, name, parent=None, position=(0, 0, 0),
                 length=0.5, angle=0, bone_type='generic'):
        """
        Add a bone to the skeleton.

        Args:
            name (str): Unique bone name
            parent (str): Parent bone name (or None for root)
            position (tuple): Local position offset
            length (float): Bone length
            angle (float): Rotation angle (degrees)
            bone_type (str): Type tag ('tentacle', 'leg', 'body', etc.)
        """
        parent_bone = self.bone_map.get(parent) if parent else None

        bone = Bone(
            name=name,
            parent=parent_bone,
            position=Vec3(*position),
            length=length,
            angle=angle,
            bone_type=bone_type
        )

        self.bones.append(bone)
        self.bone_map[name] = bone

        if parent_bone:
            parent_bone.children.append(bone)

    def get_bone(self, name):
        """Get bone by name."""
        return self.bone_map.get(name)
```

### 5.3 Bone Class

```python
class Bone:
    """
    A single bone in a skeleton hierarchy.
    """

    def __init__(self, name, parent=None, position=Vec3(0,0,0),
                 length=0.5, angle=0, bone_type='generic'):
        self.name = name
        self.parent = parent
        self.local_position = position
        self.local_rotation = Vec3(0, angle, 0)  # Euler angles
        self.length = length
        self.bone_type = bone_type
        self.children = []
        self.entity = None  # Ursina Entity attached to this bone

    def get_world_position(self):
        """
        Calculate world position by accumulating parent transforms.

        Returns:
            Vec3: World position
        """
        if self.parent:
            # Parent world position + rotated local offset
            parent_pos = self.parent.get_world_position()
            parent_rot = self.parent.get_world_rotation()
            # (Simplified - real implementation uses quaternions)
            rotated_offset = self.rotate_vector(self.local_position, parent_rot)
            return parent_pos + rotated_offset
        return self.local_position

    def get_world_rotation(self):
        """
        Calculate world rotation by accumulating parent rotations.

        Returns:
            Vec3: World rotation (Euler angles)
        """
        if self.parent:
            return self.parent.get_world_rotation() + self.local_rotation
        return self.local_rotation

    def set_local_rotation(self, angle):
        """
        Set local rotation (for animation).

        Args:
            angle (float): Rotation angle in degrees
        """
        self.local_rotation.y = angle

    def get_depth(self):
        """
        Get depth in hierarchy (distance from root).

        Returns:
            int: Depth level (0 = root)
        """
        if self.parent:
            return self.parent.get_depth() + 1
        return 0

    def get_sibling_index(self):
        """
        Get index among siblings (for animation phase offsets).

        Returns:
            int: Index in parent's children list
        """
        if self.parent:
            return self.parent.children.index(self)
        return 0

    def rotate_vector(self, vector, rotation):
        """
        Rotate a vector by Euler angles.
        (Simplified - real implementation uses quaternions)

        Args:
            vector (Vec3): Vector to rotate
            rotation (Vec3): Euler angles

        Returns:
            Vec3: Rotated vector
        """
        # TODO: Implement proper rotation math
        # For now, simplified approximation
        return vector
```

---

## 6. Usage Examples

### Generate Multiple Creatures from Same Archetype

```python
# Generate 10 unique tentacle horrors
monsters = []
for i in range(10):
    seed = game_seed + i  # Mix game seed with index
    creature = ProceduralCreature(GENOME_TENTACLE_HORROR, seed)
    creatures.append(creature)

# Each creature has:
# - Different number of tentacles (4-12)
# - Different tentacle lengths (1.0-3.0)
# - Different segment counts (5-15)
# - Different colors (purple range)
# - All animate with wave motion
```

### Spawn Creature in Game World

```python
# In game.py or renderer3d.py
def spawn_enemy(enemy_type, position, game_seed, enemy_index):
    """
    Spawn a procedurally generated enemy.

    Args:
        enemy_type (str): Archetype name (c.ENEMY_TENTACLE_HORROR)
        position (tuple): Grid position (x, y)
        game_seed (int): Current game seed
        enemy_index (int): Unique enemy number

    Returns:
        ProceduralCreature: Generated creature
    """
    # Get genome for this enemy type
    genome = ENEMY_GENOMES.get(enemy_type)

    # Create unique seed from game state
    seed = hash((game_seed, enemy_type, enemy_index))

    # Generate creature
    creature = ProceduralCreature(genome, seed)

    # Position in world
    world_pos = world_to_3d_position(position[0], position[1], height=0.5)
    for entity in creature.entities:
        entity.position += world_pos

    return creature

# Usage:
tentacle_horror = spawn_enemy(
    c.ENEMY_TENTACLE_HORROR,
    position=(10, 15),
    game_seed=12345,
    enemy_index=7
)
```

### Animate Creatures

```python
# In main_3d.py update loop
def update():
    dt = time.dt
    current_time = time.time()

    # Update all creatures
    for creature in active_creatures:
        creature.animate(current_time, dt)
```

---

## 7. Animation System

### Rule-Based Animation Types

#### Wave Tentacles
```python
# Sine wave propagates along tentacle chains
for bone in skeleton.bones:
    if bone.bone_type == 'tentacle':
        depth = bone.get_depth()
        phase = (time * wave_speed) + (depth * 0.3)
        rotation = math.sin(phase) * wave_amplitude
        bone.set_local_rotation(rotation)
```

#### Walk Cycle
```python
# Legs swing with phase offsets
for bone in skeleton.bones:
    if bone.bone_type == 'leg':
        leg_index = bone.get_sibling_index()
        phase = (time * walk_speed) + (leg_index * math.pi / 4)
        swing = math.sin(phase) * 30
        bone.set_local_rotation(swing)
```

#### Idle Breathing
```python
# Body pulsates gently
for bone in skeleton.bones:
    if bone.bone_type == 'body':
        pulse = 1.0 + (math.sin(time * 2) * 0.1)
        bone.entity.scale = base_scale * pulse
```

#### Attack Lunge
```python
# Rapid forward extension
if attacking:
    progress = attack_timer / attack_duration
    offset = math.sin(progress * math.pi) * lunge_distance
    creature.root_bone.position.z += offset
```

---

## 8. Integration Points

### 8.1 Constants Definition

Add to `constants.py`:

```python
# Procedural Enemy Types
ENEMY_TENTACLE_HORROR = "tentacle_horror"
ENEMY_SPIDER_VARIANT = "spider_variant"
ENEMY_DRAGON_WHELP = "dragon_whelp"

# Genome Registry
ENEMY_GENOMES = {
    ENEMY_TENTACLE_HORROR: {...},  # Genome dict
    ENEMY_SPIDER_VARIANT: {...},
    ENEMY_DRAGON_WHELP: {...},
}
```

### 8.2 Enemy Creation

Update `entities.py`:

```python
class Enemy:
    def __init__(self, enemy_type, x, y, game_seed, enemy_index):
        self.enemy_type = enemy_type
        self.x = x
        self.y = y

        # NEW: Generate procedural appearance
        self.creature = ProceduralCreature(
            ENEMY_GENOMES[enemy_type],
            seed=hash((game_seed, enemy_type, enemy_index))
        )

        # Existing stats...
        self.hp = ENEMY_STATS[enemy_type]['hp']
        self.attack = ENEMY_STATS[enemy_type]['attack']
```

### 8.3 Rendering

Update `renderer3d.py`:

```python
def render_enemy(enemy):
    """
    Render a procedurally generated enemy.

    Args:
        enemy (Enemy): Enemy entity with creature attribute
    """
    # Position creature entities in world
    world_pos = world_to_3d_position(enemy.x, enemy.y, height=0.5)

    for entity in enemy.creature.entities:
        entity.position = world_pos + entity.local_position
        entity.visible = True
```

### 8.4 Animation Update

Update `main_3d.py`:

```python
def update():
    # Existing update logic...

    # NEW: Animate all creatures
    current_time = time.time()
    dt = time.dt

    for enemy in game.enemies:
        if hasattr(enemy, 'creature'):
            enemy.creature.animate(current_time, dt)
```

---

## 9. File Structure

Create new files:

```
roguelike/
├── procedural/
│   ├── __init__.py
│   ├── creature.py          # ProceduralCreature class
│   ├── skeleton.py          # Skeleton, Bone classes
│   ├── genomes.py           # GENOME_* definitions
│   └── animation_rules.py   # Animation functions
├── constants.py             # Add ENEMY_GENOMES
├── entities.py              # Update Enemy class
├── renderer3d.py            # Update render_enemy()
└── main_3d.py               # Update animation loop
```

---

## 10. Future Extensions

### DNA Mutation System
```python
def mutate_dna(parent_dna, mutation_rate=0.1):
    """Create offspring with mutations"""
    child_dna = parent_dna.copy()
    for trait, value in child_dna.items():
        if random.random() < mutation_rate:
            child_dna[trait] *= random.uniform(0.8, 1.2)
    return child_dna
```

### Hybrid Creatures
```python
def crossbreed(parent1_dna, parent2_dna):
    """Mix DNA from two parents"""
    child_dna = {}
    for trait in parent1_dna:
        child_dna[trait] = random.choice([
            parent1_dna[trait],
            parent2_dna[trait]
        ])
    return child_dna
```

### Rare Traits
```python
GENOME_DRAGON = {
    'horns': (2, 6),
    'horns_rare_golden': (0.01, 'boolean'),  # 1% chance
    'wings_rare_feathered': (0.05, 'boolean'),  # 5% chance
}
```

### Environmental Adaptation
```python
# Creatures adapt to dungeon depth
if dungeon_level > 10:
    genome['scale_multiplier'] = (1.5, 2.0)  # Deeper = bigger
    genome['color_hue'] = (0, 0)  # Pure red
```

---

## 11. Performance Considerations

### Bone Count Limits
- **Target**: <50 bones per creature
- **Complex creatures** (dragons): Split into chunks if needed
- **Profiling**: Measure skeleton.update() time

### Entity Pooling
```python
class CreatureEntityPool:
    """Reuse entities instead of creating/destroying"""
    def __init__(self, max_entities=1000):
        self.pool = [Entity(enabled=False) for _ in range(max_entities)]
        self.available = list(self.pool)

    def acquire(self):
        if self.available:
            entity = self.available.pop()
            entity.enabled = True
            return entity
        return None

    def release(self, entity):
        entity.enabled = False
        self.available.append(entity)
```

### LOD (Level of Detail)
```python
def get_creature_lod(distance_from_player):
    """Reduce skeleton detail for distant creatures"""
    if distance < 5:
        return 'high'  # Full skeleton
    elif distance < 10:
        return 'medium'  # Half skeleton segments
    else:
        return 'low'  # Single entity, no bones
```

---

## 12. Testing Strategy

### Unit Tests
```python
def test_dna_generation():
    """DNA should be deterministic from seed"""
    creature1 = ProceduralCreature(GENOME_TENTACLE_HORROR, seed=42)
    creature2 = ProceduralCreature(GENOME_TENTACLE_HORROR, seed=42)
    assert creature1.dna == creature2.dna

def test_skeleton_hierarchy():
    """Bones should form valid parent-child tree"""
    creature = ProceduralCreature(GENOME_SPIDER, seed=123)
    for bone in creature.skeleton.bones:
        if bone.parent:
            assert bone in bone.parent.children
```

### Visual Tests
```python
def test_generate_creature_gallery():
    """Generate multiple creatures for visual inspection"""
    for i in range(20):
        creature = ProceduralCreature(GENOME_TENTACLE_HORROR, seed=i)
        screenshot_creature(creature, f"creature_{i}.png")
```

---

## 13. Implementation Checklist

### Phase 1: Core System (1 week)
- [ ] Create `procedural/` directory
- [ ] Implement `Skeleton` and `Bone` classes
- [ ] Implement `ProceduralCreature` class
- [ ] Test with simple genome (single tentacle)

### Phase 2: First Archetype (3 days)
- [ ] Define `GENOME_TENTACLE_HORROR`
- [ ] Implement tentacle skeleton building
- [ ] Implement tentacle entity spawning
- [ ] Implement wave animation

### Phase 3: Integration (3 days)
- [ ] Update `entities.py` Enemy class
- [ ] Update `renderer3d.py` rendering
- [ ] Update `main_3d.py` animation loop
- [ ] Test in-game spawning

### Phase 4: More Archetypes (1 week)
- [ ] Implement `GENOME_SPIDER`
- [ ] Implement `GENOME_DRAGON`
- [ ] Add 2-3 more archetypes
- [ ] Test variety in gameplay

### Phase 5: Polish (3 days)
- [ ] Performance profiling
- [ ] Add entity pooling
- [ ] Add LOD system
- [ ] Final testing

---

## 14. Success Criteria

**System is complete when:**
1. ✅ Can generate 5+ unique creatures from same genome
2. ✅ Creatures are deterministic (same seed = same creature)
3. ✅ All creatures animate procedurally
4. ✅ 3+ archetypes implemented (Tentacle, Spider, Dragon)
5. ✅ Performance is acceptable (60 FPS with 10+ creatures)
6. ✅ No external assets required
7. ✅ Integrated with existing game systems

---

## 15. References

### Existing Code to Study:
- `graphics3d/players/warrior.py` - Procedural model generation
- `animations3d.py` - Animation system architecture
- `entities.py` - Enemy class structure
- `renderer3d.py` - 3D rendering pipeline

### Mathematical Resources:
- **Inverse Kinematics**: For more advanced limb reaching
- **Procedural Animation**: Sine waves, noise functions
- **Quaternions**: For proper 3D rotation math

---

**Document Status**: Ready for Implementation
**Last Updated**: 2025-10-12
**Next Step**: Create `procedural/` directory and start Phase 1

---

**Notes for Next Developer:**

This system is designed to be **incrementally implementable**. Start with a simple tentacle horror (just 1 tentacle, no animation) and gradually add complexity. The bone hierarchy is the foundation - once that works, everything else follows naturally.

Good luck! 🎮
