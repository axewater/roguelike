"""
Slime 3D model - Gelatinous blob creature

Procedurally generated 3D model using Ursina primitives.
"""

from ursina import Entity, Vec3, color as ursina_color
import math


def create_slime_3d(position: Vec3, enemy_color: ursina_color) -> Entity:
    """
    Create a 3D slime model

    Args:
        position: 3D world position
        enemy_color: Base color for the slime (cyan/teal)

    Returns:
        Entity: Slime model with all child entities
    """
    # Container entity (invisible parent)
    slime = Entity(position=position)

    # Main body (semi-transparent sphere)
    body = Entity(
        model='sphere',
        color=enemy_color,
        scale=(0.5, 0.45, 0.5),  # Slightly flattened sphere
        parent=slime,
        position=(0, 0.3, 0),
        alpha=0.8  # Semi-transparent gelatinous effect
    )

    # Inner core (darker sphere inside)
    core = Entity(
        model='sphere',
        color=enemy_color.tint(-0.4),
        scale=0.25,
        parent=body,
        position=(0, 0, 0),
        alpha=0.6
    )

    # Small bubbles/nuclei floating inside (3 small spheres)
    bubble1 = Entity(
        model='sphere',
        color=enemy_color.tint(0.3),
        scale=0.08,
        parent=body,
        position=(0.1, 0.05, 0.08),
        alpha=0.7
    )

    bubble2 = Entity(
        model='sphere',
        color=enemy_color.tint(0.3),
        scale=0.06,
        parent=body,
        position=(-0.12, -0.05, -0.05),
        alpha=0.7
    )

    bubble3 = Entity(
        model='sphere',
        color=enemy_color.tint(0.3),
        scale=0.05,
        parent=body,
        position=(0.05, -0.1, 0.1),
        alpha=0.7
    )

    # Simple "eyes" (dark spots)
    left_eye = Entity(
        model='sphere',
        color=ursina_color.rgb(20, 20, 40),
        scale=0.08,
        parent=body,
        position=(-0.12, 0.08, 0.2),
        alpha=0.9
    )

    right_eye = Entity(
        model='sphere',
        color=ursina_color.rgb(20, 20, 40),
        scale=0.08,
        parent=body,
        position=(0.12, 0.08, 0.2),
        alpha=0.9
    )

    # Store animation state and references
    slime.idle_time = 0.0
    slime.body_ref = body
    slime.core_ref = core
    slime.base_scale_y = 0.45

    return slime


def update_slime_animation(slime: Entity, dt: float):
    """
    Update slime idle animation (squishing/wobbling movement)

    Args:
        slime: Slime entity to animate
        dt: Delta time since last frame
    """
    slime.idle_time += dt

    # Squish animation (vertical scale oscillation)
    # Frequency: 2 Hz (gentle wobble)
    squish_factor = math.sin(slime.idle_time * 2.0) * 0.15

    if hasattr(slime, 'body_ref'):
        # Squish: scale Y goes from 0.3 to 0.6 (compress/expand)
        new_scale_y = slime.base_scale_y + squish_factor
        # Inverse scale X/Z to maintain volume (squash & stretch)
        inverse_scale_xz = 0.5 + (0.1 * -squish_factor)

        slime.body_ref.scale_y = new_scale_y
        slime.body_ref.scale_x = inverse_scale_xz
        slime.body_ref.scale_z = inverse_scale_xz

    # Core pulses slightly (breathing effect)
    if hasattr(slime, 'core_ref'):
        core_pulse = math.sin(slime.idle_time * 1.5) * 0.03
        slime.core_ref.scale = 0.25 + core_pulse
