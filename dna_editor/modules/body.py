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
