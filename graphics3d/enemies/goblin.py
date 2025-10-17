"""
Goblin 3D model - Small wicked trickster with hunched posture

Procedurally generated 3D model using Ursina primitives.
"""

from ursina import Entity, Vec3, color as ursina_color, color
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

    # Eye positioning constants (calculated from head radius 0.35)
    HEAD_RADIUS = 0.35
    EYE_SPACING = 0.12  # Half-distance between eyes (34% of radius)
    EYE_HEIGHT = 0.08   # Above head center (23% of radius)
    EYE_FORWARD = 0.25  # Z-depth forward from head center (71% of radius)
    # Validation: sqrt(0.12² + 0.08² + 0.25²) ≈ 0.28 < 0.35 (eyes slightly inset)

    # Left eye (white sclera)
    left_eye = Entity(
        model='sphere',
        color=color.white,
        scale=0.08,
        parent=head,  # Parent to head for animation
        position=(-EYE_SPACING, EYE_HEIGHT, EYE_FORWARD)
    )

    # Left pupil (dark iris)
    left_pupil = Entity(
        model='sphere',
        color=color.black,
        scale=0.04,
        parent=left_eye,
        position=(0, 0, 0.06)  # Slightly forward on eyeball surface
    )

    # Right eye (white sclera)
    right_eye = Entity(
        model='sphere',
        color=color.white,
        scale=0.08,
        parent=head,  # Parent to head for animation
        position=(EYE_SPACING, EYE_HEIGHT, EYE_FORWARD)
    )

    # Right pupil (dark iris)
    right_pupil = Entity(
        model='sphere',
        color=color.black,
        scale=0.04,
        parent=right_eye,
        position=(0, 0, 0.06)  # Slightly forward on eyeball surface
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

    # Left arm (thinner and 15% shorter)
    # Body X radius is 0.4, so position at x=-0.5 to clear it
    left_arm = Entity(
        model='sphere',
        color=enemy_color.tint(-0.05),
        scale=(0.24, 0.85, 0.24),  # 50% thinner, 15% shorter
        parent=body,
        position=(-0.7, 0.0, 0),  # Further out, hangs down
        rotation=(0, 0, 15)
    )

    # Right arm (thinner and 15% shorter)
    right_arm = Entity(
        model='sphere',
        color=enemy_color.tint(-0.05),
        scale=(0.24, 0.85, 0.24),  # 50% thinner, 15% shorter
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

    # Store animation state in goblin entity
    goblin.idle_time = 0.0
    goblin.head_ref = head  # Reference for animation
    goblin.left_eye_ref = left_eye  # Reference for future eye animations
    goblin.right_eye_ref = right_eye

    return goblin


def update_goblin_animation(goblin: Entity, dt: float):
    """
    Update goblin idle animation (nervous head movement)

    Args:
        goblin: Goblin entity to animate
        dt: Delta time since last frame
    """
    goblin.idle_time += dt

    # Nervous head darting (3.5 Hz)
    head_dart = math.sin(goblin.idle_time * 3.5) * 2.5

    # Apply head dart (subtle rotation)
    if hasattr(goblin, 'head_ref'):
        goblin.head_ref.rotation_y = head_dart
