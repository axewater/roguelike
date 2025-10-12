"""
Nearby Items Display 3D Widget

Displays items near the player (within 5 tiles) with distance and stat preview.
Positioned below the equipment display on the right side.
"""

from typing import Optional, List, Tuple
from ursina import Entity, Text, color, Vec2
from game import Game
import constants as c


class NearbyItemsDisplay3D:
    """
    Widget for displaying nearby items

    Layout:
    ┌─────────────────────────────────┐
    │ [NEARBY ITEMS]                  │
    │ • Rare Sword (2t)               │  (blue)
    │   +15 ATK, +5 DEF               │  (gray)
    │ • Health Potion (3t)            │  (green)
    │   +50 HP                        │  (gray)
    │ • Ring of Strength (4t)         │  (purple)
    │   +8 ATK, +12 HP                │  (gray)
    └─────────────────────────────────┘
    """

    # Color mapping for item rarities (RGB tuples, 0-1 range)
    RARITY_COLORS = {
        c.RARITY_COMMON: (0.7, 0.7, 0.7),      # Gray
        c.RARITY_UNCOMMON: (0.4, 0.8, 0.4),    # Green
        c.RARITY_RARE: (0.4, 0.6, 1.0),        # Blue
        c.RARITY_EPIC: (0.8, 0.4, 1.0),        # Purple
        c.RARITY_LEGENDARY: (1.0, 0.7, 0.0),   # Orange/Gold
    }

    def __init__(self, game: Game, parent: Optional[Entity] = None, position: Vec2 = Vec2(0.60, 0.50)):
        """
        Initialize nearby items display

        Args:
            game: Game instance
            parent: Parent entity (defaults to None for screen space)
            position: Position in normalized screen coords (default: right side, below equipment)
        """
        self.game = game
        self.parent = parent
        self.position = position

        # UI elements
        self.background_panel: Optional[Entity] = None
        self.title_label: Optional[Text] = None
        self.item_labels: List[Text] = []  # Item name + distance labels
        self.stat_labels: List[Text] = []  # Stat preview labels

        # Layout constants (scaled for camera.ui coordinate space)
        self.PANEL_WIDTH = 0.50   # Adjusted for proper fit
        self.PANEL_HEIGHT = 0.35  # Adjusted for proper fit
        self.TEXT_SCALE = 1.0     # Increased for visibility
        self.STAT_SCALE = 0.8     # Increased for visibility
        self.TITLE_SCALE = 1.1    # Increased for visibility
        self.ITEM_SPACING = 0.08  # Vertical spacing between items
        self.MAX_VISIBLE_ITEMS = 3

        # Cached values for conditional updates (performance optimization)
        self._last_nearby_items: List[Tuple] = []

        # Create UI
        self._create_ui()

        print("✓ NearbyItemsDisplay3D initialized")
        print(f"  - Position: {self.position}")
        print(f"  - Panel size: {self.PANEL_WIDTH} x {self.PANEL_HEIGHT}")
        print(f"  - Background panel visible: {self.background_panel.visible if self.background_panel else False}")
        print(f"  - Max visible items: {self.MAX_VISIBLE_ITEMS}")

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
            text="[NEARBY ITEMS]",
            parent=self.parent,
            position=(base_x + 0.01, base_y - 0.02, 0),
            scale=self.TITLE_SCALE,
            color=color.rgba(0.7, 0.7, 0.8, 1),
            origin=(-0.5, 0.5),
            eternal=True
        )

        # Create item and stat labels (pre-allocated for performance)
        for i in range(self.MAX_VISIBLE_ITEMS):
            # Item name + distance label
            item_y = base_y - 0.06 - (i * self.ITEM_SPACING)
            item_label = Text(
                text="",
                parent=self.parent,
                position=(base_x + 0.01, item_y, 0),
                scale=self.TEXT_SCALE,
                color=color.rgba(1, 1, 1, 1),
                origin=(-0.5, 0.5),
                visible=False,  # Hidden initially
                eternal=True
            )
            self.item_labels.append(item_label)

            # Stat preview label (below item name)
            stat_y = item_y - 0.02
            stat_label = Text(
                text="",
                parent=self.parent,
                position=(base_x + 0.03, stat_y, 0),  # Indent slightly
                scale=self.STAT_SCALE,
                color=color.rgba(0.5, 0.5, 0.5, 1),  # Gray
                origin=(-0.5, 0.5),
                visible=False,  # Hidden initially
                eternal=True
            )
            self.stat_labels.append(stat_label)

    def update(self, dt: float):
        """
        Update nearby items display (conditional updates for performance)

        Args:
            dt: Delta time since last frame
        """
        if not self.game.player:
            return

        # Get nearby items (within 5 tiles)
        nearby_items = self._get_nearby_items(max_distance=5)

        # Only update if nearby items changed
        if nearby_items != self._last_nearby_items:
            self._update_item_labels(nearby_items)
            self._last_nearby_items = nearby_items

    def _get_nearby_items(self, max_distance: int) -> List[Tuple]:
        """
        Get items within max_distance tiles of player, sorted by distance

        Args:
            max_distance: Maximum distance in tiles

        Returns:
            List of (item, distance) tuples, sorted by distance
        """
        if not self.game.player:
            return []

        nearby = []
        player_x, player_y = self.game.player.x, self.game.player.y

        for item in self.game.items:
            # Manhattan distance
            distance = abs(item.x - player_x) + abs(item.y - player_y)
            if distance <= max_distance and distance > 0:  # Exclude current tile
                nearby.append((item, distance))

        # Sort by distance (closest first)
        nearby.sort(key=lambda x: x[1])

        # Return only top MAX_VISIBLE_ITEMS
        return nearby[:self.MAX_VISIBLE_ITEMS]

    def _update_item_labels(self, nearby_items: List[Tuple]):
        """
        Update item labels with nearby items data

        Args:
            nearby_items: List of (item, distance) tuples
        """
        # Update visible labels
        for i in range(self.MAX_VISIBLE_ITEMS):
            if i < len(nearby_items):
                item, distance = nearby_items[i]

                # Item name + distance
                item_name = item.get_name()
                item_color = self.RARITY_COLORS.get(item.rarity, (1, 1, 1))
                self.item_labels[i].text = f"• {item_name} ({distance}t)"
                self.item_labels[i].color = color.rgb(*item_color)
                self.item_labels[i].visible = True

                # Stat preview
                stat_preview = self._get_item_stats_preview(item)
                self.stat_labels[i].text = f"  {stat_preview}"
                self.stat_labels[i].visible = True
            else:
                # Hide unused labels
                self.item_labels[i].visible = False
                self.stat_labels[i].visible = False

        # Show "No items nearby" message if no items
        if not nearby_items:
            self.item_labels[0].text = "No items nearby"
            self.item_labels[0].color = color.rgba(0.4, 0.4, 0.4, 1)
            self.item_labels[0].visible = True
            self.stat_labels[0].visible = False

    def _get_item_stats_preview(self, item) -> str:
        """
        Get stats preview string for an item

        Args:
            item: Item instance

        Returns:
            String describing item stats (e.g., "+5 ATK, +3 DEF")
        """
        if item.item_type == c.ITEM_HEALTH_POTION:
            heal_amount = c.ITEM_EFFECTS[c.ITEM_HEALTH_POTION]["heal"]
            return f"+{heal_amount} HP"

        stats = []
        if item.get_stat_bonus("attack") > 0:
            stats.append(f"+{item.get_stat_bonus('attack')} ATK")
        if item.get_stat_bonus("defense") > 0:
            stats.append(f"+{item.get_stat_bonus('defense')} DEF")
        if item.get_stat_bonus("hp") > 0:
            stats.append(f"+{item.get_stat_bonus('hp')} HP")

        return ", ".join(stats) if stats else "No stats"

    def cleanup(self):
        """Clean up all UI elements"""
        # Clean up item and stat labels
        for label in self.item_labels + self.stat_labels:
            if label:
                label.disable()

        self.item_labels.clear()
        self.stat_labels.clear()

        # Clean up panel and title
        if self.background_panel:
            self.background_panel.disable()

        if self.title_label:
            self.title_label.disable()

        print("✓ NearbyItemsDisplay3D cleaned up")

    def __repr__(self) -> str:
        return f"<NearbyItemsDisplay3D position={self.position}>"
