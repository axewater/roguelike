"""
Ability Bar 3D Widget

Displays ability slots with cooldown indicators and hotkey labels.
Positioned in the bottom-right corner of the screen.
"""

from typing import Optional, List
from ursina import Entity, Text, color, Vec2
from game import Game


class AbilitySlot:
    """Single ability slot with cooldown visualization"""

    def __init__(
        self,
        ability_index: int,
        parent: Optional[Entity],
        position: Vec2,
        slot_size: float = 0.12  # Increased from 0.08 for visibility
    ):
        """
        Create ability slot

        Args:
            ability_index: Index of ability (0, 1, or 2)
            parent: Parent entity
            position: Slot position in normalized coords
            slot_size: Size of slot square
        """
        self.ability_index = ability_index
        self.position = position
        self.slot_size = slot_size

        # UI elements
        self.background: Optional[Entity] = None
        self.icon_bg: Optional[Entity] = None
        self.cooldown_overlay: Optional[Entity] = None
        self.ability_name_text: Optional[Text] = None
        self.hotkey_text: Optional[Text] = None
        self.cooldown_text: Optional[Text] = None

        # Cached values for conditional updates (performance optimization)
        self._last_ability_name = None
        self._last_is_ready = None
        self._last_cooldown_remaining = -1

        # Ability colors (for icon background)
        self.ABILITY_COLORS = {
            "Fireball": (1.0, 0.5, 0.0),      # Orange
            "Frost Nova": (0.3, 0.7, 1.0),    # Cyan
            "Heal": (0.3, 1.0, 0.5),          # Green
            "Dash": (0.7, 0.3, 1.0),          # Purple
            "Shadow Step": (0.5, 0.5, 0.5),   # Gray
            "Whirlwind": (1.0, 0.3, 0.3),     # Red
        }

        # Create UI
        self._create_ui(parent)

    def _create_ui(self, parent: Entity):
        """Create slot UI elements"""
        # Background (dark border)
        self.background = Entity(
            parent=parent,
            model='quad',
            color=color.rgba(0.1, 0.1, 0.15, 0.9),
            position=(self.position.x, self.position.y, -1),
            scale=(self.slot_size, self.slot_size),
            origin=(0, 0),
            eternal=True
        )

        # Icon background (ability color)
        self.icon_bg = Entity(
            parent=parent,
            model='quad',
            color=color.rgb(0.3, 0.3, 0.3),  # Gray until ability assigned
            position=(self.position.x, self.position.y, -0.9),
            scale=(self.slot_size * 0.9, self.slot_size * 0.9),
            origin=(0, 0),
            eternal=True
        )

        # Cooldown overlay (semi-transparent, covers icon when on cooldown)
        self.cooldown_overlay = Entity(
            parent=parent,
            model='quad',
            color=color.rgba(0, 0, 0, 0.7),
            position=(self.position.x, self.position.y, -0.8),
            scale=(self.slot_size * 0.9, self.slot_size * 0.9),
            origin=(0, 0),
            visible=False,  # Hidden when ready
            eternal=True
        )

        # Ability name (above slot)
        self.ability_name_text = Text(
            text="",
            parent=parent,
            position=(self.position.x, self.position.y + self.slot_size * 0.6, 0),
            scale=0.8,  # Increased from 0.5 for visibility
            color=color.rgba(1, 1, 1, 1),
            origin=(0, 0),
            eternal=True
        )

        # Hotkey label (bottom of slot)
        hotkey_number = self.ability_index + 1
        self.hotkey_text = Text(
            text=f"[{hotkey_number}]",
            parent=parent,
            position=(self.position.x, self.position.y - self.slot_size * 0.6, 0),
            scale=0.9,  # Increased from 0.6 for visibility
            color=color.rgba(1, 1, 0.5, 1),
            origin=(0, 0),
            eternal=True
        )

        # Cooldown timer text (center of slot, shown when on cooldown)
        self.cooldown_text = Text(
            text="",
            parent=parent,
            position=(self.position.x, self.position.y, 0),
            scale=1.2,  # Increased from 0.8 for visibility
            color=color.rgba(1, 1, 1, 1),
            origin=(0, 0),
            visible=False,
            eternal=True
        )

    def update_ability(self, ability):
        """
        Update slot with ability data (conditional updates for performance)

        Args:
            ability: Ability instance or None
        """
        if not ability:
            # Empty slot - only update if changed
            if self._last_ability_name is not None:
                self.ability_name_text.text = ""
                self.icon_bg.color = color.rgb(0.3, 0.3, 0.3)
                self.cooldown_overlay.visible = False
                self.cooldown_text.visible = False
                self._last_ability_name = None
                self._last_is_ready = None
                self._last_cooldown_remaining = -1
            return

        # Update ability name (only if changed)
        if ability.name != self._last_ability_name:
            self.ability_name_text.text = ability.name

            # Update icon color
            ability_color = self.ABILITY_COLORS.get(ability.name, (0.5, 0.5, 0.5))
            self.icon_bg.color = color.rgb(*ability_color)

            self._last_ability_name = ability.name

        # Update cooldown state (only if changed)
        is_ready = ability.is_ready()
        cooldown_remaining = int(ability.current_cooldown) + 1 if not is_ready else 0

        if is_ready != self._last_is_ready or cooldown_remaining != self._last_cooldown_remaining:
            if is_ready:
                # Ability ready
                self.cooldown_overlay.visible = False
                self.cooldown_text.visible = False
            else:
                # Ability on cooldown
                self.cooldown_overlay.visible = True
                self.cooldown_text.visible = True

                # Show cooldown timer
                self.cooldown_text.text = f"{cooldown_remaining}s"

                # Scale overlay based on cooldown progress
                cooldown_percent = ability.current_cooldown / ability.max_cooldown
                self.cooldown_overlay.scale_y = self.slot_size * 0.9 * cooldown_percent

            self._last_is_ready = is_ready
            self._last_cooldown_remaining = cooldown_remaining

    def cleanup(self):
        """Clean up slot UI elements"""
        elements = [
            self.background,
            self.icon_bg,
            self.cooldown_overlay,
            self.ability_name_text,
            self.hotkey_text,
            self.cooldown_text
        ]

        for element in elements:
            if element:
                element.disable()


