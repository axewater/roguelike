"""
BlobCreature model - creature made of translucent slime cubes.
"""

from ursina import Entity, Vec3, color, destroy
import math
import random
from ..core.constants import (
    DEFAULT_NUM_CUBES, DEFAULT_CUBE_SIZE_MIN, DEFAULT_CUBE_SIZE_MAX,
    DEFAULT_CUBE_SPACING, DEFAULT_BLOB_COLOR, DEFAULT_BLOB_TRANSPARENCY,
    DEFAULT_JIGGLE_SPEED, DEFAULT_BLOB_PULSE_AMOUNT,
    BLOB_JIGGLE_AMPLITUDE, BLOB_ATTACK_DURATION,
    BLOB_ATTACK_EXPAND_END, BLOB_ATTACK_CONTRACT_END, BLOB_ATTACK_RETURN_END,
    BLOB_ATTACK_EXPANSION, BLOB_ATTACK_SCALE
)
from ..shaders import create_toon_shader


class BlobCube:
    """Single cube in the blob with individual animation state."""

    def __init__(self, position, size, base_color, transparency, parent, toon_shader=None):
        """
        Create a blob cube.

        Args:
            position: Vec3 position in world space
            size: Cube scale
            base_color: RGB tuple (0-1)
            transparency: Alpha value (0-1, where 1 is fully transparent)
            parent: Parent entity
            toon_shader: Optional toon shader to apply
        """
        self.original_position = position
        self.original_size = size
        self.base_color = base_color
        self.transparency = transparency

        # Random jiggle phase offset for organic motion
        self.jiggle_phase_x = random.random() * math.pi * 2
        self.jiggle_phase_y = random.random() * math.pi * 2
        self.jiggle_phase_z = random.random() * math.pi * 2

        # Create cube entity with transparency
        # Ursina color.rgba() for transparency
        cube_color = color.rgba(base_color[0], base_color[1], base_color[2], 1.0 - transparency)

        entity_params = {
            'model': 'cube',
            'color': cube_color,
            'scale': size,
            'position': position,
            'parent': parent
        }

        # Apply toon shader if provided
        if toon_shader is not None:
            entity_params['shader'] = toon_shader

        self.entity = Entity(**entity_params)

    def update_animation(self, time, jiggle_speed, jiggle_amplitude,
                        is_attacking=False, attack_progress=0.0, attack_phase='idle'):
        """
        Update cube animation.

        Args:
            time: Current animation time
            jiggle_speed: Speed of jiggle animation
            jiggle_amplitude: Intensity of jiggle
            is_attacking: Whether attack is in progress
            attack_progress: Attack phase progress (0-1)
            attack_phase: 'expand', 'contract', 'return', or 'idle'
        """
        if is_attacking:
            # Attack animation overrides idle jiggle
            if attack_phase == 'expand':
                # Expand outward from center (smooth ease-out)
                t = self._ease_out_cubic(attack_progress)
                direction = self.original_position.normalized()
                offset = direction * (BLOB_ATTACK_EXPANSION - 1.0) * t
                self.entity.position = self.original_position + offset
                self.entity.scale = self.original_size * (1.0 + (BLOB_ATTACK_SCALE - 1.0) * t)

            elif attack_phase == 'contract':
                # Contract back (smooth ease-in)
                t = 1.0 - self._ease_in_cubic(attack_progress)
                direction = self.original_position.normalized()
                offset = direction * (BLOB_ATTACK_EXPANSION - 1.0) * t
                self.entity.position = self.original_position + offset
                self.entity.scale = self.original_size * (1.0 + (BLOB_ATTACK_SCALE - 1.0) * t)

            elif attack_phase == 'return':
                # Return to idle (ease to rest)
                t = 1.0 - self._ease_out_quad(attack_progress)
                direction = self.original_position.normalized()
                offset = direction * (BLOB_ATTACK_EXPANSION - 1.0) * t * 0.1  # Small residual
                self.entity.position = self.original_position + offset
                self.entity.scale = self.original_size
        else:
            # Idle jiggle animation (each cube jiggles independently)
            jiggle_x = math.sin(time * jiggle_speed + self.jiggle_phase_x) * jiggle_amplitude
            jiggle_y = math.sin(time * jiggle_speed * 1.3 + self.jiggle_phase_y) * jiggle_amplitude * 0.8
            jiggle_z = math.cos(time * jiggle_speed * 0.9 + self.jiggle_phase_z) * jiggle_amplitude

            self.entity.position = self.original_position + Vec3(jiggle_x, jiggle_y, jiggle_z)

            # Subtle pulse in size
            pulse = 1.0 + math.sin(time * jiggle_speed * 0.7 + self.jiggle_phase_x) * 0.05
            self.entity.scale = self.original_size * pulse

    def _ease_out_cubic(self, t):
        """Ease-out cubic (fast start, slow end)."""
        return 1 - pow(1 - t, 3)

    def _ease_in_cubic(self, t):
        """Ease-in cubic (slow start, fast end)."""
        return t * t * t

    def _ease_out_quad(self, t):
        """Ease-out quadratic."""
        return 1 - (1 - t) * (1 - t)

    def destroy(self):
        """Cleanup cube entity."""
        destroy(self.entity)


