"""
3D UI overlay module for Ursina-based 3D mode

This module provides UI widgets for the 3D mode, including:
- Stats display (HP, XP, player info, attack, defense, exploration, stealth)
- Equipment display (weapon, armor, accessory, boots)
- Nearby items display (items within 5 tiles with stats)
- Combat log (scrolling message feed)
- Ability bar (ability slots with cooldown indicators)
- Targeting system (mouse targeting for abilities)
"""

from ui3d.stats_display import StatsDisplay3D
from ui3d.equipment_display import EquipmentDisplay3D
from ui3d.nearby_items import NearbyItemsDisplay3D
from ui3d.combat_log_3d import CombatLog3D
from ui3d.ability_bar import AbilityBar3D
from ui3d.targeting import TargetingSystem

__all__ = [
    'StatsDisplay3D',
    'EquipmentDisplay3D',
    'NearbyItemsDisplay3D',
    'CombatLog3D',
    'AbilityBar3D',
    'TargetingSystem',
]
