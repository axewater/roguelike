"""
Ursina renderer - manages 3D creature rendering in separate window.

Handles Ursina initialization, scene creation, and creature management
without Qt widget dependencies.
"""

from PyQt6.QtCore import QTimer
import sys
import os


class UrsinaRenderer:
    """Manages Ursina 3D rendering in separate window."""

    def __init__(self):
        """Initialize Ursina renderer."""
        self.creature = None
        self.ursina_app = None
        self.animation_time = 0
        self.timer = None

        # Scene components
        self.ground = None
        self.sky = None
        self.lighting = {}

        # Ursina module references
        self.ursina_modules = {}

        self._init_ursina()

    def _init_ursina(self):
        """Initialize Ursina application and scene."""
        try:
            # Import Ursina
            from ursina import Ursina, Entity, camera, Sky, color, held_keys, mouse
            from ursina import AmbientLight, DirectionalLight, PointLight
            from ursina import window
            import math

            # Store module references
            self.ursina_modules = {
                'Entity': Entity,
                'camera': camera,
                'Sky': Sky,
                'color': color,
                'held_keys': held_keys,
                'mouse': mouse,
                'AmbientLight': AmbientLight,
                'DirectionalLight': DirectionalLight,
                'PointLight': PointLight,
                'window': window,
                'math': math
            }

            # Create Ursina app
            self.ursina_app = Ursina(
                title="DNA Editor - 3D Preview",
                borderless=False,
                fullscreen=False,
                size=(900, 700),
                position=(400, 50)
            )

            # Set window background
            window.color = color.rgb(0.05, 0.05, 0.1)

            # Create scene
            self._create_scene()

            # Set up camera
            camera.position = (0, 2, -6)
            camera.rotation_x = 10
            camera.fov = 60

            # Start animation timer
            self.timer = QTimer()
            self.timer.timeout.connect(self._update_animation)
            self.timer.start(16)  # ~60 FPS

            print("✓ Ursina renderer initialized (separate window)")

        except Exception as e:
            print(f"✗ Failed to initialize Ursina: {e}")
            import traceback
            traceback.print_exc()

    def _create_scene(self):
        """Create scene elements (ground, sky, lighting)."""
        Entity = self.ursina_modules['Entity']
        Sky = self.ursina_modules['Sky']
        color = self.ursina_modules['color']
        AmbientLight = self.ursina_modules['AmbientLight']
        DirectionalLight = self.ursina_modules['DirectionalLight']
        PointLight = self.ursina_modules['PointLight']

        # Ground
        self.ground = Entity(
            model='plane',
            scale=20,
            color=color.rgb(0.1, 0.1, 0.15),
            position=(0, -1, 0),
            shader='basic_lighting_shader'
        )

        # Sky
        self.sky = Sky(color=color.rgb(0.05, 0.05, 0.1))

        # 3-point lighting system
        self.lighting['ambient'] = AmbientLight(
            color=color.rgb(0.2, 0.2, 0.25),
            intensity=0.2
        )

        self.lighting['key'] = DirectionalLight(
            position=(5, 8, 3),
            rotation=(50, -35, 0),
            color=color.rgb(1.0, 0.98, 0.94),
            intensity=1.5
        )

        self.lighting['fill'] = DirectionalLight(
            position=(-3, 4, -2),
            rotation=(120, 45, 0),
            color=color.rgb(0.7, 0.75, 0.85),
            intensity=0.6
        )

        self.lighting['rim'] = DirectionalLight(
            position=(-2, 3, -5),
            rotation=(150, 20, 0),
            color=color.rgb(0.6, 0.7, 1.0),
            intensity=0.8
        )

        self.lighting['point'] = PointLight(
            position=(0, 2, 0),
            color=color.rgb(1.0, 0.95, 0.9),
            intensity=0.4
        )

        # Shadow plane
        self.shadow_plane = Entity(
            model='plane',
            scale=(3, 1, 3),
            color=color.rgba(0, 0, 0, 80),
            position=(0, -0.95, 0),
            rotation_x=90,
            unlit=True
        )

    def rebuild_creature(self, num_tentacles, segments, algorithm, params, thickness_base, taper_factor):
        """
        Rebuild creature with new parameters.

        Args:
            num_tentacles: Number of tentacles
            segments: Segments per tentacle
            algorithm: 'bezier' or 'fourier'
            params: Algorithm parameters dict
            thickness_base: Base thickness
            taper_factor: Taper factor
        """
        try:
            # Import creature model
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if parent_dir not in sys.path:
                sys.path.insert(0, parent_dir)

            from dna_editor_copy.models.creature import TentacleCreature

            # Destroy old creature
            if self.creature:
                self.creature.destroy()

            # Create new creature
            self.creature = TentacleCreature(
                num_tentacles=num_tentacles,
                segments_per_tentacle=segments,
                algorithm=algorithm,
                algorithm_params=params,
                thickness_base=thickness_base,
                taper_factor=taper_factor
            )

            print(f"✓ Creature rebuilt: {num_tentacles} tentacles, {segments} segments, {algorithm}")

        except Exception as e:
            print(f"✗ Failed to rebuild creature: {e}")
            import traceback
            traceback.print_exc()

    def _update_animation(self):
        """Update creature animation and handle rendering."""
        if self.ursina_app:
            try:
                # Step Ursina forward one frame (non-blocking)
                self.ursina_app.step()

                # Update animation time
                from ursina import time as ursina_time
                self.animation_time += ursina_time.dt

                # Update creature animation
                if self.creature:
                    self.creature.update_animation(self.animation_time)

                # Handle camera controls
                self._handle_camera_controls()

            except Exception as e:
                # Silently ignore errors (app might be closing)
                pass

    def _handle_camera_controls(self):
        """Handle mouse camera controls."""
        try:
            camera = self.ursina_modules['camera']
            held_keys = self.ursina_modules['held_keys']
            mouse = self.ursina_modules['mouse']

            # Mouse drag to rotate
            if mouse.left:
                camera.rotation_y += mouse.velocity[0] * 50
                camera.rotation_x -= mouse.velocity[1] * 50
                camera.rotation_x = max(-80, min(80, camera.rotation_x))

            # Scroll to zoom
            camera.position += camera.forward * mouse.scroll * 0.5

            # Reset camera (R key)
            if held_keys['r']:
                camera.position = (0, 2, -6)
                camera.rotation = (10, 0, 0)
                held_keys['r'] = False

        except Exception as e:
            pass

    def cleanup(self):
        """Cleanup Ursina resources."""
        try:
            if self.timer:
                self.timer.stop()

            if self.creature:
                self.creature.destroy()

            if self.ursina_app:
                self.ursina_app.exit()

            print("✓ Ursina renderer cleaned up")

        except Exception as e:
            print(f"✗ Cleanup error: {e}")
