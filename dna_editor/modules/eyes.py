"""
Eye Module - Create eye decorations

Generates eye decorations on creature body using various placement patterns.

Updated to use attachment points from constraint solver for intelligent placement.
Eyes are partially embedded in the surface for a more organic look.
"""

from ursina import Entity, color as ursina_color, Vec3
import math
from modules.body import world_to_local_position


def create_eyes(parent, count=2, pattern='dual', size=0.1, attachment_points=None):
    """
    Create eyes on body surface.

    Args:
        parent: Parent body entity
        count: Number of eyes (0-8)
        pattern: Placement pattern ('none', 'dual', 'spider', 'ring') - DEPRECATED if attachment_points provided
        size: Eye size
        attachment_points: List of AttachmentPoint from constraint solver (preferred method)

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

    # NEW METHOD: Use attachment points from constraint solver
    if attachment_points is not None and len(attachment_points) > 0:
        for i, attach_point in enumerate(attachment_points[:count]):
            # Use the embedded position (already calculated by constraint solver)
            pos = attach_point.position
            normal = attach_point.normal

            # Convert world-space position to local-space coordinates
            local_pos = world_to_local_position(parent, pos)

            # Eye white
            eye = Entity(
                model='sphere',
                color=eye_color,
                scale=size,
                parent=parent,
                position=(local_pos.x, local_pos.y, local_pos.z)
            )

            # Pupil - positioned along surface normal (relative to eye, not parent)
            pupil_offset = normal * (size * 0.3)
            pupil = Entity(
                model='sphere',
                color=pupil_color,
                scale=size * 0.5,
                parent=eye,
                position=(pupil_offset.x, pupil_offset.y, pupil_offset.z)
            )

            eyes.append(eye)

        return eyes

    # LEGACY METHOD: Pattern-based placement (for backward compatibility)

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
