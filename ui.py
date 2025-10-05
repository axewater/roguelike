"""
PyQt UI for Dungeon Delver
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton, QStackedWidget, QSlider
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QKeyEvent, QPen
import time
import math
import random
import constants as c
from game import Game
from audio import get_audio_manager
from animations import AnimationManager
import graphics as gfx


class TitleScreen(QWidget):
    """Animated title screen with particles"""
    continue_pressed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setStyleSheet(f"background-color: rgb(20, 20, 25);")

        # Animation manager for particles
        self.anim_manager = AnimationManager()
        self.time_elapsed = 0.0
        self.last_time = time.time()

        # Pulse animation for title
        self.title_pulse = 0.0

        # Fade animation for "Press Any Key"
        self.prompt_fade = 0.0

        # Timer for animations
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS

        # Spawn initial particles
        for _ in range(30):
            self.anim_manager.add_ambient_particles(count=1)

    def update_animation(self):
        """Update animations"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time

        self.time_elapsed += dt

        # Update animations
        self.anim_manager.update(dt)

        # Spawn ambient particles periodically
        if len(self.anim_manager.ambient_particles) < 40:
            self.anim_manager.add_ambient_particles(count=2)

        # Update pulse animation (sine wave for smooth pulsing)
        self.title_pulse = math.sin(self.time_elapsed * 2.0) * 0.5 + 0.5

        # Update prompt fade (slower sine wave)
        self.prompt_fade = math.sin(self.time_elapsed * 3.0) * 0.5 + 0.5

        self.update()

    def paintEvent(self, event):
        """Paint the title screen"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw background gradient
        for y in range(self.height()):
            progress = y / self.height()
            r = int(20 + progress * 15)
            g = int(20 + progress * 15)
            b = int(25 + progress * 20)
            painter.setPen(QColor(r, g, b))
            painter.drawLine(0, y, self.width(), y)

        # Draw ambient particles
        for particle in self.anim_manager.ambient_particles:
            particle_color = QColor(particle.color.red(), particle.color.green(),
                                   particle.color.blue(), particle.alpha)
            painter.setBrush(particle_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(int(particle.x - particle.size / 2),
                              int(particle.y - particle.size / 2),
                              int(particle.size), int(particle.size))

        # Draw glowing title - "DUNGEON DELVER"
        title_y = self.height() // 3

        # Glow effect (multiple layers)
        glow_intensity = int(self.title_pulse * 100)
        for i in range(5, 0, -1):
            glow_alpha = glow_intensity - (i * 15)
            if glow_alpha > 0:
                glow_color = QColor(150, 100, 255, glow_alpha)
                painter.setPen(glow_color)
                painter.setFont(QFont("Arial", 56 + i * 2, QFont.Weight.Bold))
                painter.drawText(0, title_y - i, self.width(), 100,
                               Qt.AlignmentFlag.AlignCenter, "DUNGEON DELVER")

        # Main title
        title_brightness = int(200 + self.title_pulse * 55)
        title_color = QColor(title_brightness, int(title_brightness * 0.7), 255)
        painter.setPen(title_color)
        painter.setFont(QFont("Arial", 56, QFont.Weight.Bold))
        painter.drawText(0, title_y, self.width(), 100,
                        Qt.AlignmentFlag.AlignCenter, "DUNGEON DELVER")

        # Subtitle
        subtitle_y = title_y + 90
        painter.setPen(QColor(150, 150, 160))
        painter.setFont(QFont("Arial", 18, QFont.Weight.Normal))
        painter.drawText(0, subtitle_y, self.width(), 30,
                        Qt.AlignmentFlag.AlignCenter, "A Roguelike Adventure")

        # "Press Any Key" prompt with fade
        prompt_y = self.height() - 150
        prompt_alpha = int(150 + self.prompt_fade * 105)
        prompt_color = QColor(200, 200, 210, prompt_alpha)
        painter.setPen(prompt_color)
        painter.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        painter.drawText(0, prompt_y, self.width(), 40,
                        Qt.AlignmentFlag.AlignCenter, "Press Any Key to Continue")

        # Version info
        painter.setPen(QColor(100, 100, 110))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(10, self.height() - 20, "v1.0.0")

    def keyPressEvent(self, event):
        """Handle any key press to continue"""
        audio = get_audio_manager()
        audio.play_ui_select()
        self.continue_pressed.emit()


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


class SettingsScreen(QWidget):
    """Settings screen with volume controls"""
    back_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background-color: rgb({c.COLOR_PANEL_BG.red()}, {c.COLOR_PANEL_BG.green()}, {c.COLOR_PANEL_BG.blue()});")

        # Get audio manager
        self.audio_manager = get_audio_manager()

        self.setup_ui()

    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(40)

        # Title
        title = QLabel("SETTINGS")
        title.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); padding: 20px;")
        layout.addWidget(title)

        # Settings container
        settings_container = QFrame()
        settings_container.setStyleSheet(f"""
            QFrame {{
                background-color: rgb(45, 45, 50);
                border: 2px solid rgb(80, 80, 90);
                border-radius: 15px;
                padding: 30px;
            }}
        """)
        settings_container.setFixedWidth(600)

        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(30)

        # Music Volume
        music_label = QLabel("Music Volume")
        music_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        music_label.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); border: none;")
        settings_layout.addWidget(music_label)

        music_slider_container = QHBoxLayout()
        self.music_slider = QSlider(Qt.Orientation.Horizontal)
        self.music_slider.setMinimum(0)
        self.music_slider.setMaximum(100)
        self.music_slider.setValue(int(self.audio_manager.music_volume * 100))
        self.music_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999;
                height: 8px;
                background: rgb(60, 60, 70);
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: rgb(150, 100, 255);
                border: 2px solid rgb(100, 50, 200);
                width: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: rgb(180, 130, 255);
            }
        """)
        self.music_slider.valueChanged.connect(self._on_music_volume_changed)

        self.music_value_label = QLabel(f"{self.music_slider.value()}%")
        self.music_value_label.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        self.music_value_label.setFixedWidth(60)
        self.music_value_label.setStyleSheet("color: rgb(200, 200, 200); border: none;")

        music_slider_container.addWidget(self.music_slider)
        music_slider_container.addWidget(self.music_value_label)
        settings_layout.addLayout(music_slider_container)

        # SFX Volume
        sfx_label = QLabel("Sound Effects Volume")
        sfx_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        sfx_label.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); border: none;")
        settings_layout.addWidget(sfx_label)

        sfx_slider_container = QHBoxLayout()
        self.sfx_slider = QSlider(Qt.Orientation.Horizontal)
        self.sfx_slider.setMinimum(0)
        self.sfx_slider.setMaximum(100)
        self.sfx_slider.setValue(int(self.audio_manager.sfx_volume * 100))
        self.sfx_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999;
                height: 8px;
                background: rgb(60, 60, 70);
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: rgb(100, 200, 255);
                border: 2px solid rgb(50, 150, 200);
                width: 20px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::handle:horizontal:hover {
                background: rgb(130, 220, 255);
            }
        """)
        self.sfx_slider.valueChanged.connect(self._on_sfx_volume_changed)

        self.sfx_value_label = QLabel(f"{self.sfx_slider.value()}%")
        self.sfx_value_label.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        self.sfx_value_label.setFixedWidth(60)
        self.sfx_value_label.setStyleSheet("color: rgb(200, 200, 200); border: none;")

        sfx_slider_container.addWidget(self.sfx_slider)
        sfx_slider_container.addWidget(self.sfx_value_label)
        settings_layout.addLayout(sfx_slider_container)

        settings_container.setLayout(settings_layout)
        layout.addWidget(settings_container, alignment=Qt.AlignmentFlag.AlignCenter)

        # Back button
        back_button = QPushButton("Back to Menu")
        back_button.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        back_button.setFixedSize(300, 60)
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(80, 80, 100);
                color: rgb(220, 220, 220);
                border: 3px solid rgb(100, 100, 120);
                border-radius: 10px;
                padding: 15px;
            }
            QPushButton:hover {
                background-color: rgb(100, 100, 130);
                border: 3px solid rgb(150, 150, 180);
            }
        """)
        back_button.clicked.connect(self._on_back_clicked)
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def _on_music_volume_changed(self, value):
        """Handle music volume slider change"""
        volume = value / 100.0
        self.audio_manager.set_music_volume(volume)
        self.music_value_label.setText(f"{value}%")

    def _on_sfx_volume_changed(self, value):
        """Handle SFX volume slider change"""
        volume = value / 100.0
        self.audio_manager.set_sfx_volume(volume)
        self.sfx_value_label.setText(f"{value}%")

        # Play a test sound
        if value > 0:
            self.audio_manager.play_ui_select()

    def _on_back_clicked(self):
        """Handle back button click"""
        self.audio_manager.play_ui_select()
        self.back_clicked.emit()


