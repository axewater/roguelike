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
        self.sky_layers = []
        self.shadow_layers = []
        self.lighting = {}

        # Camera orbit state
        self.camera_angle = 0
        self.camera_height = 2
        self.camera_distance = 6

        # Ursina module references (set in _init_ursina)
        self.Entity = None
        self.camera = None
        self.color = None
        self.held_keys = None
        self.mouse = None
        self.window = None
        self.math = None

        self._init_ursina()

    def _init_ursina(self):
        """Initialize Ursina application and scene."""
        try:
            # Suppress Panda3D verbose logging
            import os
            import sys
            from io import StringIO
            import warnings

            # Suppress all warnings (including PNG iCCP warnings)
            warnings.filterwarnings('ignore')

            # Set Panda3D config via environment variables (more reliable)
            os.environ['PANDA_PRC_DIR'] = ''
            os.environ['PANDA_PRC_PATH'] = ''

            # Load custom config that suppresses logging
            from panda3d.core import loadPrcFileData
            loadPrcFileData('', '''
                notify-level error
                notify-level-pnmimage error
                default-directnotify-level error
                paste-emit-keystrokes 0
            ''')

            # Redirect stdout/stderr to suppress remaining output
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = StringIO()
            sys.stderr = StringIO()

            # Import Ursina (will use our config)
            from ursina import Ursina, Entity, camera, Sky, color, held_keys, mouse
            from ursina import AmbientLight, DirectionalLight, PointLight
            from ursina import window
            import math

            # Restore stdout/stderr after imports
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            # Store module references as instance attributes
            self.Entity = Entity
            self.camera = camera
            self.Sky = Sky
            self.color = color
            self.held_keys = held_keys
            self.mouse = mouse
            self.AmbientLight = AmbientLight
            self.DirectionalLight = DirectionalLight
            self.PointLight = PointLight
            self.window = window
            self.math = math

            # Suppress Ursina initialization output temporarily
            sys.stdout = StringIO()
            sys.stderr = StringIO()

            # Create Ursina app
            self.ursina_app = Ursina(
                title="DNA Editor - 3D Preview",
                borderless=False,
                fullscreen=False,
                size=(900, 700),
                position=(400, 50)
            )

            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

            # Set window background
            self.window.color = self.color.rgb(0.05, 0.05, 0.1)

            # Create scene
            self._create_scene()

            # Set up camera with orbit position
            self.camera.position = (0, self.camera_height, -self.camera_distance)
            self.camera.look_at((0, 0, 0))
            self.camera.fov = 60

            # Start animation timer
            self.timer = QTimer()
            self.timer.timeout.connect(self._update_animation)
            self.timer.start(16)  # ~60 FPS

        except Exception as e:
            print(f"ERROR: Failed to initialize Ursina: {e}")
            import traceback
            traceback.print_exc()

    def _create_scene(self):
        """Create scene elements (ground, sky, lighting)."""
        # Import constants
        from ..core.constants import (
            GROUND_Y, SHADOW_Y, GROUND_COLOR,
            SHADOW_LAYERS, SHADOW_BASE_SIZE, SHADOW_SIZE_STEP,
            SHADOW_BASE_OPACITY, SHADOW_OPACITY_STEP,
            SKY_GRADIENT_BOTTOM, SKY_GRADIENT_TOP
        )

        # Ground (positioned below tentacles)
        self.ground = self.Entity(
            model='plane',
            scale=20,
            color=self.color.rgb(*GROUND_COLOR),
            position=(0, GROUND_Y, 0)
        )

        # Gradient sky using multiple colored layers for smooth transition
        # Create 5 layers from dark (bottom) to light (top)
        self.sky_layers = []
        num_layers = 5
        sky_radius = 500

        for i in range(num_layers):
            # Interpolate between bottom and top colors
            t = i / (num_layers - 1)  # 0.0 to 1.0
            layer_color = tuple(
                SKY_GRADIENT_BOTTOM[j] + t * (SKY_GRADIENT_TOP[j] - SKY_GRADIENT_BOTTOM[j])
                for j in range(3)
            )

            # Position layers vertically (bottom to top)
            y_offset = (i - num_layers/2) * 200  # Spread layers vertically

            # Create semi-transparent layer
            layer = self.Entity(
                model='sphere',
                scale=sky_radius - i * 2,  # Slightly smaller for each layer
                position=(0, y_offset, 0),
                color=self.color.rgb(*layer_color),
                double_sided=True,
                unlit=True,
                alpha=0.3 + (i * 0.15)  # More opaque toward top
            )
            self.sky_layers.append(layer)

        # Add base solid sky behind everything
        self.sky = self.Entity(
            model='sphere',
            scale=sky_radius + 10,
            color=self.color.rgb(*SKY_GRADIENT_BOTTOM),
            double_sided=True,
            unlit=True
        )

        # 3-point lighting system
        self.lighting = {}
        self.lighting['ambient'] = self.AmbientLight(
            color=self.color.rgb(0.2, 0.2, 0.25),
            intensity=0.2
        )

        self.lighting['key'] = self.DirectionalLight(
            position=(5, 8, 3),
            rotation=(50, -35, 0),
            color=self.color.rgb(1.0, 0.98, 0.94),
            intensity=1.5
        )

        self.lighting['fill'] = self.DirectionalLight(
            position=(-3, 4, -2),
            rotation=(120, 45, 0),
            color=self.color.rgb(0.7, 0.75, 0.85),
            intensity=0.6
        )

        self.lighting['rim'] = self.DirectionalLight(
            position=(-2, 3, -5),
            rotation=(150, 20, 0),
            color=self.color.rgb(0.6, 0.7, 1.0),
            intensity=0.8
        )

        self.lighting['point'] = self.PointLight(
            position=(0, 2, 0),
            color=self.color.rgb(1.0, 0.95, 0.9),
            intensity=0.4
        )

        # Layered circle shadow for soft shadow effect
        # Create multiple circular layers: largest/lightest to smallest/darkest
        self.shadow_layers = []
        for i in range(SHADOW_LAYERS):
            # Calculate size (largest to smallest)
            layer_size = SHADOW_BASE_SIZE - (i * SHADOW_SIZE_STEP)

            # Calculate opacity (lightest for largest, darkest for smallest)
            # Reverse the opacity so: largest circle = most transparent, smallest = darkest
            layer_opacity = SHADOW_BASE_OPACITY - ((SHADOW_LAYERS - 1 - i) * SHADOW_OPACITY_STEP)
            layer_opacity = max(5, layer_opacity)  # Minimum opacity of 5

            # Create circular shadow layer (sphere scaled very flat)
            shadow_layer = self.Entity(
                model='sphere',
                scale=(layer_size, 0.01, layer_size),  # Very flat sphere = circle
                color=self.color.rgba(0, 0, 0, layer_opacity),
                position=(0, SHADOW_Y + i * 0.001, 0),  # Slight offset to prevent z-fighting
                unlit=True
            )
            self.shadow_layers.append(shadow_layer)

    def rebuild_creature(self, num_tentacles, segments, algorithm, params, thickness_base, taper_factor,
                        branch_depth=0, branch_count=1, body_scale=1.2, tentacle_color=(0.6, 0.3, 0.7),
                        hue_shift=0.1, anim_speed=2.0, wave_amplitude=0.05, pulse_speed=1.5, pulse_amount=0.05):
        """
        Rebuild creature with new parameters.

        Args:
            num_tentacles: Number of tentacles
            segments: Segments per tentacle
            algorithm: 'bezier' or 'fourier'
            params: Algorithm parameters dict
            thickness_base: Base thickness
            taper_factor: Taper factor
            branch_depth: Maximum branching depth
            branch_count: Number of child branches per tentacle
            body_scale: Body sphere scale
            tentacle_color: Base tentacle color (RGB tuple 0-1)
            hue_shift: Color variation between tentacles
            anim_speed: Animation wave speed
            wave_amplitude: Wave motion intensity
            pulse_speed: Body pulse breathing speed
            pulse_amount: Body pulse expansion amount
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
                taper_factor=taper_factor,
                branch_depth=branch_depth,
                branch_count=branch_count,
                body_scale=body_scale,
                tentacle_color=tentacle_color,
                hue_shift=hue_shift,
                anim_speed=anim_speed,
                wave_amplitude=wave_amplitude,
                pulse_speed=pulse_speed,
                pulse_amount=pulse_amount
            )

        except Exception as e:
            print(f"ERROR: Failed to rebuild creature: {e}")
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
            # Import constants for limits
            from ..core.constants import (
                MIN_CAMERA_DISTANCE, MAX_CAMERA_DISTANCE,
                MIN_CAMERA_HEIGHT, MAX_CAMERA_HEIGHT
            )

            # Mouse drag to orbit (Ursina uses held_keys for mouse buttons)
            if self.held_keys['left mouse']:
                self.camera_angle += self.mouse.velocity[0] * 200
                self.camera_height += self.mouse.velocity[1] * 5

            # Clamp camera height
            self.camera_height = max(MIN_CAMERA_HEIGHT, min(MAX_CAMERA_HEIGHT, self.camera_height))

            # Scroll to zoom (Ursina uses held_keys for scroll events)
            if self.held_keys['scroll up']:
                self.camera_distance -= 0.5
            if self.held_keys['scroll down']:
                self.camera_distance += 0.5
            self.camera_distance = max(MIN_CAMERA_DISTANCE, min(MAX_CAMERA_DISTANCE, self.camera_distance))

            # Calculate camera position using orbit math
            angle_rad = self.math.radians(self.camera_angle)
            cam_x = self.camera_distance * self.math.sin(angle_rad)
            cam_z = -self.camera_distance * self.math.cos(angle_rad)

            # Update camera position and look at creature center
            self.camera.position = (cam_x, self.camera_height, cam_z)
            self.camera.look_at((0, 0, 0))

            # Reset camera (R key)
            if self.held_keys['r']:
                self.camera_angle = 0
                self.camera_height = 2
                self.camera_distance = 6
                self.held_keys['r'] = False

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

        except Exception as e:
            pass  # Silently ignore cleanup errors
