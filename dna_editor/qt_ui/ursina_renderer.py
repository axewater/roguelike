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
        self.sky_top = None
        self.lighting = {}

        # Camera orbit state
        self.camera_angle = 0
        self.camera_height = 2
        self.camera_distance = 6

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

            # Set up camera with orbit position
            camera.position = (0, self.camera_height, -self.camera_distance)
            camera.look_at((0, 0, 0))
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
        # Import constants
        try:
            from ..core.constants import (
                GROUND_Y, SHADOW_Y, GROUND_COLOR, SHADOW_SIZE, SHADOW_OPACITY,
                SKY_GRADIENT_BOTTOM, SKY_GRADIENT_TOP
            )
        except ImportError:
            # Fallback values
            GROUND_Y = -3.5
            SHADOW_Y = -3.45
            GROUND_COLOR = (0.1, 0.1, 0.15)
            SHADOW_SIZE = 8
            SHADOW_OPACITY = 100
            SKY_GRADIENT_BOTTOM = (0.02, 0.02, 0.08)
            SKY_GRADIENT_TOP = (0.08, 0.08, 0.15)

        Entity = self.ursina_modules['Entity']
        Sky = self.ursina_modules['Sky']
        color = self.ursina_modules['color']
        AmbientLight = self.ursina_modules['AmbientLight']
        DirectionalLight = self.ursina_modules['DirectionalLight']
        PointLight = self.ursina_modules['PointLight']

        # Ground (positioned below tentacles)
        self.ground = Entity(
            model='plane',
            scale=20,
            color=color.rgb(*GROUND_COLOR),
            position=(0, GROUND_Y, 0),
            shader='basic_lighting_shader'
        )

        # Gradient sky (dark at horizon, lighter at top)
        # Create a large inverted sphere with gradient from bottom to top
        self.sky = Entity(
            model='sphere',
            scale=500,
            color=color.rgb(*SKY_GRADIENT_BOTTOM),
            double_sided=True,
            unlit=True
        )
        # Add gradient effect using top hemisphere color
        self.sky_top = Entity(
            model='sphere',
            scale=499,
            position=(0, 250, 0),
            color=color.rgb(*SKY_GRADIENT_TOP),
            double_sided=True,
            unlit=True,
            alpha=0.5
        )

        # 3-point lighting system
        self.lighting = {}
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

        # Improved shadow plane (larger, positioned on new floor)
        self.shadow_plane = Entity(
            model='plane',
            scale=(SHADOW_SIZE, 1, SHADOW_SIZE),
            color=color.rgba(0, 0, 0, SHADOW_OPACITY),
            position=(0, SHADOW_Y, 0),
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
            # Import creature model (use relative import)
            from ..models.creature import TentacleCreature

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
        """Handle mouse camera controls with orbit system."""
        try:
            camera = self.ursina_modules['camera']
            held_keys = self.ursina_modules['held_keys']
            mouse = self.ursina_modules['mouse']
            math = self.ursina_modules['math']

            # Import constants for limits
            try:
                from ..core.constants import (
                    MIN_CAMERA_DISTANCE, MAX_CAMERA_DISTANCE,
                    MIN_CAMERA_HEIGHT, MAX_CAMERA_HEIGHT
                )
            except ImportError:
                MIN_CAMERA_DISTANCE = 2
                MAX_CAMERA_DISTANCE = 15
                MIN_CAMERA_HEIGHT = 0.5
                MAX_CAMERA_HEIGHT = 5

            # Mouse drag to orbit
            if mouse.left:
                self.camera_angle += mouse.velocity[0] * 200
                self.camera_height += mouse.velocity[1] * 5

            # Clamp camera height
            self.camera_height = max(MIN_CAMERA_HEIGHT, min(MAX_CAMERA_HEIGHT, self.camera_height))

            # Scroll to zoom
            if mouse.scroll != 0:
                self.camera_distance -= mouse.scroll * 0.5
                self.camera_distance = max(MIN_CAMERA_DISTANCE, min(MAX_CAMERA_DISTANCE, self.camera_distance))

            # Calculate camera position using orbit math
            angle_rad = math.radians(self.camera_angle)
            cam_x = self.camera_distance * math.sin(angle_rad)
            cam_z = -self.camera_distance * math.cos(angle_rad)

            # Update camera position and look at creature center
            camera.position = (cam_x, self.camera_height, cam_z)
            camera.look_at((0, 0, 0))

            # Reset camera (R key)
            if held_keys['r']:
                self.camera_angle = 0
                self.camera_height = 2
                self.camera_distance = 6
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
