"""
Creature Builder - Assembles complete creature from parameters

Main class for building tentacle horror creatures from parameter dictionaries.
Handles creation, animation, and cleanup of creature entities.
"""

from ursina import Entity, destroy
from modules.body import create_body, update_body_animation
from modules.tentacle import create_tentacle, update_tentacle_animation
from modules.eyes import create_eyes
from modules.spikes import create_spikes
import math
import random


class CreatureBuilder:
    """
    Builds and manages procedurally generated tentacle creatures.
    """

    def __init__(self):
        """Initialize creature builder"""
        self.creature_root = None
        self.body = None
        self.tentacles = []
        self.eyes = []
        self.spikes = []
        self.current_params = None
        self.time_elapsed = 0.0

    def build_from_parameters(self, params):
        """
        Build complete creature from parameter dictionary.

        Args:
            params: Dictionary with creature parameters

        Returns:
            Entity: Root creature entity
        """
        # Clear existing creature
        self.clear_creature()

        # Store parameters
        self.current_params = params

        # Create root container
        self.creature_root = Entity(position=(0, 0, 0))

        # 1. Create body
        self.body = create_body(
            parent=self.creature_root,
            size=params.get('body_size', 0.6),
            hue=params.get('body_hue', 280),
            shape_type=params.get('body_shape', 'sphere')
        )

        # 2. Create tentacles
        tentacle_count = params.get('tentacle_count', 8)
        base_length = params.get('base_length', 2.0)
        length_variation = params.get('length_variation', 20) / 100.0  # Convert % to decimal
        segments = params.get('segments', 10)
        base_thickness = params.get('base_thickness', 0.1)
        taper = params.get('taper', 50)
        body_hue = params.get('body_hue', 280)

        # Seed random for consistent variation per preset
        preset_name = params.get('preset_name', 'unnamed')
        random.seed(hash(preset_name))

        for i in range(tentacle_count):
            # Calculate angle evenly around body
            angle = (360.0 / tentacle_count) * i

            # Apply length variation
            variation = random.uniform(1.0 - length_variation, 1.0 + length_variation)
            tentacle_length = base_length * variation

            # Create tentacle
            tentacle_data = create_tentacle(
                parent=self.body,
                length=tentacle_length,
                segments=segments,
                base_thickness=base_thickness,
                angle=angle,
                taper=taper,
                hue=body_hue,
                attach_height=-0.3
            )

            self.tentacles.append(tentacle_data)

        # Reset random seed
        random.seed()

        # 3. Create eyes
        eye_count = params.get('eye_count', 2)
        eye_pattern = params.get('eye_pattern', 'dual')
        eye_size = params.get('eye_size', 0.1)

        self.eyes = create_eyes(
            parent=self.body,
            count=eye_count,
            pattern=eye_pattern,
            size=eye_size
        )

        # 4. Create spikes
        spike_count = params.get('spike_count', 15)
        spike_length = params.get('spike_length', 0.2)

        self.spikes = create_spikes(
            parent=self.body,
            count=spike_count,
            length=spike_length,
            hue=body_hue
        )

        print(f"✓ Creature built: {tentacle_count} tentacles, {eye_count} eyes, {spike_count} spikes")
        print(f"  Total entities: {self.get_entity_count()}")

        return self.creature_root

    def update(self, dt):
        """
        Update creature animations.

        Args:
            dt: Delta time since last frame
        """
        if not self.current_params or not self.current_params.get('animate', True):
            return

        self.time_elapsed += dt

        # Update body animation
        if self.body:
            update_body_animation(
                self.body,
                self.time_elapsed,
                pulse_speed=self.current_params.get('wave_speed', 2.0) * 0.5
            )

        # Update tentacle animations
        wave_speed = self.current_params.get('wave_speed', 2.0)
        wave_amplitude = self.current_params.get('wave_amplitude', 20)

        for i, tentacle_data in enumerate(self.tentacles):
            # Each tentacle has a phase offset for variety
            phase_offset = i * (360.0 / len(self.tentacles)) if self.tentacles else 0

            update_tentacle_animation(
                tentacle_data,
                self.time_elapsed,
                wave_speed=wave_speed,
                wave_amplitude=wave_amplitude,
                phase_offset=math.radians(phase_offset)
            )

    def clear_creature(self):
        """
        Destroy all creature entities.
        """
        if self.creature_root:
            destroy(self.creature_root)
            self.creature_root = None

        self.body = None
        self.tentacles.clear()
        self.eyes.clear()
        self.spikes.clear()
        self.time_elapsed = 0.0

    def get_entity_count(self):
        """
        Get total number of entities in creature.

        Returns:
            int: Entity count
        """
        count = 0

        # Root + body
        if self.creature_root:
            count += 1
        if self.body:
            count += 1

        # Tentacles (each has root + segments)
        for tentacle in self.tentacles:
            count += 1  # Root
            count += len(tentacle['segments'])

        # Eyes (each eye has eye + pupil = 2 entities)
        count += len(self.eyes) * 2

        # Spikes
        count += len(self.spikes)

        return count

    def get_creature_stats(self):
        """
        Get statistics about current creature.

        Returns:
            dict: Statistics
        """
        return {
            'entity_count': self.get_entity_count(),
            'tentacle_count': len(self.tentacles),
            'eye_count': len(self.eyes),
            'spike_count': len(self.spikes),
            'total_segments': sum(len(t['segments']) for t in self.tentacles)
        }
