"""
Warrior 3D Model - Armored tank with sword and shield

Creates a procedurally generated 3D warrior model using Ursina primitives.
Features: Heavy armor, sword, shield, bulky proportions
"""

from ursina import Entity, Vec3, color


def create_warrior_model(position=Vec3(0, 0, 0), scale=Vec3(1, 1, 1)):
    """
    Create a 3D warrior character model.

    Args:
        position: Vec3 position for the model
        scale: Vec3 scale for the model

    Returns:
        Entity: Parent entity containing all model parts
    """
    # Create parent entity to hold all parts
    warrior = Entity(position=position, scale=scale)

    # Body (main torso) - wide and armored
    body = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(180/255, 60/255, 40/255),  # Red armor
        scale=(0.5, 0.6, 0.3),
        position=(0, 0, 0)
    )

    # Head
    head = Entity(
        parent=warrior,
        model='sphere',
        color=color.rgb(200/255, 160/255, 130/255),  # Skin tone
        scale=(0.25, 0.25, 0.25),
        position=(0, 0.5, 0)
    )

    # Helmet (metal)
    helmet = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(140/255, 140/255, 150/255),  # Steel gray
        scale=(0.28, 0.15, 0.28),
        position=(0, 0.6, 0)
    )

    # Chest plate (armored layer over body)
    chest_plate = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(160/255, 160/255, 170/255),  # Polished steel
        scale=(0.52, 0.5, 0.32),
        position=(0, 0.05, 0.01)
    )

    # Left shoulder pauldron
    left_pauldron = Entity(
        parent=warrior,
        model='sphere',
        color=color.rgb(140/255, 140/255, 150/255),  # Steel
        scale=(0.2, 0.15, 0.2),
        position=(-0.35, 0.25, 0)
    )

    # Right shoulder pauldron
    right_pauldron = Entity(
        parent=warrior,
        model='sphere',
        color=color.rgb(140/255, 140/255, 150/255),  # Steel
        scale=(0.2, 0.15, 0.2),
        position=(0.35, 0.25, 0)
    )

    # Left arm
    left_arm = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(180/255, 60/255, 40/255),
        scale=(0.15, 0.5, 0.15),
        position=(-0.35, 0, 0)
    )

    # Left hand (gripping shield)
    left_hand = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(200/255, 160/255, 130/255),  # Skin tone
        scale=(0.12, 0.15, 0.12),
        position=(-0.35, -0.3, 0)
    )

    # Left gauntlet (armored glove)
    left_gauntlet = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(130/255, 130/255, 140/255),  # Steel
        scale=(0.14, 0.12, 0.14),
        position=(-0.35, -0.35, 0)
    )

    # Right arm (sword arm)
    right_arm = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(180/255, 60/255, 40/255),
        scale=(0.15, 0.5, 0.15),
        position=(0.35, 0, 0)
    )

    # Right hand (gripping sword)
    right_hand = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(200/255, 160/255, 130/255),  # Skin tone
        scale=(0.12, 0.15, 0.12),
        position=(0.35, -0.3, 0)
    )

    # Right gauntlet (armored glove)
    right_gauntlet = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(130/255, 130/255, 140/255),  # Steel
        scale=(0.14, 0.12, 0.14),
        position=(0.35, -0.35, 0)
    )

    # Sword (long blade)
    sword = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(200/255, 200/255, 210/255),  # Silver blade
        scale=(0.08, 0.8, 0.08),
        position=(0.35, 0.05, 0),
        rotation=(0, 0, 0)  # Held upright
    )

    # Sword crossguard
    crossguard = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(120/255, 100/255, 60/255),  # Bronze
        scale=(0.25, 0.05, 0.08),
        position=(0.35, -0.3, 0)
    )

    # Sword hilt
    hilt = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(100/255, 80/255, 50/255),  # Brown leather
        scale=(0.09, 0.2, 0.09),
        position=(0.35, -0.45, 0)
    )

    # Sword pommel
    pommel = Entity(
        parent=warrior,
        model='sphere',
        color=color.rgb(120/255, 100/255, 60/255),  # Bronze
        scale=(0.12, 0.12, 0.12),
        position=(0.35, -0.6, 0)
    )

    # Shield (left arm)
    shield = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(60/255, 120/255, 180/255),  # Blue shield
        scale=(0.35, 0.45, 0.08),
        position=(-0.45, 0, 0.1),
        rotation=(0, 15, 0)
    )

    # Shield boss (center decoration)
    shield_boss = Entity(
        parent=warrior,
        model='sphere',
        color=color.rgb(180/255, 160/255, 50/255),  # Gold
        scale=(0.1, 0.1, 0.05),
        position=(-0.45, 0, 0.15)
    )

    # Legs
    left_leg = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(80/255, 70/255, 60/255),  # Dark brown pants
        scale=(0.2, 0.5, 0.2),
        position=(-0.15, -0.6, 0)
    )

    # Left knee guard
    left_knee_guard = Entity(
        parent=warrior,
        model='sphere',
        color=color.rgb(130/255, 130/255, 140/255),  # Steel
        scale=(0.18, 0.15, 0.18),
        position=(-0.15, -0.55, 0.02)
    )

    right_leg = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(80/255, 70/255, 60/255),
        scale=(0.2, 0.5, 0.2),
        position=(0.15, -0.6, 0)
    )

    # Right knee guard
    right_knee_guard = Entity(
        parent=warrior,
        model='sphere',
        color=color.rgb(130/255, 130/255, 140/255),  # Steel
        scale=(0.18, 0.15, 0.18),
        position=(0.15, -0.55, 0.02)
    )

    # Belt
    belt = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(60/255, 50/255, 40/255),  # Leather belt
        scale=(0.52, 0.1, 0.32),
        position=(0, -0.3, 0)
    )

    return warrior


__all__ = ['create_warrior_model']
