"""
Tentacle Module - Create segmented articulated tentacles

Generates flexible tentacle appendages using cylinder chains.
Each segment is connected via parent-child hierarchy for wave animations.
"""

from ursina import Entity, Vec3, color as ursina_color
import math
import colorsys


def create_tentacle(parent, length=2.0, segments=10, base_thickness=0.1,
                   angle=0, taper=50, hue=280, attach_height=-0.3):
    """
    Create articulated tentacle with tapered segments.

    Args:
        parent: Parent entity (usually the body)
        length: Total tentacle length
        segments: Number of segments (5-15)
        base_thickness: Thickness at base
        angle: Angle around body (0-360 degrees)
        taper: Taper percentage (0=no taper, 100=point at tip)
        hue: Color hue (should match body)
        attach_height: Height on body to attach (-1 to 1)

    Returns:
        dict: {
            'root': root entity,
            'segments': list of segment entities,
            'angle': attachment angle
        }
    """
    # Convert HSV to RGB (slightly darker than body)
    rgb = colorsys.hsv_to_rgb(hue / 360.0, 0.7, 0.4)
    tentacle_color = ursina_color.rgb(*rgb)

    # Calculate segment length
    segment_length = length / segments

    # Calculate attachment position on body surface
    angle_rad = math.radians(angle)
    body_radius = parent.base_scale if hasattr(parent, 'base_scale') else parent.scale_x
    attach_x = body_radius * math.cos(angle_rad)
    attach_z = body_radius * math.sin(angle_rad)

    # Create root container at attachment point
    tentacle_root = Entity(
        parent=parent,
        position=(attach_x, attach_height, attach_z)
    )

    # Create segments (each is child of previous)
    segment_entities = []
    current_parent = tentacle_root

    for i in range(segments):
        # Calculate thickness for this segment (taper from base to tip)
        taper_factor = 1.0 - (i / segments) * (taper / 100.0)
        segment_thickness = base_thickness * taper_factor

        # Create segment (cube stretched to look like cylinder)
        segment = Entity(
            model='cube',
            color=tentacle_color,
            scale=(segment_length, segment_thickness, segment_thickness),
            rotation=(0, 0, 0),
            parent=current_parent,
            position=(segment_length / 2, 0, 0) if i > 0 else (0, 0, 0)
        )

        # Store segment properties for animation
        segment.segment_index = i
        segment.base_thickness = segment_thickness
        segment.segment_length = segment_length

        segment_entities.append(segment)

        # Next segment attaches to end of this one
        current_parent = segment

    # Return tentacle data structure
    return {
        'root': tentacle_root,
        'segments': segment_entities,
        'angle': angle,
        'length': length,
        'base_thickness': base_thickness
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
