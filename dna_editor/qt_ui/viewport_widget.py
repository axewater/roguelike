"""
Viewport widget for 3D creature rendering.

Manages Ursina 3D scene with creature and camera controls.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
import threading
import sys


class ViewportWidget(QWidget):
    """
    Widget containing Ursina 3D viewport.

    Uses separate window approach for simplicity.
    """

    def __init__(self, parent=None):
        """Initialize viewport widget."""
        super().__init__(parent)

        self.creature = None
        self.ursina_app = None
        self.ursina_thread = None
        self.animation_time = 0

        # Scene components
        self.ground = None
        self.sky = None
        self.sky_top = None
        self.camera_pivot = None

        # Camera orbit state
        self.camera_angle = 0
        self.camera_height = 2
        self.camera_distance = 6

        self._init_ui()
        self._init_ursina()

    def _init_ui(self):
        """Initialize UI placeholder."""
        layout = QVBoxLayout()

        # Placeholder label
        label = QLabel("3D Viewport\n(Separate Ursina Window)")
        label.setFont(QFont("Arial", 14))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("background-color: #1a1a2e; color: #ffffff; padding: 20px;")
        layout.addWidget(label)

        info_label = QLabel(
            "The 3D creature preview appears in a separate window.\n\n"
            "Camera Controls:\n"
            "• Mouse Drag - Rotate camera\n"
            "• Scroll - Zoom in/out\n"
            "• R - Reset camera"
        )
        info_label.setFont(QFont("Arial", 10))
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("color: #aaaaaa;")
        layout.addWidget(info_label)

        self.setLayout(layout)

    def _init_ursina(self):
        """Initialize Ursina in separate thread."""
        # Import Ursina here to avoid conflicts
        try:
            from ursina import Ursina, Entity, camera, Sky, color, held_keys, mouse
            from ursina import AmbientLight, DirectionalLight, PointLight
            import math

            # Store references for later use
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
                'math': math
            }

            # Initialize Ursina app
            self.ursina_app = Ursina(
                title="DNA Editor - 3D Preview",
                borderless=False,
                fullscreen=False,
                size=(800, 600),
                position=(100, 100)
            )

            # Set window color
            from ursina import window
            window.color = color.rgb(0.05, 0.05, 0.1)

            # Create scene
            self._create_scene()

            # Set up camera with orbit position
            camera.position = (0, self.camera_height, -self.camera_distance)
            camera.look_at((0, 0, 0))
            camera.fov = 60

            # Animation timer
            self.timer = QTimer()
            self.timer.timeout.connect(self._update_animation)
            self.timer.start(16)  # ~60 FPS

            print("✓ Ursina viewport initialized")

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
            position=(0, GROUND_Y, 0)
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

        # Lighting setup (3-point lighting)
        self.ambient_light = AmbientLight(
            color=color.rgb(0.2, 0.2, 0.25),
            intensity=0.2
        )

        self.key_light = DirectionalLight(
            position=(5, 8, 3),
            rotation=(50, -35, 0),
            color=color.rgb(1.0, 0.98, 0.94),
            intensity=1.5
        )

        self.fill_light = DirectionalLight(
            position=(-3, 4, -2),
            rotation=(120, 45, 0),
            color=color.rgb(0.7, 0.75, 0.85),
            intensity=0.6
        )

        self.rim_light = DirectionalLight(
            position=(-2, 3, -5),
            rotation=(150, 20, 0),
            color=color.rgb(0.6, 0.7, 1.0),
            intensity=0.8
        )

        self.point_light = PointLight(
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
            print(f"  Algorithm params: {params}")
            print(f"  Creature has {len(self.creature.tentacles)} tentacles")
            print(f"  Body position: {self.creature.body.position}")

        except Exception as e:
            print(f"✗ Failed to rebuild creature: {e}")
            import traceback
            traceback.print_exc()

    def _update_animation(self):
        """Update creature animation every frame."""
        if self.ursina_app:
            try:
                # CRITICAL: Step Ursina forward one frame
                # This renders the scene without blocking Qt's event loop
                self.ursina_app.step()

                # Update animation time
                from ursina import time as ursina_time
                self.animation_time += ursina_time.dt

                # Update creature if it exists
                if self.creature:
                    self.creature.update_animation(self.animation_time)

                # Handle camera controls
                self._handle_camera_controls()

            except Exception as e:
                # Silently ignore errors during animation (app might be closing)
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

            # Mouse drag to orbit (Ursina uses held_keys for mouse buttons)
            if held_keys['left mouse']:
                self.camera_angle += mouse.velocity[0] * 200
                self.camera_height += mouse.velocity[1] * 5

            # Clamp camera height
            self.camera_height = max(MIN_CAMERA_HEIGHT, min(MAX_CAMERA_HEIGHT, self.camera_height))

            # Scroll to zoom (Ursina uses held_keys for scroll events)
            if held_keys['scroll up']:
                self.camera_distance -= 0.5
            if held_keys['scroll down']:
                self.camera_distance += 0.5
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
            # Ignore errors during camera control
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

            print("✓ Viewport cleaned up")

        except Exception as e:
            print(f"✗ Cleanup error: {e}")
