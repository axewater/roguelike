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
        # BERSERKER - Savage rage warrior with massive axe and battle scars

        # Detect if this is selection screen (large tile size)
        is_selection_screen = tile_size > 128

        if is_selection_screen:
            # ENHANCED ANIMATIONS for character selection (4x scale)
            # Massive axe swing cycle - hand moves in arc, axe follows
            swing_cycle = idle_time * 0.5  # Slow cycle
            swing_phase = swing_cycle % 3.0  # 0 to 3 seconds

            if swing_phase < 0.8:  # Idle ready - axe resting on shoulder
                hand_x = center_x + tile_size // 4
                hand_y = center_y
                axe_angle = -135  # Pointing up-left over shoulder
            elif swing_phase < 1.5:  # Raise axe to side
                progress = (swing_phase - 0.8) / 0.7
                # Hand moves out to side
                hand_x = center_x + tile_size // 4 + int(tile_size * 0.1 * progress)
                hand_y = center_y - int(tile_size * 0.15 * progress)
                axe_angle = -135 - (45 * progress)  # -135 to -180 (straight up)
            elif swing_phase < 2.0:  # Hold raised
                hand_x = center_x + tile_size // 4 + int(tile_size * 0.1)
                hand_y = center_y - int(tile_size * 0.15)
                axe_angle = -180  # Straight up
            else:  # Swing down
                progress = (swing_phase - 2.0) / 1.0
                hand_x = center_x + tile_size // 4 + int(tile_size * 0.1 * (1 - progress))
                hand_y = center_y - int(tile_size * 0.15 * (1 - progress))
                axe_angle = -180 + (45 * progress)  # Return to -135

            # Heavy breathing
            breathing = math.sin(idle_time * 0.8) * 8
            # Rage intensity
            rage_intensity = 1.5 + abs(math.sin(idle_time * 0.7)) * 0.8
            # Eye glow
            eye_pulse = int(abs(math.sin(idle_time * 2.0)) * 100)
            # Shoulder heave
            shoulder_heave = math.sin(idle_time * 0.6) * 10
            # Battle stance
            stance_shift = math.sin(idle_time * 0.4) * 8
        else:
            # NORMAL ANIMATIONS for gameplay
            # Gentle swaying with axe on shoulder
            sway = math.sin(idle_time * 1.2) * 3
            hand_x = center_x + tile_size // 4 + int(sway)
            hand_y = center_y
            axe_angle = -135 + math.sin(idle_time * 0.8) * 5  # Slight wobble over shoulder

            breathing = math.sin(idle_time * 1.2) * 3
            rage_intensity = 1.0 + abs(math.sin(idle_time * 0.8)) * 0.4
            eye_pulse = int(abs(math.sin(idle_time * 2.5)) * 60)
            shoulder_heave = math.sin(idle_time * 0.9) * 4
            stance_shift = 0

        # Rage aura - swirling particles (drawn before character for background effect)
        rage_particle_count = int(10 * rage_intensity) if is_selection_screen else 6
        for i in range(rage_particle_count):
            angle = (i * 2 * math.pi / rage_particle_count) + (idle_time * rage_intensity * 1.5)
            radius_var = 1.0 + math.sin(idle_time * 1.3 + i) * 0.3
            particle_x = center_x + int(tile_size // 3 * radius_var * math.cos(angle))
            particle_y = center_y + int(tile_size // 4 * radius_var * math.sin(angle))

            # Red/orange rage particles
            particle_alpha = int(120 + 60 * math.sin(idle_time * 2.0 + i))
            rage_color = QColor(255, int(100 + 80 * math.sin(i)), 20, particle_alpha)
            painter.setBrush(rage_color)
            painter.setPen(Qt.PenStyle.NoPen)
            particle_size = int(4 + 3 * math.sin(idle_time + i))
            painter.drawEllipse(particle_x - particle_size // 2, particle_y - particle_size // 2,
                               particle_size, particle_size)

        # Heat distortion glow behind character
        heat_gradient = QRadialGradient(center_x, center_y, tile_size // 2)
        heat_gradient.setColorAt(0, QColor(255, 100, 0, 40))
        heat_gradient.setColorAt(0.6, QColor(255, 60, 0, 20))
        heat_gradient.setColorAt(1, QColor(255, 0, 0, 0))
        painter.setBrush(heat_gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 2, center_y - tile_size // 2,
                           tile_size, tile_size)

        # Legs (wide aggressive stance)
        leg_color = QColor(60, 50, 45)  # Dark torn pants
        painter.setBrush(leg_color)
        painter.setPen(QPen(leg_color.darker(120), 2))
        # Left leg (forward, bent)
        painter.drawRect(center_x - tile_size // 4 + int(stance_shift), center_y + tile_size // 12,
                        tile_size // 6, tile_size // 4)
        # Right leg (back, support)
        painter.drawRect(center_x + tile_size // 12 - int(stance_shift), center_y + tile_size // 10,
                        tile_size // 6, tile_size // 4)

        # Heavy boots (studded)
        painter.setBrush(QColor(40, 35, 30))
        painter.setPen(QPen(QColor(80, 70, 60), 1))
        painter.drawRect(center_x - tile_size // 4 + int(stance_shift), center_y + tile_size // 3,
                        tile_size // 6, tile_size // 12)
        painter.drawRect(center_x + tile_size // 12 - int(stance_shift), center_y + tile_size // 3,
                        tile_size // 6, tile_size // 12)

        # Torso (muscular, exposed arms) - wider than other classes
        body_gradient = QLinearGradient(center_x - tile_size // 3, center_y - tile_size // 8,
                                        center_x + tile_size // 3, center_y + tile_size // 10)
        body_gradient.setColorAt(0, color)
        body_gradient.setColorAt(0.3, color.darker(110))
        body_gradient.setColorAt(0.7, color)
        body_gradient.setColorAt(1, color.darker(120))
        painter.setBrush(body_gradient)
        painter.setPen(QPen(color.darker(140), 2))
        # Wider torso for berserker
        painter.drawEllipse(center_x - tile_size // 3, center_y - tile_size // 8 + int(breathing),
                           tile_size * 2 // 3, tile_size // 3)

        # Torn leather straps across chest
        strap_color = QColor(80, 60, 40)
        painter.setPen(QPen(strap_color, 3))
        painter.drawLine(center_x - tile_size // 4, center_y - tile_size // 10,
                        center_x + tile_size // 4, center_y + tile_size // 12)
        painter.drawLine(center_x - tile_size // 5, center_y + tile_size // 20,
                        center_x + tile_size // 5, center_y + tile_size // 10)

        # Battle scars on torso
        scar_color = QColor(220, 180, 150, 200)  # Lighter flesh tone
        painter.setPen(QPen(scar_color, 2))
        # Diagonal slash scar
        painter.drawLine(center_x - tile_size // 8, center_y - tile_size // 12,
                        center_x + tile_size // 10, center_y + tile_size // 15)
        # Vertical scar
        painter.drawLine(center_x + tile_size // 12, center_y - tile_size // 20,
                        center_x + tile_size // 12, center_y + tile_size // 12)

        # Muscular arms (bare, exposed)
        arm_color = QColor(200, 150, 120)  # Flesh tone
        painter.setBrush(arm_color)
        painter.setPen(QPen(arm_color.darker(120), 2))
        # Right arm (main gripping arm) - positioned at axe hand
        painter.drawEllipse(hand_x - tile_size // 14, hand_y - tile_size // 20,
                           tile_size // 7, tile_size // 5)
        # Left arm (support arm on shoulder)
        painter.drawEllipse(center_x - tile_size // 4, center_y - tile_size // 12 + int(shoulder_heave),
                           tile_size // 7, tile_size // 5)

        # Arm scars
        painter.setPen(QPen(QColor(200, 120, 100), 1))
        painter.drawLine(center_x - tile_size // 3 + 2, center_y - tile_size // 20,
                        center_x - tile_size // 4, center_y + tile_size // 20)

        # Belt with skull buckle
        painter.setBrush(QColor(60, 50, 40))
        painter.drawRect(center_x - tile_size // 4, center_y + tile_size // 12,
                        tile_size // 2, tile_size // 15)
        # Skull buckle
        painter.setBrush(QColor(220, 220, 220))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center_x - tile_size // 20, center_y + tile_size // 12,
                           tile_size // 10, tile_size // 12)
        # Skull eye sockets
        painter.setBrush(QColor(0, 0, 0))
        painter.drawEllipse(center_x - tile_size // 30, center_y + tile_size // 11, 2, 2)
        painter.drawEllipse(center_x + tile_size // 60, center_y + tile_size // 11, 2, 2)

        # MASSIVE TWO-HANDED AXE - held in hand and swung
        painter.save()

        # Rotate around hand position (grip point)
        painter.translate(hand_x, hand_y)
        painter.rotate(axe_angle)
        painter.translate(-hand_x, -hand_y)

        # Calculate handle end position (where blade attaches)
        handle_length = tile_size // 2
        blade_attach_y = hand_y + handle_length

        # Axe handle (thick, wrapped leather) - extends from hand
        handle_color = QColor(100, 70, 40)
        painter.setPen(QPen(handle_color, 6))
        painter.drawLine(hand_x, hand_y, hand_x, blade_attach_y)

        # Leather wrapping detail
        painter.setPen(QPen(QColor(80, 55, 30), 1))
        for i in range(5):
            y_pos = hand_y + i * tile_size // 10
            painter.drawLine(hand_x - 3, y_pos, hand_x + 3, y_pos)

        # Axe blade (massive, chipped, brutal) - attached at END of handle
        # Blade extends sideways from the handle end, no gap
        blade_points = [
            QPoint(hand_x - tile_size // 30, blade_attach_y),  # Top connection flush with handle
            QPoint(hand_x - tile_size // 3, blade_attach_y - tile_size // 20),  # Top outer edge (slight up)
            QPoint(hand_x - tile_size // 3, blade_attach_y + tile_size // 6),  # Blade tip (lower)
            QPoint(hand_x - tile_size // 5, blade_attach_y + tile_size // 7),  # Bottom outer
            QPoint(hand_x - tile_size // 30, blade_attach_y + tile_size // 10),  # Bottom connection to handle
        ]
        blade_gradient = QLinearGradient(hand_x - tile_size // 3, blade_attach_y - tile_size // 6,
                                         hand_x, blade_attach_y + tile_size // 10)
        blade_gradient.setColorAt(0, QColor(180, 180, 190))
        blade_gradient.setColorAt(0.5, QColor(140, 140, 150))
        blade_gradient.setColorAt(1, QColor(100, 100, 110))
        painter.setBrush(blade_gradient)
        painter.setPen(QPen(QColor(80, 80, 90), 2))
        painter.drawPolygon(blade_points)

        # Blood stain on blade edge
        painter.setBrush(QColor(120, 20, 20, 150))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(hand_x - tile_size // 3 + 5, blade_attach_y,
                           tile_size // 12, tile_size // 20)

        # Blade chips/notches
        painter.setPen(QPen(QColor(60, 60, 70), 2))
        painter.drawLine(hand_x - tile_size // 3, blade_attach_y - tile_size // 12,
                        hand_x - tile_size // 3 + 4, blade_attach_y - tile_size // 15)
        painter.drawLine(hand_x - tile_size // 4, blade_attach_y + tile_size // 15,
                        hand_x - tile_size // 4 + 3, blade_attach_y + tile_size // 12)

        painter.restore()

        # Head (wild, fierce)
        head_gradient = QRadialGradient(center_x, center_y - tile_size // 4, tile_size // 5)
        head_color = QColor(200, 150, 120)  # Flesh tone
        head_gradient.setColorAt(0, head_color.lighter(110))
        head_gradient.setColorAt(1, head_color.darker(110))
        painter.setBrush(head_gradient)
        painter.setPen(QPen(head_color.darker(130), 2))
        painter.drawEllipse(center_x - tile_size // 6, center_y - tile_size // 3,
                           tile_size // 3, tile_size // 3)

        # Wild hair (spiky, unkempt)
        hair_color = QColor(40, 35, 30)
        painter.setBrush(hair_color)
        painter.setPen(Qt.PenStyle.NoPen)
        # Multiple spiky triangles for hair
        for i in range(5):
            hair_x = center_x - tile_size // 6 + i * tile_size // 20
            hair_points = [
                QPoint(hair_x, center_y - tile_size // 3),
                QPoint(hair_x - tile_size // 30, center_y - tile_size // 2 + i * 2),
                QPoint(hair_x + tile_size // 30, center_y - tile_size // 2 + i * 2),
            ]
            painter.drawPolygon(hair_points)

        # War paint (tribal red markings)
        painter.setPen(QPen(QColor(200, 40, 20), 2))
        # Diagonal stripe across face
        painter.drawLine(center_x - tile_size // 8, center_y - tile_size // 5,
                        center_x + tile_size // 10, center_y - tile_size // 7)
        # Forehead marking
        painter.drawLine(center_x, center_y - tile_size // 4,
                        center_x, center_y - tile_size // 6)

        # Fierce gritted teeth
        painter.setBrush(QColor(220, 220, 220))
        painter.setPen(QPen(QColor(180, 180, 180), 1))
        painter.drawRect(center_x - tile_size // 12, center_y - tile_size // 8,
                        tile_size // 6, tile_size // 30)
        # Tooth gaps
        painter.setPen(QPen(QColor(100, 50, 50), 1))
        for i in range(3):
            tooth_x = center_x - tile_size // 12 + i * tile_size // 24
            painter.drawLine(tooth_x, center_y - tile_size // 8,
                           tooth_x, center_y - tile_size // 8 + 3)

        # Glowing rage eyes
        eye_alpha = 220 - eye_pulse
        eye_glow = QColor(255, 120, 0, eye_alpha)  # Orange glow
        painter.setBrush(eye_glow)
        painter.setPen(Qt.PenStyle.NoPen)
        # Left eye
        painter.drawEllipse(center_x - tile_size // 16, center_y - tile_size // 6, 4, 5)
        # Eye glow aura
        glow_gradient = QRadialGradient(center_x - tile_size // 16 + 2, center_y - tile_size // 6 + 2, 6)
        glow_gradient.setColorAt(0, QColor(255, 150, 50, 100))
        glow_gradient.setColorAt(1, QColor(255, 100, 0, 0))
        painter.setBrush(glow_gradient)
        painter.drawEllipse(center_x - tile_size // 16 - 3, center_y - tile_size // 6 - 2, 10, 10)

        # Right eye
        painter.setBrush(eye_glow)
        painter.drawEllipse(center_x + tile_size // 20, center_y - tile_size // 6, 4, 5)
        # Eye glow aura
        glow_gradient = QRadialGradient(center_x + tile_size // 20 + 2, center_y - tile_size // 6 + 2, 6)
        glow_gradient.setColorAt(0, QColor(255, 150, 50, 100))
        glow_gradient.setColorAt(1, QColor(255, 100, 0, 0))
        painter.setBrush(glow_gradient)
        painter.drawEllipse(center_x + tile_size // 20 - 3, center_y - tile_size // 6 - 2, 10, 10)

        # Face scar
        painter.setPen(QPen(QColor(180, 120, 100), 2))
        painter.drawLine(center_x + tile_size // 20, center_y - tile_size // 5,
                        center_x + tile_size // 12, center_y - tile_size // 10)

        # Rising embers/steam from shoulders (battle exhaustion)
        if is_selection_screen:
            ember_count = 4
        else:
            ember_count = 2
        for i in range(ember_count):
            ember_offset = int(idle_time * 20 + i * 10) % 30
            ember_x = center_x - tile_size // 4 + i * tile_size // 8
            ember_y = center_y - tile_size // 6 - ember_offset
            ember_alpha = int(150 - ember_offset * 5)
            if ember_alpha > 0:
                ember_color = QColor(255, int(100 + ember_offset * 3), 0, ember_alpha)
                painter.setBrush(ember_color)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawEllipse(ember_x - 1, ember_y - 1, 2, 3)

    elif class_type == c.CLASS_MAGE:
        # MAGE - Robed spellcaster with floating orbs

        # Detect if this is selection screen (large tile size)
        is_selection_screen = tile_size > 128

        if is_selection_screen:
            # ENHANCED ANIMATIONS for character selection (4x scale)
            # Staff spinning/twirling
            staff_rotation = (idle_time * 60) % 360  # Slow 360 rotation
            staff_float = math.sin(idle_time * 0.8) * tile_size * 0.08

            # Orb constellation - larger spiral pattern
            orb_spiral_radius = 1.0 + math.sin(idle_time * 0.4) * 0.3  # Pulsing radius
            orb_speed_variation = 0.7 + math.sin(idle_time * 0.3) * 0.3  # Variable speed

            # Arcane energy in hands
            hand_glow = int(abs(math.sin(idle_time * 2.5)) * 60)

            # Robe billowing
            robe_sway = math.sin(idle_time * 0.5) * 12
            robe_billow = abs(math.sin(idle_time * 0.6)) * 8

            # Staff pulse more dramatic
            staff_pulse = int(abs(math.sin(idle_time * 1.8)) * 80)
            rune_glow = int(abs(math.sin(idle_time * 1.2)) * 60)
        else:
            # NORMAL ANIMATIONS for gameplay
            orb_speed_variation = 1.0 + math.sin(idle_time * 0.5) * 0.3
            staff_pulse = int(abs(math.sin(idle_time * 2.0)) * 50)
            robe_sway = math.sin(idle_time * 0.7) * 3
            rune_glow = int(abs(math.sin(idle_time * 1.5)) * 40)
            staff_rotation = 0
            staff_float = 0
            orb_spiral_radius = 1.0
            hand_glow = 0
            robe_billow = 0

        # Robe bottom (flowing) with sway and billow
        robe_offset = int(robe_sway)
        robe_width_offset = int(robe_billow)
        robe_points = [
            QPoint(center_x + robe_offset, center_y + tile_size // 10),
            QPoint(center_x - tile_size // 3 + robe_offset - robe_width_offset, center_y + tile_size // 3),
            QPoint(center_x + tile_size // 3 + robe_offset + robe_width_offset, center_y + tile_size // 3),
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

        # Floating magical orbs (3 orbiting) with speed variation and spiral
        for i in range(3):
            angle = (i * 2 * math.pi / 3) + (math.pi / 4) + (idle_time * orb_speed_variation)
            orb_x = center_x + int(tile_size // 3 * orb_spiral_radius * math.cos(angle))
            orb_y = center_y + int(tile_size // 4 * orb_spiral_radius * math.sin(angle))

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

        # Detect if this is selection screen (large tile size)
        is_selection_screen = tile_size > 128

        if is_selection_screen:
            # ENHANCED ANIMATIONS for character selection (4x scale)
            # Dagger flip/twirl cycle
            dagger_spin_cycle = idle_time * 0.8  # Spin cycle
            left_dagger_angle = (dagger_spin_cycle * 180) % 360  # Left dagger rotation
            right_dagger_angle = ((dagger_spin_cycle + 0.5) * 180) % 360  # Right dagger offset

            # Stealth pose cycle - deep crouch to standing
            crouch_cycle = math.sin(idle_time * 0.4) * tile_size * 0.15
            crouch_shift = crouch_cycle

            # Shadow wisps more dramatic
            wisp_drift_speed = 0.9 + math.sin(idle_time * 0.5) * 0.5
            wisp_size_var = 1.0 + math.sin(idle_time * 0.7) * 0.6  # Larger variation
            wisp_count_mult = 1.5  # More wisps

            # Eye glow more intense
            eye_pulse = int(abs(math.sin(idle_time * 2.0)) * 100)

            # Head scan more dramatic
            head_scan = math.sin(idle_time * 0.4) * 8
        else:
            # NORMAL ANIMATIONS for gameplay
            crouch_shift = math.sin(idle_time * 1.5) * 4
            wisp_drift_speed = 1.2 + math.sin(idle_time * 0.8) * 0.4
            wisp_size_var = 1.0 + math.sin(idle_time * 1.1) * 0.3
            eye_pulse = int(abs(math.sin(idle_time * 2.5)) * 60)
            head_scan = math.sin(idle_time * 0.6) * 2
            left_dagger_angle = 0
            right_dagger_angle = 0
            wisp_count_mult = 1.0

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
        wisp_count = int(3 * wisp_count_mult)
        for i in range(wisp_count):
            angle = (i * 2 * math.pi / wisp_count) + (idle_time * wisp_drift_speed)
            wisp_x = center_x + int(tile_size // 4 * math.cos(angle))
            wisp_y = center_y + int(tile_size // 5 * math.sin(angle))
            wisp_width = int(4 * wisp_size_var)
            wisp_height = int(6 * wisp_size_var)
            painter.drawEllipse(wisp_x - wisp_width // 2, wisp_y - wisp_height // 2, wisp_width, wisp_height)

    elif class_type == c.CLASS_RANGER:
        # RANGER - Nature archer with bow and quiver

        # Detect if this is selection screen (large tile size)
        is_selection_screen = tile_size > 128

        if is_selection_screen:
            # ENHANCED ANIMATIONS for character selection (4x scale)
            # Bow draw cycle (3 second cycle)
            draw_cycle = idle_time * 0.6  # Slow cycle
            draw_phase = draw_cycle % 2.0  # 0 to 2 seconds

            if draw_phase < 0.7:  # Idle/ready
                bow_draw = 0
                arrow_pull = 0
            elif draw_phase < 1.2:  # Drawing bow
                progress = (draw_phase - 0.7) / 0.5
                bow_draw = progress
                arrow_pull = int(tile_size * 0.15 * progress)
            elif draw_phase < 1.6:  # Holding drawn
                bow_draw = 1.0
                arrow_pull = int(tile_size * 0.15)
            else:  # Release and return
                progress = (draw_phase - 1.6) / 0.4
                bow_draw = 1.0 - progress
                arrow_pull = int(tile_size * 0.15 * (1 - progress))

            # Stance shift - hunter's crouch
            stance_shift = math.sin(idle_time * 0.4) * tile_size * 0.08

            # Leaves swirl faster and larger
            leaf_orbit_speed = 1.2 + math.sin(idle_time * 0.3) * 0.4
            leaf_radius_mult = 1.3 + math.sin(idle_time * 0.5) * 0.3

            # Head scanning
            head_turn = math.sin(idle_time * 0.5) * 10

            # Breathing
            breathing = math.sin(idle_time * 0.7) * 6
        else:
            # NORMAL ANIMATIONS for gameplay
            bow_adjust = math.sin(idle_time * 1.0) * 2
            leaf_orbit_speed = 0.8 + math.sin(idle_time * 0.5) * 0.2
            head_turn = math.sin(idle_time * 0.7) * 3
            breathing = math.sin(idle_time * 0.9) * 2
            bow_draw = 0
            arrow_pull = 0
            stance_shift = 0
            leaf_radius_mult = 1.0

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

        # Bowstring - curved when drawn
        painter.setPen(QPen(QColor(200, 190, 180), 2))
        if is_selection_screen and bow_draw > 0:
            # Draw curved string when bow is drawn
            string_pull_x = center_x - tile_size // 6 - int(arrow_pull * 0.8)
            painter.drawLine(center_x - tile_size // 6, center_y - tile_size // 5,
                           string_pull_x, center_y)
            painter.drawLine(string_pull_x, center_y,
                           center_x - tile_size // 6, center_y + tile_size // 6)
        else:
            # Straight string when not drawn
            painter.drawLine(center_x - tile_size // 6, center_y - tile_size // 5,
                           center_x - tile_size // 6, center_y + tile_size // 6)

        # Nocked arrow with bow draw animation
        painter.setBrush(QColor(139, 90, 43))
        painter.setPen(QPen(QColor(100, 60, 30), 1))
        # Arrow shaft - pulled back when drawing
        arrow_start_x = center_x - tile_size // 6 - arrow_pull
        arrow_end_x = center_x - tile_size // 3 - 2
        painter.drawLine(arrow_start_x, center_y,
                        arrow_end_x, center_y)
        # Arrowhead
        arrow_head = [
            QPoint(arrow_end_x, center_y),
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
        leaf_count = 2 if not is_selection_screen else 4  # More leaves in selection
        for i in range(leaf_count):
            angle = (i * 2 * math.pi / leaf_count) + (idle_time * leaf_orbit_speed)
            leaf_x = center_x + int(tile_size // 3 * leaf_radius_mult * math.cos(angle))
            leaf_y = center_y + int(tile_size // 4 * leaf_radius_mult * math.sin(angle)) + int(breathing)
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
