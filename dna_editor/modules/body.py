"""
Body Module - Create creature body (sphere or ellipsoid)

Generates the central body that tentacles attach to.
Supports different sizes, colors (HSV hue), and shapes.
"""

from ursina import Entity, color as ursina_color
import colorsys


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

    return body


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
