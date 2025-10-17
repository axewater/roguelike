#!/usr/bin/env python3
"""
Enemy Model Viewer - Quick viewer for debugging 3D enemy models

Usage: python3 viewer_enemy_models.py

Controls:
- Left mouse drag: Rotate camera
- Scroll wheel: Zoom in/out
- R: Reset camera
- ESC: Quit
"""

from ursina import Ursina, Entity, Vec3, Text, color as ursina_color, camera, mouse, held_keys, time
import sys
import math

# Import enemy model creators
from graphics3d.enemies.goblin import create_goblin_3d, update_goblin_animation
from graphics3d.enemies.slime import create_slime_3d, update_slime_animation
from graphics3d.enemies.skeleton import create_skeleton_3d, update_skeleton_animation
from graphics3d.enemies.orc import create_orc_3d, update_orc_animation
from graphics3d.enemies.demon import create_demon_3d, update_demon_animation
from graphics3d.enemies.dragon import create_dragon_3d, update_dragon_animation
import constants as c


class OrbitCamera:
    """
    Simple orbit camera controller - adapted from DNA Editor's working implementation.
    Uses Ursina's built-in mouse velocity tracking for smooth rotation.
    """

    def __init__(self, target_position=Vec3(0, 0, 0), distance=12.0, height=2.0):
        self.target = target_position
        self.camera_angle = 0  # Horizontal rotation angle
        self.camera_height = height  # Vertical height
        self.camera_distance = distance  # Distance from target

        # Limits
        self.min_distance = 3.0
        self.max_distance = 25.0
        self.min_height = 0.5
        self.max_height = 8.0

        self.update_camera_position()

    def update_camera_position(self):
        """Update camera position using orbit math - same as DNA Editor"""
        # Calculate camera position using orbit angle
        angle_rad = math.radians(self.camera_angle)
        cam_x = self.camera_distance * math.sin(angle_rad)
        cam_z = -self.camera_distance * math.cos(angle_rad)

        # Update camera position and look at target
        camera.position = self.target + Vec3(cam_x, self.camera_height, cam_z)
        camera.look_at(self.target)

    def update(self):
        """
        Handle camera controls - adapted from DNA Editor's _handle_camera_controls().
        Uses held_keys and mouse.velocity for smooth, working controls.
        """
        # Mouse drag to orbit (use held_keys like DNA Editor does)
        if held_keys['left mouse']:
            # Use mouse.velocity for smooth rotation (automatic delta calculation!)
            self.camera_angle += mouse.velocity[0] * 200  # Horizontal rotation
            self.camera_height += mouse.velocity[1] * 5   # Vertical movement

        # Clamp camera height
        self.camera_height = max(self.min_height, min(self.max_height, self.camera_height))

        # Scroll to zoom (use held_keys like DNA Editor)
        if held_keys['scroll up']:
            self.camera_distance -= 0.5
        if held_keys['scroll down']:
            self.camera_distance += 0.5

        # Clamp distance
        self.camera_distance = max(self.min_distance, min(self.max_distance, self.camera_distance))

        # Update camera position
        self.update_camera_position()

        # Reset camera (R key)
        if held_keys['r']:
            self.camera_angle = 0
            self.camera_height = 2.0
            self.camera_distance = 12.0
            held_keys['r'] = False  # Reset key state


def create_enemy_grid():
    """
    Create all enemy models in a 3x2 grid layout on the ground

    Returns:
        list: List of dicts with enemy data (entity, type, update_func, label, name)
    """
    enemies_data = []

    # Enemy types and their configurations
    enemy_configs = [
        (c.ENEMY_GOBLIN, "Goblin", create_goblin_3d, update_goblin_animation, c.COLOR_ENEMY_GOBLIN),
        (c.ENEMY_SLIME, "Slime", create_slime_3d, update_slime_animation, c.COLOR_ENEMY_SLIME),
        (c.ENEMY_SKELETON, "Skeleton", create_skeleton_3d, update_skeleton_animation, c.COLOR_ENEMY_SKELETON),
        (c.ENEMY_ORC, "Orc", create_orc_3d, update_orc_animation, c.COLOR_ENEMY_ORC),
        (c.ENEMY_DEMON, "Demon", create_demon_3d, update_demon_animation, c.COLOR_ENEMY_DEMON),
        (c.ENEMY_DRAGON, "Dragon", create_dragon_3d, update_dragon_animation, c.COLOR_ENEMY_DRAGON),
    ]

    # Grid layout: 3 columns x 2 rows
    grid_cols = 3
    grid_spacing = 3.0

    for i, (enemy_type, name, create_func, update_func, qcolor) in enumerate(enemy_configs):
        # Calculate grid position (centered around origin)
        col = i % grid_cols
        row = i // grid_cols

        x = (col - 1) * grid_spacing  # -1 to center (cols: -1, 0, 1)
        z = (row - 0.5) * grid_spacing  # -0.5 to center (rows: -0.5, 0.5)
        y = 0  # Place on ground level

        position = Vec3(x, y, z)

        # Convert QColor to Ursina color
        from graphics3d.utils import qcolor_to_ursina_color
        enemy_color = qcolor_to_ursina_color(qcolor)

        # Create enemy model
        enemy_entity = create_func(position, enemy_color)

        # Create label text below the enemy
        label = Text(
            text=name,
            position=(x, -0.8, z),
            scale=2.5,
            color=ursina_color.white,
            origin=(0, 0),
            billboard=True
        )

        enemies_data.append({
            'entity': enemy_entity,
            'type': enemy_type,
            'update_func': update_func,
            'label': label,
            'name': name
        })

    return enemies_data


