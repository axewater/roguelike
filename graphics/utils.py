"""
Graphics utility functions
"""
from PyQt6.QtGui import QColor


def apply_fog_color(color: QColor, alpha: float) -> QColor:
    """
    Darken color for fog of war effect on explored but not visible tiles.

    Args:
        color: Base color to darken
        alpha: Brightness factor (0.0 = black, 1.0 = original)

    Returns:
        Darkened QColor
    """
    return QColor(
        int(color.red() * alpha),
        int(color.green() * alpha),
        int(color.blue() * alpha)
    )
