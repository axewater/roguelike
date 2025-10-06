"""
Enemy rendering by type
"""
from PyQt6.QtGui import QPainter, QPen, QBrush, QLinearGradient, QRadialGradient, QColor
from PyQt6.QtCore import Qt, QPoint, QRect
import constants as c
import math


def draw_enemy(painter: QPainter, x: float, y: float, tile_size: int, color: QColor, enemy_type: str, facing_direction: tuple = (0, 1), idle_time: float = 0.0):
    """Draw enemy based on type with directional facing and idle animations"""
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

        # Idle animations - Fast, twitchy, nervous
        ear_twitch = math.sin(idle_time * 8.0) * 3  # Rapid ear movement
        head_dart = math.sin(idle_time * 3.5) * 4  # Nervous head darting
        eye_flicker = int(abs(math.sin(idle_time * 6.0)) * 40)  # Eye intensity flicker
        posture_shift = math.sin(idle_time * 2.2) * 2  # Jittery body movement
        teeth_chatter = int(abs(math.sin(idle_time * 10.0)))  # Rapid teeth movement

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

        # Large bat-like ears (signature feature) with twitch
        ear_color = color.darker(110)
        painter.setBrush(ear_color)
        painter.setPen(QPen(color.darker(150), 1))
        ear_offset = int(ear_twitch)
        # Left ear
        left_ear = [
            QPoint(center_x - tile_size // 5 + int(head_dart), center_y - tile_size // 4 + int(posture_shift)),
            QPoint(center_x - tile_size // 3 + int(head_dart) + ear_offset, center_y - tile_size // 3 + int(posture_shift) - ear_offset),
            QPoint(center_x - tile_size // 4 + int(head_dart), center_y - tile_size // 6 + int(posture_shift)),
        ]
        painter.drawPolygon(left_ear)
        # Right ear
        right_ear = [
            QPoint(center_x + tile_size // 5 + int(head_dart), center_y - tile_size // 4 + int(posture_shift)),
            QPoint(center_x + tile_size // 3 + int(head_dart) - ear_offset, center_y - tile_size // 3 + int(posture_shift) - ear_offset),
            QPoint(center_x + tile_size // 4 + int(head_dart), center_y - tile_size // 6 + int(posture_shift)),
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

        # Glowing yellow menacing eyes with flicker
        eye_brightness = 230 - eye_flicker
        painter.setBrush(QColor(255, eye_brightness, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 10 + int(head_dart), center_y - tile_size // 8 + int(posture_shift), 5, 6)
        painter.drawEllipse(center_x + tile_size // 10 - 5 + int(head_dart), center_y - tile_size // 8 + int(posture_shift), 5, 6)
        # Eye glow with flicker
        glow_alpha = 180 - eye_flicker
        eye_glow = QRadialGradient(center_x - tile_size // 12 + int(head_dart), center_y - tile_size // 9 + int(posture_shift), 4)
        eye_glow.setColorAt(0, QColor(255, 255, 150, glow_alpha))
        eye_glow.setColorAt(1, QColor(255, eye_brightness, 0, 0))
        painter.setBrush(eye_glow)
        painter.drawEllipse(center_x - tile_size // 10 - 3 + int(head_dart), center_y - tile_size // 8 - 3 + int(posture_shift), 11, 12)
        eye_glow.setCenter(center_x + tile_size // 12 + int(head_dart), center_y - tile_size // 9 + int(posture_shift))
        painter.setBrush(eye_glow)
        painter.drawEllipse(center_x + tile_size // 10 - 8 + int(head_dart), center_y - tile_size // 8 - 3 + int(posture_shift), 11, 12)

    elif enemy_type == c.ENEMY_SLIME:
        # SLIME - Gelatinous Blob with translucent body

        # Idle animations - Pulsing, organic movements
        body_pulse = math.sin(idle_time * 1.2) * 4  # Body size pulsing
        nucleus_drift_x = math.sin(idle_time * 0.8) * 3  # Nucleus floating
        nucleus_drift_y = math.cos(idle_time * 0.6) * 2
        bubble_float = idle_time * 20  # Bubbles rising
        membrane_ripple = abs(math.sin(idle_time * 2.0)) * 2  # Surface tension

        # Main gelatinous body (translucent)
        body_size = tile_size // 2 + int(body_pulse)
        body_gradient = QRadialGradient(center_x, center_y, body_size)
        body_gradient.setColorAt(0, color.lighter(130))
        body_gradient.setColorAt(0.5, color)
        body_gradient.setColorAt(1, color.darker(120))
        painter.setBrush(body_gradient)
        painter.setPen(QPen(color.darker(140), 2))
        painter.drawEllipse(center_x - body_size // 2, center_y - body_size // 2,
                           body_size, body_size)

        # Inner translucent layer
        inner_size = int(body_size * 0.7)
        inner_gradient = QRadialGradient(center_x, center_y, inner_size)
        inner_gradient.setColorAt(0, QColor(color.red(), color.green(), color.blue(), 100))
        inner_gradient.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 30))
        painter.setBrush(inner_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - inner_size // 2, center_y - inner_size // 2,
                           inner_size, inner_size)

        # Nucleus core (glowing center)
        nucleus_x = center_x + int(nucleus_drift_x)
        nucleus_y = center_y + int(nucleus_drift_y)
        nucleus_gradient = QRadialGradient(nucleus_x, nucleus_y, tile_size // 6)
        nucleus_gradient.setColorAt(0, QColor(150, 255, 220, 220))
        nucleus_gradient.setColorAt(0.6, color.lighter(150))
        nucleus_gradient.setColorAt(1, color)
        painter.setBrush(nucleus_gradient)
        painter.setPen(QPen(QColor(100, 200, 180), 1))
        painter.drawEllipse(nucleus_x - tile_size // 8, nucleus_y - tile_size // 8,
                           tile_size // 4, tile_size // 4)

        # Nucleus detail (inner darker spot)
        painter.setBrush(QColor(60, 150, 130))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(nucleus_x - tile_size // 16, nucleus_y - tile_size // 16,
                           tile_size // 8, tile_size // 8)

        # Surface bubbles (floating upward)
        painter.setBrush(QColor(200, 255, 240, 120))
        painter.setPen(QPen(QColor(150, 220, 200, 180), 1))
        for i in range(4):
            bubble_phase = (bubble_float + i * 50) % 100
            bubble_x = center_x + int(math.sin(i * 1.5 + idle_time) * tile_size // 4)
            bubble_y = center_y + tile_size // 4 - int(bubble_phase * tile_size // 100)
            bubble_size = 3 + int(bubble_phase / 25)  # Bubbles grow as they rise
            if bubble_y > center_y - body_size // 2:  # Only show bubbles inside body
                painter.drawEllipse(bubble_x - bubble_size // 2, bubble_y - bubble_size // 2,
                                   bubble_size, bubble_size)

        # Pseudopod tendrils at base (3 reaching down)
        painter.setBrush(color.darker(110))
        painter.setPen(QPen(color.darker(140), 2))
        for i in range(-1, 2):
            tendril_x_offset = i * tile_size // 6
            tendril_sway = math.sin(idle_time * 1.5 + i) * 3
            tendril_points = [
                QPoint(center_x + tendril_x_offset, center_y + body_size // 3),
                QPoint(center_x + tendril_x_offset + int(tendril_sway), center_y + body_size // 2),
                QPoint(center_x + tendril_x_offset + int(tendril_sway * 1.5), center_y + body_size // 2 + 4),
            ]
            for j in range(len(tendril_points) - 1):
                painter.drawLine(tendril_points[j], tendril_points[j + 1])

        # Outer membrane ripple effect
        ripple_alpha = 80 + int(membrane_ripple * 20)
        painter.setPen(QPen(QColor(color.red(), color.green(), color.blue(), ripple_alpha), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(center_x - body_size // 2 - 2, center_y - body_size // 2 - 2,
                           body_size + 4, body_size + 4)

    elif enemy_type == c.ENEMY_SKELETON:
        # SKELETON - Risen Undead Warrior with full body

        # Idle animations - Eerie, undead movements
        wisp_orbit_speed = 1.0 + math.sin(idle_time * 0.6) * 0.3  # Spectral wisps speed
        soul_fire_flicker = int(abs(math.sin(idle_time * 3.0)) * 50)  # Eyes flicker
        bone_rattle = math.sin(idle_time * 5.0) * 1  # Subtle shake
        jaw_movement = abs(math.sin(idle_time * 1.5)) * 3  # Jaw hang open/close
        sword_sway = math.sin(idle_time * 1.2) * 4  # Sword tip drift

        # Spectral aura/wispy energy around skeleton with orbit speed
        for i in range(6):
            angle = (i * math.pi / 3) + (idle_time * wisp_orbit_speed)
            wisp_dist = tile_size // 3
            wisp_x = center_x + int(wisp_dist * math.cos(angle)) + int(bone_rattle)
            wisp_y = center_y + int(wisp_dist * math.sin(angle)) + int(bone_rattle)

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

        # Soul-fire eyes (glowing cyan/green) with flicker
        fire_intensity = 150 + soul_fire_flicker
        soul_fire_gradient = QRadialGradient(center_x - tile_size // 8, center_y - tile_size // 5, 4)
        soul_fire_gradient.setColorAt(0, QColor(fire_intensity, 255, 200))
        soul_fire_gradient.setColorAt(0.5, QColor(100 + soul_fire_flicker // 2, 255, 180))
        soul_fire_gradient.setColorAt(1, QColor(50, 200, 150, 0))
        painter.setBrush(soul_fire_gradient)
        painter.drawEllipse(center_x - tile_size // 7 + int(bone_rattle), center_y - tile_size // 5, 6, 8)

        soul_fire_gradient.setCenter(center_x + tile_size // 7, center_y - tile_size // 5)
        painter.setBrush(soul_fire_gradient)
        painter.drawEllipse(center_x + tile_size // 10 + int(bone_rattle), center_y - tile_size // 5, 6, 8)

        # Nasal cavity (triangular)
        painter.setBrush(QColor(0, 0, 0, 200))
        nose = [
            QPoint(center_x, center_y - tile_size // 10),
            QPoint(center_x - tile_size // 16, center_y - tile_size // 30),
            QPoint(center_x + tile_size // 16, center_y - tile_size // 30),
        ]
        painter.drawPolygon(nose)

        # Teeth (detailed) with jaw movement
        painter.setPen(QPen(QColor(0, 0, 0, 200), 1))
        jaw_offset = int(jaw_movement)
        for i in range(-3, 4):
            x_pos = center_x + i * tile_size // 16 + int(bone_rattle)
            painter.drawLine(x_pos, center_y + int(bone_rattle),
                           x_pos, center_y + tile_size // 16 + jaw_offset)

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

    elif enemy_type == c.ENEMY_ORC:
        # ORC - Muscular Brute Warrior

        # Idle animations - Heavy, powerful movements
        breath_expansion = abs(math.sin(idle_time * 0.7)) * 3  # Chest breathing
        axe_sway = math.sin(idle_time * 1.0) * 5  # Axe weight sway
        muscle_flex = abs(math.sin(idle_time * 0.5)) * 2  # Muscle tension
        nostril_flare = int(abs(math.sin(idle_time * 0.8)) * 2)  # Angry breathing

        # Muscular torso (large and imposing)
        torso_gradient = QLinearGradient(center_x, center_y - tile_size // 12,
                                         center_x, center_y + tile_size // 4)
        torso_gradient.setColorAt(0, color.lighter(115))
        torso_gradient.setColorAt(0.5, color)
        torso_gradient.setColorAt(1, color.darker(120))
        painter.setBrush(torso_gradient)
        painter.setPen(QPen(color.darker(150), 2))
        torso_width = tile_size // 3 + int(breath_expansion)
        painter.drawEllipse(center_x - torso_width // 2, center_y - tile_size // 12,
                           torso_width, tile_size // 3)

        # Armor plates on shoulders
        armor_color = QColor(60, 50, 40)
        painter.setBrush(armor_color)
        painter.setPen(QPen(QColor(40, 30, 20), 2))
        # Left shoulder plate
        left_plate = [
            QPoint(center_x - tile_size // 4, center_y - tile_size // 12),
            QPoint(center_x - tile_size // 3, center_y - tile_size // 8),
            QPoint(center_x - tile_size // 4, center_y),
        ]
        painter.drawPolygon(left_plate)
        # Right shoulder plate
        right_plate = [
            QPoint(center_x + tile_size // 4, center_y - tile_size // 12),
            QPoint(center_x + tile_size // 3, center_y - tile_size // 8),
            QPoint(center_x + tile_size // 4, center_y),
        ]
        painter.drawPolygon(right_plate)

        # Spikes on armor
        painter.setBrush(QColor(80, 70, 60))
        painter.setPen(Qt.PenStyle.NoPen)
        for i in range(2):
            spike_x = center_x - tile_size // 3 + i * tile_size * 2 // 3
            spike = [
                QPoint(spike_x, center_y - tile_size // 8),
                QPoint(spike_x - 3, center_y - tile_size // 5),
                QPoint(spike_x + 3, center_y - tile_size // 5),
            ]
            painter.drawPolygon(spike)

        # Muscular arms
        painter.setPen(QPen(color.darker(130), 4))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        # Right arm (holding axe)
        painter.drawLine(center_x + tile_size // 6, center_y,
                        center_x + tile_size // 3, center_y - tile_size // 10)
        # Left arm
        painter.drawLine(center_x - tile_size // 6, center_y,
                        center_x - tile_size // 4, center_y + tile_size // 12)

        # Muscle definition lines
        painter.setPen(QPen(color.darker(160), 1))
        painter.drawLine(center_x + tile_size // 6, center_y,
                        center_x + tile_size // 5, center_y - tile_size // 20)

        # Large battle axe
        axe_x = center_x + tile_size // 3
        axe_y = center_y - tile_size // 10 + int(axe_sway)

        # Axe handle (wooden)
        painter.setBrush(QColor(80, 60, 40))
        painter.setPen(QPen(QColor(60, 40, 20), 2))
        painter.drawLine(axe_x, axe_y, axe_x - 2, axe_y - tile_size // 6)

        # Axe blade (metal)
        axe_gradient = QLinearGradient(axe_x, axe_y - tile_size // 6,
                                       axe_x + tile_size // 8, axe_y - tile_size // 6)
        axe_gradient.setColorAt(0, QColor(140, 140, 140))
        axe_gradient.setColorAt(0.5, QColor(180, 180, 180))
        axe_gradient.setColorAt(1, QColor(120, 120, 120))
        painter.setBrush(axe_gradient)
        painter.setPen(QPen(QColor(80, 80, 80), 2))
        axe_blade = [
            QPoint(axe_x - 2, axe_y - tile_size // 6),
            QPoint(axe_x + tile_size // 8, axe_y - tile_size // 5),
            QPoint(axe_x + tile_size // 7, axe_y - tile_size // 6 + 4),
            QPoint(axe_x - 2, axe_y - tile_size // 6 + 2),
        ]
        painter.drawPolygon(axe_blade)

        # Large orc head
        head_gradient = QRadialGradient(center_x, center_y - tile_size // 4, tile_size // 4)
        head_gradient.setColorAt(0, color.lighter(120))
        head_gradient.setColorAt(0.7, color)
        head_gradient.setColorAt(1, color.darker(110))
        painter.setBrush(head_gradient)
        painter.setPen(QPen(color.darker(140), 2))
        painter.drawEllipse(center_x - tile_size // 5, center_y - tile_size * 2 // 5,
                           tile_size * 2 // 5, tile_size // 3)

        # War paint stripes
        painter.setPen(QPen(QColor(180, 40, 40), 2))
        for i in range(2):
            paint_y = center_y - tile_size // 3 + i * tile_size // 12
            painter.drawLine(center_x - tile_size // 6, paint_y,
                           center_x + tile_size // 6, paint_y)

        # Prominent tusks
        painter.setBrush(QColor(220, 220, 200))
        painter.setPen(QPen(QColor(180, 180, 160), 2))
        # Left tusk
        left_tusk = [
            QPoint(center_x - tile_size // 10, center_y - tile_size // 8),
            QPoint(center_x - tile_size // 8, center_y - tile_size // 6),
            QPoint(center_x - tile_size // 12, center_y - tile_size // 12),
        ]
        painter.drawPolygon(left_tusk)
        # Right tusk
        right_tusk = [
            QPoint(center_x + tile_size // 10, center_y - tile_size // 8),
            QPoint(center_x + tile_size // 8, center_y - tile_size // 6),
            QPoint(center_x + tile_size // 12, center_y - tile_size // 12),
        ]
        painter.drawPolygon(right_tusk)

        # Fierce eyes
        painter.setBrush(QColor(255, 220, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 10, center_y - tile_size // 4,
                           6, 7)
        painter.drawEllipse(center_x + tile_size // 20, center_y - tile_size // 4,
                           6, 7)
        # Pupils
        painter.setBrush(QColor(0, 0, 0))
        painter.drawEllipse(center_x - tile_size // 10 + 2, center_y - tile_size // 4 + 2,
                           3, 4)
        painter.drawEllipse(center_x + tile_size // 20 + 2, center_y - tile_size // 4 + 2,
                           3, 4)

        # Angry brow ridge
        painter.setPen(QPen(color.darker(160), 2))
        painter.drawLine(center_x - tile_size // 8, center_y - tile_size // 3,
                        center_x - tile_size // 12, center_y - tile_size // 4)
        painter.drawLine(center_x + tile_size // 8, center_y - tile_size // 3,
                        center_x + tile_size // 12, center_y - tile_size // 4)

        # Flared nostrils
        painter.setBrush(QColor(0, 0, 0))
        painter.setPen(Qt.PenStyle.NoPen)
        nostril_size = 3 + nostril_flare
        painter.drawEllipse(center_x - tile_size // 16, center_y - tile_size // 7,
                           nostril_size, 4)
        painter.drawEllipse(center_x + tile_size // 32, center_y - tile_size // 7,
                           nostril_size, 4)

    elif enemy_type == c.ENEMY_DEMON:
        # DEMON - Horned Fiend with dark aura

        # Idle animations - Menacing, supernatural movements
        wing_beat = math.sin(idle_time * 1.5) * 6  # Wing flapping
        tail_lash = math.sin(idle_time * 2.0) * 8  # Aggressive tail movement
        aura_pulse = abs(math.sin(idle_time * 1.2))  # Dark energy pulse
        eye_glow = int(abs(math.sin(idle_time * 3.0)) * 80)  # Eye intensity
        claw_flex = abs(math.sin(idle_time * 1.8)) * 2  # Claw opening/closing

        # Dark aura (behind body)
        for ring in range(3):
            ring_radius = tile_size // 3 + ring * 8 + int(aura_pulse * 10)
            aura_alpha = int(40 * (1.0 - ring / 3) * aura_pulse)
            aura_gradient = QRadialGradient(center_x, center_y, ring_radius)
            aura_gradient.setColorAt(0, QColor(color.red(), color.green(), color.blue(), aura_alpha))
            aura_gradient.setColorAt(1, QColor(color.red(), color.green(), color.blue(), 0))
            painter.setBrush(aura_gradient)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(center_x - ring_radius, center_y - ring_radius,
                               ring_radius * 2, ring_radius * 2)

        # Bat wings (behind body, spread wide)
        wing_gradient = QLinearGradient(center_x - tile_size // 3, center_y,
                                        center_x - tile_size // 6, center_y + tile_size // 6)
        wing_gradient.setColorAt(0, color.darker(140))
        wing_gradient.setColorAt(0.5, color.darker(110))
        wing_gradient.setColorAt(1, color.darker(130))
        painter.setBrush(wing_gradient)
        painter.setPen(QPen(color.darker(170), 2))

        # Left wing with beat
        left_wing_offset = int(wing_beat)
        left_wing = [
            QPoint(center_x - tile_size // 8, center_y),
            QPoint(center_x - tile_size // 3, center_y - tile_size // 6 - left_wing_offset),
            QPoint(center_x - tile_size // 4, center_y - tile_size // 12),
            QPoint(center_x - tile_size // 6, center_y + tile_size // 12),
        ]
        painter.drawPolygon(left_wing)

        # Right wing with beat
        right_wing = [
            QPoint(center_x + tile_size // 8, center_y),
            QPoint(center_x + tile_size // 3, center_y - tile_size // 6 - left_wing_offset),
            QPoint(center_x + tile_size // 4, center_y - tile_size // 12),
            QPoint(center_x + tile_size // 6, center_y + tile_size // 12),
        ]
        painter.drawPolygon(right_wing)

        # Wing membranes (veins)
        painter.setPen(QPen(color.darker(180), 1))
        painter.drawLine(center_x - tile_size // 8, center_y,
                        center_x - tile_size // 3, center_y - tile_size // 6)
        painter.drawLine(center_x + tile_size // 8, center_y,
                        center_x + tile_size // 3, center_y - tile_size // 6)

        # Muscular torso (leaner than orc)
        torso_gradient = QRadialGradient(center_x, center_y, tile_size // 4)
        torso_gradient.setColorAt(0, color.lighter(120))
        torso_gradient.setColorAt(0.6, color)
        torso_gradient.setColorAt(1, color.darker(130))
        painter.setBrush(torso_gradient)
        painter.setPen(QPen(color.darker(150), 2))
        painter.drawEllipse(center_x - tile_size // 6, center_y - tile_size // 12,
                           tile_size // 3, tile_size // 3)

        # Clawed arms (menacing pose)
        painter.setPen(QPen(color.darker(140), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        # Left arm raised
        painter.drawLine(center_x - tile_size // 8, center_y,
                        center_x - tile_size // 4, center_y - tile_size // 8)
        # Right arm raised
        painter.drawLine(center_x + tile_size // 8, center_y,
                        center_x + tile_size // 4, center_y - tile_size // 8)

        # Sharp claws (both hands)
        painter.setPen(QPen(QColor(200, 200, 180), 2))
        for hand_x in [center_x - tile_size // 4, center_x + tile_size // 4]:
            hand_y = center_y - tile_size // 8
            for i in range(3):
                claw_offset = (i - 1) * 3
                painter.drawLine(hand_x + claw_offset, hand_y,
                               hand_x + claw_offset + int(claw_flex), hand_y - 5)

        # Barbed tail (behind, curling)
        tail_x = center_x + int(tail_lash)
        tail_gradient = QLinearGradient(center_x, center_y + tile_size // 6,
                                        tail_x, center_y + tile_size // 3)
        tail_gradient.setColorAt(0, color)
        tail_gradient.setColorAt(1, color.darker(120))
        painter.setBrush(tail_gradient)
        painter.setPen(QPen(color.darker(150), 3))
        # Tail curve
        tail_points = [
            QPoint(center_x, center_y + tile_size // 6),
            QPoint(center_x + int(tail_lash * 0.5), center_y + tile_size // 4),
            QPoint(tail_x, center_y + tile_size // 3),
        ]
        for i in range(len(tail_points) - 1):
            painter.drawLine(tail_points[i], tail_points[i + 1])

        # Tail barb (spear tip)
        painter.setBrush(QColor(180, 60, 80))
        painter.setPen(QPen(QColor(140, 40, 60), 2))
        barb = [
            QPoint(tail_x, center_y + tile_size // 3),
            QPoint(tail_x - 4, center_y + tile_size // 3 + 6),
            QPoint(tail_x + 4, center_y + tile_size // 3 + 6),
        ]
        painter.drawPolygon(barb)

        # Demonic head (angular and sinister)
        head_gradient = QRadialGradient(center_x, center_y - tile_size // 4, tile_size // 5)
        head_gradient.setColorAt(0, color.lighter(125))
        head_gradient.setColorAt(0.7, color)
        head_gradient.setColorAt(1, color.darker(110))
        painter.setBrush(head_gradient)
        painter.setPen(QPen(color.darker(150), 2))
        painter.drawEllipse(center_x - tile_size // 6, center_y - tile_size * 2 // 5,
                           tile_size // 3, tile_size // 3)

        # Curved horns
        painter.setBrush(QColor(60, 40, 50))
        painter.setPen(QPen(QColor(40, 20, 30), 2))
        # Left horn
        left_horn = [
            QPoint(center_x - tile_size // 8, center_y - tile_size // 3),
            QPoint(center_x - tile_size // 5, center_y - tile_size // 2),
            QPoint(center_x - tile_size // 7, center_y - tile_size * 2 // 5),
        ]
        painter.drawPolygon(left_horn)
        # Right horn
        right_horn = [
            QPoint(center_x + tile_size // 8, center_y - tile_size // 3),
            QPoint(center_x + tile_size // 5, center_y - tile_size // 2),
            QPoint(center_x + tile_size // 7, center_y - tile_size * 2 // 5),
        ]
        painter.drawPolygon(right_horn)

        # Horn ridges
        painter.setPen(QPen(QColor(80, 60, 70), 1))
        for i in range(2):
            painter.drawLine(center_x - tile_size // 8, center_y - tile_size // 3 - i * 4,
                           center_x - tile_size // 6, center_y - tile_size * 2 // 5 - i * 4)
            painter.drawLine(center_x + tile_size // 8, center_y - tile_size // 3 - i * 4,
                           center_x + tile_size // 6, center_y - tile_size * 2 // 5 - i * 4)

        # Glowing red eyes
        eye_brightness = 200 + eye_glow
        eye_gradient = QRadialGradient(center_x - tile_size // 12, center_y - tile_size // 4, 6)
        eye_gradient.setColorAt(0, QColor(255, eye_brightness, 100))
        eye_gradient.setColorAt(0.5, QColor(255, 100, 0))
        eye_gradient.setColorAt(1, QColor(200, 50, 0, 0))
        painter.setBrush(eye_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 10, center_y - tile_size // 4,
                           7, 8)
        painter.drawEllipse(center_x + tile_size // 20, center_y - tile_size // 4,
                           7, 8)

        # Evil grin with fangs
        painter.setPen(QPen(QColor(0, 0, 0, 200), 2))
        painter.setBrush(QColor(40, 10, 20))
        mouth_rect = QRect(center_x - tile_size // 10, center_y - tile_size // 12,
                          tile_size // 5, tile_size // 12)
        painter.drawArc(mouth_rect, 0, -180 * 16)
        # Fangs
        painter.setPen(QPen(QColor(240, 240, 220), 1))
        for i in [0, 3]:
            fang_x = center_x - tile_size // 12 + i * 6
            painter.drawLine(fang_x, center_y - tile_size // 12,
                           fang_x, center_y - tile_size // 20)

    elif enemy_type == c.ENEMY_DRAGON:
        # DRAGON - Ancient Wyrm (larger, more imposing - 1.3x scale)
        scale_factor = 1.3

        # Idle animations - Slow, majestic, powerful
        wing_flutter = math.sin(idle_time * 0.8) * 8  # Slow wing movement
        tail_sway = math.sin(idle_time * 0.6) * 10  # Tail drift
        breath_pulse = int(abs(math.sin(idle_time * 1.5)) * 60)  # Fire glow pulse
        smoke_intensity = abs(math.sin(idle_time * 1.0))  # Smoke wisp pulse
        body_breathing = math.sin(idle_time * 0.5) * 3  # Deep breathing

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

        # Left wing (spread) with flutter
        wing_offset = int(wing_flutter)
        left_wing = [
            QPoint(center_x - int(tile_size * 0.15 * scale_factor), center_y + int(body_breathing)),
            QPoint(center_x - int(tile_size * 0.5 * scale_factor) - wing_offset, center_y - int(tile_size * 0.35 * scale_factor) - wing_offset),
            QPoint(center_x - int(tile_size * 0.45 * scale_factor) - wing_offset // 2, center_y - int(tile_size * 0.15 * scale_factor)),
            QPoint(center_x - int(tile_size * 0.35 * scale_factor), center_y + int(tile_size * 0.1 * scale_factor) + int(body_breathing)),
        ]
        painter.drawPolygon(left_wing)

        # Right wing (spread) with flutter
        right_wing = [
            QPoint(center_x + int(tile_size * 0.15 * scale_factor), center_y + int(body_breathing)),
            QPoint(center_x + int(tile_size * 0.5 * scale_factor) + wing_offset, center_y - int(tile_size * 0.35 * scale_factor) - wing_offset),
            QPoint(center_x + int(tile_size * 0.45 * scale_factor) + wing_offset // 2, center_y - int(tile_size * 0.15 * scale_factor)),
            QPoint(center_x + int(tile_size * 0.35 * scale_factor), center_y + int(tile_size * 0.1 * scale_factor) + int(body_breathing)),
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

        # Spined tail with barbs and sway
        painter.setPen(QPen(color.darker(130), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        # Tail curve with sway
        tail_sway_offset = int(tail_sway)
        tail_end_x = center_x - int(tile_size * 0.4 * scale_factor) + tail_sway_offset
        tail_end_y = center_y + int(tile_size * 0.3 * scale_factor)
        painter.drawLine(center_x - int(tile_size * 0.2 * scale_factor), center_y + int(tile_size * 0.15 * scale_factor) + int(body_breathing),
                        tail_end_x, tail_end_y)
        # Tail spikes with sway
        painter.setBrush(color.darker(140))
        painter.setPen(QPen(color.darker(170), 1))
        for i in range(3):
            spike_sway_amount = tail_sway_offset * (i + 1) // 3  # Progressive sway along tail
            spike_x = center_x - int(tile_size * 0.2 * scale_factor) - i * int(7 * scale_factor) + spike_sway_amount
            spike_y = center_y + int(tile_size * 0.15 * scale_factor) + i * int(5 * scale_factor) + int(body_breathing)
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

        # Smoke wisps from nostrils with pulse
        nostril_x = center_x + int(tile_size * 0.38 * scale_factor)
        nostril_y = center_y - int(tile_size * 0.4 * scale_factor)
        for i in range(3):
            smoke_alpha = int(150 * smoke_intensity)
            smoke_gradient = QRadialGradient(nostril_x + i * int(3 * scale_factor),
                                            nostril_y - i * int(4 * scale_factor),
                                            int(4 * scale_factor))
            smoke_gradient.setColorAt(0, QColor(100, 100, 100, smoke_alpha))
            smoke_gradient.setColorAt(1, QColor(80, 80, 80, 0))
            painter.setBrush(smoke_gradient)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(nostril_x + i * int(2 * scale_factor) - int(4 * scale_factor),
                               nostril_y - i * int(4 * scale_factor) - int(4 * scale_factor),
                               int(8 * scale_factor), int(8 * scale_factor))

        # Fire breath glow (enhanced) with pulse
        fire_gradient = QRadialGradient(center_x + int(tile_size * 0.45 * scale_factor),
                                        center_y - int(tile_size * 0.35 * scale_factor),
                                        int(tile_size * 0.15 * scale_factor))
        fire_gradient.setColorAt(0, QColor(255, 255, 200, 240))
        fire_gradient.setColorAt(0.3, QColor(255, 180 + breath_pulse, 0, 200))
        fire_gradient.setColorAt(0.6, QColor(255, 100 + breath_pulse, 0, 120 + breath_pulse // 2))
        fire_gradient.setColorAt(1, QColor(255, 60, 0, 0))
        painter.setBrush(fire_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        fire_size = int(tile_size * 0.15 * scale_factor * (1.0 + smoke_intensity * 0.2))
        painter.drawEllipse(center_x + int(tile_size * 0.38 * scale_factor),
                           center_y - int(tile_size * 0.4 * scale_factor),
                           fire_size,
                           fire_size)

    # Restore painter state (undo any flip)
    painter.restore()
