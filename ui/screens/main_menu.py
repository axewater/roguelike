"""
Main menu screen with navigation options
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont
import time

import constants as c
from audio import get_audio_manager
from animations import AnimationManager


class MainMenuScreen(QWidget):
    """Main menu screen with navigation options"""
    new_game_clicked = pyqtSignal()
    how_to_play_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()
    quit_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: rgb({c.COLOR_PANEL_BG.red()}, {c.COLOR_PANEL_BG.green()}, {c.COLOR_PANEL_BG.blue()});")

        # Animation manager for particles
        self.anim_manager = AnimationManager()
        self.time_elapsed = 0.0
        self.last_time = time.time()

        # Timer for animations
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS

        # Spawn initial particles
        for _ in range(25):
            self.anim_manager.add_ambient_particles(count=1)

        self.setup_ui()

    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        # Title
        title = QLabel("DUNGEON DELVER")
        title.setFont(QFont("Arial", 42, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); padding: 30px;")
        layout.addWidget(title)

        # Menu buttons
        button_width = 400
        button_height = 60

        # New Game button
        new_game_btn = self._create_menu_button("New Game", button_width, button_height)
        new_game_btn.clicked.connect(self._on_new_game)
        layout.addWidget(new_game_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # How to Play button
        how_to_btn = self._create_menu_button("How to Play", button_width, button_height)
        how_to_btn.clicked.connect(self._on_how_to_play)
        layout.addWidget(how_to_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Settings button
        settings_btn = self._create_menu_button("Settings", button_width, button_height)
        settings_btn.clicked.connect(self._on_settings)
        layout.addWidget(settings_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Quit button
        quit_btn = self._create_menu_button("Quit", button_width, button_height)
        quit_btn.clicked.connect(self._on_quit)
        layout.addWidget(quit_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def _create_menu_button(self, text: str, width: int, height: int) -> QPushButton:
        """Create a styled menu button"""
        button = QPushButton(text)
        button.setFixedSize(width, height)
        button.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Install event filter for hover sound
        button.installEventFilter(self)

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: rgb(60, 60, 70);
                color: rgb(220, 220, 220);
                border: 3px solid rgb(100, 100, 120);
                border-radius: 10px;
                padding: 15px;
            }}
            QPushButton:hover {{
                background-color: rgb(80, 80, 100);
                border: 3px solid rgb(150, 100, 255);
                color: rgb(255, 255, 255);
            }}
            QPushButton:pressed {{
                background-color: rgb(100, 100, 130);
                border: 3px solid rgb(180, 130, 255);
            }}
        """)

        return button

    def eventFilter(self, obj, event):
        """Filter events to detect hover for sound"""
        if isinstance(obj, QPushButton) and event.type() == event.Type.Enter:
            # Play hover sound
            audio = get_audio_manager()
            audio.play_ui_hover()
        return super().eventFilter(obj, event)

    def _on_new_game(self):
        """Handle New Game click"""
        audio = get_audio_manager()
        audio.play_ui_select()
        self.new_game_clicked.emit()

    def _on_how_to_play(self):
        """Handle How to Play click"""
        audio = get_audio_manager()
        audio.play_ui_select()
        self.how_to_play_clicked.emit()

    def _on_settings(self):
        """Handle Settings click"""
        audio = get_audio_manager()
        audio.play_ui_select()
        self.settings_clicked.emit()

    def _on_quit(self):
        """Handle Quit click"""
        audio = get_audio_manager()
        audio.play_ui_select()
        self.quit_clicked.emit()

    def update_animation(self):
        """Update animations"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        self.time_elapsed += dt

        # Update animations
        self.anim_manager.update(dt)

        # Spawn ambient particles periodically
        if len(self.anim_manager.ambient_particles) < 30:
            self.anim_manager.add_ambient_particles(count=1)

        self.update()

    def paintEvent(self, event):
        """Paint the menu screen with particles"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw background
        painter.fillRect(0, 0, self.width(), self.height(), c.COLOR_PANEL_BG)

        # Draw ambient particles
        for particle in self.anim_manager.ambient_particles:
            particle_color = QColor(particle.color.red(), particle.color.green(),
                                   particle.color.blue(), particle.alpha)
            painter.setBrush(particle_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(int(particle.x - particle.size / 2),
                              int(particle.y - particle.size / 2),
                              int(particle.size), int(particle.size))
