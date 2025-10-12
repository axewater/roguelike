"""
3D UI Overlay Manager

Manages all UI components for 3D mode using Ursina's UI system.
Provides a unified interface for updating and rendering UI elements.
"""

from typing import Optional
from ursina import Entity, Text, color, window, Vec2, camera
from game import Game
from ui3d.stats_display import StatsDisplay3D
from ui3d.combat_log_3d import CombatLog3D
from ui3d.ability_bar import AbilityBar3D
from ui3d.targeting import TargetingSystem
from ui3d.equipment_display import EquipmentDisplay3D
from ui3d.nearby_items import NearbyItemsDisplay3D


class UI3DManager:
    """
    Main manager for 3D UI overlay

    Coordinates all UI widgets (stats, combat log, ability bar) and
    provides lifecycle management (init, update, cleanup).
    """

    def __init__(self, game: Game):
        """
        Initialize UI manager

        Args:
            game: Game instance to display UI for
        """
        self.game = game
        self.visible = True

        # UI positioning constants (relative to screen edges)
        # Ursina camera.ui uses normalized coordinates: approximately -0.5 to 0.5 range
        # (0, 0) = screen center
        self.ANCHOR_TOP_LEFT = Vec2(-0.85, 0.45)      # Stats display
        self.ANCHOR_TOP_RIGHT = Vec2(0.35, 0.45)      # Equipment display
        self.ANCHOR_RIGHT_MID = Vec2(0.35, 0.0)       # Nearby items display
        self.ANCHOR_BOTTOM_LEFT = Vec2(-0.85, -0.30)  # Combat log
        self.ANCHOR_BOTTOM_RIGHT = Vec2(0.20, -0.40)  # Ability bar

        # UI scale factors (adjust for different resolutions)
        self.UI_SCALE = 1.0
        self.TEXT_SCALE = 1.0

        # Background panels (translucent)
        self.background_panels = []

        # UI widgets (will be initialized in subclasses)
        self.stats_display = None
        self.equipment_display = None
        self.nearby_items_display = None
        self.combat_log = None
        self.ability_bar = None
        self.targeting_system = None

        # Root UI entity (parent for all UI elements)
        # IMPORTANT: Must be parented to camera.ui for screen-space rendering
        self.ui_root = Entity(
            name='ui_root_3d',
            parent=camera.ui,  # Attach to Ursina's screen-space UI system
            eternal=True,  # Don't destroy on scene change
            enabled=True
        )

        # Initialize all widgets
        self.initialize_widgets()

        print("✓ UI3DManager initialized")
        print(f"  - Screen size: {window.size}")
        print(f"  - Anchors configured:")
        print(f"    • Top-Left (Stats): {self.ANCHOR_TOP_LEFT}")
        print(f"    • Top-Right (Equipment): {self.ANCHOR_TOP_RIGHT}")
        print(f"    • Right-Mid (Nearby Items): {self.ANCHOR_RIGHT_MID}")
        print(f"    • Bottom-Left (Combat Log): Vec2(-0.95, -0.50)")
        print(f"    • Bottom-Right (Ability Bar): Vec2(0.55, -0.85)")

    def initialize_widgets(self):
        """Initialize all UI widgets"""
        # Stats display (top-left)
        self.stats_display = StatsDisplay3D(
            game=self.game,
            parent=self.ui_root,
            position=self.ANCHOR_TOP_LEFT
        )

        # Equipment display (top-right)
        self.equipment_display = EquipmentDisplay3D(
            game=self.game,
            parent=self.ui_root,
            position=self.ANCHOR_TOP_RIGHT
        )

        # Nearby items display (right side, below equipment)
        self.nearby_items_display = NearbyItemsDisplay3D(
            game=self.game,
            parent=self.ui_root,
            position=self.ANCHOR_RIGHT_MID
        )

        # Combat log (bottom-left)
        self.combat_log = CombatLog3D(
            parent=self.ui_root,
            position=self.ANCHOR_BOTTOM_LEFT
        )

        # Ability bar (bottom-right)
        self.ability_bar = AbilityBar3D(
            game=self.game,
            parent=self.ui_root,
            position=self.ANCHOR_BOTTOM_RIGHT
        )

        # Targeting system
        self.targeting_system = TargetingSystem(
            game=self.game,
            parent=self.ui_root
        )

        print("✓ All UI widgets initialized")
        print(f"  - Widget count: 6 (Stats, Equipment, Nearby Items, Combat Log, Ability Bar, Targeting)")
        print(f"  - UI root enabled: {self.ui_root.enabled}")
        print(f"  - UI visible: {self.visible}")

    def create_background_panel(self, position: Vec2, size: Vec2, panel_color: tuple = (0.05, 0.05, 0.1, 0.7)) -> Entity:
        """
        Create a translucent background panel

        Args:
            position: Panel position (normalized screen coords)
            size: Panel size (normalized screen coords)
            panel_color: RGBA color tuple (0-1 range), default dark blue with 70% opacity

        Returns:
            Entity: Background panel entity
        """
        panel = Entity(
            parent=self.ui_root,
            model='quad',
            color=color.rgba(*panel_color),
            position=(position.x, position.y, 0),
            scale=(size.x, size.y, 1),
            origin=(0, 0),  # Anchor to center of quad
            eternal=True
        )

        self.background_panels.append(panel)
        return panel

    def create_text_label(
        self,
        text: str = "",
        position: Vec2 = Vec2(0, 0),
        scale: float = 1.0,
        text_color: tuple = (1, 1, 1, 1),
        parent: Optional[Entity] = None
    ) -> Text:
        """
        Create a text label entity

        Args:
            text: Initial text content
            position: Text position (normalized coords)
            scale: Text scale multiplier
            text_color: RGBA color tuple (0-1 range)
            parent: Parent entity (defaults to ui_root)

        Returns:
            Text: Text entity
        """
        text_entity = Text(
            text=text,
            parent=parent if parent else self.ui_root,
            position=(position.x, position.y, 0),
            scale=scale * self.TEXT_SCALE,
            color=color.rgba(*text_color),
            origin=(0, 0),
            eternal=True
        )

        return text_entity

    def set_visibility(self, visible: bool):
        """
        Toggle UI visibility

        Args:
            visible: True to show UI, False to hide
        """
        self.visible = visible
        self.ui_root.enabled = visible

        print(f"[UI3D] Visibility set to: {visible}")

    def update(self, dt: float):
        """
        Update UI state (called every frame)

        Args:
            dt: Delta time since last frame
        """
        if not self.visible:
            return

        # Update individual widgets
        if self.stats_display:
            self.stats_display.update(dt)

        if self.equipment_display:
            self.equipment_display.update(dt)

        if self.nearby_items_display:
            self.nearby_items_display.update(dt)

        if self.combat_log:
            self.combat_log.update(dt)

        if self.ability_bar:
            self.ability_bar.update(dt)

        if self.targeting_system:
            self.targeting_system.update(dt)

    def add_message(self, message: str, msg_type: str = "event"):
        """
        Add a message to the combat log

        Args:
            message: Message text
            msg_type: Message type for color coding (damage, heal, loot, event, etc.)
        """
        if self.combat_log:
            self.combat_log.add_message(message, msg_type)
        else:
            print(f"[COMBAT LOG] {message}")  # Fallback to console

    def cleanup(self):
        """
        Clean up all UI entities and resources
        """
        # Disable and destroy all background panels
        for panel in self.background_panels:
            panel.disable()
        self.background_panels.clear()

        # Clean up widgets
        if self.stats_display:
            self.stats_display.cleanup()
            self.stats_display = None

        if self.equipment_display:
            self.equipment_display.cleanup()
            self.equipment_display = None

        if self.nearby_items_display:
            self.nearby_items_display.cleanup()
            self.nearby_items_display = None

        if self.combat_log:
            self.combat_log.cleanup()
            self.combat_log = None

        if self.ability_bar:
            self.ability_bar.cleanup()
            self.ability_bar = None

        if self.targeting_system:
            self.targeting_system.cleanup()
            self.targeting_system = None

        # Destroy root entity
        if self.ui_root:
            self.ui_root.disable()
            self.ui_root = None

        print("✓ UI3DManager cleaned up")

    def get_resolution_scale(self) -> float:
        """
        Calculate UI scale factor based on window resolution

        Uses 1920x1080 as baseline (scale=1.0)

        Returns:
            float: Scale factor for UI elements
        """
        baseline_width = 1920
        current_width = window.size[0]

        scale = current_width / baseline_width
        return max(0.5, min(2.0, scale))  # Clamp between 0.5x and 2.0x

    def __repr__(self) -> str:
        return f"<UI3DManager visible={self.visible} widgets={sum([1 for w in [self.stats_display, self.equipment_display, self.nearby_items_display, self.combat_log, self.ability_bar, self.targeting_system] if w is not None])}>"
