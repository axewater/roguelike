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


def draw_player(painter: QPainter, x: float, y: float, tile_size: int, color: QColor, class_type: str, facing_direction: tuple = (0, 1)):
    """Draw player character based on class with directional facing"""
    center_x = int(x * tile_size + tile_size // 2)
    center_y = int(y * tile_size + tile_size // 2)
    import math

    # Determine if we need to flip (facing left)
    facing_dx, facing_dy = facing_direction
    flip_horizontal = facing_dx < 0

    # Save painter state
    painter.save()

    # Apply horizontal flip if facing left
    if flip_horizontal:
        painter.translate(center_x * 2, 0)
        painter.scale(-1, 1)

    # Enhanced drop shadow (larger, softer)
    shadow_color = QColor(0, 0, 0, 100)
    painter.setBrush(shadow_color)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(center_x - tile_size // 2 + 3, center_y + tile_size // 4,
                        tile_size - 6, tile_size // 6)

    if class_type == c.CLASS_WARRIOR:
        # WARRIOR - Armored tank with shield and sword

        # Legs (wide stance)
        leg_color = color.darker(130)
        painter.setBrush(leg_color)
        painter.setPen(QPen(leg_color.darker(120), 1))
        # Left leg
        painter.drawRect(center_x - tile_size // 5, center_y + tile_size // 10,
                        tile_size // 8, tile_size // 4)
        # Right leg
        painter.drawRect(center_x + tile_size // 12, center_y + tile_size // 10,
                        tile_size // 8, tile_size // 4)

        # Body (armored chest with gradient)
        body_gradient = QLinearGradient(center_x - tile_size // 4, center_y - tile_size // 8,
                                        center_x + tile_size // 4, center_y + tile_size // 8)
        body_gradient.setColorAt(0, color.lighter(120))
        body_gradient.setColorAt(0.5, color)
        body_gradient.setColorAt(1, color.darker(110))
        painter.setBrush(body_gradient)
        painter.setPen(QPen(color.darker(140), 2))
        painter.drawRoundedRect(center_x - tile_size // 4, center_y - tile_size // 6,
                               tile_size // 2, tile_size * 3 // 10, 3, 3)

        # Armor plate details
        painter.setPen(QPen(color.lighter(140), 1))
        painter.drawLine(center_x - tile_size // 6, center_y - tile_size // 12,
                        center_x + tile_size // 6, center_y - tile_size // 12)
        painter.drawLine(center_x, center_y - tile_size // 6,
                        center_x, center_y + tile_size // 8)

        # Shield (left side)
        shield_points = [
            QPoint(center_x - tile_size // 4, center_y - tile_size // 8),
            QPoint(center_x - tile_size // 6, center_y - tile_size // 5),
            QPoint(center_x - tile_size // 8, center_y - tile_size // 12),
            QPoint(center_x - tile_size // 8, center_y + tile_size // 12),
            QPoint(center_x - tile_size // 6, center_y + tile_size // 6),
        ]
        painter.setBrush(color.lighter(110))
        painter.setPen(QPen(color.darker(130), 2))
        painter.drawPolygon(shield_points)

        # Shield boss (center)
        painter.setBrush(QColor(200, 180, 100))
        painter.drawEllipse(center_x - tile_size // 5, center_y - tile_size // 20,
                           tile_size // 12, tile_size // 12)

        # Sword (right side)
        painter.setBrush(QColor(220, 220, 230))
        painter.setPen(QPen(QColor(180, 180, 190), 2))
        sword_blade = [
            QPoint(center_x + tile_size // 5, center_y - tile_size // 6),
            QPoint(center_x + tile_size // 4, center_y - tile_size // 5),
            QPoint(center_x + tile_size // 3, center_y + tile_size // 8),
            QPoint(center_x + tile_size // 4, center_y + tile_size // 8),
        ]
        painter.drawPolygon(sword_blade)

        # Sword hilt
        painter.setBrush(QColor(139, 90, 43))
        painter.drawRect(center_x + tile_size // 6, center_y + tile_size // 8,
                        tile_size // 8, tile_size // 12)

        # Helmet
        helmet_gradient = QRadialGradient(center_x, center_y - tile_size // 4, tile_size // 5)
        helmet_gradient.setColorAt(0, color.lighter(130))
        helmet_gradient.setColorAt(1, color.darker(110))
        painter.setBrush(helmet_gradient)
        painter.setPen(QPen(color.darker(140), 2))
        painter.drawEllipse(center_x - tile_size // 5, center_y - tile_size // 3,
                           tile_size * 2 // 5, tile_size * 2 // 5)

        # Visor slit (dark)
        painter.setBrush(QColor(0, 0, 0, 180))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(center_x - tile_size // 6, center_y - tile_size // 5,
                        tile_size // 3, tile_size // 20)

        # Helmet highlight
        painter.setBrush(QColor(255, 255, 255, 120))
        painter.drawEllipse(center_x - tile_size // 12, center_y - tile_size // 4,
                           tile_size // 10, tile_size // 12)

    elif class_type == c.CLASS_MAGE:
        # MAGE - Robed spellcaster with floating orbs

        # Robe bottom (flowing)
        robe_points = [
            QPoint(center_x, center_y + tile_size // 10),
            QPoint(center_x - tile_size // 3, center_y + tile_size // 3),
            QPoint(center_x + tile_size // 3, center_y + tile_size // 3),
        ]
        robe_gradient = QLinearGradient(center_x, center_y,
                                        center_x, center_y + tile_size // 3)
        robe_gradient.setColorAt(0, color)
        robe_gradient.setColorAt(1, color.darker(130))
        painter.setBrush(robe_gradient)
        painter.setPen(QPen(color.darker(150), 2))
        painter.drawPolygon(robe_points)

        # Robe body
        painter.drawEllipse(center_x - tile_size // 4, center_y - tile_size // 8,
                           tile_size // 2, tile_size * 2 // 5)

        # Belt/sash
        painter.setBrush(color.darker(140))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(center_x - tile_size // 4, center_y + tile_size // 20,
                        tile_size // 2, tile_size // 15)

        # Staff (left hand)
        painter.setPen(QPen(QColor(139, 90, 43), 3))
        painter.drawLine(center_x - tile_size // 4, center_y - tile_size // 8,
                        center_x - tile_size // 3, center_y - tile_size // 2)

        # Staff orb (glowing)
        orb_gradient = QRadialGradient(center_x - tile_size // 3, center_y - tile_size // 2,
                                       tile_size // 8)
        orb_gradient.setColorAt(0, QColor(255, 255, 255, 240))
        orb_gradient.setColorAt(0.4, color.lighter(160))
        orb_gradient.setColorAt(1, color)
        painter.setBrush(orb_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 3 - tile_size // 12,
                           center_y - tile_size // 2 - tile_size // 12,
                           tile_size // 6, tile_size // 6)

        # Floating magical orbs (3 orbiting)
        for i in range(3):
            angle = (i * 2 * math.pi / 3) + (math.pi / 4)
            orb_x = center_x + int(tile_size // 3 * math.cos(angle))
            orb_y = center_y + int(tile_size // 4 * math.sin(angle))

            # Orb glow
            mini_gradient = QRadialGradient(orb_x, orb_y, tile_size // 12)
            mini_gradient.setColorAt(0, QColor(255, 255, 255, 200))
            mini_gradient.setColorAt(0.5, color.lighter(140))
            mini_gradient.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
            painter.setBrush(mini_gradient)
            painter.drawEllipse(orb_x - tile_size // 12, orb_y - tile_size // 12,
                               tile_size // 6, tile_size // 6)

        # Hood
        hood_gradient = QRadialGradient(center_x, center_y - tile_size // 4, tile_size // 4)
        hood_gradient.setColorAt(0, color.lighter(110))
        hood_gradient.setColorAt(1, color.darker(120))
        painter.setBrush(hood_gradient)
        painter.setPen(QPen(color.darker(140), 2))
        # Hood shape
        hood_points = [
            QPoint(center_x, center_y - tile_size // 3),
            QPoint(center_x - tile_size // 4, center_y - tile_size // 6),
            QPoint(center_x - tile_size // 5, center_y - tile_size // 12),
            QPoint(center_x + tile_size // 5, center_y - tile_size // 12),
            QPoint(center_x + tile_size // 4, center_y - tile_size // 6),
        ]
        painter.drawPolygon(hood_points)

        # Glowing eyes under hood
        painter.setBrush(color.lighter(180))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 12, center_y - tile_size // 6, 3, 4)
        painter.drawEllipse(center_x + tile_size // 12 - 3, center_y - tile_size // 6, 3, 4)

        # Mystical rune on robe
        painter.setPen(QPen(color.lighter(160), 1))
        painter.drawLine(center_x - tile_size // 16, center_y,
                        center_x + tile_size // 16, center_y)
        painter.drawLine(center_x, center_y - tile_size // 16,
                        center_x, center_y + tile_size // 16)

    elif class_type == c.CLASS_ROGUE:
        # ROGUE - Stealthy assassin with dual daggers

        # Legs (agile stance)
        leg_color = QColor(40, 40, 45)
        painter.setBrush(leg_color)
        painter.setPen(QPen(leg_color.darker(120), 1))
        # Left leg (forward)
        painter.drawRect(center_x - tile_size // 6, center_y + tile_size // 12,
                        tile_size // 10, tile_size // 4)
        # Right leg (back)
        painter.drawRect(center_x + tile_size // 12, center_y + tile_size // 8,
                        tile_size // 10, tile_size // 5)

        # Cloak (flowing behind)
        cloak_gradient = QLinearGradient(center_x, center_y - tile_size // 8,
                                         center_x, center_y + tile_size // 3)
        cloak_gradient.setColorAt(0, color.darker(110))
        cloak_gradient.setColorAt(1, color.darker(140))
        painter.setBrush(cloak_gradient)
        painter.setPen(QPen(color.darker(160), 2))
        cloak_points = [
            QPoint(center_x - tile_size // 6, center_y - tile_size // 12),
            QPoint(center_x - tile_size // 4, center_y + tile_size // 8),
            QPoint(center_x - tile_size // 5, center_y + tile_size // 3),
            QPoint(center_x + tile_size // 6, center_y + tile_size // 3),
            QPoint(center_x + tile_size // 5, center_y + tile_size // 8),
            QPoint(center_x + tile_size // 6, center_y - tile_size // 12),
        ]
        painter.drawPolygon(cloak_points)

        # Body (lean, dark outfit)
        body_color = QColor(50, 45, 60)
        painter.setBrush(body_color)
        painter.setPen(QPen(body_color.darker(120), 1))
        painter.drawEllipse(center_x - tile_size // 6, center_y - tile_size // 10,
                           tile_size // 3, tile_size // 3)

        # Belt with pouches
        painter.setBrush(QColor(80, 60, 40))
        painter.drawRect(center_x - tile_size // 6, center_y + tile_size // 12,
                        tile_size // 3, tile_size // 20)

        # Left dagger
        painter.setBrush(QColor(200, 200, 210))
        painter.setPen(QPen(QColor(160, 160, 170), 2))
        left_blade = [
            QPoint(center_x - tile_size // 4, center_y - tile_size // 12),
            QPoint(center_x - tile_size // 6, center_y - tile_size // 10),
            QPoint(center_x - tile_size // 5, center_y + tile_size // 10),
            QPoint(center_x - tile_size // 4 - 2, center_y + tile_size // 12),
        ]
        painter.drawPolygon(left_blade)

        # Right dagger
        right_blade = [
            QPoint(center_x + tile_size // 4, center_y),
            QPoint(center_x + tile_size // 5, center_y + 2),
            QPoint(center_x + tile_size // 6, center_y + tile_size // 6),
            QPoint(center_x + tile_size // 5, center_y + tile_size // 6 + 2),
        ]
        painter.drawPolygon(right_blade)

        # Dagger hilts
        painter.setBrush(QColor(60, 40, 80))
        painter.drawRect(center_x - tile_size // 4, center_y + tile_size // 12,
                        tile_size // 16, tile_size // 12)
        painter.drawRect(center_x + tile_size // 6, center_y + tile_size // 6,
                        tile_size // 16, tile_size // 12)

        # Hood (concealing face)
        hood_gradient = QRadialGradient(center_x, center_y - tile_size // 5, tile_size // 4)
        hood_gradient.setColorAt(0, color)
        hood_gradient.setColorAt(1, color.darker(140))
        painter.setBrush(hood_gradient)
        painter.setPen(QPen(color.darker(150), 2))
        painter.drawEllipse(center_x - tile_size // 5, center_y - tile_size // 3,
                           tile_size * 2 // 5, tile_size * 2 // 5)

        # Face shadow (mostly hidden)
        painter.setBrush(QColor(0, 0, 0, 200))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 8, center_y - tile_size // 6,
                           tile_size // 4, tile_size // 5)

        # Glowing eyes (purple/dangerous)
        painter.setBrush(QColor(180, 100, 255, 220))
        painter.drawEllipse(center_x - tile_size // 16, center_y - tile_size // 7, 3, 3)
        painter.drawEllipse(center_x + tile_size // 16 - 3, center_y - tile_size // 7, 3, 3)

        # Shadow wisps effect
        wisp_color = QColor(color.red(), color.green(), color.blue(), 80)
        painter.setBrush(wisp_color)
        for i in range(3):
            angle = i * 2 * math.pi / 3
            wisp_x = center_x + int(tile_size // 4 * math.cos(angle))
            wisp_y = center_y + int(tile_size // 5 * math.sin(angle))
            painter.drawEllipse(wisp_x - 2, wisp_y - 2, 4, 6)

    elif class_type == c.CLASS_RANGER:
        # RANGER - Nature archer with bow and quiver

        # Legs (balanced stance)
        leg_color = QColor(80, 100, 70)
        painter.setBrush(leg_color)
        painter.setPen(QPen(leg_color.darker(120), 1))
        # Left leg
        painter.drawRect(center_x - tile_size // 7, center_y + tile_size // 10,
                        tile_size // 9, tile_size // 4)
        # Right leg
        painter.drawRect(center_x + tile_size // 14, center_y + tile_size // 10,
                        tile_size // 9, tile_size // 4)

        # Quiver on back
        painter.setBrush(QColor(100, 70, 40))
        painter.setPen(QPen(QColor(70, 50, 30), 2))
        painter.drawRect(center_x + tile_size // 6, center_y - tile_size // 12,
                        tile_size // 10, tile_size // 4)

        # Arrow fletching (3 arrows in quiver)
        painter.setPen(QPen(QColor(200, 180, 140), 1))
        for i in range(3):
            x_off = i * 2 - 2
            painter.drawLine(center_x + tile_size // 6 + x_off, center_y - tile_size // 12,
                           center_x + tile_size // 6 + x_off, center_y - tile_size // 8)

        # Body (leather armor)
        body_gradient = QLinearGradient(center_x - tile_size // 5, center_y - tile_size // 10,
                                        center_x + tile_size // 5, center_y + tile_size // 10)
        body_gradient.setColorAt(0, color.darker(110))
        body_gradient.setColorAt(0.5, color)
        body_gradient.setColorAt(1, color.darker(110))
        painter.setBrush(body_gradient)
        painter.setPen(QPen(color.darker(130), 2))
        painter.drawEllipse(center_x - tile_size // 5, center_y - tile_size // 12,
                           tile_size * 2 // 5, tile_size // 3)

        # Leather strap across chest
        painter.setPen(QPen(QColor(100, 70, 40), 2))
        painter.drawLine(center_x - tile_size // 6, center_y - tile_size // 12,
                        center_x + tile_size // 5, center_y + tile_size // 10)

        # Bow (held ready)
        bow_wood = QColor(120, 80, 40)
        painter.setPen(QPen(bow_wood, 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        # Bow curve
        bow_rect = QRect(center_x - tile_size // 3, center_y - tile_size // 4,
                        tile_size // 3, tile_size // 2)
        painter.drawArc(bow_rect, 20 * 16, 320 * 16)

        # Bowstring
        painter.setPen(QPen(QColor(200, 190, 180), 2))
        painter.drawLine(center_x - tile_size // 6, center_y - tile_size // 5,
                        center_x - tile_size // 6, center_y + tile_size // 6)

        # Nocked arrow
        painter.setBrush(QColor(139, 90, 43))
        painter.setPen(QPen(QColor(100, 60, 30), 1))
        # Arrow shaft
        painter.drawLine(center_x - tile_size // 6, center_y,
                        center_x - tile_size // 3 - 2, center_y)
        # Arrowhead
        arrow_head = [
            QPoint(center_x - tile_size // 3 - 2, center_y),
            QPoint(center_x - tile_size // 4, center_y - 2),
            QPoint(center_x - tile_size // 4, center_y + 2),
        ]
        painter.setBrush(QColor(180, 180, 190))
        painter.drawPolygon(arrow_head)

        # Head with hood/bandana
        head_gradient = QRadialGradient(center_x, center_y - tile_size // 5, tile_size // 5)
        head_gradient.setColorAt(0, color.lighter(120))
        head_gradient.setColorAt(1, color.darker(110))
        painter.setBrush(head_gradient)
        painter.setPen(QPen(color.darker(130), 2))
        painter.drawEllipse(center_x - tile_size // 6, center_y - tile_size // 3,
                           tile_size // 3, tile_size // 3)

        # Bandana/headband
        painter.setBrush(color.darker(120))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(center_x - tile_size // 6, center_y - tile_size // 5,
                        tile_size // 3, tile_size // 16)

        # Face (partial visible)
        painter.setBrush(QColor(220, 180, 150))
        painter.drawEllipse(center_x - tile_size // 12, center_y - tile_size // 8,
                           tile_size // 6, tile_size // 7)

        # Eyes (focused)
        painter.setBrush(QColor(80, 60, 40))
        painter.drawEllipse(center_x - tile_size // 20, center_y - tile_size // 10, 2, 2)
        painter.drawEllipse(center_x + tile_size // 30, center_y - tile_size // 10, 2, 2)

        # Nature leaves floating nearby
        leaf_color = QColor(120, 200, 100, 160)
        painter.setBrush(leaf_color)
        painter.setPen(Qt.PenStyle.NoPen)
        for i in range(2):
            angle = i * math.pi + math.pi / 3
            leaf_x = center_x + int(tile_size // 3 * math.cos(angle))
            leaf_y = center_y + int(tile_size // 4 * math.sin(angle))
            # Small leaf shape
            leaf_points = [
                QPoint(leaf_x, leaf_y - 4),
                QPoint(leaf_x + 3, leaf_y),
                QPoint(leaf_x, leaf_y + 4),
                QPoint(leaf_x - 2, leaf_y),
            ]
            painter.drawPolygon(leaf_points)

    # Restore painter state (undo any flip)
    painter.restore()


def draw_enemy(painter: QPainter, x: float, y: float, tile_size: int, color: QColor, enemy_type: str, facing_direction: tuple = (0, 1)):
    """Draw enemy based on type with directional facing"""
    center_x = int(x * tile_size + tile_size // 2)
    center_y = int(y * tile_size + tile_size // 2)

    # Determine if we need to flip (facing left)
    facing_dx, facing_dy = facing_direction
    flip_horizontal = facing_dx < 0

    # Save painter state
    painter.save()

    # Apply horizontal flip if facing left
    if flip_horizontal:
        painter.translate(center_x * 2, 0)
        painter.scale(-1, 1)

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

    # Restore painter state (undo any flip)
    painter.restore()


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


# Ability icon drawing functions

def draw_ability_fireball(painter: QPainter, center_x: int, center_y: int, size: int):
    """Draw a fireball ability icon with flames and heat"""
    radius = size // 2

    # Outer flame glow
    outer_gradient = QRadialGradient(center_x, center_y, radius * 0.9)
    outer_gradient.setColorAt(0, c.COLOR_ABILITY_FIREBALL.lighter(140))
    outer_gradient.setColorAt(0.4, c.COLOR_ABILITY_FIREBALL)
    outer_gradient.setColorAt(0.7, c.COLOR_ABILITY_FIREBALL_SECONDARY)
    outer_gradient.setColorAt(1, QColor(c.COLOR_ABILITY_FIREBALL_SECONDARY.red(),
                                        c.COLOR_ABILITY_FIREBALL_SECONDARY.green(),
                                        c.COLOR_ABILITY_FIREBALL_SECONDARY.blue(), 0))
    painter.setBrush(outer_gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(center_x - radius, center_y - radius, size, size)

    # Core fire orb
    core_gradient = QRadialGradient(center_x - radius * 0.15, center_y - radius * 0.15, radius * 0.6)
    core_gradient.setColorAt(0, QColor(255, 255, 200))
    core_gradient.setColorAt(0.3, QColor(255, 200, 80))
    core_gradient.setColorAt(0.7, c.COLOR_ABILITY_FIREBALL)
    core_gradient.setColorAt(1, c.COLOR_ABILITY_FIREBALL_SECONDARY)
    painter.setBrush(core_gradient)
    painter.drawEllipse(center_x - int(radius * 0.6), center_y - int(radius * 0.6),
                       int(radius * 1.2), int(radius * 1.2))

    # Flame wisps
    import math
    painter.setPen(Qt.PenStyle.NoPen)
    for i in range(6):
        angle = (i * math.pi / 3) + math.pi / 6
        wisp_dist = radius * 0.7
        wisp_x = center_x + int(wisp_dist * math.cos(angle))
        wisp_y = center_y + int(wisp_dist * math.sin(angle))

        wisp_gradient = QRadialGradient(wisp_x, wisp_y, radius * 0.15)
        wisp_gradient.setColorAt(0, QColor(255, 150, 50, 200))
        wisp_gradient.setColorAt(1, QColor(255, 80, 0, 0))
        painter.setBrush(wisp_gradient)
        painter.drawEllipse(wisp_x - int(radius * 0.15), wisp_y - int(radius * 0.15),
                           int(radius * 0.3), int(radius * 0.3))


def draw_ability_dash(painter: QPainter, center_x: int, center_y: int, size: int):
    """Draw a dash/teleport ability icon with speed lines"""
    radius = size // 2

    # Electric blue glow
    glow_gradient = QRadialGradient(center_x, center_y, radius)
    glow_gradient.setColorAt(0, c.COLOR_ABILITY_DASH.lighter(150))
    glow_gradient.setColorAt(0.5, c.COLOR_ABILITY_DASH)
    glow_gradient.setColorAt(1, QColor(c.COLOR_ABILITY_DASH.red(),
                                       c.COLOR_ABILITY_DASH.green(),
                                       c.COLOR_ABILITY_DASH.blue(), 0))
    painter.setBrush(glow_gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(center_x - radius, center_y - radius, size, size)

    # Speed lines/lightning bolts
    import math
    painter.setPen(QPen(c.COLOR_ABILITY_DASH_SECONDARY, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
    for i in range(8):
        angle = i * math.pi / 4
        # Inner point
        inner_x = center_x + int(radius * 0.3 * math.cos(angle))
        inner_y = center_y + int(radius * 0.3 * math.sin(angle))
        # Outer point
        outer_x = center_x + int(radius * 0.8 * math.cos(angle))
        outer_y = center_y + int(radius * 0.8 * math.sin(angle))

        painter.drawLine(inner_x, inner_y, outer_x, outer_y)

    # Central lightning core
    core_gradient = QRadialGradient(center_x, center_y, radius * 0.35)
    core_gradient.setColorAt(0, QColor(255, 255, 255))
    core_gradient.setColorAt(0.6, c.COLOR_ABILITY_DASH_SECONDARY)
    core_gradient.setColorAt(1, c.COLOR_ABILITY_DASH)
    painter.setBrush(core_gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(center_x - int(radius * 0.35), center_y - int(radius * 0.35),
                       int(radius * 0.7), int(radius * 0.7))


def draw_ability_healing(painter: QPainter, center_x: int, center_y: int, size: int):
    """Draw a healing ability icon with a glowing heart/cross"""
    radius = size // 2

    # Healing green glow
    glow_gradient = QRadialGradient(center_x, center_y, radius)
    glow_gradient.setColorAt(0, c.COLOR_ABILITY_HEALING_SECONDARY)
    glow_gradient.setColorAt(0.5, c.COLOR_ABILITY_HEALING)
    glow_gradient.setColorAt(1, QColor(c.COLOR_ABILITY_HEALING.red(),
                                       c.COLOR_ABILITY_HEALING.green(),
                                       c.COLOR_ABILITY_HEALING.blue(), 0))
    painter.setBrush(glow_gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(center_x - radius, center_y - radius, size, size)

    # Medical cross
    cross_size = radius * 0.7
    cross_thickness = radius * 0.25

    cross_gradient = QLinearGradient(center_x, center_y - cross_size, center_x, center_y + cross_size)
    cross_gradient.setColorAt(0, QColor(255, 255, 255))
    cross_gradient.setColorAt(0.5, c.COLOR_ABILITY_HEALING_SECONDARY)
    cross_gradient.setColorAt(1, c.COLOR_ABILITY_HEALING)

    painter.setBrush(cross_gradient)
    painter.setPen(QPen(c.COLOR_ABILITY_HEALING.darker(120), 2))

    # Vertical bar
    painter.drawRoundedRect(int(center_x - cross_thickness / 2), int(center_y - cross_size),
                           int(cross_thickness), int(cross_size * 2), 3, 3)

    # Horizontal bar
    painter.drawRoundedRect(int(center_x - cross_size), int(center_y - cross_thickness / 2),
                           int(cross_size * 2), int(cross_thickness), 3, 3)

    # Sparkles around the cross
    import math
    painter.setPen(Qt.PenStyle.NoPen)
    for i in range(4):
        angle = (i * math.pi / 2) + math.pi / 4
        sparkle_dist = radius * 0.7
        sparkle_x = center_x + int(sparkle_dist * math.cos(angle))
        sparkle_y = center_y + int(sparkle_dist * math.sin(angle))

        sparkle_points = [
            QPoint(sparkle_x, sparkle_y - 4),
            QPoint(sparkle_x + 1, sparkle_y - 1),
            QPoint(sparkle_x + 4, sparkle_y),
            QPoint(sparkle_x + 1, sparkle_y + 1),
            QPoint(sparkle_x, sparkle_y + 4),
            QPoint(sparkle_x - 1, sparkle_y + 1),
            QPoint(sparkle_x - 4, sparkle_y),
            QPoint(sparkle_x - 1, sparkle_y - 1),
        ]
        painter.setBrush(QColor(255, 255, 255, 180))
        painter.drawPolygon(sparkle_points)


def draw_ability_frost(painter: QPainter, center_x: int, center_y: int, size: int):
    """Draw a frost nova ability icon with ice crystals"""
    radius = size // 2

    # Ice blue glow
    glow_gradient = QRadialGradient(center_x, center_y, radius)
    glow_gradient.setColorAt(0, c.COLOR_ABILITY_FROST_SECONDARY)
    glow_gradient.setColorAt(0.5, c.COLOR_ABILITY_FROST)
    glow_gradient.setColorAt(1, QColor(c.COLOR_ABILITY_FROST.red(),
                                       c.COLOR_ABILITY_FROST.green(),
                                       c.COLOR_ABILITY_FROST.blue(), 0))
    painter.setBrush(glow_gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(center_x - radius, center_y - radius, size, size)

    # Snowflake/ice crystal pattern
    import math
    ice_color = c.COLOR_ABILITY_FROST_SECONDARY
    painter.setPen(QPen(ice_color, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))

    # 6 main spokes of snowflake
    for i in range(6):
        angle = i * math.pi / 3
        end_x = center_x + int(radius * 0.7 * math.cos(angle))
        end_y = center_y + int(radius * 0.7 * math.sin(angle))
        painter.drawLine(center_x, center_y, end_x, end_y)

        # Branches on each spoke
        branch_dist = radius * 0.45
        branch_x = center_x + int(branch_dist * math.cos(angle))
        branch_y = center_y + int(branch_dist * math.sin(angle))

        # Left branch
        branch_angle_l = angle - math.pi / 6
        branch_end_l_x = branch_x + int(radius * 0.25 * math.cos(branch_angle_l))
        branch_end_l_y = branch_y + int(radius * 0.25 * math.sin(branch_angle_l))
        painter.drawLine(branch_x, branch_y, branch_end_l_x, branch_end_l_y)

        # Right branch
        branch_angle_r = angle + math.pi / 6
        branch_end_r_x = branch_x + int(radius * 0.25 * math.cos(branch_angle_r))
        branch_end_r_y = branch_y + int(radius * 0.25 * math.sin(branch_angle_r))
        painter.drawLine(branch_x, branch_y, branch_end_r_x, branch_end_r_y)

    # Central ice crystal
    painter.setBrush(QColor(255, 255, 255, 220))
    painter.setPen(QPen(c.COLOR_ABILITY_FROST, 2))
    painter.drawEllipse(center_x - int(radius * 0.2), center_y - int(radius * 0.2),
                       int(radius * 0.4), int(radius * 0.4))


def draw_ability_whirlwind(painter: QPainter, center_x: int, center_y: int, size: int):
    """Draw a whirlwind ability icon with spinning blades"""
    radius = size // 2

    # Red energy glow
    glow_gradient = QRadialGradient(center_x, center_y, radius)
    glow_gradient.setColorAt(0, c.COLOR_ABILITY_WHIRLWIND_SECONDARY)
    glow_gradient.setColorAt(0.5, c.COLOR_ABILITY_WHIRLWIND)
    glow_gradient.setColorAt(1, QColor(c.COLOR_ABILITY_WHIRLWIND.red(),
                                       c.COLOR_ABILITY_WHIRLWIND.green(),
                                       c.COLOR_ABILITY_WHIRLWIND.blue(), 0))
    painter.setBrush(glow_gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(center_x - radius, center_y - radius, size, size)

    # Spinning blade arcs
    import math
    painter.setPen(Qt.PenStyle.NoPen)

    for i in range(4):
        angle = i * math.pi / 2

        # Create curved blade shape
        blade_points = []
        arc_radius = radius * 0.7

        # Blade path
        for j in range(8):
            t = j / 7.0
            blade_angle = angle + (t * math.pi / 3) - math.pi / 6
            blade_dist = arc_radius * (0.4 + t * 0.4)

            blade_x = center_x + int(blade_dist * math.cos(blade_angle))
            blade_y = center_y + int(blade_dist * math.sin(blade_angle))
            blade_points.append(QPoint(blade_x, blade_y))

        # Create the blade gradient
        blade_gradient = QLinearGradient(QPointF(blade_points[0]), QPointF(blade_points[-1]))
        blade_gradient.setColorAt(0, QColor(200, 200, 220, 250))
        blade_gradient.setColorAt(0.5, QColor(220, 220, 230))
        blade_gradient.setColorAt(1, QColor(180, 180, 200, 100))

        painter.setBrush(blade_gradient)
        painter.setPen(QPen(QColor(150, 150, 160), 2))
        painter.drawPolygon(blade_points)

    # Central hub
    hub_gradient = QRadialGradient(center_x, center_y, radius * 0.25)
    hub_gradient.setColorAt(0, QColor(255, 255, 255))
    hub_gradient.setColorAt(0.6, c.COLOR_ABILITY_WHIRLWIND_SECONDARY)
    hub_gradient.setColorAt(1, c.COLOR_ABILITY_WHIRLWIND)
    painter.setBrush(hub_gradient)
    painter.setPen(QPen(c.COLOR_ABILITY_WHIRLWIND.darker(120), 2))
    painter.drawEllipse(center_x - int(radius * 0.25), center_y - int(radius * 0.25),
                       int(radius * 0.5), int(radius * 0.5))


def draw_ability_shadow(painter: QPainter, center_x: int, center_y: int, size: int):
    """Draw a shadow step ability icon with dagger and smoke"""
    radius = size // 2

    # Dark purple/shadow glow
    glow_gradient = QRadialGradient(center_x, center_y, radius)
    glow_gradient.setColorAt(0, c.COLOR_ABILITY_SHADOW.lighter(130))
    glow_gradient.setColorAt(0.5, c.COLOR_ABILITY_SHADOW)
    glow_gradient.setColorAt(1, QColor(c.COLOR_ABILITY_SHADOW_SECONDARY.red(),
                                       c.COLOR_ABILITY_SHADOW_SECONDARY.green(),
                                       c.COLOR_ABILITY_SHADOW_SECONDARY.blue(), 0))
    painter.setBrush(glow_gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(center_x - radius, center_y - radius, size, size)

    # Shadow wisps/smoke
    import math
    for i in range(5):
        angle = (i * 2 * math.pi / 5) + math.pi / 10
        wisp_dist = radius * 0.6
        wisp_x = center_x + int(wisp_dist * math.cos(angle))
        wisp_y = center_y + int(wisp_dist * math.sin(angle))

        wisp_gradient = QRadialGradient(wisp_x, wisp_y, radius * 0.2)
        wisp_gradient.setColorAt(0, QColor(c.COLOR_ABILITY_SHADOW.red(),
                                           c.COLOR_ABILITY_SHADOW.green(),
                                           c.COLOR_ABILITY_SHADOW.blue(), 180))
        wisp_gradient.setColorAt(1, QColor(c.COLOR_ABILITY_SHADOW_SECONDARY.red(),
                                           c.COLOR_ABILITY_SHADOW_SECONDARY.green(),
                                           c.COLOR_ABILITY_SHADOW_SECONDARY.blue(), 0))
        painter.setBrush(wisp_gradient)
        painter.drawEllipse(wisp_x - int(radius * 0.2), wisp_y - int(radius * 0.2),
                           int(radius * 0.4), int(radius * 0.4))

    # Dagger in center
    dagger_length = radius * 0.8
    dagger_width = radius * 0.15

    # Dagger blade (angled)
    blade_gradient = QLinearGradient(center_x - dagger_width, center_y - dagger_length // 2,
                                     center_x + dagger_width, center_y + dagger_length // 2)
    blade_gradient.setColorAt(0, QColor(200, 200, 220))
    blade_gradient.setColorAt(0.5, QColor(220, 220, 240))
    blade_gradient.setColorAt(1, QColor(180, 180, 200))

    painter.setBrush(blade_gradient)
    painter.setPen(QPen(QColor(150, 150, 170), 2))

    blade_points = [
        QPoint(center_x, int(center_y - dagger_length // 2)),
        QPoint(int(center_x + dagger_width), int(center_y - dagger_length // 4)),
        QPoint(int(center_x + dagger_width // 2), int(center_y + dagger_length // 4)),
        QPoint(int(center_x - dagger_width // 2), int(center_y + dagger_length // 4)),
    ]
    painter.drawPolygon(blade_points)

    # Dagger hilt
    painter.setBrush(c.COLOR_ABILITY_SHADOW.darker(110))
    painter.drawRoundedRect(int(center_x - dagger_width), int(center_y + dagger_length // 4),
                           int(dagger_width * 2), int(dagger_length // 3), 2, 2)

    # Gleam on blade
    painter.setPen(QPen(QColor(255, 255, 255, 200), 2))
    painter.drawLine(center_x, int(center_y - dagger_length // 2.5),
                    int(center_x + dagger_width // 2), int(center_y - dagger_length // 6))
