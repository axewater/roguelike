"""
Player character rendering by class type
"""
from PyQt6.QtGui import QPainter, QPen, QBrush, QLinearGradient, QRadialGradient, QColor
from PyQt6.QtCore import Qt, QPoint, QRect
import constants as c
import math


def draw_player(painter: QPainter, x: float, y: float, tile_size: int, color: QColor, class_type: str, facing_direction: tuple = (0, 1), idle_time: float = 0.0):
    """Draw player character based on class with directional facing and idle animations"""
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

    # Enhanced drop shadow (larger, softer)
    shadow_color = QColor(0, 0, 0, 100)
    painter.setBrush(shadow_color)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(center_x - tile_size // 2 + 3, center_y + tile_size // 4,
                        tile_size - 6, tile_size // 6)

    if class_type == c.CLASS_WARRIOR:
        # WARRIOR - Armored tank with shield and sword

        # Idle animations
        shoulder_roll = math.sin(idle_time * 0.8) * 2  # Slow shoulder roll
        shield_bob = math.sin(idle_time * 1.2) * 3  # Shield breathing motion
        armor_shimmer = int(abs(math.sin(idle_time * 1.5)) * 20)  # Helmet glint

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

        # Shield (left side) with idle animation
        shield_offset = int(shield_bob)
        shield_points = [
            QPoint(center_x - tile_size // 4 + int(shoulder_roll), center_y - tile_size // 8 + shield_offset),
            QPoint(center_x - tile_size // 6 + int(shoulder_roll), center_y - tile_size // 5 + shield_offset),
            QPoint(center_x - tile_size // 8 + int(shoulder_roll), center_y - tile_size // 12 + shield_offset),
            QPoint(center_x - tile_size // 8 + int(shoulder_roll), center_y + tile_size // 12 + shield_offset),
            QPoint(center_x - tile_size // 6 + int(shoulder_roll), center_y + tile_size // 6 + shield_offset),
        ]
        painter.setBrush(color.lighter(110))
        painter.setPen(QPen(color.darker(130), 2))
        painter.drawPolygon(shield_points)

        # Shield boss (center) with animation
        painter.setBrush(QColor(200, 180, 100))
        painter.drawEllipse(center_x - tile_size // 5 + int(shoulder_roll), center_y - tile_size // 20 + shield_offset,
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

        # Helmet highlight with pulsing glint
        glint_alpha = 120 + armor_shimmer
        painter.setBrush(QColor(255, 255, 255, glint_alpha))
        painter.drawEllipse(center_x - tile_size // 12, center_y - tile_size // 4,
                           tile_size // 10, tile_size // 12)

    elif class_type == c.CLASS_MAGE:
        # MAGE - Robed spellcaster with floating orbs

        # Idle animations
        orb_speed_variation = 1.0 + math.sin(idle_time * 0.5) * 0.3  # Orbs speed up/slow down
        staff_pulse = int(abs(math.sin(idle_time * 2.0)) * 50)  # Staff orb brightness pulse
        robe_sway = math.sin(idle_time * 0.7) * 3  # Gentle floating sway
        rune_glow = int(abs(math.sin(idle_time * 1.5)) * 40)  # Rune brightness

        # Robe bottom (flowing) with sway
        robe_offset = int(robe_sway)
        robe_points = [
            QPoint(center_x + robe_offset, center_y + tile_size // 10),
            QPoint(center_x - tile_size // 3 + robe_offset, center_y + tile_size // 3),
            QPoint(center_x + tile_size // 3 + robe_offset, center_y + tile_size // 3),
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

        # Staff orb (glowing) with pulse
        orb_gradient = QRadialGradient(center_x - tile_size // 3, center_y - tile_size // 2,
                                       tile_size // 8)
        orb_gradient.setColorAt(0, QColor(255, 255, 255, 240))
        orb_gradient.setColorAt(0.4, color.lighter(160 + staff_pulse))
        orb_gradient.setColorAt(1, color.lighter(100 + staff_pulse // 2))
        painter.setBrush(orb_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 3 - tile_size // 12,
                           center_y - tile_size // 2 - tile_size // 12,
                           tile_size // 6, tile_size // 6)

        # Floating magical orbs (3 orbiting) with speed variation
        for i in range(3):
            angle = (i * 2 * math.pi / 3) + (math.pi / 4) + (idle_time * orb_speed_variation)
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

        # Mystical rune on robe with pulsing glow
        rune_brightness = 160 + rune_glow
        painter.setPen(QPen(color.lighter(rune_brightness), 2))
        painter.drawLine(center_x - tile_size // 16 + robe_offset, center_y,
                        center_x + tile_size // 16 + robe_offset, center_y)
        painter.drawLine(center_x + robe_offset, center_y - tile_size // 16,
                        center_x + robe_offset, center_y + tile_size // 16)

    elif class_type == c.CLASS_ROGUE:
        # ROGUE - Stealthy assassin with dual daggers

        # Idle animations
        crouch_shift = math.sin(idle_time * 1.5) * 4  # Subtle crouching motion
        wisp_drift_speed = 1.2 + math.sin(idle_time * 0.8) * 0.4  # Shadow wisps speed
        wisp_size_var = 1.0 + math.sin(idle_time * 1.1) * 0.3  # Wisp size variation
        eye_pulse = int(abs(math.sin(idle_time * 2.5)) * 60)  # Eye glow intensity
        head_scan = math.sin(idle_time * 0.6) * 2  # Subtle head movement

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

        # Glowing eyes (purple/dangerous) with pulse
        eye_alpha = 220 - eye_pulse
        painter.setBrush(QColor(180, 100, 255, eye_alpha))
        painter.drawEllipse(center_x - tile_size // 16 + int(head_scan), center_y - tile_size // 7 + int(crouch_shift), 3, 3)
        painter.drawEllipse(center_x + tile_size // 16 - 3 + int(head_scan), center_y - tile_size // 7 + int(crouch_shift), 3, 3)

        # Shadow wisps effect with drift and size variation
        wisp_color = QColor(color.red(), color.green(), color.blue(), 80)
        painter.setBrush(wisp_color)
        for i in range(3):
            angle = (i * 2 * math.pi / 3) + (idle_time * wisp_drift_speed)
            wisp_x = center_x + int(tile_size // 4 * math.cos(angle))
            wisp_y = center_y + int(tile_size // 5 * math.sin(angle))
            wisp_width = int(4 * wisp_size_var)
            wisp_height = int(6 * wisp_size_var)
            painter.drawEllipse(wisp_x - wisp_width // 2, wisp_y - wisp_height // 2, wisp_width, wisp_height)

    elif class_type == c.CLASS_RANGER:
        # RANGER - Nature archer with bow and quiver

        # Idle animations
        bow_adjust = math.sin(idle_time * 1.0) * 2  # Subtle bow position adjustment
        leaf_orbit_speed = 0.8 + math.sin(idle_time * 0.5) * 0.2  # Leaf drift variation
        head_turn = math.sin(idle_time * 0.7) * 3  # Scanning motion
        breathing = math.sin(idle_time * 0.9) * 2  # Natural breathing

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

        # Nature leaves floating nearby with drift
        leaf_color = QColor(120, 200, 100, 160)
        painter.setBrush(leaf_color)
        painter.setPen(Qt.PenStyle.NoPen)
        for i in range(2):
            angle = (i * math.pi + math.pi / 3) + (idle_time * leaf_orbit_speed)
            leaf_x = center_x + int(tile_size // 3 * math.cos(angle))
            leaf_y = center_y + int(tile_size // 4 * math.sin(angle)) + int(breathing)
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
