"""
Combat Log 3D Widget

Displays scrolling combat messages with color coding.
Positioned in the bottom-left corner of the screen.
"""

from typing import Optional, List, Tuple
from collections import deque
from ursina import Entity, Text, color, Vec2
import time


class CombatLogEntry:
    """Single combat log message with metadata"""

    def __init__(self, message: str, msg_type: str, timestamp: float):
        """
        Create log entry

        Args:
            message: Message text
            msg_type: Message type for color coding
            timestamp: Creation time (for fade calculation)
        """
        self.message = message
        self.msg_type = msg_type
        self.timestamp = timestamp
        self.text_entity: Optional[Text] = None


class CombatLog3D:
    """
    Widget for displaying scrolling combat messages

    Layout:
    ┌─────────────────────────────────┐
    │ [COMBAT LOG]                    │
    │ • You hit Goblin for 15 damage  │  (red)
    │ • Goblin hits you for 8 damage  │  (orange)
    │ • You picked up Rare Sword      │  (blue)
    │ • Level Up! Now level 5         │  (green)
    │ • Critical hit! 30 damage       │  (yellow)
    └─────────────────────────────────┘
    """

    # Color mapping for message types (RGB tuples, 0-1 range)
    MESSAGE_COLORS = {
        "damage": (1.0, 0.4, 0.4),         # Red
        "heal": (0.3, 0.8, 0.4),           # Green
        "loot": (1.0, 0.85, 0.2),          # Gold
        "loot_rare": (0.4, 0.6, 1.0),      # Blue
        "loot_legendary": (1.0, 0.7, 0.0), # Orange
        "event": (1.0, 1.0, 1.0),          # White
        "death": (0.8, 0.2, 0.2),          # Dark red
        "kill": (1.0, 0.4, 0.8),           # Pink
        "levelup": (0.3, 1.0, 0.5),        # Bright green
        "crit": (1.0, 0.65, 0.0),          # Orange
        "player_attack": (1.0, 0.6, 0.6),  # Light red
        "enemy_attack": (1.0, 0.8, 0.4),   # Light orange
        "potion": (0.5, 1.0, 0.8),         # Cyan
        "stairs": (0.8, 0.8, 1.0),         # Light blue
    }

    def __init__(self, parent: Optional[Entity] = None, position: Vec2 = Vec2(-0.95, -0.50)):
        """
        Initialize combat log

        Args:
            parent: Parent entity
            position: Position in normalized screen coords (default: bottom-left)
        """
        self.parent = parent
        self.position = position

        # Message queue (FIFO, max 50 stored)
        self.messages: deque[CombatLogEntry] = deque(maxlen=50)

        # Display settings
        self.MAX_VISIBLE_MESSAGES = 5
        self.FADE_DURATION = 5.0  # Seconds before message starts fading
        self.PANEL_WIDTH = 0.35
        self.PANEL_HEIGHT = 0.25
        self.MESSAGE_SPACING = 0.03  # Vertical spacing between messages
        self.TEXT_SCALE = 0.6

        # UI elements
        self.background_panel: Optional[Entity] = None
        self.title_label: Optional[Text] = None

        # Create UI
        self._create_ui()

        print("✓ CombatLog3D initialized")

    def _create_ui(self):
        """Create background panel and title"""
        # Background panel
        self.background_panel = Entity(
            parent=self.parent,
            model='quad',
            color=color.rgba(0.05, 0.05, 0.1, 0.85),
            position=(self.position.x, self.position.y, -1),
            scale=(self.PANEL_WIDTH, self.PANEL_HEIGHT),
            origin=(-0.5, -0.5),  # Anchor to bottom-left
            eternal=True
        )

        # Title label
        self.title_label = Text(
            text="[COMBAT LOG]",
            parent=self.parent,
            position=(self.position.x + 0.01, self.position.y + self.PANEL_HEIGHT - 0.02, 0),
            scale=self.TEXT_SCALE * 0.9,
            color=color.rgba(0.7, 0.7, 0.8, 1),
            origin=(-0.5, 0.5),
            eternal=True
        )

    def add_message(self, message: str, msg_type: str = "event"):
        """
        Add a message to the log

        Args:
            message: Message text
            msg_type: Message type for color coding (damage, heal, loot, event, etc.)
        """
        timestamp = time.time()
        entry = CombatLogEntry(message, msg_type, timestamp)
        self.messages.append(entry)

        # Rebuild visible messages
        self._rebuild_visible_messages()

    def _rebuild_visible_messages(self):
        """Rebuild visible message text entities"""
        # Clear existing text entities
        for entry in self.messages:
            if entry.text_entity:
                entry.text_entity.disable()
                entry.text_entity = None

        # Show last N messages
        visible_messages = list(self.messages)[-self.MAX_VISIBLE_MESSAGES:]

        # Create text entities for visible messages (bottom to top)
        base_y = self.position.y + 0.02
        for i, entry in enumerate(visible_messages):
            y_pos = base_y + (i * self.MESSAGE_SPACING)

            # Get color for message type
            msg_color = self.MESSAGE_COLORS.get(entry.msg_type, (1, 1, 1))

            # Calculate fade based on age
            age = time.time() - entry.timestamp
            alpha = 1.0
            if age > self.FADE_DURATION:
                # Fade out over 2 seconds after FADE_DURATION
                fade_progress = min(1.0, (age - self.FADE_DURATION) / 2.0)
                alpha = 1.0 - fade_progress

            # Create text entity
            entry.text_entity = Text(
                text=f"• {entry.message}",
                parent=self.parent,
                position=(self.position.x + 0.01, y_pos, 0),
                scale=self.TEXT_SCALE,
                color=color.rgba(*msg_color, alpha),
                origin=(-0.5, -0.5),
                eternal=True
            )

    def update(self, dt: float):
        """
        Update fade effects

        Args:
            dt: Delta time since last frame
        """
        # Update alpha for fading messages
        current_time = time.time()
        needs_rebuild = False

        for entry in self.messages:
            if entry.text_entity:
                age = current_time - entry.timestamp

                if age > self.FADE_DURATION:
                    # Calculate fade
                    fade_progress = min(1.0, (age - self.FADE_DURATION) / 2.0)
                    alpha = 1.0 - fade_progress

                    # Update text entity alpha
                    msg_color = self.MESSAGE_COLORS.get(entry.msg_type, (1, 1, 1))
                    entry.text_entity.color = color.rgba(*msg_color, alpha)

                    # Mark for rebuild if fully faded
                    if alpha <= 0:
                        needs_rebuild = True

        # Rebuild if any messages fully faded
        if needs_rebuild:
            self._rebuild_visible_messages()

    def cleanup(self):
        """Clean up all UI elements"""
        # Clear all message text entities
        for entry in self.messages:
            if entry.text_entity:
                entry.text_entity.disable()

        self.messages.clear()

        # Clean up panel and title
        if self.background_panel:
            self.background_panel.disable()

        if self.title_label:
            self.title_label.disable()

        print("✓ CombatLog3D cleaned up")

    def __repr__(self) -> str:
        return f"<CombatLog3D messages={len(self.messages)} visible={len([e for e in self.messages if e.text_entity])}>"
