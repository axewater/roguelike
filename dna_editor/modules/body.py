"""
Body Module - Create creature body (sphere or ellipsoid)

Generates the central body that tentacles attach to.
Supports different sizes, colors (HSV hue), and shapes.

Updated with surface utility methods for constraint-based anatomy system.
"""

from ursina import Entity, color as ursina_color, Vec3
import colorsys
import sys
import os

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from surface_math import BodyGeometry, get_surface_normal, project_to_sphere, project_to_ellipsoid


def create_body(parent, size=0.6, hue=280, shape_type='sphere'):
    """
    Create creature body entity.

    Args:
        parent: Parent entity to attach body to
        size: Body size (0.3 - 1.2)
        hue: Color hue (0-360 degrees, HSV)
        shape_type: 'sphere' or 'ellipsoid'

    Returns:
        Entity: Body entity
    """
    # Convert HSV hue to RGB (saturation=0.7, value=0.6 for organic look)
    rgb = colorsys.hsv_to_rgb(hue / 360.0, 0.7, 0.6)
    body_color = ursina_color.rgb(*rgb)

    # Create body based on shape type
    if shape_type == 'ellipsoid':
        # Ellipsoid is a scaled sphere (wider than tall)
        body = Entity(
            model='sphere',
            color=body_color,
            scale=(size, size * 0.7, size),  # Flatter vertically
            parent=parent,
            position=(0, 0, 0)
        )
    else:  # sphere (default)
        body = Entity(
            model='sphere',
            color=body_color,
            scale=size,
            parent=parent,
            position=(0, 0, 0)
        )

    # Store body properties for animation
    body.base_scale = size
    body.body_hue = hue
    body.shape_type = shape_type

    # Store geometry for surface math
    body.geometry = BodyGeometry(size, shape_type)

    return body


def get_body_geometry(body):
    """
    Get BodyGeometry instance for surface calculations.

    Args:
        body: Body entity

    Returns:
        BodyGeometry: Geometry instance
    """
    if hasattr(body, 'geometry'):
        return body.geometry
    else:
        # Fallback: create from stored properties
        return BodyGeometry(body.base_scale, body.shape_type)


def get_surface_point(body, position):
    """
    Project a point onto the body surface.

    Args:
        body: Body entity
        position: Vec3 or tuple to project

    Returns:
        Vec3: Point on surface
    """
    geometry = get_body_geometry(body)

    if geometry.is_sphere():
        return project_to_sphere(position, (0, 0, 0), geometry.a)
    else:
        return project_to_ellipsoid(position, (0, 0, 0), geometry.get_axes())


def get_body_surface_normal(body, position):
    """
    Get surface normal at a position on the body.

    Args:
        body: Body entity
        position: Vec3 or tuple on surface

    Returns:
        Vec3: Normalized surface normal (pointing outward)
    """
    geometry = get_body_geometry(body)
    return get_surface_normal(position, (0, 0, 0), geometry.get_axes())


def world_to_local_position(body, world_pos):
    """
    Convert a world-space position to local-space coordinates relative to the body.

    This is necessary because Ursina/Panda3D interpret child positions in the parent's
    scaled coordinate system. When the body has scale=0.6, a child at local position
    (1, 0, 0) appears at world offset (0.6, 0, 0) from the parent.

    Args:
        body: Body entity (with scale information)
        world_pos: Vec3 or tuple - position in world space

    Returns:
        Vec3: Position in body's local coordinate space
    """
    if isinstance(world_pos, (tuple, list)):
        world_pos = Vec3(*world_pos)

    # Handle both sphere (uniform scale) and ellipsoid (non-uniform scale)
    if body.shape_type == 'ellipsoid':
        # Ellipsoid has different scales per axis
        local_x = world_pos.x / body.base_scale
        local_y = world_pos.y / (body.base_scale * 0.7)
        local_z = world_pos.z / body.base_scale
        return Vec3(local_x, local_y, local_z)
    else:
        # Sphere has uniform scale
        scale = body.base_scale
        return Vec3(world_pos.x / scale, world_pos.y / scale, world_pos.z / scale)


def update_body_animation(body, time_elapsed, pulse_speed=1.0):
    """
    Update body idle animation (subtle pulsing).

    Args:
        body: Body entity to animate
        time_elapsed: Total elapsed time
        pulse_speed: Pulse frequency multiplier
    """
    import math

    # Subtle pulse (breathing effect)
    pulse = math.sin(time_elapsed * pulse_speed) * 0.03

    if body.shape_type == 'ellipsoid':
        body.scale_x = body.base_scale * (1.0 + pulse)
        body.scale_y = body.base_scale * 0.7 * (1.0 + pulse * 0.5)
        body.scale_z = body.base_scale * (1.0 + pulse)
    else:  # sphere
        body.scale = body.base_scale * (1.0 + pulse)
