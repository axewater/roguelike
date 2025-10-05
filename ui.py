"""
PyQt UI for Dungeon Delver
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QStackedWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QKeyEvent
import time
import constants as c
from game import Game
import graphics as gfx


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


class ClassSelectionScreen(QWidget):
    """Class selection screen"""
    class_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        """Setup the UI"""
        self.setStyleSheet(f"background-color: rgb({c.COLOR_PANEL_BG.red()}, {c.COLOR_PANEL_BG.green()}, {c.COLOR_PANEL_BG.blue()});")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Title
        title = QLabel("CHOOSE YOUR CLASS")
        title.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); padding: 20px;")
        layout.addWidget(title)

        # Class buttons
        classes = [
            (c.CLASS_WARRIOR, c.COLOR_CLASS_WARRIOR, "WARRIOR"),
            (c.CLASS_MAGE, c.COLOR_CLASS_MAGE, "MAGE"),
            (c.CLASS_ROGUE, c.COLOR_CLASS_ROGUE, "ROGUE"),
            (c.CLASS_RANGER, c.COLOR_CLASS_RANGER, "RANGER"),
        ]

        for class_type, color, label_text in classes:
            self._create_class_button(layout, class_type, color, label_text)

        self.setLayout(layout)

    def _create_class_button(self, layout: QVBoxLayout, class_type: str, color: QColor, label_text: str):
        """Create a class selection button"""
        stats = c.CLASS_STATS[class_type]

        # Container
        container = QWidget()
        container_layout = QVBoxLayout()
        container.setStyleSheet(f"background-color: rgb(45, 45, 50); border: 2px solid rgb({color.red()}, {color.green()}, {color.blue()}); border-radius: 10px; padding: 15px;")

        # Class name
        name_label = QLabel(label_text)
        name_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet(f"color: rgb({color.red()}, {color.green()}, {color.blue()}); border: none;")
        container_layout.addWidget(name_label)

        # Description
        desc_label = QLabel(stats["description"])
        desc_label.setFont(QFont("Arial", 11))
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"color: rgb(180, 180, 180); border: none; padding: 5px;")
        container_layout.addWidget(desc_label)

        # Stats
        stats_text = f"HP: {stats['hp']} | ATK: {stats['attack']} | DEF: {stats['defense']}"
        if 'crit_chance' in stats:
            stats_text += f" | CRIT: {int(stats['crit_chance'] * 100)}%"

        stats_label = QLabel(stats_text)
        stats_label.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
        stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_label.setStyleSheet(f"color: rgb(220, 220, 220); border: none;")
        container_layout.addWidget(stats_label)

        # Select button
        button = QPushButton("SELECT")
        button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        button.setFixedHeight(40)
        button.setStyleSheet(f"QPushButton {{ background-color: rgb({color.red()}, {color.green()}, {color.blue()}); color: rgb(20, 20, 20); border: none; border-radius: 5px; padding: 10px; }} QPushButton:hover {{ background-color: rgb({min(color.red() + 30, 255)}, {min(color.green() + 30, 255)}, {min(color.blue() + 30, 255)}); }}")
        button.clicked.connect(lambda: self.class_selected.emit(class_type))
        container_layout.addWidget(button)

        container.setLayout(container_layout)
        container.setFixedWidth(600)
        layout.addWidget(container, alignment=Qt.AlignmentFlag.AlignCenter)


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

        # Apply screen shake offset
        shake_x, shake_y = self.game.anim_manager.get_screen_offset()
        painter.translate(shake_x, shake_y)

        # Draw tiles with graphics
        for y in range(c.GRID_HEIGHT):
            for x in range(c.GRID_WIDTH):
                tile = self.game.dungeon.get_tile(x, y)

                if tile == c.TILE_WALL:
                    gfx.draw_wall_tile(painter, x, y, c.TILE_SIZE)
                elif tile == c.TILE_FLOOR:
                    gfx.draw_floor_tile(painter, x, y, c.TILE_SIZE)
                elif tile == c.TILE_STAIRS:
                    gfx.draw_floor_tile(painter, x, y, c.TILE_SIZE)  # Draw floor underneath
                    gfx.draw_stairs_tile(painter, x, y, c.TILE_SIZE)

        # Draw entities with graphics
        for y in range(c.GRID_HEIGHT):
            for x in range(c.GRID_WIDTH):
                entity = self.game.get_entity_at(x, y)
                if entity:
                    color = self._get_entity_color(entity)

                    if entity.entity_type == c.ENTITY_PLAYER:
                        gfx.draw_player(painter, x, y, c.TILE_SIZE, color, entity.class_type)
                    elif entity.entity_type == c.ENTITY_ENEMY:
                        gfx.draw_enemy(painter, x, y, c.TILE_SIZE, color, entity.enemy_type)
                    elif entity.entity_type == c.ENTITY_ITEM:
                        gfx.draw_item(painter, x, y, c.TILE_SIZE, color, entity.item_type)

        # Draw enemy health bars
        self._draw_enemy_health_bars(painter)

        # Draw flash effects (before other animations)
        for flash in self.game.anim_manager.flash_effects:
            flash_color = QColor(flash.color.red(), flash.color.green(), flash.color.blue(), flash.alpha)
            painter.fillRect(
                flash.x * c.TILE_SIZE,
                flash.y * c.TILE_SIZE,
                c.TILE_SIZE,
                c.TILE_SIZE,
                flash_color
            )

        # Draw particles
        for particle in self.game.anim_manager.particles:
            particle_color = QColor(particle.color.red(), particle.color.green(),
                                   particle.color.blue(), particle.alpha)
            painter.setBrush(particle_color)
            painter.setPen(Qt.PenStyle.NoPen)

            if particle.particle_type == "circle":
                painter.drawEllipse(int(particle.x - particle.size / 2),
                                  int(particle.y - particle.size / 2),
                                  int(particle.size), int(particle.size))
            else:  # square or star
                painter.fillRect(int(particle.x - particle.size / 2),
                               int(particle.y - particle.size / 2),
                               int(particle.size), int(particle.size),
                               particle_color)

        # Draw floating text
        text_font = QFont("Arial", 14, QFont.Weight.Bold)
        for ftext in self.game.anim_manager.floating_texts:
            if ftext.is_crit:
                text_font.setPointSize(18)
            else:
                text_font.setPointSize(14)

            painter.setFont(text_font)
            text_color = QColor(ftext.color.red(), ftext.color.green(),
                              ftext.color.blue(), ftext.alpha)
            painter.setPen(text_color)

            # Calculate position
            text_x = ftext.x * c.TILE_SIZE + c.TILE_SIZE // 2
            text_y = ftext.y * c.TILE_SIZE + int(ftext.offset_y * c.TILE_SIZE)

            painter.drawText(int(text_x - 20), int(text_y - 10), 40, 20,
                           Qt.AlignmentFlag.AlignCenter, ftext.text)

        # Draw game over overlay
        if self.game.game_over:
            # Reset transform for overlay
            painter.resetTransform()
            self._draw_game_over_overlay(painter)

    def _get_entity_color(self, entity) -> QColor:
        """Get color for entity"""
        if entity.entity_type == c.ENTITY_PLAYER:
            # Use class-specific color
            class_colors = {
                c.CLASS_WARRIOR: c.COLOR_CLASS_WARRIOR,
                c.CLASS_MAGE: c.COLOR_CLASS_MAGE,
                c.CLASS_ROGUE: c.COLOR_CLASS_ROGUE,
                c.CLASS_RANGER: c.COLOR_CLASS_RANGER,
            }
            return class_colors.get(entity.class_type, c.COLOR_PLAYER)
        elif entity.entity_type == c.ENTITY_ENEMY:
            if entity.enemy_type == c.ENEMY_GOBLIN:
                return c.COLOR_ENEMY_GOBLIN
            elif entity.enemy_type == c.ENEMY_SKELETON:
                return c.COLOR_ENEMY_SKELETON
            elif entity.enemy_type == c.ENEMY_DRAGON:
                return c.COLOR_ENEMY_DRAGON
        elif entity.entity_type == c.ENTITY_ITEM:
            # Use rarity color for items
            rarity_colors = {
                c.RARITY_COMMON: c.COLOR_RARITY_COMMON,
                c.RARITY_UNCOMMON: c.COLOR_RARITY_UNCOMMON,
                c.RARITY_RARE: c.COLOR_RARITY_RARE,
                c.RARITY_EPIC: c.COLOR_RARITY_EPIC,
                c.RARITY_LEGENDARY: c.COLOR_RARITY_LEGENDARY,
            }
            return rarity_colors.get(entity.rarity, c.COLOR_ITEM_POTION)
        return QColor(255, 255, 255)

    def _draw_enemy_health_bars(self, painter: QPainter):
        """Draw health bars below enemies"""
        for enemy in self.game.enemies:
            # Calculate bar dimensions
            bar_width = c.TILE_SIZE - 4
            bar_height = 3
            bar_x = enemy.x * c.TILE_SIZE + 2
            bar_y = enemy.y * c.TILE_SIZE + c.TILE_SIZE - 5

            # Draw background
            painter.fillRect(bar_x, bar_y, bar_width, bar_height, c.COLOR_ENEMY_HP_BAR_BG)

            # Draw health
            hp_percent = enemy.hp / enemy.max_hp if enemy.max_hp > 0 else 0
            health_width = int(bar_width * hp_percent)

            if health_width > 0:
                painter.fillRect(bar_x, bar_y, health_width, bar_height, c.COLOR_ENEMY_HP_BAR)

            # Draw border
            painter.setPen(c.COLOR_ENEMY_HP_BAR_BORDER)
            painter.drawRect(bar_x, bar_y, bar_width, bar_height)

    def _draw_game_over_overlay(self, painter: QPainter):
        """Draw game over overlay with enhanced visuals"""
        # Dark overlay with gradient effect
        overlay_color = QColor(0, 0, 0, 200)
        painter.fillRect(0, 0, self.width(), self.height(), overlay_color)

        # Draw decorative border
        border_color = QColor(255, 60, 60, 100)
        painter.setPen(border_color)
        painter.drawRect(40, 40, self.width() - 80, self.height() - 80)

        # Game over title with shadow
        title_y = self.height() // 2 - 150

        # Shadow
        painter.setPen(QColor(0, 0, 0, 150))
        painter.setFont(QFont("Arial", 56, QFont.Weight.Bold))
        painter.drawText(2, title_y + 2, self.width(), 80,
                        Qt.AlignmentFlag.AlignCenter, "GAME OVER")

        # Main title
        painter.setPen(QColor(255, 80, 80))
        painter.drawText(0, title_y, self.width(), 80,
                        Qt.AlignmentFlag.AlignCenter, "GAME OVER")

        # Stats summary with better formatting
        if self.game.player:
            stats_y = self.height() // 2 - 40

            # Class and level
            painter.setPen(c.COLOR_TEXT_LIGHT)
            painter.setFont(QFont("Arial", 20, QFont.Weight.Bold))
            painter.drawText(0, stats_y, self.width(), 30,
                           Qt.AlignmentFlag.AlignCenter,
                           f"{self.game.player.get_class_name()} - Level {self.game.player.level}")

            # Dungeon depth
            painter.setFont(QFont("Arial", 16))
            painter.setPen(QColor(180, 180, 200))
            painter.drawText(0, stats_y + 40, self.width(), 25,
                           Qt.AlignmentFlag.AlignCenter,
                           f"Reached Dungeon Level {self.game.current_level}")

            # Stats box
            box_y = stats_y + 80
            painter.setPen(QColor(100, 100, 120))
            painter.drawRect(self.width() // 2 - 120, box_y, 240, 60)

            # Stats text
            painter.setPen(QColor(220, 220, 220))
            painter.setFont(QFont("Courier New", 14, QFont.Weight.Bold))

            # Attack
            painter.drawText(self.width() // 2 - 110, box_y + 25, 100, 20,
                           Qt.AlignmentFlag.AlignLeft, f"ATK: {self.game.player.attack}")

            # Defense
            painter.drawText(self.width() // 2 + 10, box_y + 25, 100, 20,
                           Qt.AlignmentFlag.AlignLeft, f"DEF: {self.game.player.defense}")

            # HP
            painter.drawText(self.width() // 2 - 110, box_y + 50, 220, 20,
                           Qt.AlignmentFlag.AlignCenter, f"Max HP: {self.game.player.max_hp}")

        # Restart instruction with highlight
        restart_y = self.height() // 2 + 180
        painter.setPen(QColor(100, 200, 255))
        painter.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        painter.drawText(0, restart_y, self.width(), 40,
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
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Title
        title = QLabel("DUNGEON DELVER")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); padding: 8px;")
        layout.addWidget(title)

        # Player stats section
        stats_container, stats_layout = self._create_section_container("Player Stats")
        layout.addWidget(stats_container)

        # HP Bar
        hp_label = QLabel("Health")
        hp_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        hp_label.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); border: none;")
        stats_layout.addWidget(hp_label)

        self.hp_bar = ProgressBar(22)
        stats_layout.addWidget(self.hp_bar)

        # XP Bar
        xp_label = QLabel("Experience")
        xp_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        xp_label.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); border: none;")
        stats_layout.addWidget(xp_label)

        self.xp_bar = ProgressBar(18)
        stats_layout.addWidget(self.xp_bar)

        # Stats labels
        self.class_label = QLabel()
        self.level_label = QLabel()
        self.attack_label = QLabel()
        self.defense_label = QLabel()
        self.depth_label = QLabel()

        font = QFont("Courier New", 10)
        stat_style = f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); padding: 2px; border: none;"

        for label in [self.class_label, self.level_label, self.attack_label, self.defense_label, self.depth_label]:
            label.setFont(font)
            label.setStyleSheet(stat_style)
            stats_layout.addWidget(label)

        # Equipment section
        equip_container, equip_layout = self._create_section_container("Equipment")
        layout.addWidget(equip_container)

        self.weapon_label = QLabel()
        self.armor_label = QLabel()
        self.accessory_label = QLabel()
        self.boots_label = QLabel()

        equip_font = QFont("Courier New", 9)
        equip_style = f"color: rgb(200, 200, 200); padding: 2px; border: none;"

        for label in [self.weapon_label, self.armor_label, self.accessory_label, self.boots_label]:
            label.setFont(equip_font)
            label.setStyleSheet(equip_style)
            label.setWordWrap(True)
            equip_layout.addWidget(label)

        # Abilities section
        abilities_container, abilities_layout = self._create_section_container("Abilities")
        layout.addWidget(abilities_container)

        self.ability_labels = []
        for i in range(3):  # Max 3 abilities
            label = QLabel()
            label.setFont(QFont("Courier New", 9))
            label.setStyleSheet("color: rgb(200, 200, 200); padding: 2px; border: none;")
            label.setWordWrap(True)
            label.setTextFormat(Qt.TextFormat.RichText)
            self.ability_labels.append(label)
            abilities_layout.addWidget(label)

        # Nearby Items section
        items_container, items_layout = self._create_section_container("Nearby Items")
        layout.addWidget(items_container)

        self.nearby_items_label = QLabel()
        self.nearby_items_label.setFont(QFont("Courier New", 8))
        self.nearby_items_label.setWordWrap(True)
        self.nearby_items_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.nearby_items_label.setTextFormat(Qt.TextFormat.RichText)
        self.nearby_items_label.setStyleSheet("color: rgb(200, 200, 200); padding: 2px; border: none;")
        self.nearby_items_label.setMinimumHeight(60)
        items_layout.addWidget(self.nearby_items_label)

        # Combat log section
        log_container, log_layout = self._create_section_container("Combat Log")
        layout.addWidget(log_container)

        self.messages_label = QLabel()
        self.messages_label.setFont(QFont("Courier New", 9))
        self.messages_label.setWordWrap(True)
        self.messages_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.messages_label.setTextFormat(Qt.TextFormat.RichText)
        self.messages_label.setStyleSheet("color: rgb(200, 200, 200); padding: 2px; border: none;")
        self.messages_label.setMinimumHeight(80)
        log_layout.addWidget(self.messages_label)

        layout.addStretch()

        # Controls section
        controls_container, controls_layout = self._create_section_container("Controls")
        layout.addWidget(controls_container)

        controls = QLabel(
            "WASD/Arrows - Move\n"
            "1/2/3 - Abilities\n"
            "R - Restart\n"
            "Q - Quit"
        )
        controls.setFont(QFont("Courier New", 9))
        controls.setStyleSheet("color: rgb(180, 180, 185); padding: 2px; border: none;")
        controls_layout.addWidget(controls)

        self.setLayout(layout)

    def _create_section_container(self, title: str = None) -> tuple:
        """Create a styled section container with optional title. Returns (container, content_layout)"""
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background-color: rgb({c.COLOR_SECTION_BG.red()}, {c.COLOR_SECTION_BG.green()}, {c.COLOR_SECTION_BG.blue()});
                border: 1px solid rgb({c.COLOR_SECTION_BORDER.red()}, {c.COLOR_SECTION_BORDER.green()}, {c.COLOR_SECTION_BORDER.blue()});
                border-radius: 6px;
                padding: 8px;
            }}
        """)

        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(4, 4, 4, 4)
        content_layout.setSpacing(6)

        if title:
            title_label = QLabel(title)
            title_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            title_label.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); border: none; padding: 0px;")
            content_layout.addWidget(title_label)

        container.setLayout(content_layout)
        return container, content_layout

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
        self.class_label.setText(f"Class: {p.get_class_name()}")
        self.level_label.setText(f"Level: {p.level}")
        self.attack_label.setText(f"Attack: {p.attack}")
        self.defense_label.setText(f"Defense: {p.defense}")
        self.depth_label.setText(f"Dungeon Level: {self.game.current_level}")

        # Update equipment labels
        self.weapon_label.setText(f"Weapon: {p.equipment[c.SLOT_WEAPON].get_name() if p.equipment[c.SLOT_WEAPON] else 'None'}")
        self.armor_label.setText(f"Armor: {p.equipment[c.SLOT_ARMOR].get_name() if p.equipment[c.SLOT_ARMOR] else 'None'}")
        self.accessory_label.setText(f"Accessory: {p.equipment[c.SLOT_ACCESSORY].get_name() if p.equipment[c.SLOT_ACCESSORY] else 'None'}")
        self.boots_label.setText(f"Boots: {p.equipment[c.SLOT_BOOTS].get_name() if p.equipment[c.SLOT_BOOTS] else 'None'}")

        # Update ability labels
        for i, label in enumerate(self.ability_labels):
            if i < len(p.abilities):
                ability = p.abilities[i]
                key_num = i + 1
                if ability.is_ready():
                    color = "#51cf66"  # Green when ready
                    status = "READY"
                else:
                    color = "#ff6b6b"  # Red when on cooldown
                    status = f"CD: {ability.current_cooldown}"

                label.setText(f'<span style="color: {color};">[{key_num}] {ability.name}: {status}</span>')
            else:
                label.setText("")

        # Update nearby items
        nearby_items = self._get_nearby_items(5)  # Within 5 tiles
        if nearby_items:
            items_html = []
            for item, distance in nearby_items[:3]:  # Show max 3 items
                rarity_color = self._get_rarity_color_hex(item.rarity)
                stats_preview = self._get_item_stats_preview(item)
                items_html.append(
                    f'<span style="color: {rarity_color};">• {item.get_name()}</span> '
                    f'<span style="color: #aaa;">({distance}t)</span><br/>'
                    f'<span style="color: #888; font-size: 8pt;">{stats_preview}</span>'
                )
            self.nearby_items_label.setText("<br/>".join(items_html))
        else:
            self.nearby_items_label.setText('<span style="color: #666;">No items nearby</span>')

        # Update messages with color coding
        colored_messages = []
        for message, msg_type in self.game.messages[-6:]:
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

    def _get_nearby_items(self, max_distance: int) -> list:
        """Get items within max_distance tiles of player, sorted by distance"""
        if not self.game.player:
            return []

        nearby = []
        player_x, player_y = self.game.player.x, self.game.player.y

        for item in self.game.items:
            distance = abs(item.x - player_x) + abs(item.y - player_y)
            if distance <= max_distance and distance > 0:  # Exclude current tile
                nearby.append((item, distance))

        # Sort by distance (closest first)
        nearby.sort(key=lambda x: x[1])
        return nearby

    def _get_rarity_color_hex(self, rarity: str) -> str:
        """Get hex color for item rarity"""
        color_map = {
            c.RARITY_COMMON: "#b4b4b4",
            c.RARITY_UNCOMMON: "#64c864",
            c.RARITY_RARE: "#6496ff",
            c.RARITY_EPIC: "#c864ff",
            c.RARITY_LEGENDARY: "#ffb400",
        }
        return color_map.get(rarity, "#ffffff")

    def _get_item_stats_preview(self, item) -> str:
        """Get stats preview string for an item"""
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

        return " ".join(stats) if stats else "No stats"


