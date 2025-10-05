"""
Graphics rendering for Dungeon Delver
Geometric shape-based graphics to replace ASCII art
"""
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QRadialGradient
from PyQt6.QtCore import Qt, QRect, QPoint, QPointF
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


def draw_player(painter: QPainter, x: int, y: int, tile_size: int, color: QColor, class_type: str):
    """Draw player character based on class"""
    center_x = x * tile_size + tile_size // 2
    center_y = y * tile_size + tile_size // 2

    # Drop shadow
    shadow_color = QColor(0, 0, 0, 80)
    painter.setBrush(shadow_color)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(center_x - tile_size // 3 + 2, center_y - tile_size // 3 + 3,
                        tile_size * 2 // 3, tile_size * 2 // 3)

    if class_type == c.CLASS_WARRIOR:
        # Shield shape for warrior
        painter.setBrush(color)
        painter.setPen(QPen(color.darker(150), 2))

        # Shield body
        points = [
            QPoint(center_x, center_y - tile_size // 3),
            QPoint(center_x + tile_size // 3, center_y - tile_size // 6),
            QPoint(center_x + tile_size // 3, center_y + tile_size // 6),
            QPoint(center_x, center_y + tile_size // 3),
            QPoint(center_x - tile_size // 3, center_y + tile_size // 6),
            QPoint(center_x - tile_size // 3, center_y - tile_size // 6),
        ]
        painter.drawPolygon(points)

        # Shield cross
        painter.setPen(QPen(color.lighter(150), 2))
        painter.drawLine(center_x, center_y - tile_size // 4, center_x, center_y + tile_size // 4)
        painter.drawLine(center_x - tile_size // 4, center_y, center_x + tile_size // 4, center_y)

    elif class_type == c.CLASS_MAGE:
        # Star shape for mage
        painter.setBrush(color)
        painter.setPen(QPen(color.darker(150), 2))

        # Draw 5-pointed star
        import math
        outer_radius = tile_size // 3
        inner_radius = tile_size // 6
        points = []
        for i in range(10):
            angle = math.pi / 2 - (i * math.pi / 5)
            radius = outer_radius if i % 2 == 0 else inner_radius
            px = center_x + radius * math.cos(angle)
            py = center_y - radius * math.sin(angle)
            points.append(QPoint(int(px), int(py)))

        painter.drawPolygon(points)

        # Glowing center
        gradient = QRadialGradient(center_x, center_y, tile_size // 8)
        gradient.setColorAt(0, QColor(255, 255, 255, 200))
        gradient.setColorAt(1, color)
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 8, center_y - tile_size // 8,
                           tile_size // 4, tile_size // 4)

    elif class_type == c.CLASS_ROGUE:
        # Dagger shape for rogue
        painter.setBrush(color)
        painter.setPen(QPen(color.darker(150), 2))

        # Blade
        blade_points = [
            QPoint(center_x - tile_size // 8, center_y - tile_size // 3),
            QPoint(center_x + tile_size // 8, center_y - tile_size // 3),
            QPoint(center_x + 2, center_y + tile_size // 6),
            QPoint(center_x - 2, center_y + tile_size // 6),
        ]
        painter.drawPolygon(blade_points)

        # Handle
        painter.setBrush(color.darker(120))
        painter.drawRect(center_x - tile_size // 6, center_y + tile_size // 6,
                        tile_size // 3, tile_size // 8)

        # Pommel
        painter.drawEllipse(center_x - tile_size // 8, center_y + tile_size // 4,
                           tile_size // 4, tile_size // 6)

    elif class_type == c.CLASS_RANGER:
        # Bow shape for ranger
        painter.setPen(QPen(color.darker(150), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Bow arc
        bow_rect = QRect(center_x - tile_size // 4, center_y - tile_size // 3,
                        tile_size // 2, tile_size * 2 // 3)
        painter.drawArc(bow_rect, 30 * 16, 300 * 16)

        # Bowstring
        painter.setPen(QPen(color.darker(120), 1))
        painter.drawLine(center_x + tile_size // 8, center_y - tile_size // 4,
                        center_x + tile_size // 8, center_y + tile_size // 4)

        # Arrow
        painter.setBrush(color)
        painter.setPen(QPen(color.darker(150), 2))
        arrow_points = [
            QPoint(center_x - tile_size // 4, center_y),
            QPoint(center_x + tile_size // 6, center_y - 2),
            QPoint(center_x + tile_size // 6, center_y + 2),
        ]
        painter.drawPolygon(arrow_points)


def draw_enemy(painter: QPainter, x: int, y: int, tile_size: int, color: QColor, enemy_type: str):
    """Draw enemy based on type"""
    center_x = x * tile_size + tile_size // 2
    center_y = y * tile_size + tile_size // 2

    # Drop shadow
    shadow_color = QColor(0, 0, 0, 80)
    painter.setBrush(shadow_color)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(center_x - tile_size // 3 + 2, center_y - tile_size // 3 + 3,
                        tile_size * 2 // 3, tile_size * 2 // 3)

    if enemy_type == c.ENEMY_GOBLIN:
        # Small creature with horns
        painter.setBrush(color)
        painter.setPen(QPen(color.darker(150), 2))

        # Body (circle)
        painter.drawEllipse(center_x - tile_size // 4, center_y - tile_size // 4,
                           tile_size // 2, tile_size // 2)

        # Horns (triangles)
        left_horn = [
            QPoint(center_x - tile_size // 6, center_y - tile_size // 4),
            QPoint(center_x - tile_size // 4, center_y - tile_size // 3),
            QPoint(center_x - tile_size // 8, center_y - tile_size // 5),
        ]
        right_horn = [
            QPoint(center_x + tile_size // 6, center_y - tile_size // 4),
            QPoint(center_x + tile_size // 4, center_y - tile_size // 3),
            QPoint(center_x + tile_size // 8, center_y - tile_size // 5),
        ]
        painter.drawPolygon(left_horn)
        painter.drawPolygon(right_horn)

        # Evil eyes
        painter.setBrush(QColor(255, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 8, center_y - tile_size // 12, 3, 3)
        painter.drawEllipse(center_x + tile_size // 8 - 3, center_y - tile_size // 12, 3, 3)

    elif enemy_type == c.ENEMY_SKELETON:
        # Skull shape
        painter.setBrush(color)
        painter.setPen(QPen(color.darker(130), 2))

        # Skull (rounded rectangle)
        painter.drawRoundedRect(center_x - tile_size // 3, center_y - tile_size // 3,
                               tile_size * 2 // 3, tile_size * 2 // 3, 5, 5)

        # Eye sockets (dark)
        painter.setBrush(QColor(0, 0, 0, 180))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 6, center_y - tile_size // 6,
                           tile_size // 8, tile_size // 6)
        painter.drawEllipse(center_x + tile_size // 12, center_y - tile_size // 6,
                           tile_size // 8, tile_size // 6)

        # Nose (triangle)
        nose = [
            QPoint(center_x, center_y),
            QPoint(center_x - tile_size // 12, center_y + tile_size // 8),
            QPoint(center_x + tile_size // 12, center_y + tile_size // 8),
        ]
        painter.drawPolygon(nose)

        # Teeth
        painter.setPen(QPen(QColor(0, 0, 0, 180), 1))
        for i in range(-2, 3):
            x_pos = center_x + i * tile_size // 12
            painter.drawLine(x_pos, center_y + tile_size // 6,
                           x_pos, center_y + tile_size // 4)

    elif enemy_type == c.ENEMY_DRAGON:
        # Dragon with wings
        painter.setBrush(color)
        painter.setPen(QPen(color.darker(150), 2))

        # Body (larger oval)
        painter.drawEllipse(center_x - tile_size // 3, center_y - tile_size // 4,
                           tile_size * 2 // 3, tile_size // 2)

        # Wings (triangular)
        left_wing = [
            QPoint(center_x - tile_size // 6, center_y),
            QPoint(center_x - tile_size // 2, center_y - tile_size // 4),
            QPoint(center_x - tile_size // 3, center_y + tile_size // 8),
        ]
        right_wing = [
            QPoint(center_x + tile_size // 6, center_y),
            QPoint(center_x + tile_size // 2, center_y - tile_size // 4),
            QPoint(center_x + tile_size // 3, center_y + tile_size // 8),
        ]
        painter.setBrush(color.darker(120))
        painter.drawPolygon(left_wing)
        painter.drawPolygon(right_wing)

        # Head (small circle)
        painter.setBrush(color)
        painter.drawEllipse(center_x + tile_size // 6, center_y - tile_size // 3,
                           tile_size // 4, tile_size // 4)

        # Fire breath indicator (glowing)
        gradient = QRadialGradient(center_x + tile_size // 3, center_y - tile_size // 5, tile_size // 8)
        gradient.setColorAt(0, QColor(255, 200, 0, 200))
        gradient.setColorAt(1, QColor(255, 100, 0, 0))
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x + tile_size // 4, center_y - tile_size // 4,
                           tile_size // 4, tile_size // 4)


def draw_item(painter: QPainter, x: int, y: int, tile_size: int, color: QColor, item_type: str):
    """Draw item based on type"""
    center_x = x * tile_size + tile_size // 2
    center_y = y * tile_size + tile_size // 2

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