class AbilityBar3D:
    """
    Widget for displaying ability slots

    Layout:
    ┌─────────────────────────────┐
    │  Fireball   Heal   Dash     │
    │  ┌─────┐  ┌─────┐  ┌─────┐  │
    │  │  🔥 │  │  💚 │  │  💨 │  │  (ability icons)
    │  │ [1] │  │ [2] │  │ [3] │  │  (hotkeys)
    │  └─────┘  └─────┘  └─────┘  │
    └─────────────────────────────┘
    """

    def __init__(self, game: Game, parent: Optional[Entity] = None, position: Vec2 = Vec2(0.55, -0.85)):
        """
        Initialize ability bar

        Args:
            game: Game instance
            parent: Parent entity
            position: Position in normalized screen coords (default: bottom-right)
        """
        self.game = game
        self.parent = parent
        self.position = position

        # UI elements
        self.background_panel: Optional[Entity] = None
        self.slots: List[AbilitySlot] = []

        # Layout constants (scaled for camera.ui coordinate space)
        self.PANEL_WIDTH = 0.60   # Adjusted for proper fit
        self.PANEL_HEIGHT = 0.25  # Adjusted for proper fit
        self.SLOT_SIZE = 0.12     # Increased for visibility
        self.SLOT_SPACING = 0.15  # Increased spacing

        # Create UI
        self._create_ui()

        print("✓ AbilityBar3D initialized")

    def _create_ui(self):
        """Create ability bar UI"""
        # Background panel
        self.background_panel = Entity(
            parent=self.parent,
            model='quad',
            color=color.rgba(0.05, 0.05, 0.1, 0.85),
            position=(self.position.x, self.position.y, -1),
            scale=(self.PANEL_WIDTH, self.PANEL_HEIGHT),
            origin=(0, 0),
            eternal=True
        )

        # Create 3 ability slots
        start_x = self.position.x + 0.05
        slot_y = self.position.y + 0.05

        for i in range(3):
            slot_x = start_x + (i * self.SLOT_SPACING)
            slot = AbilitySlot(
                ability_index=i,
                parent=self.parent,
                position=Vec2(slot_x, slot_y),
                slot_size=self.SLOT_SIZE
            )
            self.slots.append(slot)

    def update(self, dt: float):
        """
        Update ability slots

        Args:
            dt: Delta time since last frame
        """
        if not self.game.player or not self.game.player.abilities:
            return

        # Update each slot with corresponding ability
        for i, slot in enumerate(self.slots):
            if i < len(self.game.player.abilities):
                ability = self.game.player.abilities[i]
                slot.update_ability(ability)
            else:
                slot.update_ability(None)

    def cleanup(self):
        """Clean up all UI elements"""
        # Clean up slots
        for slot in self.slots:
            slot.cleanup()
        self.slots.clear()

        # Clean up background
        if self.background_panel:
            self.background_panel.disable()

        print("✓ AbilityBar3D cleaned up")

    def __repr__(self) -> str:
        return f"<AbilityBar3D slots={len(self.slots)}>"
