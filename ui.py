"""
PyQt UI for Dungeon Delver
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QFont, QKeyEvent
import constants as c
from game import Game


class GameWidget(QWidget):
    """Widget for rendering the game grid"""
    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.setFixedSize(c.GRID_WIDTH * c.TILE_SIZE, c.GRID_HEIGHT * c.TILE_SIZE)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def paintEvent(self, event):
        """Render the game grid"""
        painter = QPainter(self)

        if not self.game.dungeon:
            return

        # Draw tiles
        for y in range(c.GRID_HEIGHT):
            for x in range(c.GRID_WIDTH):
                tile = self.game.dungeon.get_tile(x, y)
                color = self._get_tile_color(tile)

                painter.fillRect(
                    x * c.TILE_SIZE,
                    y * c.TILE_SIZE,
                    c.TILE_SIZE,
                    c.TILE_SIZE,
                    color
                )

        # Draw entities
        for y in range(c.GRID_HEIGHT):
            for x in range(c.GRID_WIDTH):
                entity = self.game.get_entity_at(x, y)
                if entity:
                    color = self._get_entity_color(entity)
                    painter.fillRect(
                        x * c.TILE_SIZE,
                        y * c.TILE_SIZE,
                        c.TILE_SIZE,
                        c.TILE_SIZE,
                        color
                    )

        # Draw grid lines (optional, subtle)
        painter.setPen(QColor(200, 200, 200))
        for x in range(0, c.GRID_WIDTH * c.TILE_SIZE, c.TILE_SIZE):
            painter.drawLine(x, 0, x, c.GRID_HEIGHT * c.TILE_SIZE)
        for y in range(0, c.GRID_HEIGHT * c.TILE_SIZE, c.TILE_SIZE):
            painter.drawLine(0, y, c.GRID_WIDTH * c.TILE_SIZE, y)

    def _get_tile_color(self, tile: int) -> QColor:
        """Get color for tile type"""
        if tile == c.TILE_FLOOR:
            return c.COLOR_FLOOR
        elif tile == c.TILE_WALL:
            return c.COLOR_WALL
        elif tile == c.TILE_STAIRS:
            return c.COLOR_STAIRS
        return c.COLOR_WALL

    def _get_entity_color(self, entity) -> QColor:
        """Get color for entity"""
        if entity.entity_type == c.ENTITY_PLAYER:
            return c.COLOR_PLAYER
        elif entity.entity_type == c.ENTITY_ENEMY:
            if entity.enemy_type == c.ENEMY_GOBLIN:
                return c.COLOR_ENEMY_GOBLIN
            elif entity.enemy_type == c.ENEMY_SKELETON:
                return c.COLOR_ENEMY_SKELETON
            elif entity.enemy_type == c.ENEMY_DRAGON:
                return c.COLOR_ENEMY_DRAGON
        elif entity.entity_type == c.ENTITY_ITEM:
            if entity.item_type == c.ITEM_HEALTH_POTION:
                return c.COLOR_ITEM_POTION
            elif entity.item_type == c.ITEM_SWORD:
                return c.COLOR_ITEM_WEAPON
            elif entity.item_type == c.ITEM_SHIELD:
                return c.COLOR_ITEM_ARMOR
        return QColor(255, 255, 255)


class StatsPanel(QWidget):
    """Panel for displaying player stats"""
    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.setFixedWidth(c.SIDEBAR_WIDTH)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title
        title = QLabel("DUNGEON DELVER")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Stats labels
        self.hp_label = QLabel()
        self.level_label = QLabel()
        self.xp_label = QLabel()
        self.attack_label = QLabel()
        self.defense_label = QLabel()
        self.depth_label = QLabel()

        font = QFont("Courier", 10)
        for label in [self.hp_label, self.level_label, self.xp_label,
                      self.attack_label, self.defense_label, self.depth_label]:
            label.setFont(font)
            layout.addWidget(label)

        layout.addSpacing(20)

        # Messages label
        messages_title = QLabel("Messages:")
        messages_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(messages_title)

        self.messages_label = QLabel()
        self.messages_label.setFont(QFont("Courier", 9))
        self.messages_label.setWordWrap(True)
        self.messages_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.messages_label)

        layout.addStretch()

        # Controls
        controls = QLabel(
            "Controls:\n"
            "WASD/Arrows - Move\n"
            "R - Restart\n"
            "Q - Quit"
        )
        controls.setFont(QFont("Courier", 8))
        controls.setStyleSheet("color: gray;")
        layout.addWidget(controls)

        self.setLayout(layout)

    def update_stats(self):
        """Update stats display"""
        if not self.game.player:
            return

        p = self.game.player

        self.hp_label.setText(f"HP: {p.hp}/{p.max_hp}")
        self.level_label.setText(f"Level: {p.level}")
        self.xp_label.setText(f"XP: {p.xp}/{p.xp_to_next_level}")
        self.attack_label.setText(f"Attack: {p.attack}")
        self.defense_label.setText(f"Defense: {p.defense}")
        self.depth_label.setText(f"Depth: {self.game.current_level}")

        # Update messages
        messages_text = "\n".join(self.game.messages[-10:])
        self.messages_label.setText(messages_text)


class MainWindow(QMainWindow):
    """Main game window"""
    def __init__(self):
        super().__init__()
        self.game = Game()
        self.game.start_new_game()

        self.setWindowTitle("Dungeon Delver")
        self.setFixedSize(c.WINDOW_WIDTH, c.WINDOW_HEIGHT)

        # Create central widget
        central = QWidget()
        layout = QHBoxLayout()

        # Game widget
        self.game_widget = GameWidget(self.game)
        layout.addWidget(self.game_widget)

        # Stats panel
        self.stats_panel = StatsPanel(self.game)
        layout.addWidget(self.stats_panel)

        central.setLayout(layout)
        self.setCentralWidget(central)

        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(100)  # Update every 100ms

        self.game_widget.setFocus()

    def update_display(self):
        """Update game display"""
        self.game_widget.update()
        self.stats_panel.update_stats()

    def keyPressEvent(self, event: QKeyEvent):
        """Handle key presses"""
        key = event.key()

        # Movement
        dx, dy = 0, 0
        if key in (Qt.Key.Key_W, Qt.Key.Key_Up):
            dy = -1
        elif key in (Qt.Key.Key_S, Qt.Key.Key_Down):
            dy = 1
        elif key in (Qt.Key.Key_A, Qt.Key.Key_Left):
            dx = -1
        elif key in (Qt.Key.Key_D, Qt.Key.Key_Right):
            dx = 1
        elif key == Qt.Key.Key_R:
            # Restart game
            self.game.start_new_game()
            return
        elif key == Qt.Key.Key_Q:
            # Quit
            self.close()
            return

        if dx != 0 or dy != 0:
            self.game.player_move(dx, dy)
            self.update_display()
