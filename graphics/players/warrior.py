"""
Warrior (Berserker) class renderer - Savage rage warrior with massive axe
"""
from PyQt6.QtGui import QPainter, QPen, QBrush, QLinearGradient, QRadialGradient, QColor
from PyQt6.QtCore import Qt, QPoint
import math


def draw_warrior(painter: QPainter, center_x: int, center_y: int, tile_size: int, color: QColor, idle_time: float):
    """Draw warrior with massive axe swing and rage effects"""
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
    handle_length = tile_size // 3  # Shorter handle
    blade_attach_y = hand_y + handle_length

    # Axe handle (thick, wrapped leather) - extends from hand
    handle_color = QColor(100, 70, 40)
    painter.setPen(QPen(handle_color, 6))
    painter.drawLine(hand_x, hand_y, hand_x, blade_attach_y)

    # Leather wrapping detail
    painter.setPen(QPen(QColor(80, 55, 30), 1))
    for i in range(3):  # Fewer wraps for shorter handle
        y_pos = hand_y + i * tile_size // 12
        painter.drawLine(hand_x - 3, y_pos, hand_x + 3, y_pos)

    # Axe blade (massive, chipped, brutal) - positioned lower on handle
    # Blade extends sideways from the handle, closer to the middle/bottom
    blade_points = [
        QPoint(hand_x - tile_size // 30, blade_attach_y + tile_size // 20),  # Top connection (lower)
        QPoint(hand_x - tile_size // 3, blade_attach_y + tile_size // 30),  # Top outer edge
        QPoint(hand_x - tile_size // 3, blade_attach_y + tile_size // 5),  # Blade tip
        QPoint(hand_x - tile_size // 5, blade_attach_y + tile_size // 6),  # Bottom outer
        QPoint(hand_x - tile_size // 30, blade_attach_y + tile_size // 8),  # Bottom connection to handle
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
