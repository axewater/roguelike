"""
Creature Builder - Assembles complete creature from parameters

Main class for building tentacle horror creatures from parameter dictionaries.
Handles creation, animation, and cleanup of creature entities.

Updated to use graph-based anatomy system with constraint solver for
anatomically-correct creature generation.
"""

from ursina import Entity, destroy
from modules.body import create_body, update_body_animation, get_body_geometry
from modules.tentacle import create_tentacle, update_tentacle_animation
from modules.eyes import create_eyes
from modules.spikes import create_spikes
import math
import random
import sys
import os

# Add current directory for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from surface_math import BodyGeometry
from anatomy_graph import CreatureAnatomyGraph
from constraint_solver import ConstraintSolver


class CreatureBuilder:
    """
    Builds and manages procedurally generated tentacle creatures.
    """

    def __init__(self, use_constraints=True):
        """
        Initialize creature builder.

        Args:
            use_constraints: If True, use constraint-based anatomy system (default)
                           If False, use legacy random placement
        """
        self.creature_root = None
        self.body = None
        self.tentacles = []
        self.eyes = []
        self.spikes = []
        self.current_params = None
        self.time_elapsed = 0.0

        # Anatomy system
        self.use_constraints = use_constraints
        self.anatomy_graph = None
        self.constraint_solver = None

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

        # Extract parameters
        tentacle_count = params.get('tentacle_count', 8)
        base_length = params.get('base_length', 2.0)
        length_variation = params.get('length_variation', 20) / 100.0
        segments = params.get('segments', 10)
        base_thickness = params.get('base_thickness', 0.1)
        taper = params.get('taper', 50)
        body_hue = params.get('body_hue', 280)
        eye_count = params.get('eye_count', 2)
        eye_pattern = params.get('eye_pattern', 'dual')
        eye_size = params.get('eye_size', 0.1)
        spike_count = params.get('spike_count', 15)
        spike_length = params.get('spike_length', 0.2)

        # Seed random for consistent variation per preset
        preset_name = params.get('preset_name', 'unnamed')
        random.seed(hash(preset_name))

        if self.use_constraints:
            # === NEW METHOD: Constraint-based anatomy system ===
            print("\n=== Building creature with constraint-based anatomy ===")

            # Initialize anatomy graph and constraint solver
            body_geometry = get_body_geometry(self.body)
            self.anatomy_graph = CreatureAnatomyGraph(body_geometry)
            self.constraint_solver = ConstraintSolver(self.anatomy_graph, seed=hash(preset_name))

            # Solve constraints to get optimal attachment points
            solved_points = self.constraint_solver.solve_all(
                tentacle_count=tentacle_count,
                eye_count=eye_count,
                spike_count=spike_count,
                eye_pattern=eye_pattern
            )

            # 2. Create tentacles using solved attachment points
            for i, attach_point in enumerate(solved_points['tentacles']):
                # Apply length variation
                variation = random.uniform(1.0 - length_variation, 1.0 + length_variation)
                tentacle_length = base_length * variation

                # Create tentacle at solved attachment point
                tentacle_data = create_tentacle(
                    parent=self.body,
                    length=tentacle_length,
                    segments=segments,
                    base_thickness=base_thickness,
                    taper=taper,
                    hue=body_hue,
                    attachment_point=attach_point  # Use solved attachment point
                )

                self.tentacles.append(tentacle_data)

            # 3. Create eyes using solved attachment points
            self.eyes = create_eyes(
                parent=self.body,
                count=eye_count,
                pattern=eye_pattern,
                size=eye_size,
                attachment_points=solved_points['eyes']  # Use solved attachment points
            )

            # 4. Create spikes using solved attachment points
            self.spikes = create_spikes(
                parent=self.body,
                count=spike_count,
                length=spike_length,
                hue=body_hue,
                attachment_points=solved_points['spikes']  # Use solved attachment points
            )

            print(f"✓ Constraint-based creature built successfully")

        else:
            # === LEGACY METHOD: Random placement (backward compatibility) ===
            print("\n=== Building creature with legacy random placement ===")

            # 2. Create tentacles (old method)
            for i in range(tentacle_count):
                angle = (360.0 / tentacle_count) * i
                variation = random.uniform(1.0 - length_variation, 1.0 + length_variation)
                tentacle_length = base_length * variation

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

            # 3. Create eyes (old method)
            self.eyes = create_eyes(
                parent=self.body,
                count=eye_count,
                pattern=eye_pattern,
                size=eye_size
            )

            # 4. Create spikes (old method)
            self.spikes = create_spikes(
                parent=self.body,
                count=spike_count,
                length=spike_length,
                hue=body_hue
            )

        # Reset random seed
        random.seed()

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
