"""Dragon creature control panel."""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel
)
from PyQt6.QtCore import Qt
from .base_creature_panel import BaseCreaturePanel
from ..widgets import ColorButton


class DragonPanel(BaseCreaturePanel):
    """Control panel for dragon creature parameters."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize dragon-specific state variables
        self._dragon_segments = 15
        self._dragon_thickness = 0.3
        self._dragon_taper = 0.6
        self._dragon_head_scale = 3.0
        self._dragon_body_color = (200, 40, 40)  # RGB 0-255
        self._dragon_head_color = (255, 200, 50)  # RGB 0-255
        self._dragon_weave_amplitude = 0.5
        self._dragon_bob_amplitude = 0.3
        self._dragon_anim_speed = 1.5
        self._dragon_num_eyes = 2
        self._dragon_eye_size = 0.15
        self._dragon_eyeball_color = (255, 200, 50)  # RGB 0-255
        self._dragon_pupil_color = (20, 0, 0)  # RGB 0-255

        self._init_ui()

    def _init_ui(self):
        """Initialize the UI layout."""
        layout = QGridLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(0, 0, 0, 0)

        # Column 1: Body Shape
        layout.addWidget(self._create_dragon_body_section(), 0, 0)

        # Column 2: Appearance
        layout.addWidget(self._create_dragon_appearance_section(), 0, 1)

        # Column 3: Animation
        layout.addWidget(self._create_dragon_animation_section(), 0, 2)

        # Row 2: Eyes section (full width, spanning 3 columns)
        layout.addWidget(self._create_dragon_eyes_section(), 1, 0, 1, 3)

        self.setLayout(layout)

    def _create_dragon_body_section(self):
        """Create Dragon Body Shape card."""
        group = self._create_card("DRAGON BODY")
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Number of Segments (5-30)
        layout.addWidget(self._create_label("Body Segments"))
        self.dragon_segments_spin = self._create_spinbox(5, 30, self._dragon_segments, self._on_dragon_segments_changed)
        layout.addWidget(self.dragon_segments_spin)
        layout.addSpacing(8)

        # Segment Thickness (0.1-0.8)
        layout.addWidget(self._create_label("Segment Thickness"))
        self.dragon_thickness_slider = self._create_slider(10, 80, 30, self._on_dragon_thickness_changed)
        layout.addWidget(self.dragon_thickness_slider)
        self.dragon_thickness_label = QLabel("0.30")
        self.dragon_thickness_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dragon_thickness_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.dragon_thickness_label)

        # Taper Factor (0.0-0.9)
        layout.addWidget(self._create_label("Tail Taper"))
        self.dragon_taper_slider = self._create_slider(0, 90, 60, self._on_dragon_taper_changed)
        layout.addWidget(self.dragon_taper_slider)
        self.dragon_taper_label = QLabel("0.60")
        self.dragon_taper_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dragon_taper_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.dragon_taper_label)

        # Head Scale (1.0-3.5)
        layout.addWidget(self._create_label("Head Size"))
        self.dragon_head_scale_slider = self._create_slider(10, 35, 30, self._on_dragon_head_scale_changed)
        layout.addWidget(self.dragon_head_scale_slider)
        self.dragon_head_scale_label = QLabel("3.0x")
        self.dragon_head_scale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dragon_head_scale_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.dragon_head_scale_label)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_dragon_appearance_section(self):
        """Create Dragon Appearance card."""
        group = self._create_card("DRAGON APPEARANCE")
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Body Color (note: ColorButton expects 0-1 range, but we store 0-255)
        layout.addWidget(self._create_label("Body Color"))
        body_color_01 = tuple(c / 255.0 for c in self._dragon_body_color)
        self.dragon_body_color_button = ColorButton(body_color_01)
        self.dragon_body_color_button.colorChanged.connect(self._on_dragon_body_color_changed)
        layout.addWidget(self.dragon_body_color_button)

        # Head Color
        layout.addWidget(self._create_label("Head Color"))
        head_color_01 = tuple(c / 255.0 for c in self._dragon_head_color)
        self.dragon_head_color_button = ColorButton(head_color_01)
        self.dragon_head_color_button.colorChanged.connect(self._on_dragon_head_color_changed)
        layout.addWidget(self.dragon_head_color_button)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_dragon_animation_section(self):
        """Create Dragon Animation card."""
        group = self._create_card("DRAGON ANIMATION")
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Weave Amplitude (0.0-1.0)
        layout.addWidget(self._create_label("Weave Amount"))
        self.dragon_weave_slider = self._create_slider(0, 100, 50, self._on_dragon_weave_changed)
        layout.addWidget(self.dragon_weave_slider)
        self.dragon_weave_label = QLabel("0.50")
        self.dragon_weave_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dragon_weave_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.dragon_weave_label)

        # Bob Amplitude (0.0-1.0)
        layout.addWidget(self._create_label("Bob Amount"))
        self.dragon_bob_slider = self._create_slider(0, 100, 30, self._on_dragon_bob_changed)
        layout.addWidget(self.dragon_bob_slider)
        self.dragon_bob_label = QLabel("0.30")
        self.dragon_bob_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dragon_bob_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.dragon_bob_label)

        # Animation Speed (0.5-5.0)
        layout.addWidget(self._create_label("Animation Speed"))
        self.dragon_anim_speed_slider = self._create_slider(50, 500, 150, self._on_dragon_anim_speed_changed)
        layout.addWidget(self.dragon_anim_speed_slider)
        self.dragon_anim_speed_label = QLabel("1.5x")
        self.dragon_anim_speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dragon_anim_speed_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.dragon_anim_speed_label)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_dragon_eyes_section(self):
        """Create Dragon Eyes card (full width)."""
        group = self._create_card("DRAGON EYES")
        layout = QHBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(15, 15, 15, 15)

        # Number of Eyes
        eyes_layout = QVBoxLayout()
        eyes_layout.addWidget(self._create_label("Number of Eyes"))
        self.dragon_num_eyes_spin = self._create_spinbox(0, 8, self._dragon_num_eyes, self._on_dragon_num_eyes_changed)
        eyes_layout.addWidget(self.dragon_num_eyes_spin)
        layout.addLayout(eyes_layout)

        # Eye Size
        eye_size_layout = QVBoxLayout()
        eye_size_layout.addWidget(self._create_label("Eye Size"))
        self.dragon_eye_size_slider = self._create_slider(5, 30, 15, self._on_dragon_eye_size_changed)
        eye_size_layout.addWidget(self.dragon_eye_size_slider)
        self.dragon_eye_size_label = QLabel("0.15")
        self.dragon_eye_size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dragon_eye_size_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        eye_size_layout.addWidget(self.dragon_eye_size_label)
        layout.addLayout(eye_size_layout)

        # Eyeball Color
        eyeball_color_layout = QVBoxLayout()
        eyeball_color_layout.addWidget(self._create_label("Eyeball Color"))
        eyeball_color_01 = tuple(c / 255.0 for c in self._dragon_eyeball_color)
        self.dragon_eyeball_color_button = ColorButton(eyeball_color_01)
        self.dragon_eyeball_color_button.colorChanged.connect(self._on_dragon_eyeball_color_changed)
        eyeball_color_layout.addWidget(self.dragon_eyeball_color_button)
        layout.addLayout(eyeball_color_layout)

        # Pupil Color
        pupil_color_layout = QVBoxLayout()
        pupil_color_layout.addWidget(self._create_label("Pupil Color"))
        pupil_color_01 = tuple(c / 255.0 for c in self._dragon_pupil_color)
        self.dragon_pupil_color_button = ColorButton(pupil_color_01)
        self.dragon_pupil_color_button.colorChanged.connect(self._on_dragon_pupil_color_changed)
        pupil_color_layout.addWidget(self.dragon_pupil_color_button)
        layout.addLayout(pupil_color_layout)

        group.setLayout(layout)
        return group

    # Event Handlers
    def _on_dragon_segments_changed(self, value):
        self._dragon_segments = value
        self._emit_change()

    def _on_dragon_thickness_changed(self, value):
        self._dragon_thickness = value / 100.0
        self.dragon_thickness_label.setText(f"{self._dragon_thickness:.2f}")
        self._emit_change()

    def _on_dragon_taper_changed(self, value):
        self._dragon_taper = value / 100.0
        self.dragon_taper_label.setText(f"{self._dragon_taper:.2f}")
        self._emit_change()

    def _on_dragon_head_scale_changed(self, value):
        self._dragon_head_scale = value / 10.0
        self.dragon_head_scale_label.setText(f"{self._dragon_head_scale:.1f}x")
        self._emit_change()

    def _on_dragon_body_color_changed(self, color):
        # Convert 0-1 to 0-255
        self._dragon_body_color = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
        self._emit_change()

    def _on_dragon_head_color_changed(self, color):
        # Convert 0-1 to 0-255
        self._dragon_head_color = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
        self._emit_change()

    def _on_dragon_weave_changed(self, value):
        self._dragon_weave_amplitude = value / 100.0
        self.dragon_weave_label.setText(f"{self._dragon_weave_amplitude:.2f}")
        self._emit_change()

    def _on_dragon_bob_changed(self, value):
        self._dragon_bob_amplitude = value / 100.0
        self.dragon_bob_label.setText(f"{self._dragon_bob_amplitude:.2f}")
        self._emit_change()

    def _on_dragon_anim_speed_changed(self, value):
        self._dragon_anim_speed = value / 100.0
        self.dragon_anim_speed_label.setText(f"{self._dragon_anim_speed:.1f}x")
        self._emit_change()

    def _on_dragon_num_eyes_changed(self, value):
        self._dragon_num_eyes = value
        self._emit_change()

    def _on_dragon_eye_size_changed(self, value):
        self._dragon_eye_size = value / 100.0
        self.dragon_eye_size_label.setText(f"{self._dragon_eye_size:.2f}")
        self._emit_change()

    def _on_dragon_eyeball_color_changed(self, color):
        # Convert 0-1 to 0-255
        self._dragon_eyeball_color = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
        self._emit_change()

    def _on_dragon_pupil_color_changed(self, color):
        # Convert 0-1 to 0-255
        self._dragon_pupil_color = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
        self._emit_change()

    def get_state(self):
        """Get current state."""
        return {
            'dragon_segments': self._dragon_segments,
            'dragon_thickness': self._dragon_thickness,
            'dragon_taper': self._dragon_taper,
            'dragon_head_scale': self._dragon_head_scale,
            'dragon_body_color': self._dragon_body_color,
            'dragon_head_color': self._dragon_head_color,
            'dragon_weave_amplitude': self._dragon_weave_amplitude,
            'dragon_bob_amplitude': self._dragon_bob_amplitude,
            'dragon_anim_speed': self._dragon_anim_speed,
            'dragon_num_eyes': self._dragon_num_eyes,
            'dragon_eye_size': self._dragon_eye_size,
            'dragon_eyeball_color': self._dragon_eyeball_color,
            'dragon_pupil_color': self._dragon_pupil_color,
        }

    def set_state(self, state):
        """Restore state."""
        self._updating = True

        # Dragon parameters
        self._dragon_segments = state.get('dragon_segments', 15)
        self._dragon_thickness = state.get('dragon_thickness', 0.3)
        self._dragon_taper = state.get('dragon_taper', 0.6)
        self._dragon_head_scale = state.get('dragon_head_scale', 3.0)
        self._dragon_body_color = state.get('dragon_body_color', (200, 40, 40))
        self._dragon_head_color = state.get('dragon_head_color', (255, 200, 50))
        self._dragon_weave_amplitude = state.get('dragon_weave_amplitude', 0.5)
        self._dragon_bob_amplitude = state.get('dragon_bob_amplitude', 0.3)
        self._dragon_anim_speed = state.get('dragon_anim_speed', 1.5)
        self._dragon_num_eyes = state.get('dragon_num_eyes', 2)
        self._dragon_eye_size = state.get('dragon_eye_size', 0.15)
        self._dragon_eyeball_color = state.get('dragon_eyeball_color', (255, 200, 50))
        self._dragon_pupil_color = state.get('dragon_pupil_color', (20, 0, 0))

        # Update UI
        self.dragon_segments_spin.setValue(self._dragon_segments)
        self.dragon_thickness_slider.setValue(int(self._dragon_thickness * 100))
        self.dragon_taper_slider.setValue(int(self._dragon_taper * 100))
        self.dragon_head_scale_slider.setValue(int(self._dragon_head_scale * 10))

        # Convert 0-255 to 0-1 for color buttons
        body_color_01 = tuple(c / 255.0 for c in self._dragon_body_color)
        self.dragon_body_color_button.set_color(body_color_01)
        head_color_01 = tuple(c / 255.0 for c in self._dragon_head_color)
        self.dragon_head_color_button.set_color(head_color_01)

        self.dragon_weave_slider.setValue(int(self._dragon_weave_amplitude * 100))
        self.dragon_bob_slider.setValue(int(self._dragon_bob_amplitude * 100))
        self.dragon_anim_speed_slider.setValue(int(self._dragon_anim_speed * 100))

        # Eye parameters
        self.dragon_num_eyes_spin.setValue(self._dragon_num_eyes)
        self.dragon_eye_size_slider.setValue(int(self._dragon_eye_size * 100))
        eyeball_color_01 = tuple(c / 255.0 for c in self._dragon_eyeball_color)
        self.dragon_eyeball_color_button.set_color(eyeball_color_01)
        pupil_color_01 = tuple(c / 255.0 for c in self._dragon_pupil_color)
        self.dragon_pupil_color_button.set_color(pupil_color_01)

        self._updating = False
