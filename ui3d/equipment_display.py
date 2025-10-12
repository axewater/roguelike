"""
Equipment Display 3D Widget

Displays player equipment (Weapon, Armor, Accessory, Boots).
Positioned in the top-right corner of the screen.
"""

from typing import Optional
from ursina import Entity, Text, color, Vec2
from game import Game
import constants as c


class EquipmentDisplay3D:
    """
    Widget for displaying player equipment

    Layout:
    ┌─────────────────────────────┐
    │ [EQUIPMENT]                 │
    │ Weapon: Iron Sword          │
    │ Armor: Leather Armor        │
    │ Accessory: Ring of Strength │
    │ Boots: Leather Boots        │
    └─────────────────────────────┘
    """

    # Color mapping for item rarities (RGB tuples, 0-1 range)
    RARITY_COLORS = {
        c.RARITY_COMMON: (0.7, 0.7, 0.7),      # Gray
        c.RARITY_UNCOMMON: (0.4, 0.8, 0.4),    # Green
        c.RARITY_RARE: (0.4, 0.6, 1.0),        # Blue
        c.RARITY_EPIC: (0.8, 0.4, 1.0),        # Purple
        c.RARITY_LEGENDARY: (1.0, 0.7, 0.0),   # Orange/Gold
    }

    def __init__(self, game: Game, parent: Optional[Entity] = None, position: Vec2 = Vec2(0.60, 0.90)):
        """
        Initialize equipment display

        Args:
            game: Game instance
            parent: Parent entity (defaults to None for screen space)
            position: Position in normalized screen coords (default: top-right)
        """
        self.game = game
        self.parent = parent
        self.position = position

        # UI elements
        self.background_panel: Optional[Entity] = None
        self.title_label: Optional[Text] = None
        self.weapon_label: Optional[Text] = None
        self.armor_label: Optional[Text] = None
        self.accessory_label: Optional[Text] = None
        self.boots_label: Optional[Text] = None

        # Layout constants (scaled for camera.ui coordinate space)
        self.PANEL_WIDTH = 0.50  # Adjusted for proper fit
        self.PANEL_HEIGHT = 0.40  # Adjusted for proper fit
        self.TEXT_SCALE = 1.0    # Increased for visibility
        self.TITLE_SCALE = 1.1   # Increased for visibility
        self.LINE_SPACING = 0.05 # Increased spacing

        # Cached values for conditional updates (performance optimization)
        self._last_weapon = None
        self._last_armor = None
        self._last_accessory = None
        self._last_boots = None

        # Create UI
        self._create_ui()

        print("✓ EquipmentDisplay3D initialized")
        print(f"  - Position: {self.position}")
        print(f"  - Panel size: {self.PANEL_WIDTH} x {self.PANEL_HEIGHT}")
        print(f"  - Background panel visible: {self.background_panel.visible if self.background_panel else False}")

    def _create_ui(self):
        """Create all UI elements"""
        # Background panel (translucent dark)
        self.background_panel = Entity(
            parent=self.parent,
            model='quad',
            color=color.rgba(0.05, 0.05, 0.1, 0.85),
            position=(self.position.x, self.position.y, -1),
            scale=(self.PANEL_WIDTH, self.PANEL_HEIGHT),
            origin=(-0.5, 0.5),  # Anchor to top-left of panel
            eternal=True
        )

        # Calculate positions relative to panel top-left
        base_x = self.position.x
        base_y = self.position.y

        # Title label
        self.title_label = Text(
            text="[EQUIPMENT]",
            parent=self.parent,
            position=(base_x + 0.01, base_y - 0.02, 0),
            scale=self.TITLE_SCALE,
            color=color.rgba(0.7, 0.7, 0.8, 1),
            origin=(-0.5, 0.5),
            eternal=True
        )

        # Equipment labels
        self.weapon_label = Text(
            text="Weapon: None",
            parent=self.parent,
            position=(base_x + 0.01, base_y - 0.06, 0),
            scale=self.TEXT_SCALE,
            color=color.rgba(0.7, 0.7, 0.7, 1),
            origin=(-0.5, 0.5),
            eternal=True
        )

        self.armor_label = Text(
            text="Armor: None",
            parent=self.parent,
            position=(base_x + 0.01, base_y - 0.06 - self.LINE_SPACING, 0),
            scale=self.TEXT_SCALE,
            color=color.rgba(0.7, 0.7, 0.7, 1),
            origin=(-0.5, 0.5),
            eternal=True
        )

        self.accessory_label = Text(
            text="Accessory: None",
            parent=self.parent,
            position=(base_x + 0.01, base_y - 0.06 - self.LINE_SPACING * 2, 0),
            scale=self.TEXT_SCALE,
            color=color.rgba(0.7, 0.7, 0.7, 1),
            origin=(-0.5, 0.5),
            eternal=True
        )

        self.boots_label = Text(
            text="Boots: None",
            parent=self.parent,
            position=(base_x + 0.01, base_y - 0.06 - self.LINE_SPACING * 3, 0),
            scale=self.TEXT_SCALE,
            color=color.rgba(0.7, 0.7, 0.7, 1),
            origin=(-0.5, 0.5),
            eternal=True
        )

    def update(self, dt: float):
        """
        Update equipment display (conditional updates for performance)

        Args:
            dt: Delta time since last frame
        """
        if not self.game.player:
            return

        player = self.game.player

        # Update weapon (only if changed)
        weapon = player.equipment[c.SLOT_WEAPON]
        if weapon != self._last_weapon:
            if weapon:
                item_name = weapon.get_name()
                item_color = self.RARITY_COLORS.get(weapon.rarity, (1, 1, 1))
                self.weapon_label.text = f"Weapon: {item_name}"
                self.weapon_label.color = color.rgb(*item_color)
            else:
                self.weapon_label.text = "Weapon: None"
                self.weapon_label.color = color.rgba(0.5, 0.5, 0.5, 1)
            self._last_weapon = weapon

        # Update armor (only if changed)
        armor = player.equipment[c.SLOT_ARMOR]
        if armor != self._last_armor:
            if armor:
                item_name = armor.get_name()
                item_color = self.RARITY_COLORS.get(armor.rarity, (1, 1, 1))
                self.armor_label.text = f"Armor: {item_name}"
                self.armor_label.color = color.rgb(*item_color)
            else:
                self.armor_label.text = "Armor: None"
                self.armor_label.color = color.rgba(0.5, 0.5, 0.5, 1)
            self._last_armor = armor

        # Update accessory (only if changed)
        accessory = player.equipment[c.SLOT_ACCESSORY]
        if accessory != self._last_accessory:
            if accessory:
                item_name = accessory.get_name()
                item_color = self.RARITY_COLORS.get(accessory.rarity, (1, 1, 1))
                self.accessory_label.text = f"Accessory: {item_name}"
                self.accessory_label.color = color.rgb(*item_color)
            else:
                self.accessory_label.text = "Accessory: None"
                self.accessory_label.color = color.rgba(0.5, 0.5, 0.5, 1)
            self._last_accessory = accessory

        # Update boots (only if changed)
        boots = player.equipment[c.SLOT_BOOTS]
        if boots != self._last_boots:
            if boots:
                item_name = boots.get_name()
                item_color = self.RARITY_COLORS.get(boots.rarity, (1, 1, 1))
                self.boots_label.text = f"Boots: {item_name}"
                self.boots_label.color = color.rgb(*item_color)
            else:
                self.boots_label.text = "Boots: None"
                self.boots_label.color = color.rgba(0.5, 0.5, 0.5, 1)
            self._last_boots = boots

    def cleanup(self):
        """Clean up all UI elements"""
        elements = [
            self.background_panel,
            self.title_label,
            self.weapon_label,
            self.armor_label,
            self.accessory_label,
            self.boots_label
        ]

        for element in elements:
            if element:
                element.disable()

        print("✓ EquipmentDisplay3D cleaned up")

    def __repr__(self) -> str:
        return f"<EquipmentDisplay3D position={self.position}>"
