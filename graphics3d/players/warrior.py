"""
Warrior 3D Model - Enhanced armored tank with sword and shield

Creates a detailed 3D warrior model using Ursina primitives.
Features: Layered armor, detailed sword and shield, improved proportions.
Optimized for fast loading without procedural textures.
"""

from ursina import Entity, Vec3, color


def create_rivets(parent, positions, rivet_color, scale=0.02):
    """Create decorative rivets on armor"""
    rivets = []
    for pos in positions:
        rivet = Entity(
            parent=parent,
            model='sphere',
            color=rivet_color,
            scale=(scale, scale, scale * 0.5),
            position=pos
        )
        rivets.append(rivet)
    return rivets


def create_warrior_model(position=Vec3(0, 0, 0), scale=Vec3(1, 1, 1)):
    """
    Create an enhanced 3D warrior character model.

    Args:
        position: Vec3 position for the model
        scale: Vec3 scale for the model

    Returns:
        Entity: Parent entity containing all model parts
    """
    warrior = Entity(position=position, scale=scale)

    # Define colors
    red_tunic = color.rgb(180/255, 60/255, 40/255)
    steel_gray = color.rgb(140/255, 140/255, 150/255)
    polished_steel = color.rgb(160/255, 160/255, 170/255)
    bronze = color.rgb(120/255, 100/255, 60/255)
    dark_bronze = color.rgb(100/255, 80/255, 50/255)
    gold = color.rgb(180/255, 160/255, 50/255)
    skin_tone = color.rgb(200/255, 160/255, 130/255)
    blue_shield = color.rgb(60/255, 120/255, 180/255)
    dark_pants = color.rgb(80/255, 70/255, 60/255)
    leather_brown = color.rgb(100/255, 80/255, 50/255)
    iron_gray = color.rgb(100/255, 100/255, 105/255)

    # ========== TORSO & BODY ==========
    # Body (main torso)
    body = Entity(
        parent=warrior,
        model='cube',
        color=red_tunic,
        scale=(0.50, 0.60, 0.30),
        position=(0, 0, 0)
    )

    # Chest plate (main armor)
    chest_plate = Entity(
        parent=warrior,
        model='cube',
        color=polished_steel,
        scale=(0.54, 0.54, 0.04),
        position=(0, 0.08, 0.16)
    )

    # Add decorative rivets to chest plate (8 rivets)
    rivet_positions = [
        (-0.22, 0.28, 0.19), (0.22, 0.28, 0.19),  # Top corners
        (-0.22, 0.08, 0.19), (0.22, 0.08, 0.19),  # Middle
        (-0.22, -0.12, 0.19), (0.22, -0.12, 0.19),  # Bottom corners
        (0, 0.32, 0.19), (0, -0.16, 0.19)  # Center top/bottom
    ]
    chest_rivets = create_rivets(warrior, rivet_positions, bronze, scale=0.022)

    # Back plate
    back_plate = Entity(
        parent=warrior,
        model='cube',
        color=steel_gray,
        scale=(0.50, 0.52, 0.04),
        position=(0, 0.05, -0.16)
    )

    # ========== HEAD & HELMET ==========
    # Neck
    neck = Entity(
        parent=warrior,
        model='cube',
        color=skin_tone,
        scale=(0.14, 0.14, 0.14),
        position=(0, 0.42, 0)
    )

    # Head
    head = Entity(
        parent=warrior,
        model='sphere',
        color=skin_tone,
        scale=(0.24, 0.26, 0.24),
        position=(0, 0.54, 0)
    )

    # Helmet base
    helmet_base = Entity(
        parent=warrior,
        model='cube',
        color=steel_gray,
        scale=(0.28, 0.18, 0.28),
        position=(0, 0.62, 0)
    )

    # Helmet visor guard
    visor = Entity(
        parent=warrior,
        model='cube',
        color=steel_gray,
        scale=(0.24, 0.08, 0.14),
        position=(0, 0.54, 0.14)
    )

    # Helmet crest
    crest = Entity(
        parent=warrior,
        model='cube',
        color=bronze,
        scale=(0.30, 0.06, 0.06),
        position=(0, 0.70, 0)
    )

    # Gorget (neck armor)
    gorget = Entity(
        parent=warrior,
        model='cube',
        color=polished_steel,
        scale=(0.18, 0.10, 0.18),
        position=(0, 0.38, 0)
    )

    # ========== SHOULDERS ==========
    # Left pauldron (main)
    left_pauldron_main = Entity(
        parent=warrior,
        model='sphere',
        color=steel_gray,
        scale=(0.24, 0.18, 0.24),
        position=(-0.38, 0.28, 0)
    )

    # Left pauldron plates (2 layers for detail)
    for i, y_offset in enumerate([0.02, -0.04]):
        plate = Entity(
            parent=warrior,
            model='sphere',
            color=polished_steel,
            scale=(0.22, 0.04, 0.22),
            position=(-0.38, 0.28 + y_offset, -0.01 - i * 0.02)
        )

    # Right pauldron (main)
    right_pauldron_main = Entity(
        parent=warrior,
        model='sphere',
        color=steel_gray,
        scale=(0.24, 0.18, 0.24),
        position=(0.38, 0.28, 0)
    )

    # Right pauldron plates (2 layers)
    for i, y_offset in enumerate([0.02, -0.04]):
        plate = Entity(
            parent=warrior,
            model='sphere',
            color=polished_steel,
            scale=(0.22, 0.04, 0.22),
            position=(0.38, 0.28 + y_offset, -0.01 - i * 0.02)
        )

    # ========== ARMS ==========
    # Left upper arm
    left_upper_arm = Entity(
        parent=warrior,
        model='cube',
        color=red_tunic,
        scale=(0.16, 0.48, 0.16),
        position=(-0.38, 0.06, 0)
    )

    # Left elbow guard
    left_elbow = Entity(
        parent=warrior,
        model='sphere',
        color=steel_gray,
        scale=(0.12, 0.10, 0.12),
        position=(-0.38, -0.16, 0)
    )

    # Left forearm
    left_forearm = Entity(
        parent=warrior,
        model='cube',
        color=red_tunic,
        scale=(0.15, 0.36, 0.15),
        position=(-0.38, -0.36, 0)
    )

    # Left gauntlet
    left_gauntlet = Entity(
        parent=warrior,
        model='cube',
        color=iron_gray,
        scale=(0.16, 0.14, 0.16),
        position=(-0.38, -0.54, 0)
    )

    # Left gauntlet plates (2 finger plates)
    for i, z_off in enumerate([0.04, -0.02]):
        plate = Entity(
            parent=warrior,
            model='cube',
            color=steel_gray,
            scale=(0.17, 0.030, 0.025),
            position=(-0.38, -0.54 + z_off, 0.09)
        )

    # Right upper arm
    right_upper_arm = Entity(
        parent=warrior,
        model='cube',
        color=red_tunic,
        scale=(0.16, 0.48, 0.16),
        position=(0.38, 0.06, 0)
    )

    # Right elbow guard
    right_elbow = Entity(
        parent=warrior,
        model='sphere',
        color=steel_gray,
        scale=(0.12, 0.10, 0.12),
        position=(0.38, -0.16, 0)
    )

    # Right forearm
    right_forearm = Entity(
        parent=warrior,
        model='cube',
        color=red_tunic,
        scale=(0.15, 0.36, 0.15),
        position=(0.38, -0.36, 0)
    )

    # Right gauntlet
    right_gauntlet = Entity(
        parent=warrior,
        model='cube',
        color=iron_gray,
        scale=(0.16, 0.14, 0.16),
        position=(0.38, -0.54, 0)
    )

    # Right gauntlet plates (2 finger plates)
    for i, z_off in enumerate([0.04, -0.02]):
        plate = Entity(
            parent=warrior,
            model='cube',
            color=steel_gray,
            scale=(0.17, 0.030, 0.025),
            position=(0.38, -0.54 + z_off, 0.09)
        )

    # ========== SWORD (DETAILED) ==========
    # Blade (main sword body) - positioned to extend diagonally forward-up from hand
    sword_blade = Entity(
        parent=warrior,
        model='cube',
        color=polished_steel,
        scale=(0.06, 0.78, 0.06),
        position=(0.42, -0.05, 0.40),
        rotation=(55, 0, 0)  # Tilt forward 55 degrees
    )

    # Fuller groove (blade center detail)
    fuller = Entity(
        parent=warrior,
        model='cube',
        color=color.rgb(0.55, 0.55, 0.60),
        scale=(0.02, 0.68, 0.01),
        position=(0.42, -0.03, 0.435),
        rotation=(55, 0, 0)  # Match blade rotation
    )

    # Crossguard (center)
    crossguard_center = Entity(
        parent=warrior,
        model='cube',
        color=bronze,
        scale=(0.28, 0.06, 0.10),
        position=(0.38, -0.30, 0.18)
    )

    # Crossguard ends (decorative spheres)
    for x_sign in [-1, 1]:
        end = Entity(
            parent=warrior,
            model='sphere',
            color=bronze,
            scale=(0.05, 0.05, 0.08),
            position=(0.38 + x_sign * 0.14, -0.30, 0.18)
        )

    # Hilt (leather grip)
    hilt = Entity(
        parent=warrior,
        model='cube',
        color=leather_brown,
        scale=(0.08, 0.22, 0.08),
        position=(0.38, -0.46, 0.15)
    )

    # Hilt wrapping detail (3 wire wraps)
    for y in [-0.38, -0.46, -0.54]:
        wrap = Entity(
            parent=warrior,
            model='cube',
            color=dark_bronze,
            scale=(0.09, 0.015, 0.09),
            position=(0.38, y, 0.15)
        )

    # Pommel (sphere)
    pommel = Entity(
        parent=warrior,
        model='sphere',
        color=bronze,
        scale=(0.10, 0.10, 0.10),
        position=(0.38, -0.62, 0.15)
    )

    # Pommel gem (decorative)
    gem = Entity(
        parent=warrior,
        model='sphere',
        color=color.rgb(0.8, 0.1, 0.1),  # Ruby red
        scale=(0.04, 0.04, 0.04),
        position=(0.38, -0.62, 0.21)
    )

    # ========== SHIELD (DETAILED) ==========
    # Shield base
    shield_base = Entity(
        parent=warrior,
        model='cube',
        color=blue_shield,
        scale=(0.38, 0.50, 0.08),
        position=(-0.48, 0, 0.12),
        rotation=(0, 20, -5)
    )

    # Shield rim (metal reinforcement)
    shield_rim = Entity(
        parent=warrior,
        model='cube',
        color=iron_gray,
        scale=(0.40, 0.52, 0.02),
        position=(-0.48, 0, 0.17),
        rotation=(0, 20, -5)
    )

    # Shield boss (large gold centerpiece)
    shield_boss = Entity(
        parent=warrior,
        model='sphere',
        color=gold,
        scale=(0.12, 0.12, 0.08),
        position=(-0.48, 0, 0.20),
        rotation=(0, 20, -5)
    )

    # Shield decorative bands (2 bands)
    for y_off in [-0.15, 0.15]:
        band = Entity(
            parent=warrior,
            model='cube',
            color=gold,
            scale=(0.36, 0.04, 0.02),
            position=(-0.48, y_off, 0.18),
            rotation=(0, 20, -5)
        )

    # ========== LEGS & LOWER BODY ==========
    # Belt
    belt_base = Entity(
        parent=warrior,
        model='cube',
        color=leather_brown,
        scale=(0.56, 0.12, 0.32),
        position=(0, -0.32, 0)
    )

    # Belt buckle
    buckle = Entity(
        parent=warrior,
        model='cube',
        color=bronze,
        scale=(0.10, 0.10, 0.04),
        position=(0, -0.32, 0.18)
    )

    # Tassets (hip armor plates)
    left_tasset = Entity(
        parent=warrior,
        model='cube',
        color=steel_gray,
        scale=(0.18, 0.20, 0.04),
        position=(-0.18, -0.48, 0.16)
    )

    right_tasset = Entity(
        parent=warrior,
        model='cube',
        color=steel_gray,
        scale=(0.18, 0.20, 0.04),
        position=(0.18, -0.48, 0.16)
    )

    # Legs (thighs)
    left_thigh = Entity(
        parent=warrior,
        model='cube',
        color=dark_pants,
        scale=(0.22, 0.50, 0.22),
        position=(-0.16, -0.70, 0)
    )

    right_thigh = Entity(
        parent=warrior,
        model='cube',
        color=dark_pants,
        scale=(0.22, 0.50, 0.22),
        position=(0.16, -0.70, 0)
    )

    # Knee guards (main)
    left_knee_main = Entity(
        parent=warrior,
        model='sphere',
        color=steel_gray,
        scale=(0.14, 0.12, 0.14),
        position=(-0.16, -0.92, 0.04)
    )

    # Left knee plates (2 layers)
    for i in range(2):
        plate = Entity(
            parent=warrior,
            model='cube',
            color=polished_steel,
            scale=(0.16, 0.030, 0.02),
            position=(-0.16, -0.92 - i * 0.05, 0.13)
        )

    right_knee_main = Entity(
        parent=warrior,
        model='sphere',
        color=steel_gray,
        scale=(0.14, 0.12, 0.14),
        position=(0.16, -0.92, 0.04)
    )

    # Right knee plates (2 layers)
    for i in range(2):
        plate = Entity(
            parent=warrior,
            model='cube',
            color=polished_steel,
            scale=(0.16, 0.030, 0.02),
            position=(0.16, -0.92 - i * 0.05, 0.13)
        )

    # Lower legs (shins)
    left_shin = Entity(
        parent=warrior,
        model='cube',
        color=steel_gray,
        scale=(0.20, 0.42, 0.20),
        position=(-0.16, -1.16, 0)
    )

    right_shin = Entity(
        parent=warrior,
        model='cube',
        color=steel_gray,
        scale=(0.20, 0.42, 0.20),
        position=(0.16, -1.16, 0)
    )

    # Boots
    left_boot = Entity(
        parent=warrior,
        model='cube',
        color=leather_brown,
        scale=(0.14, 0.10, 0.18),
        position=(-0.16, -1.42, 0.04)
    )

    right_boot = Entity(
        parent=warrior,
        model='cube',
        color=leather_brown,
        scale=(0.14, 0.10, 0.18),
        position=(0.16, -1.42, 0.04)
    )

    return warrior


__all__ = ['create_warrior_model']
