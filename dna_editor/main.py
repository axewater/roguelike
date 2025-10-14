"""
DNA Creature Editor - Main Application

Standalone tool for designing tentacle horror creatures.
Combines Ursina 3D preview with parameter controls for real-time creature design.

Usage:
    python3 dna_editor/main.py
"""

from ursina import Ursina, Entity, camera, held_keys, time as ursina_time, mouse
from ursina import color as ursina_color, window, Vec3, Sky, EditorCamera
from creature_builder import CreatureBuilder
from preset_manager import PresetManager
from ui_controls import ControlPanel
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class DNACreatureEditor(Entity):
    """
    Main application controller for DNA Creature Editor.
    """

    def __init__(self):
        super().__init__()

        # Initialize managers
        self.preset_manager = PresetManager()
        self.creature_builder = CreatureBuilder()

        # Create scene
        self._setup_scene()

        # Create UI
        self.control_panel = ControlPanel(
            self.preset_manager,
            on_parameters_changed=self._on_parameters_changed
        )
        self.control_panel.show()

        # Setup camera controls
        self._setup_camera()

        # Build initial creature (first preset or default)
        preset_names = self.preset_manager.get_preset_names()
        if preset_names:
            initial_params = self.preset_manager.load_preset(preset_names[0])
        else:
            initial_params = self.preset_manager.get_default_parameters()

        self.control_panel.current_params = initial_params
        self.creature_builder.build_from_parameters(initial_params)
        self._update_stats()

        # State
        self.camera_orbit_enabled = True
        self.camera_angle = 0
        self.camera_height = 2
        self.camera_distance = 5
        self.show_help = False
        self.help_text_entity = None

        print("\n" + "=" * 60)
        print("DNA CREATURE EDITOR v1.0")
        print("=" * 60)
        print("Controls:")
        print("  Mouse Drag - Orbit camera")
        print("  Scroll - Zoom in/out")
        print("  Arrow Keys - Adjust camera height")
        print("  R - Reset camera")
        print("  H - Toggle help")
        print("  ESC - Quit")
        print("=" * 60)
        print()

    def _setup_scene(self):
        """Create 3D scene with lighting and grid"""
        # Ground grid
        self.ground = Entity(
            model='plane',
            scale=20,
            color=ursina_color.rgb(0.1, 0.1, 0.15),
            position=(0, -1, 0),
            texture='white_cube',
            texture_scale=(20, 20)
        )

        # Sky
        self.sky = Sky(color=ursina_color.rgb(0.05, 0.05, 0.1))

        # Reference grid lines
        grid_size = 10
        for i in range(-grid_size, grid_size + 1, 2):
            # X-axis lines
            Entity(
                model='cube',
                color=ursina_color.rgb(0.2, 0.2, 0.25),
                scale=(0.02, 0.01, grid_size * 2),
                position=(i, -0.99, 0)
            )
            # Z-axis lines
            Entity(
                model='cube',
                color=ursina_color.rgb(0.2, 0.2, 0.25),
                scale=(grid_size * 2, 0.01, 0.02),
                position=(0, -0.99, i)
            )

    def _setup_camera(self):
        """Setup camera position and controls"""
        camera.position = (0, 2, -5)
        camera.look_at((0, 0, 0))
        camera.fov = 60

    def _on_parameters_changed(self, params):
        """Callback when parameters change - rebuild creature"""
        self.creature_builder.build_from_parameters(params)
        self._update_stats()

    def _update_stats(self):
        """Update UI stats display"""
        stats = self.creature_builder.get_creature_stats()
        self.control_panel.update_stats(stats)

    def _update_camera_orbit(self):
        """Update camera orbital motion"""
        # Mouse drag to orbit
        if held_keys['left mouse']:
            self.camera_angle += mouse.velocity[0] * 200
            self.camera_height += mouse.velocity[1] * 5

        # Clamp height
        self.camera_height = max(0.5, min(5, self.camera_height))

        # Scroll to zoom (using held_keys for Ursina 8.2.0+)
        if held_keys['scroll up']:
            self.camera_distance -= 0.5
        if held_keys['scroll down']:
            self.camera_distance += 0.5
        self.camera_distance = max(2, min(15, self.camera_distance))

        # Calculate camera position
        import math
        angle_rad = math.radians(self.camera_angle)
        cam_x = self.camera_distance * math.sin(angle_rad)
        cam_z = -self.camera_distance * math.cos(angle_rad)
        cam_y = self.camera_height

        camera.position = Vec3(cam_x, cam_y, cam_z)
        camera.look_at((0, 0, 0))

    def _reset_camera(self):
        """Reset camera to default position"""
        self.camera_angle = 0
        self.camera_height = 2
        self.camera_distance = 5
        camera.position = (0, 2, -5)
        camera.look_at((0, 0, 0))
        print("Camera reset")

    def _toggle_help(self):
        """Toggle help text display"""
        self.show_help = not self.show_help

        if self.show_help:
            from ursina import Text
            self.help_text_entity = Text(
                text=(
                    "CONTROLS:\n"
                    "Mouse Drag - Orbit camera\n"
                    "Scroll - Zoom in/out\n"
                    "Arrow Keys - Camera height\n"
                    "R - Reset camera\n"
                    "H - Toggle this help\n"
                    "ESC - Quit\n\n"
                    "TIPS:\n"
                    "- Use PREV/NEXT to browse presets\n"
                    "- Click RANDOM for inspiration\n"
                    "- Adjust parameters with +/- buttons\n"
                    "- Higher segment count = smoother tentacles"
                ),
                position=(0.3, 0.3),
                origin=(0, 0),
                scale=0.8,
                background=True,
                color=ursina_color.rgb(0.9, 0.9, 1.0),
                parent=camera.ui
            )
        else:
            if self.help_text_entity:
                from ursina import destroy
                destroy(self.help_text_entity)
                self.help_text_entity = None

    def update(self):
        """Update loop called every frame"""
        dt = ursina_time.dt

        # Update creature animations
        self.creature_builder.update(dt)

        # Update camera
        self._update_camera_orbit()

        # Handle keyboard input
        if held_keys['up arrow']:
            self.camera_height += dt * 2
        if held_keys['down arrow']:
            self.camera_height -= dt * 2

        # Check for key presses (one-time)
        if held_keys['r']:
            self._reset_camera()
            held_keys['r'] = False

        if held_keys['h']:
            self._toggle_help()
            held_keys['h'] = False

        if held_keys['escape']:
            print("Exiting DNA Creature Editor...")
            application.quit()


def main():
    """
    Main entry point for DNA Creature Editor.
    """
    # Create Ursina application
    app = Ursina(
        title="DNA Creature Editor v1.0",
        borderless=False,
        fullscreen=False,
        development_mode=False
    )

    # Set window properties
    window.size = (1600, 900)
    window.position = (100, 50)
    window.color = ursina_color.rgb(0.05, 0.05, 0.1)

    # Create editor
    editor = DNACreatureEditor()

    # Run application
    app.run()


if __name__ == "__main__":
    main()
