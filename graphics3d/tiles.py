"""
3D tile rendering for dungeon generation

Converts 2D tile grid into 3D meshes using Ursina Engine.
"""

from typing import Tuple
from ursina import Entity, color as ursina_color
from PyQt6.QtGui import QColor
import constants as c
from graphics3d.utils import world_to_3d_position, qcolor_to_ursina_color, rgb_to_ursina_color
from textures import get_moss_stone_texture, get_brick_texture


# ===== CACHED PROCEDURAL TEXTURES =====
# Generate these once at module load for performance
print("Generating procedural dungeon textures (AAA quality - 512px, 4 variants)...")

# Wall: Generate 4 variants at 512x512 to break repetition
# Each variant uses a different random seed for unique patterns
from textures import RandomSeed
from textures.organic import generate_moss_stone_texture, generate_moss_overlay
from textures.bricks import generate_brick_pattern
from ursina import Texture

DUNGEON_WALL_TEXTURES = []
wall_seeds = [12345, 67890, 24680, 13579]
for i, seed in enumerate(wall_seeds):
    print(f"  - Generating wall variant {i+1}/4 (seed={seed})...")
    with RandomSeed(seed):
        wall_pil = generate_moss_stone_texture(size=512, moss_density='medium')
        DUNGEON_WALL_TEXTURES.append(Texture(wall_pil))

print(f"  ✓ {len(DUNGEON_WALL_TEXTURES)} wall variants generated")

# Floor: Brick with subtle moss accents

_floor_brick = generate_brick_pattern(size=256, darkness=0.8)
_floor_mossy_pil = generate_moss_overlay(_floor_brick, density='light')
DUNGEON_FLOOR_TEXTURE = Texture(_floor_mossy_pil)  # Wrap PIL Image in Ursina Texture

# Ceiling: Dark weathered stone with hanging moss and water damage
from textures.organic import generate_ceiling_texture
_ceiling_pil = generate_ceiling_texture(size=256, moisture_level='medium')
DUNGEON_CEILING_TEXTURE = Texture(_ceiling_pil)  # Wrap PIL Image in Ursina Texture

print("✓ Procedural textures generated and cached")


def create_floor_mesh(x: int, y: int, biome_color):
    """
    Create a 3D floor tile mesh with procedural brick texture

    Args:
        x: Grid X position
        y: Grid Y position (becomes Z in 3D space)
        biome_color: QColor or RGB tuple for the biome (used for subtle tinting)

    Returns:
        Ursina Entity representing the floor tile
    """
    pos = world_to_3d_position(x, y, 0)

    # Convert color for subtle tinting
    if isinstance(biome_color, QColor):
        floor_color = qcolor_to_ursina_color(biome_color)
    elif isinstance(biome_color, tuple):
        floor_color = rgb_to_ursina_color(*biome_color)
    else:
        floor_color = biome_color

    # Slight tint to preserve some biome identity, but let texture show through
    subtle_tint = ursina_color.rgb(
        min(1.0, 0.5 + floor_color.r * 0.5),  # 50% white + 50% biome color
        min(1.0, 0.5 + floor_color.g * 0.5),
        min(1.0, 0.5 + floor_color.b * 0.5)
    )

    return Entity(
        model='plane',
        position=pos,
        scale=(1, 1, 1),
        color=subtle_tint,  # Subtle tint to preserve biome identity
        texture=DUNGEON_FLOOR_TEXTURE,  # Procedural brick texture
        collider=None  # No collision for floors
    )


def create_wall_mesh(x: int, y: int, biome_color, height: float = None):
    """
    Create a 3D wall tile mesh with procedural moss-covered stone texture

    Args:
        x: Grid X position
        y: Grid Y position (becomes Z in 3D space)
        biome_color: QColor or RGB tuple for the biome (now unused - texture provides color)
        height: Wall height in world units (defaults to c.WALL_HEIGHT)

    Returns:
        Ursina Entity representing the wall tile
    """
    if height is None:
        height = c.WALL_HEIGHT

    pos = world_to_3d_position(x, y, height / 2)

    # Select texture variant based on position (deterministic hash)
    # This breaks repetition while being deterministic
    variant_idx = (x * 7 + y * 13) % len(DUNGEON_WALL_TEXTURES)
    wall_texture = DUNGEON_WALL_TEXTURES[variant_idx]

    # Use procedural moss-covered stone texture (no color tinting needed)
    return Entity(
        model='cube',
        position=pos,
        scale=(1, height, 1),
        color=ursina_color.white,  # Neutral tint - let texture show its true colors
        texture=wall_texture,  # Select from 4 variants
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


def create_ceiling_mesh(x: int, y: int):
    """
    Create a 3D ceiling tile mesh with procedural hanging moss texture

    Args:
        x: Grid X position
        y: Grid Y position (becomes Z in 3D space)

    Returns:
        Ursina Entity representing the ceiling tile
    """
    # Position ceiling at top of walls
    pos = world_to_3d_position(x, y, c.WALL_HEIGHT)

    # Create ceiling plane facing downward
    return Entity(
        model='plane',
        position=pos,
        scale=(1, 1, 1),
        color=ursina_color.white,  # No tinting - let texture show
        texture=DUNGEON_CEILING_TEXTURE,  # Procedural ceiling with hanging moss
        rotation_x=180,  # Flip to face downward
        collider=None  # No collision for ceilings
    )
