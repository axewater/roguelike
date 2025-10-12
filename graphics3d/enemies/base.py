"""
Base utilities for 3D enemy model rendering

Shared functions for all enemy models.
"""

# from ursina import Entity, Vec3  # TODO: Import when Ursina is installed


def apply_idle_animation(entity, idle_time: float, animation_speed: float = 1.0):
    """
    Apply breathing/hovering idle animation to enemy model

    Args:
        entity: Ursina Entity to animate
        idle_time: Current idle time for animation cycle
        animation_speed: Speed multiplier for animation
    """
    # TODO: Implement in Phase 4
    pass


def create_health_bar_3d(entity, hp_percentage: float):
    """
    Create a 3D health bar billboard above enemy

    Args:
        entity: Enemy entity to attach health bar to
        hp_percentage: Health percentage (0.0-1.0)

    Returns:
        Ursina Entity representing the health bar
    """
    # TODO: Implement in Phase 4
    # Create a plane billboard that always faces camera
    # Color: Green -> Yellow -> Red based on hp_percentage
    pass