class MainWindow(QMainWindow):
    """Main game window"""
    def __init__(self):
        super().__init__()
        self.game = Game()

        self.setWindowTitle("Dungeon Delver")
        self.setFixedSize(c.WINDOW_WIDTH, c.WINDOW_HEIGHT)

        # Create stacked widget to switch between screens
        self.stacked_widget = QStackedWidget()

        # Class selection screen
        self.class_selection = ClassSelectionScreen()
        self.class_selection.class_selected.connect(self.on_class_selected)
        self.stacked_widget.addWidget(self.class_selection)

        # Game screen
        self.game_screen = QWidget()
        game_layout = QHBoxLayout()

        self.game_widget = GameWidget(self.game)
        game_layout.addWidget(self.game_widget)

        self.stats_panel = StatsPanel(self.game)
        game_layout.addWidget(self.stats_panel)

        self.game_screen.setLayout(game_layout)
        self.stacked_widget.addWidget(self.game_screen)

        # Set stacked widget as central widget
        self.setCentralWidget(self.stacked_widget)

        # Time tracking for animations
        self.last_time = time.time()

        # Update timer - faster for smooth animations
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(16)  # ~60 FPS

    def on_class_selected(self, class_type: str):
        """Handle class selection"""
        self.game.selected_class = class_type
        self.game.start_new_game()
        self.stacked_widget.setCurrentWidget(self.game_screen)
        self.game_widget.setFocus()

    def update_display(self):
        """Update game display"""
        # Calculate delta time
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        # Update animations
        self.game.anim_manager.update(dt)

        # Update display
        self.game_widget.update()
        self.stats_panel.update_stats()

    def keyPressEvent(self, event: QKeyEvent):
        """Handle key presses"""
        key = event.key()

        # Abilities (keys 1, 2, 3)
        if key == Qt.Key.Key_1:
            self.game.use_ability(0)
            self.update_display()
            return
        elif key == Qt.Key.Key_2:
            self.game.use_ability(1)
            self.update_display()
            return
        elif key == Qt.Key.Key_3:
            self.game.use_ability(2)
            self.update_display()
            return

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
            # Restart game - go back to class selection
            self.stacked_widget.setCurrentWidget(self.class_selection)
            return
        elif key == Qt.Key.Key_Q:
            # Quit
            self.close()
            return

        if dx != 0 or dy != 0:
            self.game.player_move(dx, dy)
            self.update_display()