class AbilityButton(QPushButton):
    """Custom button for abilities with visual feedback"""
    ability_clicked = pyqtSignal(int)  # Emits ability index

    def __init__(self, ability_index: int):
        super().__init__()
        self.ability_index = ability_index
        self.is_ready = False
        self.ability_name = ""
        self.ability_status = ""

        self.setMinimumHeight(32)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(lambda: self.ability_clicked.emit(self.ability_index))

    def set_ability_state(self, name: str, is_ready: bool, status: str):
        """Update ability state and appearance"""
        self.ability_name = name
        self.is_ready = is_ready
        self.ability_status = status

        # Update text
        key_num = self.ability_index + 1
        self.setText(f"[{key_num}] {name}: {status}")

        # Update style based on readiness
        if is_ready:
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgba(81, 207, 102, 0.2);
                    color: rgb(81, 207, 102);
                    border: 2px solid rgb(81, 207, 102);
                    border-radius: 4px;
                    padding: 6px;
                    font-family: 'Courier New';
                    font-size: 9pt;
                    font-weight: bold;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: rgba(81, 207, 102, 0.4);
                    border: 2px solid rgb(100, 230, 120);
                }
                QPushButton:pressed {
                    background-color: rgba(81, 207, 102, 0.6);
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: rgba(100, 100, 100, 0.2);
                    color: rgb(150, 150, 150);
                    border: 2px solid rgb(100, 100, 100);
                    border-radius: 4px;
                    padding: 6px;
                    font-family: 'Courier New';
                    font-size: 9pt;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: rgba(100, 100, 100, 0.3);
                }
            """)


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


class CharacterPreviewPanel(QWidget):
    """Left panel showing animated character preview"""
    def __init__(self):
        super().__init__()
        self.current_class = c.CLASS_WARRIOR
        self.float_offset = 0.0
        self.time_elapsed = 0.0
        self.anim_manager = AnimationManager()
        self.particle_spawn_timer = 0.0

        self.setStyleSheet("background-color: rgb(25, 25, 30);")
        self.setMinimumHeight(600)

    def set_class(self, class_type: str):
        """Set the class to display"""
        if self.current_class != class_type:
            self.current_class = class_type
            # Spawn transition particles
            self._spawn_class_particles(burst=True)

    def update_animation(self, dt: float):
        """Update animations"""
        self.time_elapsed += dt

        # Floating animation (slow sine wave)
        self.float_offset = math.sin(self.time_elapsed * 2.0) * 10

        # Update particle system
        self.anim_manager.update(dt)

        # Spawn class-themed particles periodically
        self.particle_spawn_timer += dt
        if self.particle_spawn_timer > 0.5:
            self.particle_spawn_timer = 0.0
            self._spawn_class_particles(burst=False)

        self.update()

    def _spawn_class_particles(self, burst: bool = False):
        """Spawn class-themed particles"""
        count = 8 if burst else 2
        center_x = self.width() // 2
        center_y = self.height() // 2

        color = self._get_class_color()

        for _ in range(count):
            # Orbit around character
            angle = random.uniform(0, 6.28)
            radius = random.uniform(80, 120) if not burst else random.uniform(50, 150)
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle) - 50

            # Velocity for orbit
            vx = -math.sin(angle) * 0.5
            vy = math.cos(angle) * 0.5 - 0.3  # Slight upward drift

            from animations import Particle
            particle = Particle(
                x, y, vx, vy,
                color,
                size=random.uniform(2, 5),
                lifetime=random.uniform(1.5, 2.5),
                particle_type="circle" if self.current_class == c.CLASS_MAGE else "square",
                apply_gravity=False
            )
            self.anim_manager.particles.append(particle)

    def _get_class_color(self) -> QColor:
        """Get current class color"""
        colors = {
            c.CLASS_WARRIOR: c.COLOR_CLASS_WARRIOR,
            c.CLASS_MAGE: c.COLOR_CLASS_MAGE,
            c.CLASS_ROGUE: c.COLOR_CLASS_ROGUE,
            c.CLASS_RANGER: c.COLOR_CLASS_RANGER,
        }
        return colors.get(self.current_class, c.COLOR_TEXT_LIGHT)

    def paintEvent(self, event):
        """Render character preview"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background gradient
        from PyQt6.QtGui import QLinearGradient
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(25, 25, 30))
        gradient.setColorAt(1, QColor(35, 35, 40))
        painter.fillRect(0, 0, self.width(), self.height(), gradient)

        # Draw particles in background
        for particle in self.anim_manager.particles:
            particle_color = QColor(
                particle.color.red(),
                particle.color.green(),
                particle.color.blue(),
                particle.alpha
            )
            painter.setBrush(particle_color)
            painter.setPen(Qt.PenStyle.NoPen)
            if particle.particle_type == "circle":
                painter.drawEllipse(
                    int(particle.x - particle.size / 2),
                    int(particle.y - particle.size / 2),
                    int(particle.size),
                    int(particle.size)
                )
            else:
                painter.fillRect(
                    int(particle.x - particle.size / 2),
                    int(particle.y - particle.size / 2),
                    int(particle.size),
                    int(particle.size),
                    particle_color
                )

        # Calculate character position (centered, with float offset)
        char_x = self.width() // 2 - c.TILE_SIZE * 2
        char_y = self.height() // 2 - c.TILE_SIZE * 2 + int(self.float_offset)

        # Scale up character (4x size for preview)
        scale = 4
        tile_size = c.TILE_SIZE * scale

        # Save painter state
        painter.save()

        # Create a larger virtual tile at the scaled position
        # Draw character using graphics functions
        screen_x = 0  # Will draw at specific pixel position
        screen_y = 0

        # Temporarily modify tile size for drawing
        painter.translate(char_x, char_y)

        # Draw a glowing aura behind character
        class_color = self._get_class_color()
        from PyQt6.QtGui import QRadialGradient
        aura_gradient = QRadialGradient(tile_size // 2, tile_size // 2, tile_size)
        aura_gradient.setColorAt(0, QColor(class_color.red(), class_color.green(), class_color.blue(), 100))
        aura_gradient.setColorAt(0.5, QColor(class_color.red(), class_color.green(), class_color.blue(), 40))
        aura_gradient.setColorAt(1, QColor(class_color.red(), class_color.green(), class_color.blue(), 0))
        painter.fillRect(0, 0, tile_size, tile_size, aura_gradient)

        # Draw the character (scaled up)
        gfx.draw_player(painter, screen_x, screen_y, tile_size, class_color, self.current_class)

        painter.restore()

        # Draw class name below character
        painter.setPen(class_color.lighter(130))
        painter.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        class_names = {
            c.CLASS_WARRIOR: "WARRIOR",
            c.CLASS_MAGE: "MAGE",
            c.CLASS_ROGUE: "ROGUE",
            c.CLASS_RANGER: "RANGER",
        }
        class_name = class_names.get(self.current_class, "")
        painter.drawText(0, self.height() - 80, self.width(), 40,
                        Qt.AlignmentFlag.AlignCenter, class_name)

        # Draw class description
        painter.setPen(c.COLOR_TEXT_LIGHT)
        painter.setFont(QFont("Arial", 12))
        stats = c.CLASS_STATS.get(self.current_class, {})
        desc = stats.get("description", "")
        painter.drawText(20, self.height() - 45, self.width() - 40, 40,
                        Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop, desc)


class StatComparisonPanel(QWidget):
    """Panel showing stat bars for comparison"""
    def __init__(self):
        super().__init__()
        self.current_class = None
        self.target_values = {'hp': 0, 'attack': 0, 'defense': 0}
        self.current_values = {'hp': 0.0, 'attack': 0.0, 'defense': 0.0}

        self.setFixedHeight(120)
        self.setStyleSheet("background-color: rgb(40, 40, 45); border-radius: 10px; padding: 15px;")

    def set_class(self, class_type: str):
        """Set class and update stat targets"""
        self.current_class = class_type
        stats = c.CLASS_STATS.get(class_type, {})
        self.target_values = {
            'hp': stats.get('hp', 0),
            'attack': stats.get('attack', 0),
            'defense': stats.get('defense', 0)
        }

    def update_animation(self, dt: float):
        """Animate stat bars toward target values"""
        lerp_speed = 5.0
        for stat in ['hp', 'attack', 'defense']:
            target = self.target_values[stat]
            current = self.current_values[stat]
            # Lerp toward target
            self.current_values[stat] += (target - current) * lerp_speed * dt

    def paintEvent(self, event):
        """Draw stat bars"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background
        painter.fillRect(0, 0, self.width(), self.height(), QColor(40, 40, 45))

        if not self.current_class:
            return

        # Stat bar configuration
        stats_config = [
            ('HP', self.current_values['hp'], 120, QColor(100, 200, 120), 10),
            ('ATK', self.current_values['attack'], 20, QColor(255, 100, 100), 45),
            ('DEF', self.current_values['defense'], 12, QColor(100, 150, 255), 80),
        ]

        for stat_name, value, max_val, color, y_offset in stats_config:
            y_pos = y_offset

            # Stat label
            painter.setPen(c.COLOR_TEXT_LIGHT)
            painter.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            painter.drawText(15, y_pos, 50, 20, Qt.AlignmentFlag.AlignLeft, stat_name)

            # Value label
            painter.drawText(self.width() - 60, y_pos, 50, 20,
                           Qt.AlignmentFlag.AlignRight, f"{int(value)}")

            # Bar background
            bar_x = 70
            bar_width = self.width() - 140
            bar_height = 18
            painter.fillRect(bar_x, y_pos - 2, bar_width, bar_height, QColor(30, 30, 35))

            # Bar fill (animated)
            fill_width = int((value / max_val) * bar_width)
            if fill_width > 0:
                # Gradient fill
                from PyQt6.QtGui import QLinearGradient
                gradient = QLinearGradient(bar_x, y_pos, bar_x + fill_width, y_pos)
                gradient.setColorAt(0, color.darker(110))
                gradient.setColorAt(1, color.lighter(120))
                painter.fillRect(bar_x, y_pos - 2, fill_width, bar_height, gradient)

            # Bar border
            painter.setPen(QColor(70, 70, 75))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(bar_x, y_pos - 2, bar_width, bar_height)


class ClassCard(QWidget):
    """Individual class selection card with hover effects"""
    clicked = pyqtSignal()
    hovered = pyqtSignal()
    unhovered = pyqtSignal()

    def __init__(self, class_type: str, color: QColor, label: str, abilities: list):
        super().__init__()
        self.class_type = class_type
        self.color = color
        self.label = label
        self.abilities = abilities
        self.is_hovered = False
        self.is_selected = False
        self.hover_glow = 0.0

        self.setMinimumSize(220, 160)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setup_ui()

    def setup_ui(self):
        """Setup card UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        # Class name
        name_label = QLabel(self.label)
        name_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setStyleSheet(f"color: rgb({self.color.red()}, {self.color.green()}, {self.color.blue()}); background: transparent; border: none;")
        layout.addWidget(name_label)

        # Stats (mini version)
        stats = c.CLASS_STATS[self.class_type]
        stats_text = f"HP:{stats['hp']} ATK:{stats['attack']} DEF:{stats['defense']}"
        stats_label = QLabel(stats_text)
        stats_label.setFont(QFont("Courier New", 9, QFont.Weight.Bold))
        stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_label.setStyleSheet("color: rgb(180, 180, 180); background: transparent; border: none;")
        layout.addWidget(stats_label)

        # Abilities (compact)
        abilities_text = " • ".join(self.abilities)
        abilities_label = QLabel(abilities_text)
        abilities_label.setFont(QFont("Arial", 8))
        abilities_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        abilities_label.setWordWrap(True)
        abilities_label.setStyleSheet("color: rgb(150, 150, 180); background: transparent; border: none; padding: 4px;")
        layout.addWidget(abilities_label)

        layout.addStretch()

        # SELECT label
        select_label = QLabel("CLICK TO SELECT")
        select_label.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        select_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        select_label.setStyleSheet("color: rgb(120, 120, 130); background: transparent; border: none;")
        layout.addWidget(select_label)

        self.setLayout(layout)

    def set_selected(self, selected: bool):
        """Set selection state"""
        self.is_selected = selected
        self.update()

    def enterEvent(self, event):
        """Mouse enter"""
        self.is_hovered = True
        self.hovered.emit()
        self.update()

    def leaveEvent(self, event):
        """Mouse leave"""
        self.is_hovered = False
        self.unhovered.emit()
        self.update()

    def mousePressEvent(self, event):
        """Mouse click"""
        self.clicked.emit()

    def paintEvent(self, event):
        """Custom paint with glow effects"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Determine colors based on state
        if self.is_selected:
            border_color = self.color.lighter(140)
            border_width = 3
            bg_alpha = 30
        elif self.is_hovered:
            border_color = self.color.lighter(120)
            border_width = 3
            bg_alpha = 20
        else:
            border_color = QColor(70, 70, 80)
            border_width = 2
            bg_alpha = 10

        # Background with class tint
        bg_color = QColor(
            min(40 + self.color.red() // 10, 60),
            min(40 + self.color.green() // 10, 60),
            min(45 + self.color.blue() // 10, 65),
            bg_alpha if not self.is_selected else 40
        )
        painter.fillRect(0, 0, self.width(), self.height(), bg_color)

        # Glow effect when hovered or selected
        if self.is_hovered or self.is_selected:
            from PyQt6.QtGui import QLinearGradient
            glow_gradient = QLinearGradient(0, 0, self.width(), self.height())
            glow_color = QColor(self.color.red(), self.color.green(), self.color.blue(), 40)
            glow_gradient.setColorAt(0, glow_color)
            glow_gradient.setColorAt(1, QColor(self.color.red(), self.color.green(), self.color.blue(), 10))
            painter.fillRect(0, 0, self.width(), self.height(), glow_gradient)

        # Border
        painter.setPen(QPen(border_color, border_width))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(
            border_width // 2,
            border_width // 2,
            self.width() - border_width,
            self.height() - border_width,
            8, 8
        )


class ClassSelectionScreen(QWidget):
    """Enhanced class selection screen with live preview and animations"""
    class_selected = pyqtSignal(str)
    back_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Class ability descriptions
        self.class_abilities = {
            c.CLASS_WARRIOR: ["Healing Touch", "Whirlwind", "Dash"],
            c.CLASS_MAGE: ["Fireball", "Frost Nova", "Healing Touch"],
            c.CLASS_ROGUE: ["Shadow Step", "Dash", "Healing Touch"],
            c.CLASS_RANGER: ["Fireball", "Dash", "Healing Touch"],
        }

        # Animation system
        self.anim_manager = AnimationManager()
        self.time_elapsed = 0.0
        self.last_time = time.time()

        # Selected/hovered class tracking
        self.selected_class = None
        self.hovered_class = None

        # Animation values for smooth transitions
        self.preview_float_offset = 0.0
        self.stat_bar_progress = {
            'hp': 0.0,
            'attack': 0.0,
            'defense': 0.0
        }

        # Class cards for hover detection
        self.class_cards = {}

        self.setup_ui()

        # Start animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS

    def setup_ui(self):
        """Setup the enhanced split-view UI"""
        self.setStyleSheet(f"background-color: rgb({c.COLOR_PANEL_BG.red()}, {c.COLOR_PANEL_BG.green()}, {c.COLOR_PANEL_BG.blue()});")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Title bar
        title = QLabel("CHOOSE YOUR CLASS")
        title.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); padding: 25px; background-color: rgb(25, 25, 30);")
        main_layout.addWidget(title)

        # Split view: Preview (left) | Class Grid (right)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)

        # LEFT: Character Preview Panel
        self.preview_panel = CharacterPreviewPanel()
        self.preview_panel.setFixedWidth(int(c.WINDOW_WIDTH * 0.45))
        content_layout.addWidget(self.preview_panel)

        # RIGHT: Class Selection Grid
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(30, 30, 30, 20)
        right_layout.setSpacing(20)

        # Stat comparison panel
        self.stat_panel = StatComparisonPanel()
        right_layout.addWidget(self.stat_panel)

        # Class cards in 2x2 grid
        from PyQt6.QtWidgets import QGridLayout
        grid_container = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)

        classes = [
            (c.CLASS_WARRIOR, c.COLOR_CLASS_WARRIOR, "WARRIOR", 0, 0),
            (c.CLASS_MAGE, c.COLOR_CLASS_MAGE, "MAGE", 0, 1),
            (c.CLASS_ROGUE, c.COLOR_CLASS_ROGUE, "ROGUE", 1, 0),
            (c.CLASS_RANGER, c.COLOR_CLASS_RANGER, "RANGER", 1, 1),
        ]

        for class_type, color, label_text, row, col in classes:
            card = ClassCard(class_type, color, label_text, self.class_abilities[class_type])
            card.clicked.connect(lambda ct=class_type: self._on_class_select(ct))
            card.hovered.connect(lambda ct=class_type: self._on_class_hover(ct))
            card.unhovered.connect(self._on_class_unhover)
            self.class_cards[class_type] = card
            grid_layout.addWidget(card, row, col)

        grid_container.setLayout(grid_layout)
        right_layout.addWidget(grid_container)

        # Back button
        back_button = QPushButton("Back to Menu")
        back_button.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        back_button.setFixedHeight(45)
        back_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(60, 60, 70);
                color: rgb(180, 180, 185);
                border: 2px solid rgb(80, 80, 90);
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(80, 80, 90);
                border: 2px solid rgb(150, 150, 180);
                color: rgb(220, 220, 220);
            }
        """)
        back_button.clicked.connect(self._on_back_clicked)
        back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        right_layout.addWidget(back_button)

        right_panel.setLayout(right_layout)
        content_layout.addWidget(right_panel)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        # Initialize with warrior selected
        self.selected_class = c.CLASS_WARRIOR
        self._update_preview()

    def _on_class_select(self, class_type: str):
        """Handle class selection"""
        audio = get_audio_manager()
        audio.play_ui_select()
        self.selected_class = class_type
        self._update_preview()

        # Highlight selected card
        for ct, card in self.class_cards.items():
            card.set_selected(ct == class_type)

        # Emit signal to start game
        self.class_selected.emit(class_type)

    def _on_class_hover(self, class_type: str):
        """Handle class hover"""
        if self.hovered_class != class_type:
            audio = get_audio_manager()
            audio.play_ui_hover()
            self.hovered_class = class_type
            self._update_preview()

    def _on_class_unhover(self):
        """Handle mouse leaving class card"""
        self.hovered_class = None
        self._update_preview()

    def _update_preview(self):
        """Update character preview and stats"""
        display_class = self.hovered_class if self.hovered_class else self.selected_class
        if display_class:
            self.preview_panel.set_class(display_class)
            self.stat_panel.set_class(display_class)

    def _on_back_clicked(self):
        """Handle back button click"""
        audio = get_audio_manager()
        audio.play_ui_select()
        self.back_clicked.emit()

    def update_animation(self):
        """Update animations"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        self.time_elapsed += dt

        # Update animation manager
        self.anim_manager.update(dt)

        # Update preview panel animations
        if hasattr(self, 'preview_panel'):
            self.preview_panel.update_animation(dt)

        # Update stat panel animations
        if hasattr(self, 'stat_panel'):
            self.stat_panel.update_animation(dt)

        # Update display
        self.update()


class GameWidget(QWidget):
    """Widget for rendering the game grid"""
    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.setFixedSize(c.VIEWPORT_WIDTH * c.TILE_SIZE, c.VIEWPORT_HEIGHT * c.TILE_SIZE)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setStyleSheet(f"background-color: rgb({c.COLOR_FLOOR.red()}, {c.COLOR_FLOOR.green()}, {c.COLOR_FLOOR.blue()});")

        # Mouse tracking for hover effects
        self.setMouseTracking(True)
        self.hover_world_x = None
        self.hover_world_y = None

        # Ability targeting mode
        self.targeting_mode = False
        self.targeting_ability_index = None

    def paintEvent(self, event):
        """Render the game grid"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if not self.game.dungeon:
            return

        # Apply screen shake offset
        shake_x, shake_y = self.game.anim_manager.get_screen_offset()
        painter.translate(shake_x, shake_y)

        # Draw tiles with graphics (only visible viewport)
        for screen_y in range(c.VIEWPORT_HEIGHT):
            for screen_x in range(c.VIEWPORT_WIDTH):
                # Convert screen coords to world coords
                world_x = screen_x + self.game.camera_x
                world_y = screen_y + self.game.camera_y

                # Check bounds
                if not (0 <= world_x < c.GRID_WIDTH and 0 <= world_y < c.GRID_HEIGHT):
                    continue

                tile = self.game.dungeon.get_tile(world_x, world_y)

                if tile == c.TILE_WALL:
                    gfx.draw_wall_tile(painter, screen_x, screen_y, c.TILE_SIZE)
                elif tile == c.TILE_FLOOR:
                    gfx.draw_floor_tile(painter, screen_x, screen_y, c.TILE_SIZE)
                elif tile == c.TILE_STAIRS:
                    gfx.draw_floor_tile(painter, screen_x, screen_y, c.TILE_SIZE)  # Draw floor underneath
                    gfx.draw_stairs_tile(painter, screen_x, screen_y, c.TILE_SIZE)

        # Draw entities with graphics (only visible viewport)
        for screen_y in range(c.VIEWPORT_HEIGHT):
            for screen_x in range(c.VIEWPORT_WIDTH):
                # Convert screen coords to world coords
                world_x = screen_x + self.game.camera_x
                world_y = screen_y + self.game.camera_y

                # Check bounds
                if not (0 <= world_x < c.GRID_WIDTH and 0 <= world_y < c.GRID_HEIGHT):
                    continue

                entity = self.game.get_entity_at(world_x, world_y)
                if entity:
                    color = self._get_entity_color(entity)

                    if entity.entity_type == c.ENTITY_PLAYER:
                        gfx.draw_player(painter, screen_x, screen_y, c.TILE_SIZE, color, entity.class_type)
                    elif entity.entity_type == c.ENTITY_ENEMY:
                        gfx.draw_enemy(painter, screen_x, screen_y, c.TILE_SIZE, color, entity.enemy_type)
                    elif entity.entity_type == c.ENTITY_ITEM:
                        gfx.draw_item(painter, screen_x, screen_y, c.TILE_SIZE, color, entity.item_type)

        # Draw enemy health bars
        self._draw_enemy_health_bars(painter)

        # Draw flash effects (before other animations)
        for flash in self.game.anim_manager.flash_effects:
            # Convert to screen coords
            screen_x = flash.x - self.game.camera_x
            screen_y = flash.y - self.game.camera_y

            # Only draw if visible
            if not (0 <= screen_x < c.VIEWPORT_WIDTH and 0 <= screen_y < c.VIEWPORT_HEIGHT):
                continue

            flash_color = QColor(flash.color.red(), flash.color.green(), flash.color.blue(), flash.alpha)
            painter.fillRect(
                screen_x * c.TILE_SIZE,
                screen_y * c.TILE_SIZE,
                c.TILE_SIZE,
                c.TILE_SIZE,
                flash_color
            )

        # Draw ambient particles (background layer)
        for particle in self.game.anim_manager.ambient_particles:
            # Convert pixel coords to screen space
            screen_pixel_x = particle.x - (self.game.camera_x * c.TILE_SIZE)
            screen_pixel_y = particle.y - (self.game.camera_y * c.TILE_SIZE)

            # Only draw if within viewport bounds
            if not (0 <= screen_pixel_x < c.VIEWPORT_WIDTH * c.TILE_SIZE and
                    0 <= screen_pixel_y < c.VIEWPORT_HEIGHT * c.TILE_SIZE):
                continue

            particle_color = QColor(particle.color.red(), particle.color.green(),
                                   particle.color.blue(), particle.alpha)
            painter.setBrush(particle_color)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(int(screen_pixel_x - particle.size / 2),
                              int(screen_pixel_y - particle.size / 2),
                              int(particle.size), int(particle.size))

        # Draw trail effects
        for trail in self.game.anim_manager.trails:
            # Convert to screen coords
            screen_x = trail.x - self.game.camera_x
            screen_y = trail.y - self.game.camera_y

            # Only draw if visible
            if not (0 <= screen_x < c.VIEWPORT_WIDTH and 0 <= screen_y < c.VIEWPORT_HEIGHT):
                continue

            trail_color = QColor(trail.color.red(), trail.color.green(),
                               trail.color.blue(), trail.alpha)
            painter.setBrush(trail_color)
            painter.setPen(Qt.PenStyle.NoPen)

            # Draw as fading circle
            painter.drawEllipse(int(screen_x * c.TILE_SIZE + c.TILE_SIZE / 2 - trail.size / 2),
                              int(screen_y * c.TILE_SIZE + c.TILE_SIZE / 2 - trail.size / 2),
                              int(trail.size), int(trail.size))

        # Draw regular particles
        for particle in self.game.anim_manager.particles:
            # Convert pixel coords to screen space
            screen_pixel_x = particle.x - (self.game.camera_x * c.TILE_SIZE)
            screen_pixel_y = particle.y - (self.game.camera_y * c.TILE_SIZE)

            # Only draw if within viewport bounds
            if not (0 <= screen_pixel_x < c.VIEWPORT_WIDTH * c.TILE_SIZE and
                    0 <= screen_pixel_y < c.VIEWPORT_HEIGHT * c.TILE_SIZE):
                continue

            particle_color = QColor(particle.color.red(), particle.color.green(),
                                   particle.color.blue(), particle.alpha)
            painter.setBrush(particle_color)
            painter.setPen(Qt.PenStyle.NoPen)

            if particle.particle_type == "circle":
                painter.drawEllipse(int(screen_pixel_x - particle.size / 2),
                                  int(screen_pixel_y - particle.size / 2),
                                  int(particle.size), int(particle.size))
            else:  # square or star
                painter.fillRect(int(screen_pixel_x - particle.size / 2),
                               int(screen_pixel_y - particle.size / 2),
                               int(particle.size), int(particle.size),
                               particle_color)

        # Draw directional particles
        for particle in self.game.anim_manager.directional_particles:
            # Convert pixel coords to screen space
            screen_pixel_x = particle.x - (self.game.camera_x * c.TILE_SIZE)
            screen_pixel_y = particle.y - (self.game.camera_y * c.TILE_SIZE)

            # Only draw if within viewport bounds
            if not (0 <= screen_pixel_x < c.VIEWPORT_WIDTH * c.TILE_SIZE and
                    0 <= screen_pixel_y < c.VIEWPORT_HEIGHT * c.TILE_SIZE):
                continue

            particle_color = QColor(particle.color.red(), particle.color.green(),
                                   particle.color.blue(), particle.alpha)
            painter.setBrush(particle_color)
            painter.setPen(Qt.PenStyle.NoPen)

            if particle.particle_type == "circle":
                painter.drawEllipse(int(screen_pixel_x - particle.size / 2),
                                  int(screen_pixel_y - particle.size / 2),
                                  int(particle.size), int(particle.size))
            else:
                painter.fillRect(int(screen_pixel_x - particle.size / 2),
                               int(screen_pixel_y - particle.size / 2),
                               int(particle.size), int(particle.size),
                               particle_color)

        # Draw floating text
        text_font = QFont("Arial", 14, QFont.Weight.Bold)
        for ftext in self.game.anim_manager.floating_texts:
            # Convert to screen coords
            screen_x = ftext.x - self.game.camera_x
            screen_y = ftext.y - self.game.camera_y

            # Only draw if visible
            if not (0 <= screen_x < c.VIEWPORT_WIDTH and 0 <= screen_y < c.VIEWPORT_HEIGHT):
                continue

            if ftext.is_crit:
                text_font.setPointSize(18)
            else:
                text_font.setPointSize(14)

            painter.setFont(text_font)
            text_color = QColor(ftext.color.red(), ftext.color.green(),
                              ftext.color.blue(), ftext.alpha)
            painter.setPen(text_color)

            # Calculate position
            text_x = screen_x * c.TILE_SIZE + c.TILE_SIZE // 2
            text_y = screen_y * c.TILE_SIZE + int(ftext.offset_y * c.TILE_SIZE)

            painter.drawText(int(text_x - 20), int(text_y - 10), 40, 20,
                           Qt.AlignmentFlag.AlignCenter, ftext.text)

        # Draw ability range indicator if in targeting mode
        if self.targeting_mode and self.targeting_ability_index is not None:
            self._draw_ability_range(painter)

        # Draw hover highlight (before game over overlay)
        if self.hover_world_x is not None and self.hover_world_y is not None:
            self._draw_hover_highlight(painter)

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
            # Convert world coords to screen coords
            screen_x = enemy.x - self.game.camera_x
            screen_y = enemy.y - self.game.camera_y

            # Only draw if enemy is visible in viewport
            if not (0 <= screen_x < c.VIEWPORT_WIDTH and 0 <= screen_y < c.VIEWPORT_HEIGHT):
                continue

            # Calculate bar dimensions
            bar_width = c.TILE_SIZE - 4
            bar_height = 3
            bar_x = screen_x * c.TILE_SIZE + 2
            bar_y = screen_y * c.TILE_SIZE + c.TILE_SIZE - 5

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

    def _draw_ability_range(self, painter: QPainter):
        """Draw ability range/area indicator when in targeting mode"""
        if not self.game.player or self.targeting_ability_index >= len(self.game.player.abilities):
            return

        ability = self.game.player.abilities[self.targeting_ability_index]
        player_x, player_y = self.game.player.x, self.game.player.y

        # Define range and area based on ability type
        range_color = QColor(100, 150, 255, 60)
        area_color = QColor(255, 100, 100, 80)

        # Ability-specific range visualization
        if ability.name == "Fireball":
            # Show max range and AOE area
            max_range = 8  # Fireball can be cast far
            radius = 1

            # Show range circles
            for y in range(c.GRID_HEIGHT):
                for x in range(c.GRID_WIDTH):
                    dist = abs(x - player_x) + abs(y - player_y)
                    if dist <= max_range:
                        screen_x = x - self.game.camera_x
                        screen_y = y - self.game.camera_y
                        if 0 <= screen_x < c.VIEWPORT_WIDTH and 0 <= screen_y < c.VIEWPORT_HEIGHT:
                            painter.fillRect(screen_x * c.TILE_SIZE, screen_y * c.TILE_SIZE,
                                           c.TILE_SIZE, c.TILE_SIZE, range_color)

            # Show AOE at cursor position
            if self.hover_world_x is not None and self.hover_world_y is not None:
                for dy in range(-radius, radius + 1):
                    for dx in range(-radius, radius + 1):
                        aoe_x = self.hover_world_x + dx
                        aoe_y = self.hover_world_y + dy
                        screen_x = aoe_x - self.game.camera_x
                        screen_y = aoe_y - self.game.camera_y
                        if 0 <= screen_x < c.VIEWPORT_WIDTH and 0 <= screen_y < c.VIEWPORT_HEIGHT:
                            painter.fillRect(screen_x * c.TILE_SIZE, screen_y * c.TILE_SIZE,
                                           c.TILE_SIZE, c.TILE_SIZE, area_color)

        elif ability.name == "Dash":
            # Show max dash range
            max_distance = 4
            for y in range(c.GRID_HEIGHT):
                for x in range(c.GRID_WIDTH):
                    dist = abs(x - player_x) + abs(y - player_y)
                    if dist <= max_distance and self.game.dungeon.is_walkable(x, y):
                        screen_x = x - self.game.camera_x
                        screen_y = y - self.game.camera_y
                        if 0 <= screen_x < c.VIEWPORT_WIDTH and 0 <= screen_y < c.VIEWPORT_HEIGHT:
                            painter.fillRect(screen_x * c.TILE_SIZE, screen_y * c.TILE_SIZE,
                                           c.TILE_SIZE, c.TILE_SIZE, QColor(150, 200, 255, 80))

        elif ability.name == "Shadow Step":
            # Show enemy targets
            for enemy in self.game.enemies:
                # Check if there's a valid position behind enemy
                dx = enemy.x - player_x
                dy = enemy.y - player_y
                behind_x = enemy.x + (1 if dx > 0 else -1 if dx < 0 else 0)
                behind_y = enemy.y + (1 if dy > 0 else -1 if dy < 0 else 0)

                valid = self.game.dungeon.is_walkable(behind_x, behind_y)
                color = QColor(180, 100, 255, 100) if valid else QColor(100, 100, 100, 50)

                screen_x = enemy.x - self.game.camera_x
                screen_y = enemy.y - self.game.camera_y
                if 0 <= screen_x < c.VIEWPORT_WIDTH and 0 <= screen_y < c.VIEWPORT_HEIGHT:
                    painter.fillRect(screen_x * c.TILE_SIZE, screen_y * c.TILE_SIZE,
                                   c.TILE_SIZE, c.TILE_SIZE, color)

        elif ability.name == "Frost Nova":
            # Show radius around player
            radius = 2
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    if abs(dx) + abs(dy) <= radius:
                        nova_x = player_x + dx
                        nova_y = player_y + dy
                        screen_x = nova_x - self.game.camera_x
                        screen_y = nova_y - self.game.camera_y
                        if 0 <= screen_x < c.VIEWPORT_WIDTH and 0 <= screen_y < c.VIEWPORT_HEIGHT:
                            painter.fillRect(screen_x * c.TILE_SIZE, screen_y * c.TILE_SIZE,
                                           c.TILE_SIZE, c.TILE_SIZE, QColor(150, 220, 255, 80))

        elif ability.name == "Whirlwind":
            # Show adjacent tiles
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if dx != 0 or dy != 0:
                        whirl_x = player_x + dx
                        whirl_y = player_y + dy
                        screen_x = whirl_x - self.game.camera_x
                        screen_y = whirl_y - self.game.camera_y
                        if 0 <= screen_x < c.VIEWPORT_WIDTH and 0 <= screen_y < c.VIEWPORT_HEIGHT:
                            painter.fillRect(screen_x * c.TILE_SIZE, screen_y * c.TILE_SIZE,
                                           c.TILE_SIZE, c.TILE_SIZE, QColor(255, 150, 150, 80))

    def _draw_hover_highlight(self, painter: QPainter):
        """Draw hover highlight on the tile under cursor"""
        # Convert world coords to screen coords
        screen_x = self.hover_world_x - self.game.camera_x
        screen_y = self.hover_world_y - self.game.camera_y

        # Only draw if visible in viewport
        if not (0 <= screen_x < c.VIEWPORT_WIDTH and 0 <= screen_y < c.VIEWPORT_HEIGHT):
            return

        # Determine highlight color based on what's at the tile
        highlight_color, can_interact = self._get_hover_color()

        if can_interact:
            # Draw highlight border
            painter.setPen(highlight_color)
            for i in range(3):  # Draw multiple borders for glow effect
                alpha = 255 - (i * 60)
                glow_color = QColor(highlight_color.red(), highlight_color.green(),
                                   highlight_color.blue(), alpha)
                painter.setPen(glow_color)
                offset = i * 2
                painter.drawRect(
                    screen_x * c.TILE_SIZE - offset,
                    screen_y * c.TILE_SIZE - offset,
                    c.TILE_SIZE + offset * 2 - 1,
                    c.TILE_SIZE + offset * 2 - 1
                )

            # Fill with semi-transparent color
            fill_color = QColor(highlight_color.red(), highlight_color.green(),
                               highlight_color.blue(), 40)
            painter.fillRect(
                screen_x * c.TILE_SIZE,
                screen_y * c.TILE_SIZE,
                c.TILE_SIZE,
                c.TILE_SIZE,
                fill_color
            )

    def _get_hover_color(self) -> tuple:
        """Get hover highlight color based on tile content. Returns (color, can_interact)"""
        if not self.game.player or self.game.game_over:
            return (QColor(100, 100, 100), False)

        x, y = self.hover_world_x, self.hover_world_y

        # Check if player is hovering over themselves
        if x == self.game.player.x and y == self.game.player.y:
            return (QColor(100, 200, 255), False)  # Blue, but no interaction

        # Check for enemy (attack)
        entity = self.game.get_entity_at(x, y)
        if entity and entity.entity_type == c.ENTITY_ENEMY:
            # Check if adjacent
            if abs(x - self.game.player.x) + abs(y - self.game.player.y) == 1:
                return (QColor(255, 80, 80), True)  # Red - attack
            else:
                return (QColor(255, 150, 80), False)  # Orange - out of range

        # Check for item
        if entity and entity.entity_type == c.ENTITY_ITEM:
            return (QColor(255, 215, 0), True)  # Gold - pickup

        # Check for stairs
        if self.game.dungeon and self.game.dungeon.get_tile(x, y) == c.TILE_STAIRS:
            return (QColor(180, 100, 255), True)  # Purple - descend

        # Check if walkable
        if self.game.dungeon and self.game.dungeon.is_walkable(x, y):
            return (QColor(100, 220, 100), True)  # Green - move

        # Wall or unwalkable
        return (QColor(100, 100, 100), False)  # Gray - blocked

    def _find_path_step(self, start_x: int, start_y: int, goal_x: int, goal_y: int):
        """
        A* pathfinding to find the next step towards goal.
        Returns (dx, dy) for the next move, or (0, 0) if no path.
        """
        from collections import deque
        import heapq

        # Simple heuristic (Manhattan distance)
        def heuristic(x, y):
            return abs(x - goal_x) + abs(y - goal_y)

        # Priority queue: (f_score, counter, x, y)
        counter = 0
        open_set = [(heuristic(start_x, start_y), counter, start_x, start_y)]
        counter += 1

        # Track where we came from
        came_from = {}

        # Cost from start
        g_score = {(start_x, start_y): 0}

        # Visited set
        visited = set()

        while open_set:
            _, _, current_x, current_y = heapq.heappop(open_set)

            # Skip if already visited
            if (current_x, current_y) in visited:
                continue
            visited.add((current_x, current_y))

            # Reached goal
            if current_x == goal_x and current_y == goal_y:
                # Reconstruct path to find first step
                path = []
                cx, cy = current_x, current_y
                while (cx, cy) in came_from:
                    path.append((cx, cy))
                    cx, cy = came_from[(cx, cy)]

                if len(path) >= 1:
                    # Get the first step after start
                    next_x, next_y = path[-1]
                    return (next_x - start_x, next_y - start_y)
                else:
                    return (0, 0)

            # Explore neighbors (4-directional)
            current_g = g_score[(current_x, current_y)]
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = current_x + dx, current_y + dy

                # Check if walkable
                if not self.game.dungeon.is_walkable(nx, ny):
                    continue

                # Skip if occupied by enemy (unless it's the goal - attacking)
                if (nx, ny) != (goal_x, goal_y):
                    entity = self.game.get_entity_at(nx, ny)
                    if entity and entity.entity_type == c.ENTITY_ENEMY:
                        continue

                tentative_g = current_g + 1

                if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                    came_from[(nx, ny)] = (current_x, current_y)
                    g_score[(nx, ny)] = tentative_g
                    f_score = tentative_g + heuristic(nx, ny)
                    heapq.heappush(open_set, (f_score, counter, nx, ny))
                    counter += 1

        # No path found
        return (0, 0)

    def mouseMoveEvent(self, event):
        """Track mouse position for hover effects"""
        # Convert mouse position to world coordinates
        mouse_x = event.pos().x()
        mouse_y = event.pos().y()

        screen_x = mouse_x // c.TILE_SIZE
        screen_y = mouse_y // c.TILE_SIZE

        self.hover_world_x = screen_x + self.game.camera_x
        self.hover_world_y = screen_y + self.game.camera_y

        # Trigger repaint for hover effect
        self.update()

    def mousePressEvent(self, event):
        """Handle mouse clicks for movement and interaction"""
        if self.game.game_over or not self.game.player:
            return

        # Get world coordinates of click
        mouse_x = event.pos().x()
        mouse_y = event.pos().y()

        screen_x = mouse_x // c.TILE_SIZE
        screen_y = mouse_y // c.TILE_SIZE

        world_x = screen_x + self.game.camera_x
        world_y = screen_y + self.game.camera_y

        # Handle targeting mode
        if self.targeting_mode and event.button() == Qt.MouseButton.LeftButton:
            # Use ability at target position
            self.game.use_ability(self.targeting_ability_index, world_x, world_y)
            self.targeting_mode = False
            self.targeting_ability_index = None
            self.update()
            return

        # Cancel targeting with right click
        if self.targeting_mode and event.button() == Qt.MouseButton.RightButton:
            self.targeting_mode = False
            self.targeting_ability_index = None
            self.update()
            return

        # Normal movement/interaction (left click only)
        if event.button() != Qt.MouseButton.LeftButton:
            return

        # Don't do anything if clicking on player
        if world_x == self.game.player.x and world_y == self.game.player.y:
            return

        # Use A* pathfinding to find next step
        dx, dy = self._find_path_step(
            self.game.player.x, self.game.player.y,
            world_x, world_y
        )

        # If pathfinding found a valid move, execute it
        if dx != 0 or dy != 0:
            self.game.player_move(dx, dy)

        # Update display
        self.update()

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
        stats_container, stats_layout = self._create_section_container()
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
        equip_container, equip_layout = self._create_section_container()
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
        abilities_container, abilities_layout = self._create_section_container()
        layout.addWidget(abilities_container)

        self.ability_buttons = []
        for i in range(3):  # Max 3 abilities
            button = AbilityButton(i)
            button.ability_clicked.connect(self._on_ability_clicked)
            self.ability_buttons.append(button)
            abilities_layout.addWidget(button)

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


