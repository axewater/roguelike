"""
Item rendering by type
"""
from PyQt6.QtGui import QPainter, QPen, QRadialGradient, QColor
from PyQt6.QtCore import Qt, QPoint
import constants as c


def draw_item(painter: QPainter, x: float, y: float, tile_size: int, color: QColor, item_type: str):
    """Draw item based on type"""
    center_x = int(x * tile_size + tile_size // 2)
    center_y = int(y * tile_size + tile_size // 2)

    # Drop shadow
    shadow_color = QColor(0, 0, 0, 60)
    painter.setBrush(shadow_color)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(center_x - tile_size // 4 + 2, center_y - tile_size // 4 + 2,
                        tile_size // 2, tile_size // 2)

    # Rarity glow
    gradient = QRadialGradient(center_x, center_y, tile_size // 2)
    gradient.setColorAt(0, color.lighter(130))
    gradient.setColorAt(0.7, color)
    gradient.setColorAt(1, QColor(0, 0, 0, 0))
    painter.setBrush(gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(center_x - tile_size // 2, center_y - tile_size // 2,
                        tile_size, tile_size)

    if item_type == c.ITEM_HEALTH_POTION:
        # Potion bottle
        painter.setBrush(QColor(220, 50, 50))
        painter.setPen(QPen(QColor(180, 30, 30), 2))

        # Bottle body
        painter.drawRoundedRect(center_x - tile_size // 6, center_y - tile_size // 8,
                               tile_size // 3, tile_size // 3, 3, 3)

        # Bottle neck
        painter.drawRect(center_x - tile_size // 12, center_y - tile_size // 4,
                        tile_size // 6, tile_size // 8)

        # Cork
        painter.setBrush(QColor(139, 90, 43))
        painter.drawRect(center_x - tile_size // 10, center_y - tile_size // 3,
                        tile_size // 5, tile_size // 12)

        # Liquid shine
        painter.setBrush(QColor(255, 255, 255, 150))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 12, center_y - tile_size // 16, 4, 6)

    elif item_type == c.ITEM_SWORD:
        # Sword
        painter.setBrush(QColor(192, 192, 192))
        painter.setPen(QPen(QColor(128, 128, 128), 2))

        # Blade
        blade = [
            QPoint(center_x - tile_size // 12, center_y - tile_size // 3),
            QPoint(center_x + tile_size // 12, center_y - tile_size // 3),
            QPoint(center_x + tile_size // 16, center_y + tile_size // 8),
            QPoint(center_x - tile_size // 16, center_y + tile_size // 8),
        ]
        painter.drawPolygon(blade)

        # Crossguard
        painter.setBrush(QColor(139, 90, 43))
        painter.drawRect(center_x - tile_size // 4, center_y + tile_size // 8,
                        tile_size // 2, tile_size // 12)

        # Handle
        painter.setBrush(QColor(100, 60, 30))
        painter.drawRect(center_x - tile_size // 12, center_y + tile_size // 6,
                        tile_size // 6, tile_size // 5)

        # Gleam
        painter.setPen(QPen(QColor(255, 255, 255, 200), 2))
        painter.drawLine(center_x, center_y - tile_size // 4,
                        center_x + tile_size // 16, center_y)

    elif item_type == c.ITEM_SHIELD:
        # Shield
        painter.setBrush(color)
        painter.setPen(QPen(color.darker(150), 2))

        # Shield body
        points = [
            QPoint(center_x, center_y - tile_size // 3),
            QPoint(center_x + tile_size // 4, center_y - tile_size // 8),
            QPoint(center_x + tile_size // 4, center_y + tile_size // 8),
            QPoint(center_x, center_y + tile_size // 3),
            QPoint(center_x - tile_size // 4, center_y + tile_size // 8),
            QPoint(center_x - tile_size // 4, center_y - tile_size // 8),
        ]
        painter.drawPolygon(points)

        # Shield rim
        painter.setBrush(color.lighter(120))
        painter.drawEllipse(center_x - tile_size // 8, center_y - tile_size // 8,
                           tile_size // 4, tile_size // 4)

    elif item_type == c.ITEM_BOOTS:
        # Boots
        painter.setBrush(QColor(101, 67, 33))
        painter.setPen(QPen(QColor(70, 45, 20), 2))

        # Left boot
        painter.drawRoundedRect(center_x - tile_size // 4, center_y - tile_size // 8,
                               tile_size // 5, tile_size // 3, 2, 2)

        # Right boot
        painter.drawRoundedRect(center_x + tile_size // 12, center_y - tile_size // 8,
                               tile_size // 5, tile_size // 3, 2, 2)

        # Laces
        painter.setPen(QPen(QColor(240, 230, 140), 1))
        for i in range(3):
            y_pos = center_y - tile_size // 16 + i * tile_size // 12
            painter.drawLine(center_x - tile_size // 5, y_pos,
                           center_x - tile_size // 12, y_pos)
            painter.drawLine(center_x + tile_size // 10, y_pos,
                           center_x + tile_size // 4, y_pos)

    elif item_type == c.ITEM_RING:
        # Ring (diamond shape)
        painter.setBrush(color)
        painter.setPen(QPen(color.darker(130), 2))

        # Outer diamond
        points = [
            QPoint(center_x, center_y - tile_size // 4),
            QPoint(center_x + tile_size // 4, center_y),
            QPoint(center_x, center_y + tile_size // 4),
            QPoint(center_x - tile_size // 4, center_y),
        ]
        painter.drawPolygon(points)

        # Inner sparkle
        painter.setBrush(QColor(255, 255, 255, 220))
        painter.setPen(Qt.PenStyle.NoPen)
        inner_points = [
            QPoint(center_x, center_y - tile_size // 8),
            QPoint(center_x + tile_size // 12, center_y),
            QPoint(center_x, center_y + tile_size // 8),
            QPoint(center_x - tile_size // 12, center_y),
        ]
        painter.drawPolygon(inner_points)

    else:
        # Generic item (glowing orb)
        gradient = QRadialGradient(center_x, center_y, tile_size // 4)
        gradient.setColorAt(0, QColor(255, 255, 255, 200))
        gradient.setColorAt(0.5, color)
        gradient.setColorAt(1, color.darker(120))

        painter.setBrush(gradient)
        painter.setPen(QPen(color.darker(150), 2))
        painter.drawEllipse(center_x - tile_size // 4, center_y - tile_size // 4,
                           tile_size // 2, tile_size // 2)
