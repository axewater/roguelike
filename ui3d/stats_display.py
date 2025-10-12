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
        self.attack_label: Optional[Text] = None
        self.defense_label: Optional[Text] = None
        self.depth_label: Optional[Text] = None
        self.exploration_label: Optional[Text] = None
        self.stealth_label: Optional[Text] = None

        # Layout constants (scaled for camera.ui coordinate space)
        self.PANEL_WIDTH = 0.50  # Reduced from 0.25
        self.PANEL_HEIGHT = 0.55  # Reduced from 0.30
        self.BAR_WIDTH = 0.40   # Reduced from 0.20
        self.BAR_HEIGHT = 0.04  # Adjusted
        self.TEXT_SCALE = 1.2   # Increased for visibility
        self.LABEL_SCALE = 1.0  # Increased for visibility

        # Cached values for conditional updates (performance optimization)
        self._last_hp = 0
        self._last_max_hp = 0
        self._last_xp = 0
        self._last_xp_to_next = 0
        self._last_level = 0
        self._last_attack = 0
        self._last_defense = 0
        self._last_depth = 0
        self._last_exploration = 0.0
        self._last_stealth_status = ""

        # Create UI
        self._create_ui()

        print("✓ StatsDisplay3D initialized")
        print(f"  - Position: {self.position}")
        print(f"  - Panel size: {self.PANEL_WIDTH} x {self.PANEL_HEIGHT}")
        print(f"  - Background panel visible: {self.background_panel.visible if self.background_panel else False}")
        print(f"  - NEW: Added Attack, Defense, Exploration %, Stealth status")

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

        # Attack label
        self.attack_label = Text(
            text="Attack: 10",
            parent=self.parent,
            position=(base_x + 0.01, base_y - 0.12, 0),
            scale=self.LABEL_SCALE,
            color=color.rgba(1.0, 0.7, 0.7, 1),  # Light red
            origin=(-0.5, 0.5),
            eternal=True
        )

        # Defense label
        self.defense_label = Text(
            text="Defense: 5",
            parent=self.parent,
            position=(base_x + 0.01, base_y - 0.15, 0),
            scale=self.LABEL_SCALE,
            color=color.rgba(0.7, 0.7, 1.0, 1),  # Light blue
            origin=(-0.5, 0.5),
            eternal=True
        )

        # Depth label
        self.depth_label = Text(
            text="Depth: 1",
            parent=self.parent,
            position=(base_x + 0.01, base_y - 0.18, 0),
            scale=self.LABEL_SCALE,
            color=color.rgba(0.8, 0.8, 0.8, 1),
            origin=(-0.5, 0.5),
            eternal=True
        )

        # Exploration label
        self.exploration_label = Text(
            text="Explored: 0.0%",
            parent=self.parent,
            position=(base_x + 0.01, base_y - 0.21, 0),
            scale=self.LABEL_SCALE,
            color=color.rgba(0.7, 0.9, 0.7, 1),  # Light green
            origin=(-0.5, 0.5),
            eternal=True
        )

        # Stealth label (Rogue only - initially hidden)
        self.stealth_label = Text(
            text="",
            parent=self.parent,
            position=(base_x + 0.01, base_y - 0.24, 0),
            scale=self.LABEL_SCALE,
            color=color.rgba(0.3, 0.9, 0.5, 1),  # Bright green for HIDDEN
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

        # Update attack stat (only if changed)
        if player.attack != self._last_attack:
            self.attack_label.text = f"Attack: {player.attack}"
            self._last_attack = player.attack

        # Update defense stat (only if changed)
        if player.defense != self._last_defense:
            self.defense_label.text = f"Defense: {player.defense}"
            self._last_defense = player.defense

        # Update depth (only if level changed)
        if self.game.current_level != self._last_depth:
            self.depth_label.text = f"Depth: {self.game.current_level}"
            self._last_depth = self.game.current_level

        # Update exploration percentage (every frame, but cache comparison)
        exploration_percent = self._calculate_exploration_percentage()
        if abs(exploration_percent - self._last_exploration) > 0.1:  # Only update if changed by 0.1%
            self.exploration_label.text = f"Explored: {exploration_percent:.1f}%"
            self._last_exploration = exploration_percent

        # Update stealth status (Rogue only)
        if player.class_type == c.CLASS_ROGUE:
            stealth_status = self._get_stealth_status()
            if stealth_status != self._last_stealth_status:
                self.stealth_label.text = stealth_status

                # Change color based on stealth state
                if "HIDDEN" in stealth_status:
                    self.stealth_label.color = color.rgba(0.3, 0.9, 0.5, 1)  # Bright green
                else:
                    self.stealth_label.color = color.rgba(1.0, 0.3, 0.3, 1)  # Red

                self._last_stealth_status = stealth_status
        else:
            # Hide stealth label for non-Rogue classes
            if self._last_stealth_status != "":
                self.stealth_label.text = ""
                self._last_stealth_status = ""

    def _calculate_exploration_percentage(self) -> float:
        """Calculate percentage of dungeon explored"""
        if not self.game.visibility_map or not self.game.dungeon:
            return 0.0

        explored_count = self.game.visibility_map.count_explored()

        # Count total walkable tiles (floor + stairs)
        total_floor_tiles = sum(
            1 for y in range(self.game.dungeon.height)
            for x in range(self.game.dungeon.width)
            if self.game.dungeon.is_walkable(x, y) or
               self.game.dungeon.get_tile(x, y) == c.TILE_STAIRS
        )

        if total_floor_tiles > 0:
            return (explored_count / total_floor_tiles) * 100
        return 0.0

    def _get_stealth_status(self) -> str:
        """Get stealth status for Rogue (HIDDEN or DETECTED)"""
        if not self.game.player or not self.game.dungeon:
            return ""

        # Count enemies that can see the player
        enemies_detecting = self._count_enemies_detecting_player()

        if enemies_detecting == 0:
            return "HIDDEN"
        else:
            return f"DETECTED ({enemies_detecting})"

    def _count_enemies_detecting_player(self) -> int:
        """Count how many enemies can currently see the player"""
        if not self.game.player or not self.game.dungeon:
            return 0

        count = 0
        from fov import calculate_fov

        for enemy in self.game.enemies:
            # Calculate enemy's FOV
            enemy_fov = calculate_fov(
                self.game.dungeon,
                enemy.x,
                enemy.y,
                enemy.vision_radius
            )

            # Check if player is in enemy's FOV
            if (self.game.player.x, self.game.player.y) in enemy_fov:
                count += 1

        return count

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
            self.attack_label,
            self.defense_label,
            self.depth_label,
            self.exploration_label,
            self.stealth_label
        ]

        for element in elements:
            if element:
                element.disable()

        print("✓ StatsDisplay3D cleaned up")

    def __repr__(self) -> str:
        return f"<StatsDisplay3D position={self.position}>"
