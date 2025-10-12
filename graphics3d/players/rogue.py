"""
Rogue 3D Model - Stealthy assassin with daggers and hood

Creates a procedurally generated 3D rogue model using Ursina primitives.
Features: Dark clothing, dual daggers, hood, lean proportions
"""

from ursina import Entity, Vec3, color


def create_rogue_model(position=Vec3(0, 0, 0), scale=Vec3(1, 1, 1)):
    """
    Create a 3D rogue character model.

    Args:
        position: Vec3 position for the model
        scale: Vec3 scale for the model

    Returns:
        Entity: Parent entity containing all model parts
    """
    # Create parent entity to hold all parts
    rogue = Entity(position=position, scale=scale)

    # Body (lean torso in dark leather)
    body = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(80, 80, 80),  # Dark gray leather
        scale=(0.35, 0.6, 0.25),
        position=(0, 0, 0)
    )

    # Head
    head = Entity(
        parent=rogue,
        model='sphere',
        color=color.rgb(200, 160, 130),  # Skin tone
        scale=(0.2, 0.2, 0.2),
        position=(0, 0.45, 0)
    )

    # Hood (dark, covering head)
    hood = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(50, 50, 60),  # Very dark
        scale=(0.28, 0.25, 0.28),
        position=(0, 0.55, -0.02)
    )

    # Hood shadow (face concealment)
    hood_shadow = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(20, 20, 25),  # Nearly black
        scale=(0.22, 0.12, 0.05),
        position=(0, 0.48, 0.1)
    )

    # Left arm (holding dagger)
    left_arm = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(70, 70, 75),
        scale=(0.12, 0.45, 0.12),
        position=(-0.28, -0.05, 0),
        rotation=(0, 0, -20)  # Slightly angled
    )

    # Right arm (holding dagger)
    right_arm = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(70, 70, 75),
        scale=(0.12, 0.45, 0.12),
        position=(0.28, -0.05, 0),
        rotation=(0, 0, 20)  # Slightly angled
    )

    # Left dagger (blade)
    left_dagger = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(150, 150, 160),  # Steel
        scale=(0.05, 0.35, 0.05),
        position=(-0.35, -0.25, 0.15),
        rotation=(-30, 0, 0)  # Pointed forward
    )

    # Left dagger hilt
    left_hilt = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(40, 40, 45),  # Black leather
        scale=(0.08, 0.12, 0.08),
        position=(-0.35, -0.4, 0.1),
        rotation=(-30, 0, 0)
    )

    # Right dagger (blade)
    right_dagger = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(150, 150, 160),  # Steel
        scale=(0.05, 0.35, 0.05),
        position=(0.35, -0.25, 0.15),
        rotation=(-30, 0, 0)  # Pointed forward
    )

    # Right dagger hilt
    right_hilt = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(40, 40, 45),  # Black leather
        scale=(0.08, 0.12, 0.08),
        position=(0.35, -0.4, 0.1),
        rotation=(-30, 0, 0)
    )

    # Legs (lean and agile)
    left_leg = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(60, 60, 65),  # Dark pants
        scale=(0.15, 0.5, 0.15),
        position=(-0.12, -0.6, 0)
    )

    right_leg = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(60, 60, 65),
        scale=(0.15, 0.5, 0.15),
        position=(0.12, -0.6, 0)
    )

    # Belt with pouches
    belt = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(50, 45, 40),  # Dark leather
        scale=(0.38, 0.08, 0.27),
        position=(0, -0.3, 0)
    )

    # Pouch (left side)
    pouch = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(60, 50, 45),
        scale=(0.12, 0.12, 0.12),
        position=(-0.25, -0.35, 0)
    )

    # Cloak/cape (flowing behind)
    cape = Entity(
        parent=rogue,
        model='cube',
        color=color.rgb(40, 40, 50),  # Very dark blue-gray
        scale=(0.38, 0.6, 0.05),
        position=(0, -0.05, -0.2)
    )

    return rogue


__all__ = ['create_rogue_model']
