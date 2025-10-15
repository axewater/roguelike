"""
Camera controller - handles orbital camera movement and zoom.
"""

from ursina import camera, held_keys, mouse, Vec3
import math
from ..core.constants import (
    DEFAULT_CAMERA_DISTANCE, DEFAULT_CAMERA_HEIGHT, DEFAULT_CAMERA_ANGLE,
    MIN_CAMERA_DISTANCE, MAX_CAMERA_DISTANCE,
    MIN_CAMERA_HEIGHT, MAX_CAMERA_HEIGHT
)


class CameraController:
    """Handles orbital camera controls and positioning."""

    def __init__(self):
        """Initialize camera controller with default position."""
        self.camera_angle = DEFAULT_CAMERA_ANGLE
        self.camera_height = DEFAULT_CAMERA_HEIGHT
        self.camera_distance = DEFAULT_CAMERA_DISTANCE

        # Set initial camera position
        camera.position = Vec3(0, self.camera_height, -self.camera_distance)
        camera.look_at(Vec3(0, 0, 0))
        print(f"Camera initialized at: {camera.position}, looking at origin")

    def update(self):
        """Update camera position based on input."""
        # Update camera orbit with mouse drag
        if held_keys['left mouse']:
            self.camera_angle += mouse.velocity[0] * 200
            self.camera_height += mouse.velocity[1] * 5

        self.camera_height = max(MIN_CAMERA_HEIGHT, min(MAX_CAMERA_HEIGHT, self.camera_height))

        # Zoom with scroll
        if held_keys['scroll up']:
            self.camera_distance -= 0.5
        if held_keys['scroll down']:
            self.camera_distance += 0.5
        self.camera_distance = max(MIN_CAMERA_DISTANCE, min(MAX_CAMERA_DISTANCE, self.camera_distance))

        # Calculate camera position
        angle_rad = math.radians(self.camera_angle)
        cam_x = self.camera_distance * math.sin(angle_rad)
        cam_z = -self.camera_distance * math.cos(angle_rad)

        camera.position = Vec3(cam_x, self.camera_height, cam_z)
        camera.look_at((0, 0, 0))

    def reset(self):
        """Reset camera to default position."""
        self.camera_angle = DEFAULT_CAMERA_ANGLE
        self.camera_height = DEFAULT_CAMERA_HEIGHT
        self.camera_distance = DEFAULT_CAMERA_DISTANCE
        print("Camera reset")

    def handle_reset_key(self):
        """Check for reset key press."""
        if held_keys['r']:
            self.reset()
            held_keys['r'] = False
