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

    # Hunched body (stretched sphere for organic look)
    body = Entity(
        model='sphere',
        color=enemy_color,
        scale=(0.4, 0.5, 0.35),  # Wider, taller, hunched
        parent=goblin,
        position=(0, 0.35, 0)
    )

    # Oversized head (signature goblin feature)
    head = Entity(
        model='sphere',
        color=enemy_color.tint(0.2),  # Slightly lighter
        scale=0.35,
        parent=goblin,
        position=(0, 0.75, 0)  # Adjusted for taller body
    )

    # Left ear (bat-like, positioned OUTSIDE head sphere)
    # Head radius is 0.35, so position at x=-0.38 to clear it
    left_ear = Entity(
        model='sphere',
        color=enemy_color.tint(-0.1),
        scale=(0.08, 0.18, 0.06),  # Stretched sphere for ear shape
        parent=head,
        position=(-0.38, 0.1, -0.05),  # Outside head, slightly back
        rotation=(0, 0, 25)
    )

    # Right ear
    right_ear = Entity(
        model='sphere',
        color=enemy_color.tint(-0.1),
        scale=(0.08, 0.18, 0.06),
        parent=head,
        position=(0.38, 0.1, -0.05),
        rotation=(0, 0, -25)
    )

    # Glowing yellow eyes (positioned ON head surface)
    # Head radius is 0.35, so z=0.37 places eyes just outside surface
    left_eye = Entity(
        model='sphere',
        color=ursina_color.rgb(255, 255, 0),
        scale=(0.09, 0.09, 0.04),  # Slightly protruding
        parent=head,
        position=(-0.1, 0.05, 0.37),
        unlit=True  # Emissive glow effect
    )

    # Right eye
    right_eye = Entity(
        model='sphere',
        color=ursina_color.rgb(255, 255, 0),
        scale=(0.09, 0.09, 0.04),
        parent=head,
        position=(0.1, 0.05, 0.37),
        unlit=True
    )

    # Left shoulder joint
    left_shoulder = Entity(
        model='sphere',
        color=enemy_color.tint(-0.08),
        scale=0.18,
        parent=body,
        position=(-0.45, 0.2, 0)  # At body edge
    )

    # Right shoulder joint
    right_shoulder = Entity(
        model='sphere',
        color=enemy_color.tint(-0.08),
        scale=0.18,
        parent=body,
        position=(0.45, 0.2, 0)  # At body edge
    )

    # Left arm (4x original size)
    # Body X radius is 0.4, so position at x=-0.5 to clear it
    left_arm = Entity(
        model='sphere',
        color=enemy_color.tint(-0.05),
        scale=(0.48, 1.0, 0.48),  # 4x larger, stretched vertically
        parent=body,
        position=(-0.7, 0.0, 0),  # Further out, hangs down
        rotation=(0, 0, 15)
    )

    # Right arm (4x original size)
    right_arm = Entity(
        model='sphere',
        color=enemy_color.tint(-0.05),
        scale=(0.48, 1.0, 0.48),
        parent=body,
        position=(0.7, 0.0, 0),  # Further out, hangs down
        rotation=(0, 0, -15)
    )

    # Left hip joint
    left_hip = Entity(
        model='sphere',
        color=enemy_color.tint(-0.12),
        scale=0.2,
        parent=body,
        position=(-0.2, -0.5, 0)  # At body bottom
    )

    # Right hip joint
    right_hip = Entity(
        model='sphere',
        color=enemy_color.tint(-0.12),
        scale=0.2,
        parent=body,
        position=(0.2, -0.5, 0)  # At body bottom
    )

    # Left leg (4x original size)
    # Body Y radius is 0.5, bottom at y=-0.5, so position at y=-0.65 to clear it
    left_leg = Entity(
        model='sphere',
        color=enemy_color.tint(-0.1),
        scale=(0.6, 0.8, 0.6),  # 4x larger
        parent=body,
        position=(-0.2, -1.0, 0)  # Below body, adjusted for larger size
    )

    # Right leg (4x original size)
    right_leg = Entity(
        model='sphere',
        color=enemy_color.tint(-0.1),
        scale=(0.6, 0.8, 0.6),  # 4x larger
        parent=body,
        position=(0.2, -1.0, 0)  # Below body, adjusted for larger size
    )

    # Crude club weapon in right "hand" (positioned away from body)
    club_handle = Entity(
        model='sphere',
        color=ursina_color.rgb(80, 60, 40),
        scale=(0.05, 0.3, 0.05),  # Thin stretched sphere
        parent=right_arm,
        position=(0.1, -0.15, 0.15),  # Forward and down from arm
        rotation=(45, 0, -20)
    )

    # Club head (larger, more menacing)
    club_head = Entity(
        model='sphere',
        color=ursina_color.rgb(60, 40, 20),
        scale=(0.1, 0.12, 0.1),  # Slightly stretched
        parent=club_handle,
        position=(0, -0.18, 0)
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
