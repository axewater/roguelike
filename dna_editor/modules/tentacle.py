"""
Tentacle Module - Create segmented articulated tentacles

Generates flexible tentacle appendages using cylinder chains.
Each segment is connected via parent-child hierarchy for wave animations.

Updated to use attachment points from constraint solver for proper surface placement.
"""

from ursina import Entity, Vec3, color as ursina_color
import math
import colorsys
from modules.body import world_to_local_position


def create_tentacle(parent, length=2.0, segments=10, base_thickness=0.1,
                   angle=0, taper=50, hue=280, attach_height=-0.3,
                   attachment_point=None):
    """
    Create articulated tentacle with tapered segments.

    Args:
        parent: Parent entity (usually the body)
        length: Total tentacle length
        segments: Number of segments (5-15)
        base_thickness: Thickness at base
        angle: Angle around body (0-360 degrees) - DEPRECATED if attachment_point provided
        taper: Taper percentage (0=no taper, 100=point at tip)
        hue: Color hue (should match body)
        attach_height: Height on body to attach (-1 to 1) - DEPRECATED if attachment_point provided
        attachment_point: AttachmentPoint from constraint solver (preferred method)

    Returns:
        dict: {
            'root': root entity,
            'segments': list of segment entities,
            'angle': attachment angle,
            'attachment_point': AttachmentPoint if provided
        }
    """
    # Convert HSV to RGB (slightly darker than body)
    rgb = colorsys.hsv_to_rgb(hue / 360.0, 0.7, 0.4)
    tentacle_color = ursina_color.rgb(*rgb)

    # Use requested segment count (no doubling - keep it simple)
    actual_segments = segments

    # Fixed spacing for sphere chain (simple and reliable)
    # Spacing as fraction of base thickness for consistent overlap
    sphere_spacing = base_thickness * 0.3  # 70% overlap

    # Determine attachment position and orientation
    if attachment_point is not None:
        # Use constraint-solved attachment point (NEW METHOD)
        attach_pos = attachment_point.position
        attach_normal = attachment_point.normal

        # Convert world-space position to local-space coordinates
        # (parent body has scale applied, so we need to account for it)
        local_pos = world_to_local_position(parent, attach_pos)

        # Create root container at attachment point
        tentacle_root = Entity(
            parent=parent,
            position=(local_pos.x, local_pos.y, local_pos.z)
        )

        # Orient tentacle along surface normal (pointing outward)
        # look_at() in Ursina expects world coordinates, NOT local!
        world_target = attach_pos + attach_normal * length
        tentacle_root.look_at(world_target)

    else:
        # Legacy method: Use angle and height (OLD METHOD - for backward compatibility)
        angle_rad = math.radians(angle)
        body_radius = parent.base_scale if hasattr(parent, 'base_scale') else parent.scale_x
        attach_x = body_radius * math.cos(angle_rad)
        attach_z = body_radius * math.sin(angle_rad)

        # Create root container at attachment point
        tentacle_root = Entity(
            parent=parent,
            position=(attach_x, attach_height, attach_z)
        )

    # Create segments as overlapping spheres (ultra-simple fixed spacing)
    segment_entities = []
    current_parent = tentacle_root

    for i in range(actual_segments):
        # SIMPLE: All spheres same size (no tapering for now - get it working first!)
        segment_thickness = base_thickness

        # Convert diameter to radius for positioning (CRITICAL FIX!)
        # Ursina sphere scale is diameter, but position needs radius-based math
        sphere_radius = segment_thickness / 2.0

        # SIMPLE: Fixed position along parent's local X-axis
        # First sphere: half-embedded in body (radius offset)
        # Other spheres: fixed spacing for overlap
        if i == 0:
            sphere_position = (sphere_radius, 0, 0)
        else:
            sphere_position = (sphere_spacing, 0, 0)

        # Create segment as sphere (smooth organic look)
        segment = Entity(
            model='sphere',
            color=tentacle_color,
            scale=segment_thickness,  # This is diameter
            rotation=(0, 0, 0),
            parent=current_parent,
            position=sphere_position
        )

        # Store segment properties for animation
        segment.segment_index = i
        segment.base_thickness = segment_thickness
        segment.segment_radius = sphere_radius

        segment_entities.append(segment)

        # Next segment attaches to this one
        current_parent = segment

    # Return tentacle data structure
    return {
        'root': tentacle_root,
        'segments': segment_entities,
        'angle': angle if attachment_point is None else 0,
        'length': length,
        'base_thickness': base_thickness,
        'attachment_point': attachment_point
    }


def update_tentacle_animation(tentacle_data, time_elapsed, wave_speed=2.0,
                              wave_amplitude=20, phase_offset=0):
    """
    Animate tentacle with wave motion.

    Args:
        tentacle_data: Tentacle dict from create_tentacle()
        time_elapsed: Total elapsed time
        wave_speed: Wave frequency (Hz)
        wave_amplitude: Wave strength (degrees)
        phase_offset: Phase shift for multiple tentacles
    """
    segments = tentacle_data['segments']

    for i, segment in enumerate(segments):
        # Wave propagates from base to tip
        # Each segment has a phase delay based on its index
        phase = time_elapsed * wave_speed + phase_offset + (i * 0.3)
        wave_angle = math.sin(phase) * wave_amplitude

        # Apply rotation to segment (sway side to side)
        segment.rotation_y = wave_angle

        # Add slight twist for more organic motion
        twist_angle = math.sin(phase * 1.3 + i * 0.5) * (wave_amplitude * 0.3)
        segment.rotation_z = twist_angle
