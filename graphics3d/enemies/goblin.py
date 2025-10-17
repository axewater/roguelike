"""
Goblin 3D model - Small wicked trickster with hunched posture

Procedurally generated 3D model using Ursina primitives.
"""

from ursina import Entity, Vec3, color as ursina_color
import math


def create_goblin_3d(position: Vec3, enemy_color: ursina_color) -> Entity:
    """
    Create a 3D goblin model with detailed accessories and clothing

    Args:
        position: 3D world position
        enemy_color: Base color for the goblin (green)

    Returns:
        Entity: Goblin model with all child entities
    """
    # Container entity (invisible parent)
    goblin = Entity(position=position)

    # Define goblin colors (using 0-1 float scale, divide by 255)
    skin_color = ursina_color.rgb(85/255, 110/255, 70/255)  # Muddy green skin
    skin_dark = ursina_color.rgb(70/255, 90/255, 55/255)  # Darker green for shadows
    skin_light = ursina_color.rgb(100/255, 125/255, 85/255)  # Lighter green for highlights
    leather_color = ursina_color.rgb(80/255, 60/255, 40/255)  # Brown leather
    rag_color = ursina_color.rgb(85/255, 70/255, 55/255)  # Dirty brown rags (lighter)
    tooth_color = ursina_color.rgb(200/255, 190/255, 150/255)  # Dirty yellow teeth
    claw_color = ursina_color.rgb(180/255, 180/255, 160/255)  # Gray claws
    wood_color = ursina_color.rgb(100/255, 75/255, 45/255)  # Dark wood (lighter)
    bone_color = ursina_color.rgb(220/255, 210/255, 190/255)  # Bone/ivory

    # Hunched body (stretched sphere for organic look)
    body = Entity(
        model='sphere',
        color=skin_color,
        scale=(0.4, 0.5, 0.35),  # Wider, taller, hunched
        parent=goblin,
        position=(0, 0.35, 0)
    )

    # Oversized head (signature goblin feature)
    head = Entity(
        model='sphere',
        color=skin_light,  # Slightly lighter
        scale=0.35,
        parent=goblin,
        position=(0, 0.75, 0)  # Adjusted for taller body
    )

    # Pointed left ear
    left_ear = Entity(
        model='cube',
        color=skin_color,
        scale=(0.08, 0.15, 0.05),
        parent=head,
        position=(-0.25, 0.1, 0),
        rotation=(0, 0, -20)  # Angled outward
    )

    # Pointed right ear
    right_ear = Entity(
        model='cube',
        color=skin_color,
        scale=(0.08, 0.15, 0.05),
        parent=head,
        position=(0.25, 0.1, 0),
        rotation=(0, 0, 20)  # Angled outward
    )

    # Left tusk/tooth
    left_tusk = Entity(
        model='cube',
        color=tooth_color,
        scale=(0.04, 0.08, 0.04),
        parent=head,
        position=(-0.08, -0.1, 0.15),
        rotation=(15, 0, 0)  # Angled up
    )

    # Right tusk/tooth
    right_tusk = Entity(
        model='cube',
        color=tooth_color,
        scale=(0.04, 0.08, 0.04),
        parent=head,
        position=(0.08, -0.1, 0.15),
        rotation=(15, 0, 0)  # Angled up
    )

    # Ragged vest/torso covering (larger and protruding)
    vest = Entity(
        model='cube',
        color=rag_color,
        scale=(0.45, 0.45, 0.3),
        parent=body,
        position=(0, 0.05, 0.05)  # Stick out more
    )

    # Left shoulder joint
    left_shoulder = Entity(
        model='sphere',
        color=skin_dark,
        scale=0.18,
        parent=body,
        position=(-0.45, 0.2, 0)  # At body edge
    )

    # Right shoulder joint
    right_shoulder = Entity(
        model='sphere',
        color=skin_dark,
        scale=0.18,
        parent=body,
        position=(0.45, 0.2, 0)  # At body edge
    )

    # Left arm (thinner and 15% shorter)
    left_arm = Entity(
        model='sphere',
        color=skin_color,
        scale=(0.24, 0.85, 0.24),  # 50% thinner, 15% shorter
        parent=body,
        position=(-0.7, 0.0, 0),  # Further out, hangs down
        rotation=(0, 0, 15)
    )

    # Left hand (clawed)
    left_hand = Entity(
        model='sphere',
        color=skin_dark,
        scale=(0.15, 0.15, 0.15),
        parent=body,
        position=(-0.8, -0.35, 0)
    )

    # Left claws (3 small cubes)
    for i in range(3):
        Entity(
            model='cube',
            color=claw_color,
            scale=(0.03, 0.08, 0.03),
            parent=left_hand,
            position=((-0.05 + i * 0.05), -0.1, 0.08),
            rotation=(20, 0, 0)
        )

    # Right arm (thinner and 15% shorter)
    right_arm = Entity(
        model='sphere',
        color=skin_color,
        scale=(0.24, 0.85, 0.24),  # 50% thinner, 15% shorter
        parent=body,
        position=(0.7, 0.0, 0),  # Further out, hangs down
        rotation=(0, 0, -15)
    )

    # Right hand (clawed)
    right_hand = Entity(
        model='sphere',
        color=skin_dark,
        scale=(0.15, 0.15, 0.15),
        parent=body,
        position=(0.8, -0.35, 0)
    )

    # Right claws (3 small cubes)
    for i in range(3):
        Entity(
            model='cube',
            color=claw_color,
            scale=(0.03, 0.08, 0.03),
            parent=right_hand,
            position=((-0.05 + i * 0.05), -0.1, 0.08),
            rotation=(20, 0, 0)
        )

    # Crude wooden club (parented to body like rogue's daggers, not to hand!)
    # Position it near the right hand at (0.8, -0.35, 0) but sticking forward
    club_handle = Entity(
        model='cube',
        color=wood_color,
        scale=(0.1, 0.55, 0.1),  # Thin handle for taper
        parent=body,  # Parent to body, not hand!
        position=(0.77, -0.45, 0.35),  # Moved closer by ~0.18 (foot width)
        rotation=(-45, 0, 15)  # Angled forward and out
    )

    # Club head (MUCH bigger for heavy taper)
    club_head = Entity(
        model='cube',
        color=ursina_color.rgb(130/255, 95/255, 60/255),  # Much lighter brown
        scale=(0.3, 0.35, 0.3),  # 3x wider than handle!
        parent=club_handle,
        position=(0, -0.38, 0)  # Below handle
    )

    # Debug logging for club visibility
    print("\n=== GOBLIN CLUB DEBUG ===")
    print(f"Right hand position (local): {right_hand.position}")
    print(f"Right hand position (world): {right_hand.world_position}")
    print(f"Right hand scale: {right_hand.scale}")
    print(f"Club handle parent: {club_handle.parent.name if hasattr(club_handle.parent, 'name') else 'body'}")
    print(f"Club handle position (local to body): {club_handle.position}")
    print(f"Club handle position (world): {club_handle.world_position}")
    print(f"Club handle scale: {club_handle.scale}")
    print(f"Club handle rotation: {club_handle.rotation}")
    print(f"Club handle color: {club_handle.color}")
    print(f"Club head position (local): {club_head.position}")
    print(f"Club head position (world): {club_head.world_position}")
    print(f"Club head scale: {club_head.scale}")
    print(f"Club head color: {club_head.color}")
    print(f"Body position (world): {body.world_position}")
    print(f"Body scale: {body.scale}")

    # Calculate distance from body edge
    body_right_edge = 0.4  # body x scale
    club_beyond_body = club_handle.position.x - body_right_edge
    print(f"Body right edge: {body_right_edge:.3f}")
    print(f"Club x position: {club_handle.position.x:.3f}")
    print(f"Club extends beyond body by: {club_beyond_body:.3f}")
    print("========================\n")

    # Leather belt
    belt = Entity(
        model='cube',
        color=leather_color,
        scale=(0.45, 0.1, 0.3),
        parent=body,
        position=(0, -0.35, 0)
    )

    # Small pouch on belt
    pouch = Entity(
        model='cube',
        color=rag_color,
        scale=(0.12, 0.12, 0.12),
        parent=belt,
        position=(-0.2, -0.08, 0.05)
    )

    # Ragged loincloth (more visible)
    loincloth = Entity(
        model='cube',
        color=ursina_color.rgb(75/255, 65/255, 55/255),  # Slightly lighter brown
        scale=(0.35, 0.3, 0.08),  # Bigger and thicker
        parent=body,
        position=(0, -0.5, 0.15)  # Further forward
    )

    # Left hip joint
    left_hip = Entity(
        model='sphere',
        color=skin_dark,
        scale=0.2,
        parent=body,
        position=(-0.2, -0.5, 0)  # At body bottom
    )

    # Right hip joint
    right_hip = Entity(
        model='sphere',
        color=skin_dark,
        scale=0.2,
        parent=body,
        position=(0.2, -0.5, 0)  # At body bottom
    )

    # Left leg (skinny)
    left_leg = Entity(
        model='sphere',
        color=skin_color,
        scale=(0.25, 0.7, 0.25),  # Thin legs
        parent=body,
        position=(-0.2, -1.0, 0)  # Below body, adjusted for larger size
    )

    # Left foot (big goblin foot)
    left_foot = Entity(
        model='cube',
        color=skin_dark,
        scale=(0.18, 0.12, 0.28),
        parent=body,
        position=(-0.2, -1.42, 0.05)
    )

    # Right leg (skinny)
    right_leg = Entity(
        model='sphere',
        color=skin_color,
        scale=(0.25, 0.7, 0.25),  # Thin legs
        parent=body,
        position=(0.2, -1.0, 0)  # Below body, adjusted for larger size
    )

    # Right foot (big goblin foot)
    right_foot = Entity(
        model='cube',
        color=skin_dark,
        scale=(0.18, 0.12, 0.28),
        parent=body,
        position=(0.2, -1.42, 0.05)
    )

    # Bone necklace (center)
    necklace_cord = Entity(
        model='cube',
        color=leather_color,
        scale=(0.3, 0.03, 0.03),
        parent=body,
        position=(0, 0.45, 0.15)
    )

    # Bone pendant on necklace
    bone_pendant = Entity(
        model='cube',
        color=bone_color,
        scale=(0.08, 0.12, 0.05),
        parent=necklace_cord,
        position=(0, -0.08, 0)
    )

    # Store animation state in goblin entity
    goblin.idle_time = 0.0
    goblin.head_ref = head  # Reference for animation

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
