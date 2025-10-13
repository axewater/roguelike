"""
Boots 3D model - Footwear equipment with rarity variants

Procedurally generated 3D model using Ursina primitives.
"""

from ursina import Entity, Vec3, color as ursina_color
import constants as c
from graphics3d.utils import rgb_to_ursina_color


def create_boots_3d(position: Vec3, rarity: str) -> Entity:
    """
    Create a 3D boots model with rarity-based appearance

    Args:
        position: 3D world position
        rarity: Item rarity (common, uncommon, rare, epic, legendary)

    Returns:
        Entity: Boots 3D model
    """
    # Container entity (invisible parent)
    boots = Entity(position=position)

    # Rarity-based colors and materials
    if rarity == c.RARITY_COMMON:
        boot_color = rgb_to_ursina_color(100, 60, 30)  # Brown leather
        accent_color = rgb_to_ursina_color(80, 50, 25)  # Dark brown
        has_glow = False
    elif rarity == c.RARITY_UNCOMMON:
        boot_color = rgb_to_ursina_color(80, 80, 90)  # Gray leather
        accent_color = rgb_to_ursina_color(120, 120, 130)  # Light gray
        has_glow = False
    elif rarity == c.RARITY_RARE:
        boot_color = rgb_to_ursina_color(100, 130, 200)  # Blue leather
        accent_color = rgb_to_ursina_color(150, 150, 150)  # Silver buckles
        has_glow = False
    elif rarity == c.RARITY_EPIC:
        boot_color = rgb_to_ursina_color(150, 50, 200)  # Purple
        accent_color = rgb_to_ursina_color(220, 180, 100)  # Gold buckles
        has_glow = True
        glow_color = rgb_to_ursina_color(200, 100, 255)
    else:  # LEGENDARY
        boot_color = rgb_to_ursina_color(50, 50, 80)  # Dark mythic
        accent_color = rgb_to_ursina_color(255, 215, 0)  # Bright gold
        has_glow = True
        glow_color = rgb_to_ursina_color(100, 200, 255)

    # Glow for epic/legendary
    if has_glow:
        glow = Entity(
            model='sphere',
            color=glow_color,
            scale=0.3,
            parent=boots,
            position=(0, 0, 0),
            alpha=0.3,
            unlit=True
        )

    # Left boot
    left_boot = Entity(
        model='cube',
        color=boot_color,
        scale=(0.12, 0.15, 0.18),
        parent=boots,
        position=(-0.1, -0.05, 0),
        rotation=(0, -10, 0)  # Slight outward angle
    )

    # Left boot toe
    left_toe = Entity(
        model='cube',
        color=boot_color.tint(-0.1),
        scale=(0.1, 0.12, 0.08),
        parent=left_boot,
        position=(0, 0, 0.13)
    )

    # Right boot
    right_boot = Entity(
        model='cube',
        color=boot_color,
        scale=(0.12, 0.15, 0.18),
        parent=boots,
        position=(0.1, -0.05, 0),
        rotation=(0, 10, 0)  # Slight outward angle
    )

    # Right boot toe
    right_toe = Entity(
        model='cube',
        color=boot_color.tint(-0.1),
        scale=(0.1, 0.12, 0.08),
        parent=right_boot,
        position=(0, 0, 0.13)
    )

    # Accent details (buckles/straps) for uncommon+
    if rarity != c.RARITY_COMMON:
        # Left boot buckle
        left_buckle = Entity(
            model='cube',
            color=accent_color,
            scale=(0.13, 0.03, 0.02),
            parent=left_boot,
            position=(0, 0.05, 0.09)
        )

        # Right boot buckle
        right_buckle = Entity(
            model='cube',
            color=accent_color,
            scale=(0.13, 0.03, 0.02),
            parent=right_boot,
            position=(0, 0.05, 0.09)
        )

    # Store animation state
    boots.float_time = 0.0
    boots.rotation_speed = 50.0

    return boots
