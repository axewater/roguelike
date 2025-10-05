"""
Stats panel widget displaying player info, equipment, abilities, and combat log
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

import constants as c
from game import Game
from ui.widgets.progress_bar import ProgressBar
from ui.widgets.ability_button import AbilityButton


class StatsPanel(QWidget):
    """Panel for displaying player stats"""
    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.setFixedWidth(c.SIDEBAR_WIDTH)

        # Set background color
        self.setStyleSheet(f"background-color: rgb({c.COLOR_PANEL_BG.red()}, {c.COLOR_PANEL_BG.green()}, {c.COLOR_PANEL_BG.blue()});")

        # Main grid layout: 2 columns x 3 rows + combat log at bottom
        main_grid = QGridLayout()
        main_grid.setContentsMargins(12, 12, 12, 12)
        main_grid.setSpacing(12)

        # ROW 0: HP and XP bars (span full width)
        bars_container, bars_layout = self._create_section_container()

        # HP Bar
        hp_label = QLabel("Health")
        hp_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        hp_label.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); border: none;")
        bars_layout.addWidget(hp_label)

        self.hp_bar = ProgressBar(24)
        bars_layout.addWidget(self.hp_bar)

        # XP Bar
        xp_label = QLabel("Experience")
        xp_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        xp_label.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); border: none;")
        bars_layout.addWidget(xp_label)

        self.xp_bar = ProgressBar(20)
        bars_layout.addWidget(self.xp_bar)

        main_grid.addWidget(bars_container, 0, 0, 1, 2)  # Row 0, span 2 columns

        # ROW 1, COL 0: Player Stats
        stats_container, stats_layout = self._create_section_container("Player Stats")

        self.class_label = QLabel()
        self.level_label = QLabel()
        self.attack_label = QLabel()
        self.defense_label = QLabel()
        self.depth_label = QLabel()

        stat_font = QFont("Courier New", 10)
        stat_style = f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); padding: 4px; border: none;"

        for label in [self.class_label, self.level_label, self.attack_label, self.defense_label, self.depth_label]:
            label.setFont(stat_font)
            label.setStyleSheet(stat_style)
            stats_layout.addWidget(label)

        main_grid.addWidget(stats_container, 1, 0)  # Row 1, Col 0

        # ROW 1, COL 1: Equipment
        equip_container, equip_layout = self._create_section_container("Equipment")

        self.weapon_label = QLabel()
        self.armor_label = QLabel()
        self.accessory_label = QLabel()
        self.boots_label = QLabel()

        equip_font = QFont("Courier New", 10)
        equip_style = f"color: rgb(200, 200, 200); padding: 4px; border: none;"

        for label in [self.weapon_label, self.armor_label, self.accessory_label, self.boots_label]:
            label.setFont(equip_font)
            label.setStyleSheet(equip_style)
            label.setWordWrap(True)
            equip_layout.addWidget(label)

        main_grid.addWidget(equip_container, 1, 1)  # Row 1, Col 1

        # ROW 2, COL 0: Abilities
        abilities_container, abilities_layout = self._create_section_container("Abilities")

        self.ability_buttons = []
        for i in range(3):  # Max 3 abilities
            button = AbilityButton(i)
            button.ability_clicked.connect(self._on_ability_clicked)
            self.ability_buttons.append(button)
            abilities_layout.addWidget(button)

        main_grid.addWidget(abilities_container, 2, 0)  # Row 2, Col 0

        # ROW 2, COL 1: Nearby Items
        items_container, items_layout = self._create_section_container("Nearby Items")

        self.nearby_items_label = QLabel()
        self.nearby_items_label.setFont(QFont("Courier New", 10))
        self.nearby_items_label.setWordWrap(True)
        self.nearby_items_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.nearby_items_label.setTextFormat(Qt.TextFormat.RichText)
        self.nearby_items_label.setStyleSheet("color: rgb(200, 200, 200); padding: 4px; border: none;")
        self.nearby_items_label.setMinimumHeight(80)
        items_layout.addWidget(self.nearby_items_label)

        main_grid.addWidget(items_container, 2, 1)  # Row 2, Col 1

        # ROW 3: Combat Log (span full width)
        log_container, log_layout = self._create_section_container("Combat Log")

        self.messages_label = QLabel()
        self.messages_label.setFont(QFont("Courier New", 10))
        self.messages_label.setWordWrap(True)
        self.messages_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.messages_label.setTextFormat(Qt.TextFormat.RichText)
        self.messages_label.setStyleSheet("color: rgb(200, 200, 200); padding: 4px; border: none;")
        self.messages_label.setMinimumHeight(100)
        log_layout.addWidget(self.messages_label)

        main_grid.addWidget(log_container, 3, 0, 1, 2)  # Row 3, span 2 columns

        # Set row stretch to push everything to top
        main_grid.setRowStretch(4, 1)

        self.setLayout(main_grid)

    def _on_ability_clicked(self, ability_index: int):
        """Handle ability button click"""
        if not self.game or not self.game.player:
            return

        if ability_index >= len(self.game.player.abilities):
            return

        ability = self.game.player.abilities[ability_index]

        # Abilities that need targeting
        targeting_abilities = ["Fireball", "Dash", "Shadow Step"]

        if ability.name in targeting_abilities:
            # Enter targeting mode
            # Find the game widget to set targeting mode
            main_window = self.window()
            if hasattr(main_window, 'game_widget'):
                main_window.game_widget.targeting_mode = True
                main_window.game_widget.targeting_ability_index = ability_index
        else:
            # Use ability immediately (no targeting needed)
            self.game.use_ability(ability_index)

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

        # Update ability buttons
        for i, button in enumerate(self.ability_buttons):
            if i < len(p.abilities):
                ability = p.abilities[i]
                is_ready = ability.is_ready()
                status = "READY" if is_ready else f"CD: {ability.current_cooldown}"
                button.set_ability_state(ability.name, is_ready, status)
                button.setVisible(True)
            else:
                button.setVisible(False)

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
