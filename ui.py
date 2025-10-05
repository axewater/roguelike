"""
PyQt UI for Dungeon Delver
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QFont, QKeyEvent
import constants as c
from game import Game


class ProgressBar(QWidget):
    """Custom progress bar widget"""
    def __init__(self, height=20):
        super().__init__()
        self.value = 0
        self.max_value = 100
        self.bar_color = c.COLOR_HP_BAR_FULL
        self.bg_color = c.COLOR_HP_BAR_BG
        self.text = ""
        self.setFixedHeight(height)
        self.setMinimumWidth(200)

    def set_value(self, value: int, max_value: int, text: str = "", color: QColor = None):
        """Set progress bar value"""
        self.value = value
        self.max_value = max_value
        self.text = text
        if color:
            self.bar_color = color
        self.update()

    def paintEvent(self, event):
        """Paint the progress bar"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw background
        painter.fillRect(0, 0, self.width(), self.height(), self.bg_color)

        # Draw progress
        if self.max_value > 0:
            progress_width = int((self.value / self.max_value) * self.width())
            painter.fillRect(0, 0, progress_width, self.height(), self.bar_color)

        # Draw border
        painter.setPen(QColor(70, 70, 75))
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

        # Draw text
        if self.text:
            painter.setPen(c.COLOR_TEXT_LIGHT)
            painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            painter.drawText(0, 0, self.width(), self.height(),
                           Qt.AlignmentFlag.AlignCenter, self.text)


