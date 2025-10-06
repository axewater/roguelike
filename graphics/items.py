"""
Item rendering by type
"""
from PyQt6.QtGui import QPainter, QPen, QRadialGradient, QLinearGradient, QColor, QPainterPath
from PyQt6.QtCore import Qt, QPoint, QPointF
import constants as c
from graphics.utils import draw_gem, draw_rune, draw_metallic_gradient, draw_sparkle
import math


def draw_item(painter: QPainter, x: float, y: float, tile_size: int, color: QColor, item_type: str, rarity: str = c.RARITY_COMMON):
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
        # Enhanced potion with rarity-based details
        bottle_width = tile_size // 3
        bottle_height = int(tile_size * 0.4)
        neck_width = tile_size // 6
        neck_height = tile_size // 8

        # Determine liquid color based on rarity
        if rarity == c.RARITY_COMMON:
            liquid_color = QColor(220, 50, 50)
            liquid_top = QColor(255, 80, 80)
        elif rarity == c.RARITY_UNCOMMON:
            liquid_color = QColor(80, 220, 100)
            liquid_top = QColor(120, 255, 140)
        elif rarity == c.RARITY_RARE:
            liquid_color = QColor(80, 120, 255)
            liquid_top = QColor(140, 180, 255)
        elif rarity == c.RARITY_EPIC:
            liquid_color = QColor(200, 80, 255)
            liquid_top = QColor(240, 140, 255)
        else:  # LEGENDARY
            liquid_color = QColor(255, 180, 0)
            liquid_top = QColor(255, 220, 100)

        # Bottle body with gradient
        bottle_gradient = QLinearGradient(center_x - bottle_width // 2, center_y - bottle_height // 2,
                                         center_x + bottle_width // 2, center_y + bottle_height // 2)
        bottle_gradient.setColorAt(0, QColor(200, 220, 240, 100))
        bottle_gradient.setColorAt(0.5, QColor(180, 200, 220, 120))
        bottle_gradient.setColorAt(1, QColor(160, 180, 200, 140))

        painter.setBrush(bottle_gradient)
        painter.setPen(QPen(QColor(140, 160, 180), 2))
        painter.drawRoundedRect(center_x - bottle_width // 2, center_y - bottle_height // 2,
                               bottle_width, bottle_height, 4, 4)

        # Liquid with gradient (swirling effect)
        liquid_gradient = QLinearGradient(center_x, center_y - bottle_height // 2 + 2,
                                         center_x, center_y + bottle_height // 2 - 2)
        liquid_gradient.setColorAt(0, liquid_top)
        liquid_gradient.setColorAt(0.6, liquid_color)
        liquid_gradient.setColorAt(1, liquid_color.darker(120))

        painter.setBrush(liquid_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(center_x - bottle_width // 2 + 3, center_y - bottle_height // 2 + 3,
                               bottle_width - 6, bottle_height - 6, 3, 3)

        # Bubbles for uncommon+
        if rarity in [c.RARITY_UNCOMMON, c.RARITY_RARE]:
            painter.setBrush(QColor(255, 255, 255, 100))
            painter.drawEllipse(center_x - tile_size // 16, center_y, 4, 4)
            painter.drawEllipse(center_x + tile_size // 20, center_y - tile_size // 16, 3, 3)
        elif rarity in [c.RARITY_EPIC, c.RARITY_LEGENDARY]:
            # More bubbles
            painter.setBrush(QColor(255, 255, 255, 120))
            for i, (bx, by, bs) in enumerate([(0, 0, 4), (tile_size // 20, -tile_size // 20, 3),
                                              (-tile_size // 24, tile_size // 24, 3)]):
                painter.drawEllipse(center_x + bx - bs // 2, center_y + by - bs // 2, bs, bs)

        # Bottle neck
        neck_gradient = QLinearGradient(center_x - neck_width // 2, center_y - bottle_height // 2,
                                       center_x + neck_width // 2, center_y - bottle_height // 2 - neck_height)
        neck_gradient.setColorAt(0, QColor(180, 200, 220, 120))
        neck_gradient.setColorAt(1, QColor(200, 220, 240, 100))

        painter.setBrush(neck_gradient)
        painter.setPen(QPen(QColor(140, 160, 180), 2))
        painter.drawRect(center_x - neck_width // 2, center_y - bottle_height // 2 - neck_height,
                        neck_width, neck_height)

        # Cork with rarity-based detail
        cork_color = QColor(139, 90, 43) if rarity == c.RARITY_COMMON else QColor(180, 140, 90)
        painter.setBrush(cork_color)
        painter.setPen(QPen(cork_color.darker(130), 1))
        cork_height = tile_size // 12
        painter.drawRoundedRect(center_x - tile_size // 10, center_y - bottle_height // 2 - neck_height - cork_height,
                               tile_size // 5, cork_height, 2, 2)

        # Wax seal for rare+
        if rarity in [c.RARITY_RARE, c.RARITY_EPIC, c.RARITY_LEGENDARY]:
            seal_color = QColor(180, 30, 30) if rarity == c.RARITY_RARE else QColor(200, 150, 0)
            painter.setBrush(seal_color)
            painter.setPen(Qt.PenStyle.NoPen)
            # Wax drip
            painter.drawEllipse(center_x - tile_size // 12, center_y - bottle_height // 2 - neck_height - 2,
                               tile_size // 6, 4)

        # Rune on bottle for epic+
        if rarity == c.RARITY_EPIC:
            draw_rune(painter, center_x, center_y, tile_size // 12, QColor(200, 100, 255), "circle")
        elif rarity == c.RARITY_LEGENDARY:
            draw_rune(painter, center_x, center_y, tile_size // 10, QColor(255, 215, 0), "star")
            # Extra sparkles
            draw_sparkle(painter, center_x + tile_size // 5, center_y - tile_size // 6, tile_size // 16,
                        QColor(255, 255, 200))

        # Glass highlights (all rarities)
        painter.setBrush(QColor(255, 255, 255, 180))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - bottle_width // 4, center_y - bottle_height // 3, 4, 8)
        painter.drawEllipse(center_x - bottle_width // 3, center_y, 3, 4)

    elif item_type == c.ITEM_SWORD:
        # Enhanced sword with rarity-based details
        blade_length = tile_size // 2
        blade_width = tile_size // 6

        # Determine blade material and color based on rarity
        if rarity == c.RARITY_COMMON:
            blade_base = QColor(160, 160, 160)  # Iron
            crossguard_color = QColor(100, 100, 100)
            has_gem = False
            has_runes = False
            blade_glow = False
        elif rarity == c.RARITY_UNCOMMON:
            blade_base = QColor(180, 180, 180)  # Steel
            crossguard_color = QColor(180, 140, 80)  # Brass
            has_gem = False
            has_runes = False
            blade_glow = False
        elif rarity == c.RARITY_RARE:
            blade_base = QColor(200, 200, 210)  # Silver steel
            crossguard_color = QColor(192, 192, 192)
            has_gem = True
            has_runes = False
            blade_glow = False
        elif rarity == c.RARITY_EPIC:
            blade_base = QColor(210, 210, 220)
            crossguard_color = QColor(220, 180, 100)  # Gold
            has_gem = True
            has_runes = True
            blade_glow = True
            glow_color = QColor(150, 100, 255)
        else:  # LEGENDARY
            blade_base = QColor(220, 220, 240)
            crossguard_color = QColor(255, 215, 0)
            has_gem = True
            has_runes = True
            blade_glow = True
            glow_color = QColor(100, 200, 255)

        # Blade glow for epic+
        if blade_glow:
            glow = QRadialGradient(center_x, center_y - blade_length // 4, blade_length)
            glow.setColorAt(0, QColor(glow_color.red(), glow_color.green(), glow_color.blue(), 100))
            glow.setColorAt(0.5, QColor(glow_color.red(), glow_color.green(), glow_color.blue(), 40))
            glow.setColorAt(1, QColor(glow_color.red(), glow_color.green(), glow_color.blue(), 0))
            painter.setBrush(glow)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(center_x - blade_length, center_y - blade_length,
                               blade_length * 2, blade_length * 2)

        # Blade with metallic gradient
        blade_gradient = draw_metallic_gradient(blade_base, center_x - blade_width // 2,
                                               center_y - blade_length, center_x + blade_width // 2,
                                               center_y)
        painter.setBrush(blade_gradient)
        painter.setPen(QPen(blade_base.darker(150), 2))

        # Blade shape with point
        blade_points = [
            QPointF(center_x, center_y - blade_length),
            QPointF(center_x + blade_width // 2, center_y - blade_length + blade_width),
            QPointF(center_x + blade_width // 3, center_y + tile_size // 10),
            QPointF(center_x - blade_width // 3, center_y + tile_size // 10),
            QPointF(center_x - blade_width // 2, center_y - blade_length + blade_width),
        ]
        painter.drawPolygon(blade_points)

        # Fuller (groove down center)
        painter.setPen(QPen(blade_base.darker(110), 1))
        painter.drawLine(center_x, center_y - blade_length + blade_width + 2,
                        center_x, center_y + tile_size // 12)

        # Runes on blade for epic+
        if has_runes:
            rune_color = QColor(150, 100, 255) if rarity == c.RARITY_EPIC else QColor(100, 200, 255)
            draw_rune(painter, center_x, center_y - blade_length // 2, tile_size // 16, rune_color, "cross")
            if rarity == c.RARITY_LEGENDARY:
                draw_rune(painter, center_x, center_y - blade_length // 4, tile_size // 16, rune_color, "circle")

        # Crossguard with ornate design
        crossguard_y = center_y + tile_size // 10
        crossguard_gradient = draw_metallic_gradient(crossguard_color, center_x - tile_size // 4,
                                                     crossguard_y, center_x + tile_size // 4, crossguard_y + tile_size // 12)
        painter.setBrush(crossguard_gradient)
        painter.setPen(QPen(crossguard_color.darker(140), 2))

        if rarity in [c.RARITY_COMMON, c.RARITY_UNCOMMON]:
            # Simple crossguard
            painter.drawRect(center_x - tile_size // 4, crossguard_y, tile_size // 2, tile_size // 12)
        else:
            # Ornate curved crossguard
            path = QPainterPath()
            path.moveTo(center_x - tile_size // 4, crossguard_y + tile_size // 24)
            path.quadTo(center_x - tile_size // 5, crossguard_y - tile_size // 48,
                       center_x, crossguard_y + tile_size // 24)
            path.quadTo(center_x + tile_size // 5, crossguard_y + tile_size // 16,
                       center_x + tile_size // 4, crossguard_y + tile_size // 24)
            path.lineTo(center_x + tile_size // 4, crossguard_y + tile_size // 12)
            path.lineTo(center_x - tile_size // 4, crossguard_y + tile_size // 12)
            path.closeSubpath()
            painter.drawPath(path)

        # Handle
        handle_y = crossguard_y + tile_size // 12
        handle_height = tile_size // 5
        handle_color = QColor(100, 60, 30) if rarity == c.RARITY_COMMON else QColor(80, 40, 20)
        handle_gradient = QLinearGradient(center_x - tile_size // 12, handle_y,
                                         center_x + tile_size // 12, handle_y + handle_height)
        handle_gradient.setColorAt(0, handle_color.lighter(120))
        handle_gradient.setColorAt(0.5, handle_color)
        handle_gradient.setColorAt(1, handle_color.darker(110))

        painter.setBrush(handle_gradient)
        painter.setPen(QPen(handle_color.darker(130), 1))
        painter.drawRoundedRect(center_x - tile_size // 12, handle_y, tile_size // 6, handle_height, 2, 2)

        # Wrapped grip lines
        painter.setPen(QPen(handle_color.darker(150), 1))
        for i in range(3):
            y = handle_y + (i + 1) * handle_height // 4
            painter.drawLine(center_x - tile_size // 12, y, center_x + tile_size // 12, y)

        # Pommel with gem for rare+
        pommel_y = handle_y + handle_height
        painter.setBrush(crossguard_gradient)
        painter.setPen(QPen(crossguard_color.darker(130), 1))
        painter.drawEllipse(center_x - tile_size // 10, pommel_y, tile_size // 5, tile_size // 10)

        if has_gem:
            gem_color = color if rarity == c.RARITY_RARE else QColor(200, 50, 255)
            gem_size = 6 if rarity == c.RARITY_RARE else 8
            cut = "round" if rarity == c.RARITY_RARE else "star"
            draw_gem(painter, center_x, pommel_y + tile_size // 20, gem_size, gem_color, cut)

        # Blade gleam/highlight
        painter.setPen(QPen(QColor(255, 255, 255, 200), 2))
        painter.drawLine(center_x + blade_width // 6, center_y - blade_length + blade_width,
                        center_x + blade_width // 8, center_y - tile_size // 16)

        # Legendary sparkles
        if rarity == c.RARITY_LEGENDARY:
            draw_sparkle(painter, center_x - blade_width // 4, center_y - blade_length * 2 // 3,
                        tile_size // 20, QColor(200, 230, 255))

    elif item_type == c.ITEM_SHIELD:
        # Enhanced shield with rarity-based details
        shield_size = tile_size // 2

        # Determine shield material and details based on rarity
        if rarity == c.RARITY_COMMON:
            shield_color = color.darker(110)
            rim_color = QColor(100, 100, 100)
            has_emblem = False
            has_gems = False
            has_runes = False
            studs = True
        elif rarity == c.RARITY_UNCOMMON:
            shield_color = color
            rim_color = QColor(180, 140, 80)  # Brass
            has_emblem = True
            emblem_type = "cross"
            has_gems = False
            has_runes = False
            studs = True
        elif rarity == c.RARITY_RARE:
            shield_color = color.lighter(110)
            rim_color = QColor(192, 192, 192)  # Silver
            has_emblem = True
            emblem_type = "star"
            has_gems = True
            gem_count = 4
            has_runes = False
            studs = False
        elif rarity == c.RARITY_EPIC:
            shield_color = color.lighter(120)
            rim_color = QColor(220, 180, 100)  # Gold
            has_emblem = True
            emblem_type = "spiral"
            has_gems = True
            gem_count = 4
            has_runes = True
            studs = False
        else:  # LEGENDARY
            shield_color = color.lighter(130)
            rim_color = QColor(255, 215, 0)
            has_emblem = True
            emblem_type = "star"
            has_gems = True
            gem_count = 5
            has_runes = True
            studs = False

        # Shield body - kite shape
        shield_gradient = draw_metallic_gradient(shield_color, center_x - shield_size // 2,
                                                center_y - shield_size // 2, center_x + shield_size // 2,
                                                center_y + shield_size // 2)
        painter.setBrush(shield_gradient)
        painter.setPen(QPen(shield_color.darker(140), 2))

        shield_points = [
            QPointF(center_x, center_y - shield_size * 0.65),
            QPointF(center_x + shield_size * 0.5, center_y - shield_size * 0.3),
            QPointF(center_x + shield_size * 0.5, center_y + shield_size * 0.2),
            QPointF(center_x, center_y + shield_size * 0.65),
            QPointF(center_x - shield_size * 0.5, center_y + shield_size * 0.2),
            QPointF(center_x - shield_size * 0.5, center_y - shield_size * 0.3),
        ]
        painter.drawPolygon(shield_points)

        # Metal studs for common/uncommon
        if studs:
            painter.setBrush(rim_color)
            painter.setPen(QPen(rim_color.darker(130), 1))
            stud_positions = [
                (0, -shield_size * 0.5), (shield_size * 0.35, -shield_size * 0.2),
                (shield_size * 0.35, shield_size * 0.1), (0, shield_size * 0.5),
                (-shield_size * 0.35, shield_size * 0.1), (-shield_size * 0.35, -shield_size * 0.2)
            ]
            for sx, sy in stud_positions:
                painter.drawEllipse(int(center_x + sx - 3), int(center_y + sy - 3), 6, 6)

        # Decorative rim
        rim_gradient = draw_metallic_gradient(rim_color, center_x - shield_size // 2, center_y,
                                             center_x + shield_size // 2, center_y)
        painter.setBrush(rim_gradient)
        painter.setPen(QPen(rim_color.darker(150), 2))

        # Rim border
        if rarity in [c.RARITY_RARE, c.RARITY_EPIC, c.RARITY_LEGENDARY]:
            painter.setPen(QPen(rim_color, 4))
            path = QPainterPath()
            path.moveTo(shield_points[0])
            for p in shield_points[1:]:
                path.lineTo(p)
            path.closeSubpath()
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)

        # Shield boss (center piece)
        boss_size = shield_size // 3
        boss_gradient = QRadialGradient(center_x, center_y, boss_size // 2)
        boss_gradient.setColorAt(0, rim_color.lighter(140))
        boss_gradient.setColorAt(0.5, rim_color)
        boss_gradient.setColorAt(1, rim_color.darker(120))

        painter.setBrush(boss_gradient)
        painter.setPen(QPen(rim_color.darker(150), 2))
        painter.drawEllipse(center_x - boss_size // 2, center_y - boss_size // 2, boss_size, boss_size)

        # Emblem on boss
        if has_emblem:
            emblem_color = rim_color.lighter(150)
            draw_rune(painter, center_x, center_y, boss_size // 3, emblem_color, emblem_type)

        # Corner gems for rare+
        if has_gems:
            gem_positions = [
                (0, -shield_size * 0.5),
                (shield_size * 0.35, -shield_size * 0.15),
                (shield_size * 0.35, shield_size * 0.15),
                (-shield_size * 0.35, shield_size * 0.15),
                (-shield_size * 0.35, -shield_size * 0.15),
            ]
            gem_color = color.lighter(150)
            for i in range(min(gem_count, len(gem_positions))):
                gx, gy = gem_positions[i]
                draw_gem(painter, center_x + gx, center_y + gy, 6, gem_color, "round")

        # Runes around edge for epic+
        if has_runes:
            rune_color = QColor(150, 100, 255) if rarity == c.RARITY_EPIC else QColor(100, 200, 255)
            rune_positions = [
                (shield_size * 0.25, -shield_size * 0.4),
                (shield_size * 0.25, shield_size * 0.1),
                (-shield_size * 0.25, shield_size * 0.1),
                (-shield_size * 0.25, -shield_size * 0.4),
            ]
            for rx, ry in rune_positions:
                draw_rune(painter, center_x + rx, center_y + ry, tile_size // 20, rune_color, "circle")

        # Energy field for legendary
        if rarity == c.RARITY_LEGENDARY:
            field = QRadialGradient(center_x, center_y, shield_size)
            field.setColorAt(0, QColor(100, 200, 255, 0))
            field.setColorAt(0.7, QColor(100, 200, 255, 40))
            field.setColorAt(1, QColor(100, 200, 255, 0))
            painter.setBrush(field)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(center_x - shield_size, center_y - shield_size,
                               shield_size * 2, shield_size * 2)
            draw_sparkle(painter, center_x + shield_size * 0.4, center_y - shield_size * 0.3,
                        tile_size // 18, QColor(200, 230, 255))

    elif item_type == c.ITEM_BOOTS:
        # Enhanced boots with rarity-based details
        boot_width = tile_size // 5
        boot_height = tile_size // 3

        # Determine boot material and details based on rarity
        if rarity == c.RARITY_COMMON:
            boot_color = QColor(101, 67, 33)  # Brown leather
            trim_color = QColor(70, 45, 20)
            has_buckles = False
            has_gems = False
            has_wings = False
            has_runes = False
            worn = True
        elif rarity == c.RARITY_UNCOMMON:
            boot_color = QColor(120, 80, 40)  # Better leather
            trim_color = QColor(180, 140, 80)  # Brass
            has_buckles = True
            has_gems = False
            has_wings = False
            has_runes = False
            worn = False
        elif rarity == c.RARITY_RARE:
            boot_color = QColor(80, 60, 40)  # Fine leather
            trim_color = QColor(192, 192, 192)  # Silver
            has_buckles = True
            has_gems = True
            has_wings = True
            wing_style = "small"
            has_runes = False
            worn = False
        elif rarity == c.RARITY_EPIC:
            boot_color = QColor(60, 40, 60)  # Enchanted leather
            trim_color = QColor(220, 180, 100)  # Gold
            has_buckles = True
            has_gems = True
            has_wings = True
            wing_style = "large"
            has_runes = True
            worn = False
        else:  # LEGENDARY
            boot_color = QColor(40, 60, 80)  # Magical material
            trim_color = QColor(255, 215, 0)
            has_buckles = True
            has_gems = True
            has_wings = True
            wing_style = "ethereal"
            has_runes = True
            worn = False

        # Function to draw a single boot
        def draw_boot(boot_x):
            # Boot body with gradient
            boot_gradient = QLinearGradient(boot_x, center_y - boot_height // 2,
                                           boot_x + boot_width, center_y + boot_height // 2)
            boot_gradient.setColorAt(0, boot_color.lighter(120))
            boot_gradient.setColorAt(0.5, boot_color)
            boot_gradient.setColorAt(1, boot_color.darker(120))

            painter.setBrush(boot_gradient)
            painter.setPen(QPen(trim_color, 2))
            painter.drawRoundedRect(boot_x, center_y - boot_height // 2,
                                   boot_width, boot_height, 3, 3)

            # Sole
            painter.setBrush(trim_color.darker(130))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(boot_x, center_y + boot_height // 2 - 3, boot_width, 3)

            # Toe cap
            painter.setBrush(trim_color)
            painter.drawRoundedRect(boot_x, center_y + boot_height // 4,
                                   boot_width, boot_height // 5, 2, 2)

            # Decorative stitching
            painter.setPen(QPen(boot_color.lighter(130), 1))
            painter.drawLine(boot_x + 2, center_y - boot_height // 4,
                           boot_x + boot_width - 2, center_y - boot_height // 4)

            # Buckles vs Laces
            if has_buckles:
                # Metal buckles
                painter.setBrush(trim_color)
                painter.setPen(QPen(trim_color.darker(130), 1))
                for i in range(2):
                    buckle_y = center_y - boot_height // 6 + i * boot_height // 4
                    painter.drawRect(boot_x + boot_width // 4, buckle_y, boot_width // 2, 3)
                    painter.drawRect(boot_x + boot_width // 3, buckle_y - 1, 3, 5)
            else:
                # Simple laces
                painter.setPen(QPen(QColor(240, 230, 140), 1))
                for i in range(3):
                    lace_y = center_y - boot_height // 8 + i * boot_height // 5
                    painter.drawLine(boot_x + 3, lace_y, boot_x + boot_width - 3, lace_y)

            # Wear marks for common
            if worn:
                painter.setPen(QPen(boot_color.darker(140), 1))
                for i in range(2):
                    wx = boot_x + boot_width // 4 + i * boot_width // 3
                    painter.drawLine(wx, center_y, wx + boot_width // 8, center_y + 2)

            # Gems on toe for rare+
            if has_gems:
                gem_color = color.lighter(140)
                draw_gem(painter, boot_x + boot_width // 2, center_y + boot_height // 3,
                        4, gem_color, "round")

            # Glowing seams for epic+
            if has_runes:
                rune_color = QColor(150, 100, 255) if rarity == c.RARITY_EPIC else QColor(100, 200, 255)
                painter.setPen(QPen(rune_color, 1))
                painter.drawLine(boot_x + 2, center_y - boot_height // 3,
                               boot_x + 2, center_y + boot_height // 3)

            # Wing decorations for rare+
            if has_wings:
                wing_color = trim_color if wing_style == "small" else QColor(200, 220, 255, 180)
                wing_base_x = boot_x + boot_width
                wing_base_y = center_y

                if wing_style == "small":
                    # Small decorative wing
                    wing_points = [
                        QPointF(wing_base_x, wing_base_y),
                        QPointF(wing_base_x + boot_width // 4, wing_base_y - boot_height // 6),
                        QPointF(wing_base_x + boot_width // 3, wing_base_y),
                        QPointF(wing_base_x + boot_width // 4, wing_base_y + boot_height // 8),
                    ]
                    painter.setBrush(wing_color)
                    painter.setPen(QPen(wing_color.darker(120), 1))
                    painter.drawPolygon(wing_points)
                elif wing_style == "large":
                    # Larger wing with feathers
                    wing_points = [
                        QPointF(wing_base_x, wing_base_y),
                        QPointF(wing_base_x + boot_width // 3, wing_base_y - boot_height // 4),
                        QPointF(wing_base_x + boot_width // 2, wing_base_y - boot_height // 6),
                        QPointF(wing_base_x + boot_width // 2, wing_base_y + boot_height // 8),
                        QPointF(wing_base_x + boot_width // 3, wing_base_y + boot_height // 5),
                    ]
                    painter.setBrush(QColor(220, 180, 100))
                    painter.setPen(QPen(QColor(180, 140, 60), 1))
                    painter.drawPolygon(wing_points)
                    # Feather details
                    painter.setPen(QPen(QColor(200, 160, 80), 1))
                    painter.drawLine(int(wing_base_x + boot_width // 6), int(wing_base_y - boot_height // 8),
                                   int(wing_base_x + boot_width // 3), int(wing_base_y - boot_height // 5))
                else:  # ethereal
                    # Magical ethereal wings
                    for offset in range(3):
                        alpha = 100 - offset * 30
                        glow_color = QColor(100, 200, 255, alpha)
                        wing_points = [
                            QPointF(wing_base_x, wing_base_y),
                            QPointF(wing_base_x + boot_width // 2 + offset * 2, wing_base_y - boot_height // 3),
                            QPointF(wing_base_x + boot_width // 2 + offset * 3, wing_base_y),
                            QPointF(wing_base_x + boot_width // 2 + offset * 2, wing_base_y + boot_height // 4),
                        ]
                        painter.setBrush(glow_color)
                        painter.setPen(Qt.PenStyle.NoPen)
                        painter.drawPolygon(wing_points)

        # Draw both boots
        draw_boot(center_x - tile_size // 4)
        draw_boot(center_x + tile_size // 20)

        # Legendary trail effect
        if rarity == c.RARITY_LEGENDARY:
            # Magical footprint glow
            trail = QRadialGradient(center_x, center_y + boot_height // 2, tile_size // 4)
            trail.setColorAt(0, QColor(100, 200, 255, 80))
            trail.setColorAt(0.5, QColor(100, 200, 255, 40))
            trail.setColorAt(1, QColor(100, 200, 255, 0))
            painter.setBrush(trail)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(center_x - tile_size // 4, center_y + boot_height // 3,
                               tile_size // 2, tile_size // 6)
            draw_sparkle(painter, center_x + tile_size // 6, center_y - boot_height // 4,
                        tile_size // 20, QColor(200, 230, 255))

    elif item_type == c.ITEM_RING:
        # Enhanced ring with rarity-based details
        ring_size = tile_size // 3

        # Determine ring material and details based on rarity
        if rarity == c.RARITY_COMMON:
            band_color = QColor(100, 100, 100)  # Iron
            gem_color = QColor(150, 150, 150)  # Dull stone
            gem_cut = "round"
            gem_size = 8
            has_filigree = False
            has_accent_gems = False
            has_runes = False
            gem_glow = False
        elif rarity == c.RARITY_UNCOMMON:
            band_color = QColor(180, 140, 80)  # Bronze
            gem_color = color.lighter(120)
            gem_cut = "oval"
            gem_size = 10
            has_filigree = False
            has_accent_gems = False
            has_runes = False
            gem_glow = False
        elif rarity == c.RARITY_RARE:
            band_color = QColor(192, 192, 192)  # Silver
            gem_color = color.lighter(130)
            gem_cut = "emerald"
            gem_size = 12
            has_filigree = True
            has_accent_gems = False
            has_runes = False
            gem_glow = True
            glow_color = color
        elif rarity == c.RARITY_EPIC:
            band_color = QColor(220, 180, 100)  # Gold
            gem_color = QColor(200, 100, 255)
            gem_cut = "star"
            gem_size = 14
            has_filigree = True
            has_accent_gems = True
            has_runes = False
            gem_glow = True
            glow_color = QColor(200, 100, 255)
        else:  # LEGENDARY
            band_color = QColor(255, 215, 0)  # Pure gold
            gem_color = QColor(100, 200, 255)
            gem_cut = "star"
            gem_size = 16
            has_filigree = True
            has_accent_gems = True
            has_runes = True
            gem_glow = True
            glow_color = QColor(100, 200, 255)

        # Ring viewed at an angle (perspective)
        band_width = ring_size
        band_height = ring_size // 3

        # Gem glow for rare+
        if gem_glow:
            gem_glow_grad = QRadialGradient(center_x, center_y - ring_size // 4, ring_size)
            gem_glow_grad.setColorAt(0, QColor(glow_color.red(), glow_color.green(), glow_color.blue(), 100))
            gem_glow_grad.setColorAt(0.5, QColor(glow_color.red(), glow_color.green(), glow_color.blue(), 50))
            gem_glow_grad.setColorAt(1, QColor(glow_color.red(), glow_color.green(), glow_color.blue(), 0))
            painter.setBrush(gem_glow_grad)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(center_x - ring_size, center_y - ring_size,
                               ring_size * 2, ring_size * 2)

        # Band with metallic gradient (ellipse for perspective)
        band_gradient = draw_metallic_gradient(band_color, center_x - band_width // 2, center_y,
                                              center_x + band_width // 2, center_y + band_height)
        painter.setBrush(band_gradient)
        painter.setPen(QPen(band_color.darker(150), 2))

        # Outer ellipse (band outer edge)
        painter.drawEllipse(center_x - band_width // 2, center_y,
                           band_width, band_height)

        # Inner ellipse (band inner edge) - slightly smaller
        inner_width = band_width - 8
        inner_height = band_height - 4
        painter.setBrush(QColor(40, 40, 40))
        painter.setPen(QPen(band_color.darker(180), 1))
        painter.drawEllipse(center_x - inner_width // 2, center_y + 2,
                           inner_width, inner_height)

        # Filigree pattern on band for rare+
        if has_filigree:
            painter.setPen(QPen(band_color.lighter(140), 1))
            # Draw ornate pattern on band
            for i in range(5):
                angle = i * math.pi / 2.5
                x1 = center_x + (band_width // 2 - 4) * math.cos(angle)
                y1 = center_y + band_height // 2 + (band_height // 2 - 2) * math.sin(angle)
                painter.drawPoint(int(x1), int(y1))

            # Decorative lines
            painter.drawArc(center_x - band_width // 2 + 2, center_y + 1,
                           band_width - 4, band_height - 2, 0, 180 * 16)

        # Band top section with highlight
        top_band_gradient = draw_metallic_gradient(band_color, center_x - band_width // 2,
                                                   center_y - ring_size // 3,
                                                   center_x + band_width // 2,
                                                   center_y + ring_size // 6)
        painter.setBrush(top_band_gradient)
        painter.setPen(QPen(band_color.darker(140), 2))

        # Top band sections (sides)
        left_band = [
            QPointF(center_x - band_width // 2, center_y + band_height // 2),
            QPointF(center_x - band_width // 3, center_y - ring_size // 6),
            QPointF(center_x - band_width // 4, center_y - ring_size // 6),
            QPointF(center_x - band_width // 2 + 4, center_y + band_height // 2),
        ]
        painter.drawPolygon(left_band)

        right_band = [
            QPointF(center_x + band_width // 2, center_y + band_height // 2),
            QPointF(center_x + band_width // 3, center_y - ring_size // 6),
            QPointF(center_x + band_width // 4, center_y - ring_size // 6),
            QPointF(center_x + band_width // 2 - 4, center_y + band_height // 2),
        ]
        painter.drawPolygon(right_band)

        # Gem setting (prongs)
        setting_color = band_color.lighter(110)
        painter.setBrush(setting_color)
        painter.setPen(QPen(setting_color.darker(130), 1))

        # Top setting platform
        setting_width = gem_size + 4
        painter.drawEllipse(center_x - setting_width // 2, center_y - ring_size // 4 - 2,
                           setting_width, 4)

        # Prongs
        prong_positions = [
            (-gem_size // 2 - 1, 0), (gem_size // 2 + 1, 0),
            (0, -gem_size // 2 - 1), (0, gem_size // 2 + 1)
        ]
        for px, py in prong_positions:
            painter.drawLine(center_x + px, center_y - ring_size // 4,
                           center_x + px, center_y - ring_size // 4 - 3)

        # Main gemstone
        draw_gem(painter, center_x, center_y - ring_size // 4, gem_size, gem_color, gem_cut)

        # Accent gems for epic+
        if has_accent_gems:
            accent_size = 4
            accent_color = gem_color.lighter(120)
            # Two small gems on band
            draw_gem(painter, center_x - band_width // 4, center_y - ring_size // 12,
                    accent_size, accent_color, "round")
            draw_gem(painter, center_x + band_width // 4, center_y - ring_size // 12,
                    accent_size, accent_color, "round")

        # Runes on band for legendary
        if has_runes:
            rune_color = QColor(100, 200, 255)
            draw_rune(painter, center_x - band_width // 3, center_y + band_height // 3,
                     tile_size // 24, rune_color, "circle")
            draw_rune(painter, center_x + band_width // 3, center_y + band_height // 3,
                     tile_size // 24, rune_color, "circle")

        # Sparkles for legendary
        if rarity == c.RARITY_LEGENDARY:
            # Orbiting sparkles
            for i in range(3):
                angle = i * 2 * math.pi / 3
                sx = center_x + ring_size * 0.6 * math.cos(angle)
                sy = center_y - ring_size // 4 + ring_size * 0.3 * math.sin(angle)
                draw_sparkle(painter, sx, sy, tile_size // 24, QColor(200, 230, 255))

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