class BlobCreature:
    """Creature made of translucent slime cubes in random 3D cluster."""

    def __init__(self, num_cubes=DEFAULT_NUM_CUBES,
                 cube_size_min=DEFAULT_CUBE_SIZE_MIN,
                 cube_size_max=DEFAULT_CUBE_SIZE_MAX,
                 cube_spacing=DEFAULT_CUBE_SPACING,
                 blob_color=DEFAULT_BLOB_COLOR,
                 transparency=DEFAULT_BLOB_TRANSPARENCY,
                 jiggle_speed=DEFAULT_JIGGLE_SPEED,
                 pulse_amount=DEFAULT_BLOB_PULSE_AMOUNT):
        """
        Create a blob creature.

        Args:
            num_cubes: Number of cubes in blob (1-20)
            cube_size_min: Minimum cube size
            cube_size_max: Maximum cube size
            cube_spacing: Distance between cube centers
            blob_color: Base color (RGB tuple 0-1)
            transparency: Alpha transparency (0=opaque, 1=fully transparent)
            jiggle_speed: Animation speed
            pulse_amount: Pulse animation intensity
        """
        # Create root entity
        self.root = Entity(position=(0, 0, 0))
        self.cubes = []

        # Store parameters
        self.num_cubes = num_cubes
        self.cube_size_min = cube_size_min
        self.cube_size_max = cube_size_max
        self.cube_spacing = cube_spacing
        self.blob_color = blob_color
        self.transparency = transparency
        self.jiggle_speed = jiggle_speed
        self.pulse_amount = pulse_amount

        # Attack animation state
        self.is_attacking = False
        self.attack_start_time = 0

        # Create toon shader (shared across all cubes)
        self.toon_shader = create_toon_shader()
        if self.toon_shader is None:
            print("WARNING: Toon shader creation failed in BlobCreature, using default rendering")

        # Generate blob cubes
        self._generate_cubes()

    def _generate_cubes(self):
        """Generate random 3D cluster of cubes."""
        # Clear existing cubes
        for cube in self.cubes:
            cube.destroy()
        self.cubes.clear()

        # Track occupied positions for random cluster growth
        occupied_positions = []

        for i in range(self.num_cubes):
            if i == 0:
                # First cube at origin
                position = Vec3(0, 0, 0)
            else:
                # Find random adjacent position to existing cube
                # Pick random existing cube as base
                base_cube_pos = random.choice(occupied_positions)

                # Generate random adjacent position (6 cardinal directions + diagonals)
                attempts = 0
                max_attempts = 20

                while attempts < max_attempts:
                    # Random offset in 3D grid with spacing
                    offset_x = random.choice([-1, 0, 1]) * self.cube_spacing
                    offset_y = random.choice([-1, 0, 1]) * self.cube_spacing
                    offset_z = random.choice([-1, 0, 1]) * self.cube_spacing

                    # Skip if zero offset (same position)
                    if offset_x == 0 and offset_y == 0 and offset_z == 0:
                        attempts += 1
                        continue

                    position = base_cube_pos + Vec3(offset_x, offset_y, offset_z)

                    # Check if position is already occupied (within tolerance)
                    collision = False
                    for occupied_pos in occupied_positions:
                        if (position - occupied_pos).length() < self.cube_spacing * 0.5:
                            collision = True
                            break

                    if not collision:
                        break

                    attempts += 1

                # If couldn't find non-colliding position, use last attempt
                # (allows overlapping for dense blobs)

            # Random size within range
            size = random.uniform(self.cube_size_min, self.cube_size_max)

            # Add slight color variation per cube
            hue_variation = (random.random() - 0.5) * 0.1  # ±5% variation
            cube_color = (
                max(0.0, min(1.0, self.blob_color[0] + hue_variation)),
                max(0.0, min(1.0, self.blob_color[1] + hue_variation * 0.5)),
                max(0.0, min(1.0, self.blob_color[2] + hue_variation))
            )

            # Create cube
            cube = BlobCube(
                position=position,
                size=size,
                base_color=cube_color,
                transparency=self.transparency,
                parent=self.root,
                toon_shader=self.toon_shader
            )

            self.cubes.append(cube)
            occupied_positions.append(position)

    def rebuild(self, num_cubes, cube_size_min, cube_size_max, cube_spacing,
                blob_color, transparency, jiggle_speed, pulse_amount):
        """
        Rebuild blob with new parameters.

        Args:
            num_cubes: Number of cubes
            cube_size_min: Minimum cube size
            cube_size_max: Maximum cube size
            cube_spacing: Cube spacing
            blob_color: Base color RGB tuple
            transparency: Alpha transparency
            jiggle_speed: Animation speed
            pulse_amount: Pulse intensity
        """
        self.num_cubes = num_cubes
        self.cube_size_min = cube_size_min
        self.cube_size_max = cube_size_max
        self.cube_spacing = cube_spacing
        self.blob_color = blob_color
        self.transparency = transparency
        self.jiggle_speed = jiggle_speed
        self.pulse_amount = pulse_amount

        # Regenerate cubes
        self._generate_cubes()

    def start_attack(self, camera_position):
        """
        Start attack animation.

        Args:
            camera_position: Vec3 position of camera (not used for blob, but kept for interface consistency)
        """
        self.is_attacking = True
        self.attack_start_time = 0  # Will be set on first update

    def start_attack_2(self, camera_position):
        """
        Start attack 2 animation (same as attack 1 for blob).

        Args:
            camera_position: Vec3 position of camera
        """
        # Blob only has one attack type, so both attacks do the same thing
        self.start_attack(camera_position)

    def update_animation(self, time, camera_position=None):
        """
        Update blob animation.

        Args:
            time: Current animation time
            camera_position: Optional camera position (for interface consistency)
        """
        # Handle attack state
        attack_phase = 'idle'
        attack_progress = 0.0

        if self.is_attacking:
            # Initialize attack start time on first frame
            if self.attack_start_time == 0:
                self.attack_start_time = time

            # Calculate attack progress
            attack_elapsed = time - self.attack_start_time

            if attack_elapsed < BLOB_ATTACK_EXPAND_END:
                # Expansion phase
                attack_phase = 'expand'
                attack_progress = attack_elapsed / BLOB_ATTACK_EXPAND_END
            elif attack_elapsed < BLOB_ATTACK_CONTRACT_END:
                # Contraction phase
                attack_phase = 'contract'
                attack_progress = (attack_elapsed - BLOB_ATTACK_EXPAND_END) / (BLOB_ATTACK_CONTRACT_END - BLOB_ATTACK_EXPAND_END)
            elif attack_elapsed < BLOB_ATTACK_RETURN_END:
                # Return to idle phase
                attack_phase = 'return'
                attack_progress = (attack_elapsed - BLOB_ATTACK_CONTRACT_END) / (BLOB_ATTACK_RETURN_END - BLOB_ATTACK_CONTRACT_END)
            else:
                # Attack complete
                self.is_attacking = False
                self.attack_start_time = 0
                attack_phase = 'idle'

        # Update all cubes
        jiggle_amplitude = BLOB_JIGGLE_AMPLITUDE * (1.0 + self.pulse_amount)

        for cube in self.cubes:
            cube.update_animation(
                time=time,
                jiggle_speed=self.jiggle_speed,
                jiggle_amplitude=jiggle_amplitude,
                is_attacking=self.is_attacking,
                attack_progress=attack_progress,
                attack_phase=attack_phase
            )

    def destroy(self):
        """Cleanup all cube entities."""
        for cube in self.cubes:
            cube.destroy()
        destroy(self.root)