class GameWidget(QWidget):
    """Widget for rendering the game grid"""
    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.setFixedSize(c.GRID_WIDTH * c.TILE_SIZE, c.GRID_HEIGHT * c.TILE_SIZE)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setStyleSheet(f"background-color: rgb({c.COLOR_FLOOR.red()}, {c.COLOR_FLOOR.green()}, {c.COLOR_FLOOR.blue()});")

    def paintEvent(self, event):
        """Render the game grid"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self.game.dungeon:
            return

        # Draw tiles with background colors
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

        # Draw entities with colors and symbols
        font = QFont("Courier New", int(c.TILE_SIZE * 0.7), QFont.Weight.Bold)
        painter.setFont(font)

        for y in range(c.GRID_HEIGHT):
            for x in range(c.GRID_WIDTH):
                entity = self.game.get_entity_at(x, y)
                if entity:
                    # Draw background color
                    color = self._get_entity_color(entity)
                    painter.fillRect(
                        x * c.TILE_SIZE,
                        y * c.TILE_SIZE,
                        c.TILE_SIZE,
                        c.TILE_SIZE,
                        color
                    )

                    # Draw symbol
                    symbol = self._get_entity_symbol(entity)
                    text_color = self._get_entity_text_color(entity)
                    painter.setPen(text_color)

                    # Center the text
                    painter.drawText(
                        x * c.TILE_SIZE,
                        y * c.TILE_SIZE,
                        c.TILE_SIZE,
                        c.TILE_SIZE,
                        Qt.AlignmentFlag.AlignCenter,
                        symbol
                    )
                else:
                    # Draw floor/wall symbols for empty tiles
                    tile = self.game.dungeon.get_tile(x, y)
                    if tile == c.TILE_STAIRS:
                        painter.setPen(c.COLOR_TEXT_LIGHT)
                        painter.drawText(
                            x * c.TILE_SIZE,
                            y * c.TILE_SIZE,
                            c.TILE_SIZE,
                            c.TILE_SIZE,
                            Qt.AlignmentFlag.AlignCenter,
                            c.SYMBOL_STAIRS
                        )

        # Draw game over overlay
        if self.game.game_over:
            self._draw_game_over_overlay(painter)

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

    def _get_entity_symbol(self, entity) -> str:
        """Get symbol for entity"""
        if entity.entity_type == c.ENTITY_PLAYER:
            return c.SYMBOL_PLAYER
        elif entity.entity_type == c.ENTITY_ENEMY:
            if entity.enemy_type == c.ENEMY_GOBLIN:
                return c.SYMBOL_GOBLIN
            elif entity.enemy_type == c.ENEMY_SKELETON:
                return c.SYMBOL_SKELETON
            elif entity.enemy_type == c.ENEMY_DRAGON:
                return c.SYMBOL_DRAGON
        elif entity.entity_type == c.ENTITY_ITEM:
            if entity.item_type == c.ITEM_HEALTH_POTION:
                return c.SYMBOL_POTION
            elif entity.item_type == c.ITEM_SWORD:
                return c.SYMBOL_SWORD
            elif entity.item_type == c.ITEM_SHIELD:
                return c.SYMBOL_SHIELD
        return "?"

    def _get_entity_text_color(self, entity) -> QColor:
        """Get text color for entity symbol"""
        # Use dark text on light backgrounds, light text on dark backgrounds
        if entity.entity_type == c.ENTITY_PLAYER:
            return c.COLOR_TEXT_DARK
        elif entity.entity_type == c.ENTITY_ENEMY:
            if entity.enemy_type == c.ENEMY_SKELETON:
                return c.COLOR_TEXT_DARK
            return c.COLOR_TEXT_DARK
        elif entity.entity_type == c.ENTITY_ITEM:
            return c.COLOR_TEXT_DARK
        return c.COLOR_TEXT_LIGHT

    def _draw_game_over_overlay(self, painter: QPainter):
        """Draw game over overlay"""
        # Semi-transparent dark overlay
        overlay_color = QColor(0, 0, 0, 180)
        painter.fillRect(0, 0, self.width(), self.height(), overlay_color)

        # Game over text
        painter.setPen(QColor(255, 60, 60))
        painter.setFont(QFont("Arial", 48, QFont.Weight.Bold))
        painter.drawText(0, self.height() // 2 - 100, self.width(), 100,
                        Qt.AlignmentFlag.AlignCenter, "GAME OVER")

        # Stats summary
        if self.game.player:
            painter.setPen(c.COLOR_TEXT_LIGHT)
            painter.setFont(QFont("Arial", 18))

            stats_text = (
                f"Level {self.game.player.level} Hero\n"
                f"Reached Dungeon Level {self.game.current_level}\n"
                f"Attack: {self.game.player.attack} | Defense: {self.game.player.defense}"
            )

            painter.drawText(0, self.height() // 2, self.width(), 150,
                           Qt.AlignmentFlag.AlignCenter, stats_text)

        # Restart instruction
        painter.setPen(QColor(150, 150, 150))
        painter.setFont(QFont("Arial", 16))
        painter.drawText(0, self.height() // 2 + 120, self.width(), 50,
                        Qt.AlignmentFlag.AlignCenter, "Press R to Restart")


class StatsPanel(QWidget):
    """Panel for displaying player stats"""
    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.setFixedWidth(c.SIDEBAR_WIDTH)

        # Set background color
        self.setStyleSheet(f"background-color: rgb({c.COLOR_PANEL_BG.red()}, {c.COLOR_PANEL_BG.green()}, {c.COLOR_PANEL_BG.blue()});")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("DUNGEON DELVER")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); padding: 10px;")
        layout.addWidget(title)

        # Divider
        line1 = QFrame()
        line1.setFrameShape(QFrame.Shape.HLine)
        line1.setStyleSheet("background-color: rgb(70, 70, 75);")
        layout.addWidget(line1)

        # HP Bar
        hp_title = QLabel("Health")
        hp_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        hp_title.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()});")
        layout.addWidget(hp_title)

        self.hp_bar = ProgressBar(24)
        layout.addWidget(self.hp_bar)

        layout.addSpacing(10)

        # XP Bar
        xp_title = QLabel("Experience")
        xp_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        xp_title.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()});")
        layout.addWidget(xp_title)

        self.xp_bar = ProgressBar(20)
        layout.addWidget(self.xp_bar)

        layout.addSpacing(10)

        # Stats labels
        self.level_label = QLabel()
        self.attack_label = QLabel()
        self.defense_label = QLabel()
        self.depth_label = QLabel()

        font = QFont("Courier New", 11)
        stat_style = f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); padding: 3px;"

        for label in [self.level_label, self.attack_label, self.defense_label, self.depth_label]:
            label.setFont(font)
            label.setStyleSheet(stat_style)
            layout.addWidget(label)

        layout.addSpacing(15)

        # Divider
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)
        line2.setStyleSheet("background-color: rgb(70, 70, 75);")
        layout.addWidget(line2)

        # Messages label
        messages_title = QLabel("Combat Log")
        messages_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        messages_title.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); padding-top: 5px;")
        layout.addWidget(messages_title)

        self.messages_label = QLabel()
        self.messages_label.setFont(QFont("Courier New", 9))
        self.messages_label.setWordWrap(True)
        self.messages_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.messages_label.setTextFormat(Qt.TextFormat.RichText)
        self.messages_label.setStyleSheet("color: rgb(200, 200, 200); padding: 5px;")
        layout.addWidget(self.messages_label)

        layout.addStretch()

        # Divider
        line3 = QFrame()
        line3.setFrameShape(QFrame.Shape.HLine)
        line3.setStyleSheet("background-color: rgb(70, 70, 75);")
        layout.addWidget(line3)

        # Controls
        controls = QLabel(
            "Controls:\n"
            "WASD/Arrows - Move\n"
            "R - Restart\n"
            "Q - Quit"
        )
        controls.setFont(QFont("Courier New", 9))
        controls.setStyleSheet("color: rgb(120, 120, 125); padding: 5px;")
        layout.addWidget(controls)

        self.setLayout(layout)

    def update_stats(self):
        """Update stats display"""
        if not self.game.player:
            return

        p = self.game.player

        # Update HP bar with color based on health percentage
        hp_percent = p.hp / p.max_hp if p.max_hp > 0 else 0
        if hp_percent > 0.6:
            hp_color = c.COLOR_HP_BAR_FULL
        elif hp_percent > 0.3:
            hp_color = c.COLOR_HP_BAR_MID
        else:
            hp_color = c.COLOR_HP_BAR_LOW

        self.hp_bar.set_value(p.hp, p.max_hp, f"{p.hp} / {p.max_hp}", hp_color)

        # Update XP bar
        self.xp_bar.set_value(p.xp, p.xp_to_next_level, f"{p.xp} / {p.xp_to_next_level}", c.COLOR_XP_BAR)

        # Update stat labels
        self.level_label.setText(f"Level: {p.level}")
        self.attack_label.setText(f"Attack: {p.attack}")
        self.defense_label.setText(f"Defense: {p.defense}")
        self.depth_label.setText(f"Dungeon Level: {self.game.current_level}")

        # Update messages with color coding
        colored_messages = []
        for message, msg_type in self.game.messages[-8:]:
            color = self._get_message_color(msg_type)
            colored_messages.append(f'<span style="color: {color};">{message}</span>')

        messages_html = "<br>".join(colored_messages)
        self.messages_label.setText(messages_html)

    def _get_message_color(self, msg_type: str) -> str:
        """Get color for message type"""
        color_map = {
            "damage": c.COLOR_MSG_DAMAGE,
            "heal": c.COLOR_MSG_HEAL,
            "item": c.COLOR_MSG_ITEM,
            "event": c.COLOR_MSG_EVENT,
            "death": c.COLOR_MSG_DEATH,
            "levelup": c.COLOR_MSG_LEVELUP,
        }
        return color_map.get(msg_type, c.COLOR_MSG_EVENT)


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
