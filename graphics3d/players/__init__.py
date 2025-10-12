"""
3D player class model renderers

Each player class has a unique procedurally generated 3D model.
Phase 2: Simple colored cubes
Phase 4: Full detailed character models
"""

from ursina import Entity, color as ursina_color
import constants as c
from graphics3d.utils import world_to_3d_position


def draw_player_3d(player, position=None, facing_direction=None, idle_time=0):
    """
    Dispatcher for player 3D model rendering

    Args:
        player: Player entity
        position: (x, y, z) tuple (optional, will use player.x, player.y if not provided)
        facing_direction: (dx, dy) facing direction (unused in Phase 2)
        idle_time: Time for idle animations (unused in Phase 2)

    Returns:
        Ursina Entity representing the player
    """
    # Calculate position if not provided
    if position is None:
        position = world_to_3d_position(
            player.x,
            player.y,
            c.PLAYER_HEIGHT / 2
        )

    # Get class-specific color (Phase 2: simple color coding)
    class_colors = {
        c.CLASS_WARRIOR: (100, 200, 255),   # Blue - strong and reliable
        c.CLASS_MAGE: (150, 100, 255),      # Purple - magical
        c.CLASS_ROGUE: (80, 80, 80),        # Gray - stealthy
        c.CLASS_RANGER: (100, 220, 80),     # Green - nature-themed
    }

    color_rgb = class_colors.get(player.player_class, (100, 200, 255))
    player_color = ursina_color.rgb(
        color_rgb[0] / 255.0,
        color_rgb[1] / 255.0,
        color_rgb[2] / 255.0
    )

    # Phase 2: Simple cube model
    # TODO Phase 4: Replace with detailed character models
    return Entity(
        model='cube',
        color=player_color,
        scale=(c.ENTITY_SCALE, c.PLAYER_HEIGHT, c.ENTITY_SCALE),
        position=position,
        texture='white_cube'
    )


__all__ = ['draw_player_3d']