def create_ground_plane():
    """Create a simple ground plane for spatial reference - like DNA Editor"""
    # Main ground plane
    ground = Entity(
        model='plane',
        scale=20,
        color=ursina_color.rgb(40, 40, 45),
        position=(0, -0.5, 0)
    )

    # Add grid lines for better depth perception
    grid_color = ursina_color.rgb(60, 60, 65)
    line_thickness = 0.02
    grid_range = 10
    grid_spacing = 2

    for i in range(-grid_range, grid_range + 1, grid_spacing):
        # X-axis lines (parallel to X)
        Entity(
            model='cube',
            scale=(20, 0.01, line_thickness),
            color=grid_color,
            position=(0, -0.49, i)
        )
        # Z-axis lines (parallel to Z)
        Entity(
            model='cube',
            scale=(line_thickness, 0.01, 20),
            color=grid_color,
            position=(i, -0.49, 0)
        )

    return ground


# Global variables for update function
orbit_cam = None
enemies = []


def update():
    """
    Global update function - called automatically by Ursina every frame.
    Must be defined at module level for Ursina to find it.
    """
    global orbit_cam, enemies

    if orbit_cam is None:
        return

    # Update camera controls
    orbit_cam.update()

    # Update all enemy animations
    for enemy_data in enemies:
        enemy_data['update_func'](enemy_data['entity'], time.dt)

    # ESC to quit
    if held_keys['escape']:
        print("Exiting viewer...")
        sys.exit(0)


def main():
    """Main entry point for the enemy model viewer"""
    global orbit_cam, enemies

    # Initialize Ursina with simple window settings
    app = Ursina(
        title="Enemy Model Viewer",
        borderless=False,
        fullscreen=False,
        size=(1280, 720),
        vsync=True
    )

    # Set window background color
    from ursina import window
    window.color = ursina_color.rgb(25, 25, 30)

    # Set up camera
    camera.fov = 60
    camera.clip_plane_near = 0.1

    # Create ground plane
    ground = create_ground_plane()

    # Create all enemies in a grid
    print("Loading enemy models...")
    enemies = create_enemy_grid()
    print(f"Loaded {len(enemies)} enemy models")

    # Setup orbit camera (look at center of grid, slightly above ground)
    orbit_cam = OrbitCamera(target_position=Vec3(0, 0.5, 0), distance=12.0, height=2.0)

    # Create controls text (top-left corner)
    controls_text = Text(
        text=(
            "Enemy Model Viewer\n"
            "---------------------\n"
            "Left Mouse Drag: Rotate\n"
            "Scroll Wheel: Zoom\n"
            "R: Reset Camera\n"
            "ESC: Quit"
        ),
        position=(-0.85, 0.45),
        scale=1.2,
        color=ursina_color.rgb(200, 200, 200),
        origin=(-0.5, 0.5),
        background=True
    )

    # Create info text (top-right corner) showing model count
    info_text = Text(
        text=f"{len(enemies)} Enemy Models",
        position=(0.75, 0.45),
        scale=1.5,
        color=ursina_color.rgb(100, 200, 255),
        origin=(0.5, 0.5)
    )

    print("\nViewer ready!")
    print("Controls: Left mouse drag to rotate, scroll to zoom, R to reset, ESC to quit")
    print(f"Camera position: {camera.position}")
    print(f"Camera looking at: {orbit_cam.target}")

    # Run the app (update function will be called automatically)
    app.run()


if __name__ == "__main__":
    main()
