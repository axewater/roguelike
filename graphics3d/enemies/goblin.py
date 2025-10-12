"""
Goblin 3D model - Small wicked trickster with hunched posture

Procedurally generated 3D model using Ursina primitives.
"""

from ursina import Entity, Vec3, color as ursina_color
import math


def create_goblin_3d(position: Vec3, enemy_color: ursina_color) -> Entity:
    """
    Create a 3D goblin model

    Args:
        position: 3D world position
        enemy_color: Base color for the goblin (green)

    Returns:
        Entity: Goblin model with all child entities
    """
    # Container entity (invisible parent)
    goblin = Entity(position=position)

    # Hunched body (small, lower than head)
    body = Entity(
        model='cube',
        color=enemy_color,
        scale=(0.35, 0.45, 0.3),
        parent=goblin,
        position=(0, 0.3, 0)
    )

    # Oversized head (signature goblin feature)
    head = Entity(
        model='sphere',
        color=enemy_color.tint(0.2),  # Slightly lighter
        scale=0.35,
        parent=goblin,
        position=(0, 0.7, 0)
    )

    # Left ear (bat-like triangular shape)
    left_ear = Entity(
        model='cube',
        color=enemy_color.tint(-0.1),
        scale=(0.05, 0.15, 0.08),
        parent=head,
        position=(-0.25, 0.08, 0),
        rotation=(0, 0, 20)
    )

    # Right ear
    right_ear = Entity(
        model='cube',
        color=enemy_color.tint(-0.1),
        scale=(0.05, 0.15, 0.08),
        parent=head,
        position=(0.25, 0.08, 0),
        rotation=(0, 0, -20)
    )

    # Glowing yellow eyes (left)
    left_eye = Entity(
        model='cube',
        color=ursina_color.rgb(255, 255, 0),
        scale=(0.08, 0.08, 0.05),
        parent=head,
        position=(-0.1, 0.05, 0.18),
        unlit=True  # Emissive glow effect
    )

    # Right eye
    right_eye = Entity(
        model='cube',
        color=ursina_color.rgb(255, 255, 0),
        scale=(0.08, 0.08, 0.05),
        parent=head,
        position=(0.1, 0.05, 0.18),
        unlit=True
    )

    # Crude club weapon in right "hand"
    club_handle = Entity(
        model='cube',
        color=ursina_color.rgb(80, 60, 40),
        scale=(0.04, 0.25, 0.04),
        parent=body,
        position=(0.25, 0, 0.1),
        rotation=(45, 0, 0)
    )

    # Club head
    club_head = Entity(
        model='sphere',
        color=ursina_color.rgb(60, 40, 20),
        scale=0.08,
        parent=club_handle,
        position=(0, 0.15, 0)
    )

    # Store animation state in goblin entity
    goblin.idle_time = 0.0
    goblin.head_ref = head  # Reference for animation
    goblin.left_ear_ref = left_ear
    goblin.right_ear_ref = right_ear
    goblin.left_eye_ref = left_eye
    goblin.right_eye_ref = right_eye

    return goblin


def update_goblin_animation(goblin: Entity, dt: float):
    """
    Update goblin idle animation (twitchy, nervous movement)

    Args:
        goblin: Goblin entity to animate
        dt: Delta time since last frame
    """
    goblin.idle_time += dt

    # Fast ear twitch (8 Hz frequency)
    ear_twitch = math.sin(goblin.idle_time * 8.0) * 3.0

    # Nervous head darting (3.5 Hz)
    head_dart = math.sin(goblin.idle_time * 3.5) * 2.5

    # Eye intensity flicker (6 Hz)
    eye_flicker_factor = abs(math.sin(goblin.idle_time * 6.0))

    # Apply ear twitch (rotate back and forth)
    if hasattr(goblin, 'left_ear_ref'):
        goblin.left_ear_ref.rotation_z = 20 + ear_twitch
        goblin.right_ear_ref.rotation_z = -20 - ear_twitch

    # Apply head dart (subtle rotation)
    if hasattr(goblin, 'head_ref'):
        goblin.head_ref.rotation_y = head_dart

    # Apply eye flicker (brightness via scale)
    if hasattr(goblin, 'left_eye_ref'):
        flicker_scale = 0.08 + (eye_flicker_factor * 0.02)
        goblin.left_eye_ref.scale = (flicker_scale, flicker_scale, 0.05)
        goblin.right_eye_ref.scale = (flicker_scale, flicker_scale, 0.05)
