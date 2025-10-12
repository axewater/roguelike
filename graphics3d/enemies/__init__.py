"""
3D enemy model renderers

Each enemy type has a unique procedurally generated 3D model.
"""

# from .goblin import create_goblin_model  # TODO: Phase 4
# from .slime import create_slime_model
# from .skeleton import create_skeleton_model
# from .orc import create_orc_model
# from .demon import create_demon_model
# from .dragon import create_dragon_model

import constants as c


def draw_enemy_3d(enemy, position, facing_direction, idle_time):
    """
    Dispatcher for enemy 3D model rendering

    Args:
        enemy: Enemy entity
        position: (x, y, z) tuple
        facing_direction: (dx, dy) facing direction
        idle_time: Time for idle animations

    Returns:
        Ursina Entity representing the enemy
    """
    # TODO: Implement in Phase 4
    # enemy_type = enemy.enemy_type
    #
    # if enemy_type == c.ENEMY_GOBLIN:
    #     return create_goblin_model(position, facing_direction, idle_time)
    # elif enemy_type == c.ENEMY_SLIME:
    #     return create_slime_model(position, facing_direction, idle_time)
    # elif enemy_type == c.ENEMY_SKELETON:
    #     return create_skeleton_model(position, facing_direction, idle_time)
    # elif enemy_type == c.ENEMY_ORC:
    #     return create_orc_model(position, facing_direction, idle_time)
    # elif enemy_type == c.ENEMY_DEMON:
    #     return create_demon_model(position, facing_direction, idle_time)
    # elif enemy_type == c.ENEMY_DRAGON:
    #     return create_dragon_model(position, facing_direction, idle_time)
    pass


__all__ = ['draw_enemy_3d']
