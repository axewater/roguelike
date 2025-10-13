"""
Ring 3D model - Accessory equipment with rarity variants

Procedurally generated 3D model using Ursina primitives.
"""

from ursina import Entity, Vec3, color as ursina_color
import constants as c
from graphics3d.utils import rgb_to_ursina_color


def create_ring_3d(position: Vec3, rarity: str) -> Entity:
    """
    Create a 3D ring model with rarity-based appearance

    Args:
        position: 3D world position
        rarity: Item rarity (common, uncommon, rare, epic, legendary)

    Returns:
        Entity: Ring 3D model
    """
    # Container entity (invisible parent)
    ring = Entity(position=position)

    # Rarity-based colors and gem types
    if rarity == c.RARITY_COMMON:
        band_color = rgb_to_ursina_color(140, 140, 140)  # Iron/silver
        gem_color = None  # No gem
        has_glow = False
    elif rarity == c.RARITY_UNCOMMON:
        band_color = rgb_to_ursina_color(180, 140, 80)  # Brass/bronze
        gem_color = rgb_to_ursina_color(100, 200, 100)  # Green gem
        has_glow = False
    elif rarity == c.RARITY_RARE:
        band_color = rgb_to_ursina_color(192, 192, 192)  # Silver
        gem_color = rgb_to_ursina_color(100, 150, 255)  # Blue gem
        has_glow = False
    elif rarity == c.RARITY_EPIC:
        band_color = rgb_to_ursina_color(220, 180, 100)  # Gold
        gem_color = rgb_to_ursina_color(200, 50, 255)  # Purple gem
        has_glow = True
        glow_color = rgb_to_ursina_color(200, 100, 255)
    else:  # LEGENDARY
        band_color = rgb_to_ursina_color(255, 215, 0)  # Bright gold
        gem_color = rgb_to_ursina_color(100, 255, 255)  # Cyan gem
        has_glow = True
        glow_color = rgb_to_ursina_color(100, 200, 255)

    # Glow for epic/legendary
    if has_glow:
        glow = Entity(
            model='sphere',
            color=glow_color,
            scale=0.25,
            parent=ring,
            position=(0, 0, 0),
            alpha=0.4,
            unlit=True
        )

    # Ring band (torus approximation using rotated cubes)
    # Create 8 small cubes arranged in a circle
    num_segments = 8
    for i in range(num_segments):
        angle = (i / num_segments) * 360
        x = 0.12 * (i % 2) * 0.5  # Slight variation
        z = 0.12 * ((i + 1) % 2) * 0.5

        segment = Entity(
            model='cube',
            color=band_color,
            scale=(0.05, 0.04, 0.05),
            parent=ring,
            position=(x, 0, z),
            rotation=(0, angle, 0)
        )

    # Inner core to make it look more ring-like
    core = Entity(
        model='cube',
        color=band_color,
        scale=(0.15, 0.03, 0.15),
        parent=ring,
        position=(0, 0, 0),
        rotation=(0, 45, 0)
    )

    # Gem on top (if has gem)
    if gem_color:
        gem = Entity(
            model='sphere',
            color=gem_color,
            scale=0.08,
            parent=ring,
            position=(0, 0.06, 0),
            unlit=True  # Emissive gem
        )

        # Gem setting/prongs
        gem_setting = Entity(
            model='cube',
            color=band_color,
            scale=(0.04, 0.03, 0.04),
            parent=ring,
            position=(0, 0.03, 0)
        )

    # Store animation state
    ring.float_time = 0.0
    ring.rotation_speed = 60.0  # Faster rotation to show ring shape

    return ring