class MainWindow(QMainWindow):
    """Main game window"""
    def __init__(self):
        super().__init__()
        self.game = Game()

        self.setWindowTitle("Dungeon Delver")
        self.setFixedSize(c.WINDOW_WIDTH, c.WINDOW_HEIGHT)

        # Create stacked widget to switch between screens
        self.stacked_widget = QStackedWidget()

        # Title screen (shown first)
        self.title_screen = TitleScreen()
        self.title_screen.continue_pressed.connect(self.on_title_continue)
        self.stacked_widget.addWidget(self.title_screen)

        # Main menu screen
        self.main_menu = MainMenuScreen()
        self.main_menu.new_game_clicked.connect(self.on_new_game)
        self.main_menu.how_to_play_clicked.connect(self.on_how_to_play)
        self.main_menu.settings_clicked.connect(self.on_settings)
        self.main_menu.quit_clicked.connect(self.close)
        self.stacked_widget.addWidget(self.main_menu)

        # Settings screen
        self.settings_screen = SettingsScreen()
        self.settings_screen.back_clicked.connect(self.on_settings_back)
        self.stacked_widget.addWidget(self.settings_screen)

        # Class selection screen
        self.class_selection = ClassSelectionScreen()
        self.class_selection.class_selected.connect(self.on_class_selected)
        self.class_selection.back_clicked.connect(self.on_class_back)
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

        # Start background music on title screen
        audio = get_audio_manager()
        audio.start_background_music()

    def on_title_continue(self):
        """Handle title screen continue"""
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def on_new_game(self):
        """Handle New Game from main menu"""
        self.stacked_widget.setCurrentWidget(self.class_selection)

    def on_class_back(self):
        """Handle back from class selection"""
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def on_settings(self):
        """Handle Settings from main menu"""
        self.stacked_widget.setCurrentWidget(self.settings_screen)

    def on_settings_back(self):
        """Handle back from settings"""
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def on_how_to_play(self):
        """Show How to Play dialog"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

        dialog = QDialog(self)
        dialog.setWindowTitle("How to Play")
        dialog.setModal(True)
        dialog.setFixedSize(600, 500)
        dialog.setStyleSheet(f"background-color: rgb({c.COLOR_PANEL_BG.red()}, {c.COLOR_PANEL_BG.green()}, {c.COLOR_PANEL_BG.blue()});")

        layout = QVBoxLayout()

        # Title
        title = QLabel("HOW TO PLAY")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(f"color: rgb({c.COLOR_TEXT_LIGHT.red()}, {c.COLOR_TEXT_LIGHT.green()}, {c.COLOR_TEXT_LIGHT.blue()}); padding: 15px;")
        layout.addWidget(title)

        # Instructions
        instructions = """
        <p style='color: rgb(200, 200, 200); font-size: 12pt; line-height: 1.8;'>
        <b>OBJECTIVE:</b><br/>
        Explore procedurally generated dungeons, defeat enemies, collect loot, and descend deeper!<br/><br/>

        <b>CONTROLS:</b><br/>
        • <b>WASD / Arrow Keys</b> - Move your character<br/>
        • <b>Click</b> - Move to location (pathfinding)<br/>
        • <b>Bump into enemies</b> - Attack them<br/>
        • <b>1, 2, 3</b> - Use abilities (class-specific)<br/>
        • <b>R</b> - Restart game<br/>
        • <b>Q</b> - Quit<br/><br/>

        <b>GAMEPLAY:</b><br/>
        • Fight enemies to gain XP and level up<br/>
        • Collect equipment to boost your stats<br/>
        • Find the stairs (purple) to descend to the next level<br/>
        • Health potions restore HP immediately<br/>
        • Abilities have cooldowns (shown in turns)<br/><br/>

        <b>TIPS:</b><br/>
        • Choose your class wisely - each has unique abilities<br/>
        • Higher dungeon levels have better loot but stronger enemies<br/>
        • Equipment rarity affects stat bonuses (Common → Legendary)<br/>
        </p>
        """

        info_label = QLabel(instructions)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.TextFormat.RichText)
        info_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        info_label.setStyleSheet("padding: 10px;")
        layout.addWidget(info_label)

        # Close button
        close_btn = QPushButton("Got it!")
        close_btn.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(100, 100, 255);
                color: rgb(255, 255, 255);
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: rgb(130, 130, 255);
            }
        """)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.setLayout(layout)
        dialog.exec()

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

        # Update game state
        self.game.update(dt)

        # Update animations
        self.game.anim_manager.update(dt)

        # Update display
        self.game_widget.update()
        self.stats_panel.update_stats()

    def keyPressEvent(self, event: QKeyEvent):
        """Handle key presses"""
        key = event.key()

        # ESC to cancel targeting mode
        if key == Qt.Key.Key_Escape:
            if self.game_widget.targeting_mode:
                self.game_widget.targeting_mode = False
                self.game_widget.targeting_ability_index = None
                self.update_display()
                return

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
            # Restart game - go back to main menu
            self.stacked_widget.setCurrentWidget(self.main_menu)
            return
        elif key == Qt.Key.Key_Q:
            # Quit
            self.close()
            return

        if dx != 0 or dy != 0:
            self.game.player_move(dx, dy)
            self.update_display()
