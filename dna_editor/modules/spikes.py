"""
Spike Module - Create surface spike decorations

Generates spikes on creature body surface using constraint-aware placement.
Avoids tentacle and eye attachment points for anatomically-correct placement.

Updated to use attachment points from constraint solver.
"""

from ursina import Entity, Vec3, color as ursina_color
import math
import random
import colorsys
from modules.body import world_to_local_position


def create_spikes(parent, count=15, length=0.2, hue=280, attachment_points=None):
    """
    Create spikes on body surface.

    Args:
        parent: Parent body entity
        count: Number of spikes (0-30)
        length: Spike length
        hue: Color hue (matches body)
        attachment_points: List of AttachmentPoint from constraint solver (preferred method)

    Returns:
        list: Spike entities
    """
    if count == 0:
        return []

    spikes = []
    body_radius = parent.base_scale if hasattr(parent, 'base_scale') else parent.scale_x

    # Spike color (slightly darker than body, more saturated)
    rgb = colorsys.hsv_to_rgb(hue / 360.0, 0.9, 0.5)
    spike_color = ursina_color.rgb(*rgb)

    # NEW METHOD: Use attachment points from constraint solver
    if attachment_points is not None and len(attachment_points) > 0:
        for i, attach_point in enumerate(attachment_points[:count]):
            # Use solved position and normal
            pos = attach_point.position
            normal = attach_point.normal

            # Convert world-space position to local-space coordinates
            local_pos = world_to_local_position(parent, pos)

            # Create spike (stretched cube to simulate cone)
            spike = Entity(
                model='cube',
                color=spike_color,
                scale=(length * 0.15, length, length * 0.15),  # Thin spike
                parent=parent,
                position=(local_pos.x, local_pos.y, local_pos.z)
            )

            # Point spike along surface normal (outward)
            # Convert look_at target to local space as well
            world_target = pos + normal * length
            local_target = world_to_local_position(parent, world_target)
            spike.look_at(local_target)

            # Slight random rotation variance for organic look
            spike.rotation_z += random.uniform(-15, 15)

            spikes.append(spike)

        return spikes

    # LEGACY METHOD: Fibonacci sphere distribution (for backward compatibility)
    for i in range(count):
        # Random position on sphere surface using spherical coordinates
        # Use Fibonacci sphere distribution for even distribution
        phi = math.acos(1 - 2 * (i + 0.5) / count)
        theta = math.pi * (1 + 5**0.5) * i

        # Convert spherical to cartesian
        x = body_radius * math.cos(theta) * math.sin(phi)
        y = body_radius * math.sin(theta) * math.sin(phi)
        z = body_radius * math.cos(phi)

        # Calculate spike direction (outward from center)
        direction = Vec3(x, y, z).normalized()

        # Create spike (stretched cube to simulate cone)
        spike = Entity(
            model='cube',
            color=spike_color,
            scale=(length * 0.15, length, length * 0.15),  # Thin spike
            parent=parent,
            position=(x, y, z)
        )

        # Point spike outward
        # Calculate rotation to point in direction
        spike.look_at(parent.position + direction * (body_radius + length))

        # Slight random rotation variance for organic look
        spike.rotation_z += random.uniform(-15, 15)

        spikes.append(spike)

    return spikes
