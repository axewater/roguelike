"""
Enemy rendering by type
"""
from PyQt6.QtGui import QPainter, QPen, QBrush, QLinearGradient, QRadialGradient, QColor
from PyQt6.QtCore import Qt, QPoint, QRect
import constants as c
import math


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
        # GOBLIN - Wicked Trickster with hunched posture

        # Hunched body (smaller, lower)
        body_gradient = QLinearGradient(center_x, center_y,
                                        center_x, center_y + tile_size // 3)
        body_gradient.setColorAt(0, color.lighter(110))
        body_gradient.setColorAt(1, color.darker(120))
        painter.setBrush(body_gradient)
        painter.setPen(QPen(color.darker(150), 2))
        painter.drawEllipse(center_x - tile_size // 6, center_y + tile_size // 12,
                           tile_size // 3, tile_size // 4)

        # Tattered loincloth
        loincloth_color = color.darker(140)
        painter.setBrush(loincloth_color)
        painter.setPen(Qt.PenStyle.NoPen)
        loincloth = [
            QPoint(center_x - tile_size // 8, center_y + tile_size // 8),
            QPoint(center_x - tile_size // 6, center_y + tile_size // 3),
            QPoint(center_x - tile_size // 12, center_y + tile_size // 3 - 2),
            QPoint(center_x, center_y + tile_size // 4),
            QPoint(center_x + tile_size // 12, center_y + tile_size // 3 - 2),
            QPoint(center_x + tile_size // 6, center_y + tile_size // 3),
            QPoint(center_x + tile_size // 8, center_y + tile_size // 8),
        ]
        painter.drawPolygon(loincloth)

        # Hunched oversized head
        head_gradient = QRadialGradient(center_x, center_y - tile_size // 8, tile_size // 3)
        head_gradient.setColorAt(0, color.lighter(120))
        head_gradient.setColorAt(0.7, color)
        head_gradient.setColorAt(1, color.darker(110))
        painter.setBrush(head_gradient)
        painter.setPen(QPen(color.darker(140), 2))
        painter.drawEllipse(center_x - tile_size // 4, center_y - tile_size // 3,
                           tile_size // 2, tile_size * 2 // 5)

        # Warty skin details (dark spots)
        painter.setBrush(color.darker(180))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 6, center_y - tile_size // 6, 3, 3)
        painter.drawEllipse(center_x + tile_size // 8, center_y - tile_size // 5, 2, 2)
        painter.drawEllipse(center_x - tile_size // 12, center_y - tile_size // 8, 2, 2)

        # Large bat-like ears (signature feature)
        ear_color = color.darker(110)
        painter.setBrush(ear_color)
        painter.setPen(QPen(color.darker(150), 1))
        # Left ear
        left_ear = [
            QPoint(center_x - tile_size // 5, center_y - tile_size // 4),
            QPoint(center_x - tile_size // 3, center_y - tile_size // 3),
            QPoint(center_x - tile_size // 4, center_y - tile_size // 6),
        ]
        painter.drawPolygon(left_ear)
        # Right ear
        right_ear = [
            QPoint(center_x + tile_size // 5, center_y - tile_size // 4),
            QPoint(center_x + tile_size // 3, center_y - tile_size // 3),
            QPoint(center_x + tile_size // 4, center_y - tile_size // 6),
        ]
        painter.drawPolygon(right_ear)

        # Inner ear detail
        painter.setBrush(color.darker(140))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 4, center_y - tile_size // 5, 4, 6)
        painter.drawEllipse(center_x + tile_size // 5, center_y - tile_size // 5, 4, 6)

        # Crude weapon (club in right hand/arm)
        painter.setBrush(QColor(80, 60, 40))
        painter.setPen(QPen(QColor(60, 40, 20), 2))
        # Club handle
        painter.drawLine(center_x + tile_size // 5, center_y,
                        center_x + tile_size // 3, center_y - tile_size // 6)
        # Club head
        painter.drawEllipse(center_x + tile_size // 3 - 4, center_y - tile_size // 5,
                           8, 8)

        # Clawed left arm/hand
        painter.setPen(QPen(color.darker(130), 2))
        painter.drawLine(center_x - tile_size // 6, center_y,
                        center_x - tile_size // 4, center_y + tile_size // 12)
        # Claws
        painter.setPen(QPen(QColor(100, 100, 80), 1))
        for i in range(3):
            claw_x = center_x - tile_size // 4 + i * 2
            claw_y = center_y + tile_size // 12
            painter.drawLine(claw_x, claw_y, claw_x - 1, claw_y + 3)

        # Wicked grin with sharp teeth
        painter.setPen(QPen(QColor(0, 0, 0, 200), 2))
        painter.setBrush(QColor(40, 20, 20))
        # Mouth
        mouth_rect = QRect(center_x - tile_size // 8, center_y - tile_size // 20,
                          tile_size // 4, tile_size // 12)
        painter.drawArc(mouth_rect, 0, -180 * 16)  # Evil grin arc
        # Sharp teeth
        painter.setPen(QPen(QColor(220, 220, 200), 1))
        for i in range(5):
            tooth_x = center_x - tile_size // 10 + i * 4
            painter.drawLine(tooth_x, center_y - tile_size // 20,
                           tooth_x, center_y + tile_size // 30)

        # Glowing yellow menacing eyes
        painter.setBrush(QColor(255, 230, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 10, center_y - tile_size // 8, 5, 6)
        painter.drawEllipse(center_x + tile_size // 10 - 5, center_y - tile_size // 8, 5, 6)
        # Eye glow
        eye_glow = QRadialGradient(center_x - tile_size // 12, center_y - tile_size // 9, 4)
        eye_glow.setColorAt(0, QColor(255, 255, 150, 180))
        eye_glow.setColorAt(1, QColor(255, 230, 0, 0))
        painter.setBrush(eye_glow)
        painter.drawEllipse(center_x - tile_size // 10 - 3, center_y - tile_size // 8 - 3, 11, 12)
        eye_glow.setCenter(center_x + tile_size // 12, center_y - tile_size // 9)
        painter.setBrush(eye_glow)
        painter.drawEllipse(center_x + tile_size // 10 - 8, center_y - tile_size // 8 - 3, 11, 12)

    elif enemy_type == c.ENEMY_SKELETON:
        # SKELETON - Risen Undead Warrior with full body

        # Spectral aura/wispy energy around skeleton
        for i in range(6):
            angle = i * math.pi / 3
            wisp_dist = tile_size // 3
            wisp_x = center_x + int(wisp_dist * math.cos(angle))
            wisp_y = center_y + int(wisp_dist * math.sin(angle))

            wisp_gradient = QRadialGradient(wisp_x, wisp_y, tile_size // 12)
            wisp_gradient.setColorAt(0, QColor(100, 255, 200, 100))
            wisp_gradient.setColorAt(1, QColor(100, 255, 200, 0))
            painter.setBrush(wisp_gradient)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(wisp_x - tile_size // 12, wisp_y - tile_size // 12,
                               tile_size // 6, tile_size // 6)

        # Ribcage with individual ribs
        painter.setBrush(color)
        painter.setPen(QPen(color.darker(130), 2))
        # Ribcage oval
        painter.drawEllipse(center_x - tile_size // 5, center_y + tile_size // 12,
                           tile_size * 2 // 5, tile_size // 3)
        # Individual ribs
        painter.setPen(QPen(color.darker(150), 2))
        for i in range(4):
            rib_y = center_y + tile_size // 12 + i * 6
            rib_width = tile_size // 5 - i * 4
            painter.drawArc(center_x - rib_width, rib_y,
                           rib_width * 2, 8, 0, 180 * 16)

        # Spine (vertebrae)
        painter.setPen(QPen(color.darker(120), 3))
        spine_top = center_y - tile_size // 12
        spine_bottom = center_y + tile_size // 3
        painter.drawLine(center_x, spine_top, center_x, spine_bottom)
        # Vertebrae bumps
        painter.setBrush(color.darker(110))
        painter.setPen(Qt.PenStyle.NoPen)
        for i in range(5):
            vert_y = spine_top + i * 8
            painter.drawEllipse(center_x - 3, vert_y, 6, 4)

        # Tattered cape/armor remnants
        cape_gradient = QLinearGradient(center_x, center_y,
                                        center_x, center_y + tile_size // 3)
        cape_gradient.setColorAt(0, QColor(60, 50, 80, 180))
        cape_gradient.setColorAt(1, QColor(40, 30, 60, 100))
        painter.setBrush(cape_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        # Tattered cape shape
        cape = [
            QPoint(center_x - tile_size // 6, center_y - tile_size // 12),
            QPoint(center_x - tile_size // 4, center_y + tile_size // 6),
            QPoint(center_x - tile_size // 5, center_y + tile_size // 4),
            QPoint(center_x + tile_size // 5, center_y + tile_size // 4),
            QPoint(center_x + tile_size // 4, center_y + tile_size // 6),
            QPoint(center_x + tile_size // 6, center_y - tile_size // 12),
        ]
        painter.drawPolygon(cape)

        # Bony arms with weapon
        painter.setPen(QPen(color.darker(120), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        # Right arm holding weapon (extended)
        painter.drawLine(center_x + tile_size // 8, center_y,
                        center_x + tile_size // 4, center_y - tile_size // 12)
        painter.drawLine(center_x + tile_size // 4, center_y - tile_size // 12,
                        center_x + tile_size // 3, center_y - tile_size // 6)

        # Bony hand/fingers
        painter.setPen(QPen(color.darker(130), 2))
        for i in range(3):
            finger_x = center_x + tile_size // 3 + i
            painter.drawLine(finger_x, center_y - tile_size // 6,
                           finger_x + 1, center_y - tile_size // 5)

        # Rusted sword
        sword_gradient = QLinearGradient(center_x + tile_size // 3, center_y - tile_size // 4,
                                         center_x + tile_size // 3, center_y + tile_size // 8)
        sword_gradient.setColorAt(0, QColor(160, 140, 120))
        sword_gradient.setColorAt(1, QColor(100, 80, 60))
        painter.setBrush(sword_gradient)
        painter.setPen(QPen(QColor(80, 60, 40), 2))
        # Blade
        sword_blade = [
            QPoint(center_x + tile_size // 3 - 2, center_y - tile_size // 4),
            QPoint(center_x + tile_size // 3 + 2, center_y - tile_size // 4),
            QPoint(center_x + tile_size // 3 + 1, center_y + tile_size // 12),
            QPoint(center_x + tile_size // 3 - 1, center_y + tile_size // 12),
        ]
        painter.drawPolygon(sword_blade)

        # Left arm (hanging down)
        painter.setPen(QPen(color.darker(120), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(center_x - tile_size // 8, center_y,
                        center_x - tile_size // 5, center_y + tile_size // 8)

        # Skull (larger, more detailed)
        skull_gradient = QRadialGradient(center_x, center_y - tile_size // 5, tile_size // 4)
        skull_gradient.setColorAt(0, color.lighter(110))
        skull_gradient.setColorAt(0.8, color)
        skull_gradient.setColorAt(1, color.darker(120))
        painter.setBrush(skull_gradient)
        painter.setPen(QPen(color.darker(130), 2))
        painter.drawRoundedRect(center_x - tile_size // 4, center_y - tile_size * 2 // 5,
                               tile_size // 2, tile_size * 2 // 5, 6, 6)

        # Bone cracks on skull
        painter.setPen(QPen(color.darker(180), 1))
        painter.drawLine(center_x - tile_size // 10, center_y - tile_size // 3,
                        center_x + tile_size // 20, center_y - tile_size // 5)
        painter.drawLine(center_x + tile_size // 12, center_y - tile_size // 4,
                        center_x + tile_size // 6, center_y - tile_size // 6)

        # Eye sockets (deep and dark)
        painter.setBrush(QColor(0, 0, 0, 220))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 6, center_y - tile_size // 4,
                           tile_size // 10, tile_size // 8)
        painter.drawEllipse(center_x + tile_size // 12, center_y - tile_size // 4,
                           tile_size // 10, tile_size // 8)

        # Soul-fire eyes (glowing cyan/green)
        soul_fire_gradient = QRadialGradient(center_x - tile_size // 8, center_y - tile_size // 5, 4)
        soul_fire_gradient.setColorAt(0, QColor(150, 255, 200))
        soul_fire_gradient.setColorAt(0.5, QColor(100, 255, 180))
        soul_fire_gradient.setColorAt(1, QColor(50, 200, 150, 0))
        painter.setBrush(soul_fire_gradient)
        painter.drawEllipse(center_x - tile_size // 7, center_y - tile_size // 5, 6, 8)

        soul_fire_gradient.setCenter(center_x + tile_size // 7, center_y - tile_size // 5)
        painter.setBrush(soul_fire_gradient)
        painter.drawEllipse(center_x + tile_size // 10, center_y - tile_size // 5, 6, 8)

        # Nasal cavity (triangular)
        painter.setBrush(QColor(0, 0, 0, 200))
        nose = [
            QPoint(center_x, center_y - tile_size // 10),
            QPoint(center_x - tile_size // 16, center_y - tile_size // 30),
            QPoint(center_x + tile_size // 16, center_y - tile_size // 30),
        ]
        painter.drawPolygon(nose)

        # Teeth (detailed)
        painter.setPen(QPen(QColor(0, 0, 0, 200), 1))
        for i in range(-3, 4):
            x_pos = center_x + i * tile_size // 16
            painter.drawLine(x_pos, center_y,
                           x_pos, center_y + tile_size // 16)

        # Ancient helmet/crown remnants
        painter.setBrush(QColor(80, 70, 60, 180))
        painter.setPen(QPen(QColor(60, 50, 40), 2))
        helmet = [
            QPoint(center_x - tile_size // 5, center_y - tile_size // 3),
            QPoint(center_x - tile_size // 4, center_y - tile_size // 2),
            QPoint(center_x, center_y - tile_size * 2 // 5),
            QPoint(center_x + tile_size // 4, center_y - tile_size // 2),
            QPoint(center_x + tile_size // 5, center_y - tile_size // 3),
        ]
        painter.drawPolygon(helmet)

    elif enemy_type == c.ENEMY_DRAGON:
        # DRAGON - Ancient Wyrm (larger, more imposing - 1.3x scale)
        scale_factor = 1.3

        # Detailed wings with membrane veins (behind body)
        wing_gradient = QLinearGradient(center_x - int(tile_size * 0.5 * scale_factor),
                                        center_y - int(tile_size * 0.3 * scale_factor),
                                        center_x - int(tile_size * 0.2 * scale_factor),
                                        center_y + int(tile_size * 0.1 * scale_factor))
        wing_gradient.setColorAt(0, color.darker(130))
        wing_gradient.setColorAt(0.5, color.darker(110))
        wing_gradient.setColorAt(1, color.darker(140))
        painter.setBrush(wing_gradient)
        painter.setPen(QPen(color.darker(160), 2))

        # Left wing (spread)
        left_wing = [
            QPoint(center_x - int(tile_size * 0.15 * scale_factor), center_y),
            QPoint(center_x - int(tile_size * 0.5 * scale_factor), center_y - int(tile_size * 0.35 * scale_factor)),
            QPoint(center_x - int(tile_size * 0.45 * scale_factor), center_y - int(tile_size * 0.15 * scale_factor)),
            QPoint(center_x - int(tile_size * 0.35 * scale_factor), center_y + int(tile_size * 0.1 * scale_factor)),
        ]
        painter.drawPolygon(left_wing)

        # Right wing (spread)
        right_wing = [
            QPoint(center_x + int(tile_size * 0.15 * scale_factor), center_y),
            QPoint(center_x + int(tile_size * 0.5 * scale_factor), center_y - int(tile_size * 0.35 * scale_factor)),
            QPoint(center_x + int(tile_size * 0.45 * scale_factor), center_y - int(tile_size * 0.15 * scale_factor)),
            QPoint(center_x + int(tile_size * 0.35 * scale_factor), center_y + int(tile_size * 0.1 * scale_factor)),
        ]
        painter.drawPolygon(right_wing)

        # Wing membrane veins
        painter.setPen(QPen(color.darker(180), 1))
        painter.drawLine(center_x - int(tile_size * 0.15 * scale_factor), center_y,
                        center_x - int(tile_size * 0.45 * scale_factor), center_y - int(tile_size * 0.25 * scale_factor))
        painter.drawLine(center_x + int(tile_size * 0.15 * scale_factor), center_y,
                        center_x + int(tile_size * 0.45 * scale_factor), center_y - int(tile_size * 0.25 * scale_factor))

        # Wing talons/claws
        painter.setPen(QPen(color.darker(170), 2))
        painter.drawLine(center_x - int(tile_size * 0.5 * scale_factor), center_y - int(tile_size * 0.35 * scale_factor),
                        center_x - int(tile_size * 0.52 * scale_factor), center_y - int(tile_size * 0.4 * scale_factor))
        painter.drawLine(center_x + int(tile_size * 0.5 * scale_factor), center_y - int(tile_size * 0.35 * scale_factor),
                        center_x + int(tile_size * 0.52 * scale_factor), center_y - int(tile_size * 0.4 * scale_factor))

        # Main body with scale gradient
        body_gradient = QLinearGradient(center_x, center_y - int(tile_size * 0.2 * scale_factor),
                                        center_x, center_y + int(tile_size * 0.25 * scale_factor))
        body_gradient.setColorAt(0, color.lighter(115))
        body_gradient.setColorAt(0.5, color)
        body_gradient.setColorAt(1, color.darker(120))
        painter.setBrush(body_gradient)
        painter.setPen(QPen(color.darker(150), 2))
        painter.drawEllipse(center_x - int(tile_size * 0.25 * scale_factor),
                           center_y - int(tile_size * 0.15 * scale_factor),
                           int(tile_size * 0.5 * scale_factor),
                           int(tile_size * 0.4 * scale_factor))

        # Underbelly scales (lighter)
        underbelly_gradient = QLinearGradient(center_x, center_y,
                                              center_x, center_y + int(tile_size * 0.2 * scale_factor))
        underbelly_gradient.setColorAt(0, color.lighter(140))
        underbelly_gradient.setColorAt(1, color.lighter(120))
        painter.setBrush(underbelly_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - int(tile_size * 0.15 * scale_factor),
                           center_y - int(tile_size * 0.05 * scale_factor),
                           int(tile_size * 0.3 * scale_factor),
                           int(tile_size * 0.25 * scale_factor))

        # Scale pattern on body (diamond shapes)
        painter.setPen(QPen(color.darker(140), 1))
        for row in range(3):
            for col in range(4):
                scale_x = center_x - int(tile_size * 0.15 * scale_factor) + col * int(8 * scale_factor)
                scale_y = center_y - int(tile_size * 0.08 * scale_factor) + row * int(6 * scale_factor)
                offset = (row % 2) * int(4 * scale_factor)
                scale_diamond = [
                    QPoint(scale_x + offset, scale_y - 2),
                    QPoint(scale_x + offset + 3, scale_y),
                    QPoint(scale_x + offset, scale_y + 2),
                    QPoint(scale_x + offset - 3, scale_y),
                ]
                painter.drawPolygon(scale_diamond)

        # Spined tail with barbs
        painter.setPen(QPen(color.darker(130), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        # Tail curve
        tail_end_x = center_x - int(tile_size * 0.4 * scale_factor)
        tail_end_y = center_y + int(tile_size * 0.3 * scale_factor)
        painter.drawLine(center_x - int(tile_size * 0.2 * scale_factor), center_y + int(tile_size * 0.15 * scale_factor),
                        tail_end_x, tail_end_y)
        # Tail spikes
        painter.setBrush(color.darker(140))
        painter.setPen(QPen(color.darker(170), 1))
        for i in range(3):
            spike_x = center_x - int(tile_size * 0.2 * scale_factor) - i * int(7 * scale_factor)
            spike_y = center_y + int(tile_size * 0.15 * scale_factor) + i * int(5 * scale_factor)
            spike = [
                QPoint(spike_x, spike_y),
                QPoint(spike_x - int(3 * scale_factor), spike_y - int(6 * scale_factor)),
                QPoint(spike_x + int(2 * scale_factor), spike_y - int(4 * scale_factor)),
            ]
            painter.drawPolygon(spike)

        # Serpentine neck
        neck_gradient = QLinearGradient(center_x + int(tile_size * 0.1 * scale_factor), center_y - int(tile_size * 0.1 * scale_factor),
                                        center_x + int(tile_size * 0.3 * scale_factor), center_y - int(tile_size * 0.35 * scale_factor))
        neck_gradient.setColorAt(0, color)
        neck_gradient.setColorAt(1, color.lighter(110))
        painter.setBrush(neck_gradient)
        painter.setPen(QPen(color.darker(150), 2))
        # Neck segments (3 curved sections)
        for i in range(3):
            seg_x = center_x + int(tile_size * 0.15 * scale_factor) + i * int(6 * scale_factor)
            seg_y = center_y - int(tile_size * 0.15 * scale_factor) - i * int(8 * scale_factor)
            painter.drawEllipse(seg_x - int(5 * scale_factor), seg_y,
                               int(10 * scale_factor), int(8 * scale_factor))

        # Dragon head (detailed)
        head_gradient = QRadialGradient(center_x + int(tile_size * 0.32 * scale_factor),
                                        center_y - int(tile_size * 0.38 * scale_factor),
                                        int(tile_size * 0.18 * scale_factor))
        head_gradient.setColorAt(0, color.lighter(120))
        head_gradient.setColorAt(0.7, color)
        head_gradient.setColorAt(1, color.darker(110))
        painter.setBrush(head_gradient)
        painter.setPen(QPen(color.darker(150), 2))
        painter.drawEllipse(center_x + int(tile_size * 0.22 * scale_factor),
                           center_y - int(tile_size * 0.45 * scale_factor),
                           int(tile_size * 0.2 * scale_factor),
                           int(tile_size * 0.15 * scale_factor))

        # Crown of horns on head
        painter.setBrush(color.darker(130))
        painter.setPen(QPen(color.darker(170), 2))
        for i in range(3):
            horn_x = center_x + int(tile_size * 0.24 * scale_factor) + i * int(4 * scale_factor)
            horn_y = center_y - int(tile_size * 0.45 * scale_factor)
            horn = [
                QPoint(horn_x, horn_y),
                QPoint(horn_x - int(2 * scale_factor), horn_y - int(6 * scale_factor)),
                QPoint(horn_x + int(2 * scale_factor), horn_y - int(5 * scale_factor)),
            ]
            painter.drawPolygon(horn)

        # Fierce reptilian eye with slit pupil
        painter.setBrush(QColor(255, 200, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x + int(tile_size * 0.28 * scale_factor),
                           center_y - int(tile_size * 0.4 * scale_factor),
                           int(6 * scale_factor), int(5 * scale_factor))
        # Slit pupil
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(center_x + int(tile_size * 0.3 * scale_factor),
                        center_y - int(tile_size * 0.4 * scale_factor),
                        int(2 * scale_factor), int(5 * scale_factor))

        # Open maw with fangs
        painter.setBrush(QColor(60, 20, 20))
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        maw_points = [
            QPoint(center_x + int(tile_size * 0.4 * scale_factor), center_y - int(tile_size * 0.38 * scale_factor)),
            QPoint(center_x + int(tile_size * 0.42 * scale_factor), center_y - int(tile_size * 0.35 * scale_factor)),
            QPoint(center_x + int(tile_size * 0.38 * scale_factor), center_y - int(tile_size * 0.33 * scale_factor)),
        ]
        painter.drawPolygon(maw_points)

        # Sharp fangs
        painter.setBrush(QColor(240, 240, 230))
        painter.setPen(Qt.PenStyle.NoPen)
        for i in range(3):
            fang_x = center_x + int(tile_size * 0.38 * scale_factor) + i * int(2 * scale_factor)
            fang = [
                QPoint(fang_x, center_y - int(tile_size * 0.36 * scale_factor)),
                QPoint(fang_x - 1, center_y - int(tile_size * 0.33 * scale_factor)),
                QPoint(fang_x + 1, center_y - int(tile_size * 0.33 * scale_factor)),
            ]
            painter.drawPolygon(fang)

        # Smoke wisps from nostrils
        nostril_x = center_x + int(tile_size * 0.38 * scale_factor)
        nostril_y = center_y - int(tile_size * 0.4 * scale_factor)
        for i in range(3):
            smoke_gradient = QRadialGradient(nostril_x + i * int(3 * scale_factor),
                                            nostril_y - i * int(4 * scale_factor),
                                            int(4 * scale_factor))
            smoke_gradient.setColorAt(0, QColor(100, 100, 100, 150))
            smoke_gradient.setColorAt(1, QColor(80, 80, 80, 0))
            painter.setBrush(smoke_gradient)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(nostril_x + i * int(2 * scale_factor) - int(4 * scale_factor),
                               nostril_y - i * int(4 * scale_factor) - int(4 * scale_factor),
                               int(8 * scale_factor), int(8 * scale_factor))

        # Fire breath glow (enhanced)
        fire_gradient = QRadialGradient(center_x + int(tile_size * 0.45 * scale_factor),
                                        center_y - int(tile_size * 0.35 * scale_factor),
                                        int(tile_size * 0.15 * scale_factor))
        fire_gradient.setColorAt(0, QColor(255, 255, 200, 240))
        fire_gradient.setColorAt(0.3, QColor(255, 180, 0, 200))
        fire_gradient.setColorAt(0.6, QColor(255, 100, 0, 120))
        fire_gradient.setColorAt(1, QColor(255, 60, 0, 0))
        painter.setBrush(fire_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x + int(tile_size * 0.38 * scale_factor),
                           center_y - int(tile_size * 0.4 * scale_factor),
                           int(tile_size * 0.15 * scale_factor),
                           int(tile_size * 0.15 * scale_factor))

    # Restore painter state (undo any flip)
    painter.restore()
