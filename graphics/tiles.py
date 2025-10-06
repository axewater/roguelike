"""
Tile rendering functions for dungeon elements
"""
from PyQt6.QtGui import QPainter, QPen, QLinearGradient, QRadialGradient, QColor
from PyQt6.QtCore import QRect, QPointF
import constants as c


def draw_wall_tile(painter: QPainter, x: int, y: int, tile_size: int):
    """Draw a stone brick wall with depth"""
    # Base wall color
    base_color = c.COLOR_WALL

    # Create brick pattern
    brick_rect = QRect(x * tile_size, y * tile_size, tile_size, tile_size)

    # Gradient for 3D effect
    gradient = QLinearGradient(x * tile_size, y * tile_size,
                                (x + 1) * tile_size, (y + 1) * tile_size)
    gradient.setColorAt(0, base_color.lighter(120))
    gradient.setColorAt(1, base_color.darker(130))

    painter.fillRect(brick_rect, gradient)

    # Draw mortar lines for brick effect
    painter.setPen(QPen(base_color.darker(160), 1))

    # Horizontal mortar line (offset for brick pattern)
    offset = (y % 2) * (tile_size // 2)
    mid_y = y * tile_size + tile_size // 2
    painter.drawLine(x * tile_size, mid_y, (x + 1) * tile_size, mid_y)

    # Vertical mortar line
    mid_x = x * tile_size + tile_size // 2 + offset
    if mid_x < (x + 1) * tile_size:
        painter.drawLine(mid_x, y * tile_size, mid_x, (y + 1) * tile_size)

    # Dark outline for definition
    painter.setPen(QPen(QColor(20, 20, 25), 1))
    painter.drawRect(x * tile_size, y * tile_size, tile_size - 1, tile_size - 1)


def draw_floor_tile(painter: QPainter, x: int, y: int, tile_size: int):
    """Draw a checkered floor tile"""
    base_color = c.COLOR_FLOOR

    # Alternating floor pattern
    is_dark = (x + y) % 2 == 0
    if is_dark:
        tile_color = base_color.darker(105)
    else:
        tile_color = base_color.lighter(105)

    painter.fillRect(x * tile_size, y * tile_size, tile_size, tile_size, tile_color)

    # Subtle border
    painter.setPen(QPen(base_color.darker(115), 1))
    painter.drawRect(x * tile_size, y * tile_size, tile_size - 1, tile_size - 1)


def draw_stairs_tile(painter: QPainter, x: int, y: int, tile_size: int):
    """Draw glowing stairs"""
    base_color = c.COLOR_STAIRS

    # Glowing radial gradient background
    center = QPointF(x * tile_size + tile_size / 2, y * tile_size + tile_size / 2)
    gradient = QRadialGradient(center, tile_size * 0.7)
    gradient.setColorAt(0, base_color.lighter(150))
    gradient.setColorAt(0.5, base_color)
    gradient.setColorAt(1, base_color.darker(120))

    painter.fillRect(x * tile_size, y * tile_size, tile_size, tile_size, gradient)

    # Draw stair steps
    painter.setPen(QPen(QColor(255, 255, 255, 180), 2))
    step_height = tile_size // 5
    for i in range(4):
        y_pos = y * tile_size + (i + 1) * step_height
        x_start = x * tile_size + i * 3
        x_end = (x + 1) * tile_size - i * 3
        painter.drawLine(x_start, y_pos, x_end, y_pos)
