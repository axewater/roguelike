"""
3D tile rendering for dungeon generation

Converts 2D tile grid into 3D meshes using Ursina Engine.
"""

from typing import Tuple
from ursina import Entity, color as ursina_color
from PyQt6.QtGui import QColor
import constants as c
from graphics3d.utils import world_to_3d_position, qcolor_to_ursina_color, rgb_to_ursina_color


def create_floor_mesh(x: int, y: int, biome_color):
    """
    Create a 3D floor tile mesh

    Args:
        x: Grid X position
        y: Grid Y position (becomes Z in 3D space)
        biome_color: QColor or RGB tuple for the biome

    Returns:
        Ursina Entity representing the floor tile
    """
    pos = world_to_3d_position(x, y, 0)

    # Convert color
    if isinstance(biome_color, QColor):
        floor_color = qcolor_to_ursina_color(biome_color)
    elif isinstance(biome_color, tuple):
        floor_color = rgb_to_ursina_color(*biome_color)
    else:
        floor_color = biome_color

    return Entity(
        model='plane',
        position=pos,
        scale=(1, 1, 1),
        color=floor_color,
        texture='white_cube',  # Flat color texture
        collider=None  # No collision for floors
    )


def create_wall_mesh(x: int, y: int, biome_color, height: float = None):
    """
    Create a 3D wall tile mesh

    Args:
        x: Grid X position
        y: Grid Y position (becomes Z in 3D space)
        biome_color: QColor or RGB tuple for the biome
        height: Wall height in world units (defaults to c.WALL_HEIGHT)

    Returns:
        Ursina Entity representing the wall tile
    """
    if height is None:
        height = c.WALL_HEIGHT

    pos = world_to_3d_position(x, y, height / 2)

    # Convert color
    if isinstance(biome_color, QColor):
        wall_color = qcolor_to_ursina_color(biome_color)
    elif isinstance(biome_color, tuple):
        wall_color = rgb_to_ursina_color(*biome_color)
    else:
        wall_color = biome_color

    # Darken wall color slightly for depth
    darker_color = ursina_color.rgb(
        max(0, wall_color.r * 0.8),
        max(0, wall_color.g * 0.8),
        max(0, wall_color.b * 0.8)
    )

    return Entity(
        model='cube',
        position=pos,
        scale=(1, height, 1),
        color=darker_color,
        texture='white_cube',
        collider='box'  # Walls have collision
    )


def create_stairs_mesh(x: int, y: int, biome_color):
    """
    Create a 3D staircase mesh

    Args:
        x: Grid X position
        y: Grid Y position (becomes Z in 3D space)
        biome_color: QColor or RGB tuple for the biome

    Returns:
        Ursina Entity representing stairs going down
    """
    pos = world_to_3d_position(x, y, 0.2)

    # Convert color
    if isinstance(biome_color, QColor):
        stairs_color = qcolor_to_ursina_color(biome_color)
    elif isinstance(biome_color, tuple):
        stairs_color = rgb_to_ursina_color(*biome_color)
    else:
        stairs_color = biome_color

    # Brighten stairs to make them stand out
    bright_color = ursina_color.rgb(
        min(1, stairs_color.r * 1.5),
        min(1, stairs_color.g * 1.5),
        min(1, stairs_color.b * 1.5)
    )

    # Simple stairs: cube with glow effect
    return Entity(
        model='cube',
        position=pos,
        scale=(0.8, 0.4, 0.8),
        color=bright_color,
        texture='white_cube'
    )
