"""
Eye Module - Create eye decorations

Generates eye decorations on creature body using various placement patterns.
"""

from ursina import Entity, color as ursina_color
import math


def create_eyes(parent, count=2, pattern='dual', size=0.1):
    """
    Create eyes on body surface.

    Args:
        parent: Parent body entity
        count: Number of eyes (0-8)
        pattern: Placement pattern ('none', 'dual', 'spider', 'ring')
        size: Eye size

    Returns:
        list: Eye entities
    """
    if count == 0 or pattern == 'none':
        return []

    eyes = []
    body_radius = parent.base_scale if hasattr(parent, 'base_scale') else parent.scale_x

    # Eye color (dark)
    eye_color = ursina_color.rgb(0.1, 0.1, 0.15)
    pupil_color = ursina_color.rgb(0.8, 0.0, 0.0)  # Red pupils

    if pattern == 'dual':
        # Two eyes on front (forward-facing)
        positions = [
            (-size * 1.5, size * 0.5, body_radius * 0.5),  # Left eye
            (size * 1.5, size * 0.5, body_radius * 0.5),   # Right eye
        ]

        for i, pos in enumerate(positions[:count]):
            # Eye white
            eye = Entity(
                model='sphere',
                color=eye_color,
                scale=size,
                parent=parent,
                position=pos
            )

            # Pupil
            pupil = Entity(
                model='sphere',
                color=pupil_color,
                scale=size * 0.5,
                parent=eye,
                position=(0, 0, size * 0.3)  # Slightly forward
            )

            eyes.append(eye)

    elif pattern == 'spider':
        # Multiple eyes arranged in spider pattern (clustered on front)
        positions = [
            (0, size * 0.8, body_radius * 0.5),           # Top center
            (-size * 1.2, size * 0.3, body_radius * 0.5), # Left top
            (size * 1.2, size * 0.3, body_radius * 0.5),  # Right top
            (-size * 2.0, 0, body_radius * 0.5),          # Far left
            (size * 2.0, 0, body_radius * 0.5),           # Far right
            (-size * 1.2, -size * 0.5, body_radius * 0.5),# Left bottom
            (size * 1.2, -size * 0.5, body_radius * 0.5), # Right bottom
            (0, -size * 0.8, body_radius * 0.5),          # Bottom center
        ]

        for i, pos in enumerate(positions[:count]):
            eye_size = size * (0.8 if i > 1 else 1.0)  # Main eyes bigger
            eye = Entity(
                model='sphere',
                color=eye_color,
                scale=eye_size,
                parent=parent,
                position=pos
            )

            pupil = Entity(
                model='sphere',
                color=pupil_color,
                scale=eye_size * 0.5,
                parent=eye,
                position=(0, 0, eye_size * 0.3)
            )

            eyes.append(eye)

    elif pattern == 'ring':
        # Eyes evenly distributed around body equator
        for i in range(count):
            angle = (360.0 / count) * i
            angle_rad = math.radians(angle)

            x = body_radius * 0.6 * math.cos(angle_rad)
            z = body_radius * 0.6 * math.sin(angle_rad)

            eye = Entity(
                model='sphere',
                color=eye_color,
                scale=size,
                parent=parent,
                position=(x, 0, z)
            )

            # Pupil faces outward
            pupil_offset_x = size * 0.3 * math.cos(angle_rad)
            pupil_offset_z = size * 0.3 * math.sin(angle_rad)

            pupil = Entity(
                model='sphere',
                color=pupil_color,
                scale=size * 0.5,
                parent=eye,
                position=(pupil_offset_x, 0, pupil_offset_z)
            )

            eyes.append(eye)

    return eyes
