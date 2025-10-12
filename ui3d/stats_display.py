"""
Stats Display 3D Widget

Displays player statistics including HP bar, XP bar, and character info.
Positioned in the top-left corner of the screen.
"""

from typing import Optional
from ursina import Entity, Text, color, Vec2, Vec3
from game import Game
import constants as c


class StatsDisplay3D:
    """
    Widget for displaying player stats (HP, XP, level, class)

    Layout:
    ┌─────────────────────────────┐
    │ Warrior - Level 5           │
    │ █████████░░ 120/150 HP      │
    │ ███████░░░░ 450/1000 XP     │
    │ Depth: 12                   │
    └─────────────────────────────┘
    """

    def __init__(self, game: Game, parent: Optional[Entity] = None, position: Vec2 = Vec2(-0.95, 0.90)):
        """
        Initialize stats display

        Args:
            game: Game instance
            parent: Parent entity (defaults to None for screen space)
            position: Position in normalized screen coords (default: top-left)
        """
        self.game = game
        self.parent = parent
        self.position = position

        # UI elements
        self.background_panel: Optional[Entity] = None
        self.class_level_label: Optional[Text] = None
        self.hp_bar_bg: Optional[Entity] = None
        self.hp_bar_fill: Optional[Entity] = None
        self.hp_text: Optional[Text] = None
        self.xp_bar_bg: Optional[Entity] = None
        self.xp_bar_fill: Optional[Entity] = None
        self.xp_text: Optional[Text] = None
        self.depth_label: Optional[Text] = None

        # Layout constants
        self.PANEL_WIDTH = 0.25
        self.PANEL_HEIGHT = 0.20
        self.BAR_WIDTH = 0.20
        self.BAR_HEIGHT = 0.02
        self.TEXT_SCALE = 0.8
        self.LABEL_SCALE = 0.7

        # Cached values for conditional updates (performance optimization)
        self._last_hp = 0
        self._last_max_hp = 0
        self._last_xp = 0
        self._last_xp_to_next = 0
        self._last_level = 0
        self._last_depth = 0

        # Create UI
        self._create_ui()

        print("✓ StatsDisplay3D initialized")

    def _create_ui(self):
        """Create all UI elements"""
        # Background panel (translucent dark)
        self.background_panel = Entity(
            parent=self.parent,
            model='quad',
            color=color.rgba(0.05, 0.05, 0.15, 0.8),
            position=(self.position.x, self.position.y, -1),
            scale=(self.PANEL_WIDTH, self.PANEL_HEIGHT),
            origin=(-0.5, 0.5),  # Anchor to top-left of panel
            eternal=True
        )

        # Calculate positions relative to panel top-left
        base_x = self.position.x
        base_y = self.position.y

        # Class and level label (top)
        self.class_level_label = Text(
            text="Warrior - Level 1",
            parent=self.parent,
            position=(base_x + 0.01, base_y - 0.02, 0),
            scale=self.TEXT_SCALE,
            color=color.rgba(1, 1, 1, 1),
            origin=(-0.5, 0.5),
            eternal=True
        )

        # HP Bar (background)
        hp_bar_y = base_y - 0.05
        self.hp_bar_bg = Entity(
            parent=self.parent,
            model='quad',
            color=color.rgba(0.2, 0.2, 0.2, 0.9),
            position=(base_x + 0.01, hp_bar_y, -0.5),
            scale=(self.BAR_WIDTH, self.BAR_HEIGHT),
            origin=(-0.5, 0.5),
            eternal=True
        )

        # HP Bar (fill) - will be scaled based on HP percentage
        self.hp_bar_fill = Entity(
            parent=self.parent,
            model='quad',
            color=color.rgb(0.2, 0.8, 0.2),  # Green (will change based on HP %)
            position=(base_x + 0.01, hp_bar_y, -0.4),
            scale=(self.BAR_WIDTH, self.BAR_HEIGHT),
            origin=(-0.5, 0.5),
            eternal=True
        )

        # HP Text label
        self.hp_text = Text(
            text="100/100 HP",
            parent=self.parent,
            position=(base_x + 0.01 + self.BAR_WIDTH + 0.01, hp_bar_y, 0),
            scale=self.LABEL_SCALE,
            color=color.rgba(1, 1, 1, 1),
            origin=(-0.5, 0.5),
            eternal=True
        )

        # XP Bar (background)
        xp_bar_y = base_y - 0.08
        self.xp_bar_bg = Entity(
            parent=self.parent,
            model='quad',
            color=color.rgba(0.2, 0.2, 0.2, 0.9),
            position=(base_x + 0.01, xp_bar_y, -0.5),
            scale=(self.BAR_WIDTH, self.BAR_HEIGHT),
            origin=(-0.5, 0.5),
            eternal=True
        )

        # XP Bar (fill)
        self.xp_bar_fill = Entity(
            parent=self.parent,
            model='quad',
            color=color.rgb(1, 0.8, 0),  # Gold
            position=(base_x + 0.01, xp_bar_y, -0.4),
            scale=(self.BAR_WIDTH, self.BAR_HEIGHT),
            origin=(-0.5, 0.5),
            eternal=True
        )

        # XP Text label
        self.xp_text = Text(
            text="0/100 XP",
            parent=self.parent,
            position=(base_x + 0.01 + self.BAR_WIDTH + 0.01, xp_bar_y, 0),
            scale=self.LABEL_SCALE,
            color=color.rgba(1, 1, 1, 1),
            origin=(-0.5, 0.5),
            eternal=True
        )

        # Depth label (bottom)
        self.depth_label = Text(
            text="Depth: 1",
            parent=self.parent,
            position=(base_x + 0.01, base_y - 0.12, 0),
            scale=self.LABEL_SCALE,
            color=color.rgba(0.8, 0.8, 0.8, 1),
            origin=(-0.5, 0.5),
            eternal=True
        )

    def update(self, dt: float):
        """
        Update stats display (conditional updates for performance)

        Args:
            dt: Delta time since last frame
        """
        if not self.game.player:
            return

        player = self.game.player

        # Update class and level (only if level changed)
        if player.level != self._last_level:
            class_name = player.get_class_name()
            self.class_level_label.text = f"{class_name} - Level {player.level}"
            self._last_level = player.level

        # Update HP bar (only if HP or max HP changed)
        if player.hp != self._last_hp or player.max_hp != self._last_max_hp:
            hp_percent = player.hp / player.max_hp if player.max_hp > 0 else 0
            self.hp_bar_fill.scale_x = self.BAR_WIDTH * hp_percent

            # Color code HP bar based on percentage
            if hp_percent > 0.6:
                self.hp_bar_fill.color = color.rgb(0.2, 0.8, 0.2)  # Green
            elif hp_percent > 0.3:
                self.hp_bar_fill.color = color.rgb(1.0, 0.8, 0.0)  # Yellow
            else:
                self.hp_bar_fill.color = color.rgb(1.0, 0.2, 0.2)  # Red

            self.hp_text.text = f"{player.hp}/{player.max_hp} HP"
            self._last_hp = player.hp
            self._last_max_hp = player.max_hp

        # Update XP bar (only if XP or XP requirement changed)
        if player.xp != self._last_xp or player.xp_to_next_level != self._last_xp_to_next:
            xp_percent = player.xp / player.xp_to_next_level if player.xp_to_next_level > 0 else 0
            self.xp_bar_fill.scale_x = self.BAR_WIDTH * xp_percent
            self.xp_text.text = f"{player.xp}/{player.xp_to_next_level} XP"
            self._last_xp = player.xp
            self._last_xp_to_next = player.xp_to_next_level

        # Update depth (only if level changed)
        if self.game.current_level != self._last_depth:
            self.depth_label.text = f"Depth: {self.game.current_level}"
            self._last_depth = self.game.current_level

    def cleanup(self):
        """Clean up all UI elements"""
        elements = [
            self.background_panel,
            self.class_level_label,
            self.hp_bar_bg,
            self.hp_bar_fill,
            self.hp_text,
            self.xp_bar_bg,
            self.xp_bar_fill,
            self.xp_text,
            self.depth_label
        ]

        for element in elements:
            if element:
                element.disable()

        print("✓ StatsDisplay3D cleaned up")

    def __repr__(self) -> str:
        return f"<StatsDisplay3D position={self.position}>"
