"""
Modern 3-column control panel with card-based design.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QLabel, QSlider,
    QSpinBox, QComboBox, QPushButton, QColorDialog, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from ..core.constants import PRESETS


class ColorButton(QPushButton):
    """Custom button that opens a color picker."""
    colorChanged = pyqtSignal(tuple)  # Emits RGB tuple (0-1 range)

    def __init__(self, initial_color=(0.6, 0.3, 0.7), parent=None):
        super().__init__(parent)
        self.color = initial_color
        self.setMinimumHeight(45)
        self.setMinimumWidth(100)
        self.clicked.connect(self._pick_color)
        self._update_display()

    def _update_display(self):
        """Update button appearance to show current color."""
        r, g, b = [int(c * 255) for c in self.color]
        self.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 rgb({r}, {g}, {b}),
                                           stop:1 rgb({max(0, r-30)}, {max(0, g-30)}, {max(0, b-30)}));
                border: 2px solid #4a4a4a;
                border-radius: 8px;
                min-height: 45px;
                color: white;
                font-weight: bold;
                font-size: 11pt;
            }}
            QPushButton:hover {{
                border: 2px solid #8b5cf6;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 rgb({min(255, r+20)}, {min(255, g+20)}, {min(255, b+20)}),
                                           stop:1 rgb({r}, {g}, {b}));
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 rgb({max(0, r-40)}, {max(0, g-40)}, {max(0, b-40)}),
                                           stop:1 rgb({max(0, r-20)}, {max(0, g-20)}, {max(0, b-20)}));
            }}
        """)
        self.setText(f"RGB({r}, {g}, {b})")

    def _pick_color(self):
        """Open color picker dialog."""
        r, g, b = [int(c * 255) for c in self.color]
        initial = QColor(r, g, b)
        color = QColorDialog.getColor(initial, self, "Choose Color")

        if color.isValid():
            self.color = (color.red() / 255.0, color.green() / 255.0, color.blue() / 255.0)
            self._update_display()
            self.colorChanged.emit(self.color)

    def set_color(self, rgb_tuple):
        """Set color programmatically."""
        self.color = rgb_tuple
        self._update_display()


class ModernControlPanel(QWidget):
    """Modern 3-column control panel."""

    creature_changed = pyqtSignal()
    creature_type_changed = pyqtSignal(str)  # Emits 'tentacle' or 'blob'
    undo_requested = pyqtSignal()
    redo_requested = pyqtSignal()
    export_requested = pyqtSignal()
    attack_requested = pyqtSignal()
    attack_2_requested = pyqtSignal()

    SPINBOX_STYLE = """
        QSpinBox {
            background-color: #2a2a2a;
            color: #e0e0e0;
            border: 2px solid #4a4a4a;
            border-radius: 6px;
            padding: 5px 10px;
            font-size: 11pt;
            font-weight: bold;
        }
        QSpinBox:hover {
            border: 2px solid #8b5cf6;
            background-color: #323232;
        }
        QSpinBox:focus {
            border: 2px solid #a78bfa;
            background-color: #353535;
        }
        QSpinBox::up-button {
            background-color: #3a3a3a;
            border-radius: 3px;
            border: none;
            width: 24px;
            subcontrol-origin: border;
            subcontrol-position: top right;
        }
        QSpinBox::down-button {
            background-color: #3a3a3a;
            border-radius: 3px;
            border: none;
            width: 24px;
            subcontrol-origin: border;
            subcontrol-position: bottom right;
        }
        QSpinBox::up-button:hover {
            background-color: #8b5cf6;
        }
        QSpinBox::down-button:hover {
            background-color: #8b5cf6;
        }
        QSpinBox::up-arrow {
            width: 0;
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-bottom: 6px solid #e0e0e0;
        }
        QSpinBox::down-arrow {
            width: 0;
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid #e0e0e0;
        }
        QSpinBox::up-arrow:hover {
            border-bottom-color: #ffffff;
        }
        QSpinBox::down-arrow:hover {
            border-top-color: #ffffff;
        }
    """

    COMBOBOX_STYLE = """
        QComboBox {
            background-color: #2a2a2a;
            color: #e0e0e0;
            border: 2px solid #4a4a4a;
            border-radius: 6px;
            padding: 5px 10px;
            padding-right: 30px;
            font-size: 11pt;
            font-weight: bold;
        }
        QComboBox:hover {
            border: 2px solid #8b5cf6;
            background-color: #323232;
        }
        QComboBox:focus {
            border: 2px solid #a78bfa;
            background-color: #353535;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 28px;
            background-color: #3a3a3a;
            border-radius: 3px;
            border: none;
        }
        QComboBox::drop-down:hover {
            background-color: #8b5cf6;
        }
        QComboBox::down-arrow {
            width: 0;
            height: 0;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid #e0e0e0;
        }
        QComboBox::down-arrow:hover {
            border-top-color: #ffffff;
        }
        QComboBox QAbstractItemView {
            background-color: #2a2a2a;
            color: #e0e0e0;
            selection-background-color: #8b5cf6;
            selection-color: #ffffff;
            border: 2px solid #8b5cf6;
        }
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize all state variables
        self._num_tentacles = 2
        self._segments = 12
        self._algorithm = 'bezier'
        self._bezier_control_strength = 0.4
        self._fourier_waves = 3
        self._fourier_amplitude = 0.15
        self._thickness_base = 0.25
        self._taper_factor = 0.6
        self._branch_depth = 0
        self._branch_count = 1

        # New appearance parameters
        self._body_scale = 1.2
        self._tentacle_color = (0.6, 0.3, 0.7)
        self._hue_shift = 0.1

        # New animation parameters
        self._anim_speed = 2.0
        self._wave_amplitude = 0.05
        self._pulse_speed = 1.5
        self._pulse_amount = 0.05

        # Eye parameters
        self._num_eyes = 3
        self._eye_size_min = 0.1
        self._eye_size_max = 0.25
        self._eyeball_color = (1.0, 1.0, 1.0)
        self._pupil_color = (0.0, 0.0, 0.0)

        # Creature type
        self._creature_type = 'tentacle'  # 'tentacle' or 'blob'

        # Blob parameters
        self._blob_branch_depth = 2
        self._blob_branch_count = 2
        self._cube_size_min = 0.3
        self._cube_size_max = 0.8
        self._cube_spacing = 1.2
        self._blob_color = (0.2, 0.8, 0.4)  # Green slime
        self._blob_transparency = 0.7
        self._jiggle_speed = 2.0
        self._blob_pulse_amount = 0.1

        # Polyp parameters
        self._num_spheres = 4
        self._base_sphere_size = 0.8
        self._polyp_color = (0.6, 0.3, 0.7)
        self._curve_intensity = 0.4
        self._polyp_tentacles_per_sphere = 6
        self._polyp_segments = 12

        # Starfish parameters
        self._num_arms = 5
        self._arm_segments = 6
        self._central_body_size = 0.8
        self._arm_base_thickness = 0.4
        self._starfish_color = (0.9, 0.5, 0.3)  # Orange
        self._curl_factor = 0.3
        self._starfish_anim_speed = 1.5
        self._starfish_pulse = 0.06

        self._updating = False
        self._init_ui()

    def _init_ui(self):
        """Initialize UI with tabbed interface."""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create tab widget
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3a3a3a;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1a1a1a, stop:1 #1e1e1e);
                border-radius: 8px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #2d2d2d, stop:1 #252525);
                border: 1px solid #3a3a3a;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                padding: 12px 24px;
                margin-right: 4px;
                color: #a0a0a0;
                font-size: 11pt;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #6366f1, stop:1 #8b5cf6);
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #3a3a3a, stop:1 #323232);
                color: #d0d0d0;
            }
        """)

        # Tab 1: Design
        design_tab = QWidget()
        design_layout = QVBoxLayout()
        design_layout.setSpacing(20)
        design_layout.setContentsMargins(20, 20, 20, 20)

        # Creature Type Selector
        type_selector_layout = QHBoxLayout()
        type_label = QLabel("Creature Type:")
        type_label.setStyleSheet("color: #e5e5e5; font-size: 12pt; font-weight: bold;")
        type_selector_layout.addWidget(type_label)

        self.creature_type_combo = QComboBox()
        self.creature_type_combo.addItems(["Tentacle Creature", "Blob Creature", "Polyp Creature", "Starfish Creature"])
        self.creature_type_combo.setMinimumHeight(40)
        self.creature_type_combo.setStyleSheet(self.COMBOBOX_STYLE)
        self.creature_type_combo.currentTextChanged.connect(self._on_creature_type_changed)
        type_selector_layout.addWidget(self.creature_type_combo)
        type_selector_layout.addStretch()
        design_layout.addLayout(type_selector_layout)

        # Title
        title = QLabel("CREATURE DESIGNER")
        title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                  stop:0 #8b5cf6, stop:0.5 #a78bfa, stop:1 #06b6d4);
            padding: 15px;
            letter-spacing: 2px;
        """)
        design_layout.addWidget(title)

        # ===== TENTACLE CREATURE SECTIONS =====
        self.tentacle_container = QWidget()
        tentacle_layout = QVBoxLayout()
        tentacle_layout.setContentsMargins(0, 0, 0, 0)

        tentacle_grid = QGridLayout()
        tentacle_grid.setSpacing(20)

        # Column 1: Shape & Algorithm
        tentacle_grid.addWidget(self._create_shape_section(), 0, 0)

        # Column 2: Appearance
        tentacle_grid.addWidget(self._create_appearance_section(), 0, 1)

        # Column 3: Branching
        tentacle_grid.addWidget(self._create_branching_section(), 0, 2)

        # Row 2: Eyes section (full width, spanning 3 columns)
        tentacle_grid.addWidget(self._create_eyes_section(), 1, 0, 1, 3)

        tentacle_layout.addLayout(tentacle_grid)
        self.tentacle_container.setLayout(tentacle_layout)

        # ===== BLOB CREATURE SECTIONS =====
        self.blob_container = QWidget()
        blob_layout = QVBoxLayout()
        blob_layout.setContentsMargins(0, 0, 0, 0)

        blob_grid = QGridLayout()
        blob_grid.setSpacing(20)

        # Column 1: Blob Shape
        blob_grid.addWidget(self._create_blob_shape_section(), 0, 0)

        # Column 2: Blob Appearance
        blob_grid.addWidget(self._create_blob_appearance_section(), 0, 1)

        # Column 3: Blob Animation
        blob_grid.addWidget(self._create_blob_animation_section(), 0, 2)

        blob_layout.addLayout(blob_grid)
        self.blob_container.setLayout(blob_layout)
        self.blob_container.setVisible(False)  # Hidden by default

        # ===== POLYP CREATURE SECTIONS =====
        self.polyp_container = QWidget()
        polyp_layout = QVBoxLayout()
        polyp_layout.setContentsMargins(0, 0, 0, 0)

        polyp_grid = QGridLayout()
        polyp_grid.setSpacing(20)

        # Column 1: Spine Shape
        polyp_grid.addWidget(self._create_polyp_spine_section(), 0, 0)

        # Column 2: Tentacles
        polyp_grid.addWidget(self._create_polyp_tentacles_section(), 0, 1)

        # Column 3: Appearance
        polyp_grid.addWidget(self._create_polyp_appearance_section(), 0, 2)

        polyp_layout.addLayout(polyp_grid)
        self.polyp_container.setLayout(polyp_layout)
        self.polyp_container.setVisible(False)  # Hidden by default

        # ===== STARFISH CREATURE SECTIONS =====
        self.starfish_container = QWidget()
        starfish_layout = QVBoxLayout()
        starfish_layout.setContentsMargins(0, 0, 0, 0)

        starfish_grid = QGridLayout()
        starfish_grid.setSpacing(20)

        # Column 1: Arms & Body
        starfish_grid.addWidget(self._create_starfish_arms_section(), 0, 0)

        # Column 2: Appearance
        starfish_grid.addWidget(self._create_starfish_appearance_section(), 0, 1)

        # Column 3: Animation
        starfish_grid.addWidget(self._create_starfish_animation_section(), 0, 2)

        starfish_layout.addLayout(starfish_grid)
        self.starfish_container.setLayout(starfish_layout)
        self.starfish_container.setVisible(False)  # Hidden by default

        # Add all containers to design layout
        design_layout.addWidget(self.tentacle_container)
        design_layout.addWidget(self.blob_container)
        design_layout.addWidget(self.polyp_container)
        design_layout.addWidget(self.starfish_container)

        design_layout.addStretch()
        design_tab.setLayout(design_layout)

        # Tab 2: Animation
        animation_tab = QWidget()
        animation_layout = QVBoxLayout()
        animation_layout.setSpacing(20)
        animation_layout.setContentsMargins(20, 20, 20, 20)

        # Animation title
        anim_title = QLabel("ANIMATION CONTROLS")
        anim_title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        anim_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        anim_title.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                  stop:0 #8b5cf6, stop:0.5 #a78bfa, stop:1 #06b6d4);
            padding: 15px;
            letter-spacing: 2px;
        """)
        animation_layout.addWidget(anim_title)

        # Full-width Animation section
        animation_layout.addWidget(self._create_animation_section())

        # Full-width Actions
        animation_layout.addWidget(self._create_actions_section())

        animation_layout.addStretch()
        animation_tab.setLayout(animation_layout)

        # Add tabs to widget
        tab_widget.addTab(design_tab, "Design")
        tab_widget.addTab(animation_tab, "Animation")

        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

    def _create_shape_section(self):
        """Create Shape & Algorithm card."""
        group = QGroupBox("SHAPE & ALGORITHM")
        group.setMinimumWidth(280)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Tentacles
        layout.addWidget(self._create_label("Tentacles"))
        self.tentacles_spin = QSpinBox()
        self.tentacles_spin.setRange(1, 12)
        self.tentacles_spin.setValue(self._num_tentacles)
        self.tentacles_spin.setMinimumHeight(35)
        self.tentacles_spin.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        self.tentacles_spin.setStyleSheet(self.SPINBOX_STYLE)
        self.tentacles_spin.valueChanged.connect(self._on_tentacles_changed)
        layout.addWidget(self.tentacles_spin)
        layout.addSpacing(8)

        # Segments
        layout.addWidget(self._create_label("Segments"))
        self.segments_spin = QSpinBox()
        self.segments_spin.setRange(5, 20)
        self.segments_spin.setValue(self._segments)
        self.segments_spin.setMinimumHeight(35)
        self.segments_spin.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        self.segments_spin.setStyleSheet(self.SPINBOX_STYLE)
        self.segments_spin.valueChanged.connect(self._on_segments_changed)
        layout.addWidget(self.segments_spin)
        layout.addSpacing(8)

        # Algorithm
        layout.addWidget(self._create_label("Algorithm"))
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(["Bezier", "Fourier"])
        self.algorithm_combo.setMinimumHeight(35)
        self.algorithm_combo.setStyleSheet(self.COMBOBOX_STYLE)
        self.algorithm_combo.currentTextChanged.connect(self._on_algorithm_changed)
        layout.addWidget(self.algorithm_combo)
        layout.addSpacing(8)

        # Bezier controls
        self.bezier_widget = QWidget()
        bezier_layout = QVBoxLayout()
        bezier_layout.setContentsMargins(0, 10, 0, 0)
        bezier_layout.addWidget(self._create_label("Control Strength"))
        self.bezier_slider = QSlider(Qt.Orientation.Horizontal)
        self.bezier_slider.setRange(10, 80)
        self.bezier_slider.setValue(40)
        self.bezier_slider.setMinimumHeight(30)
        self.bezier_slider.valueChanged.connect(self._on_bezier_changed)
        bezier_layout.addWidget(self.bezier_slider)
        self.bezier_value_label = QLabel("0.40")
        self.bezier_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bezier_value_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        bezier_layout.addWidget(self.bezier_value_label)
        self.bezier_widget.setLayout(bezier_layout)
        layout.addWidget(self.bezier_widget)

        # Fourier controls
        self.fourier_widget = QWidget()
        fourier_layout = QVBoxLayout()
        fourier_layout.setContentsMargins(0, 10, 0, 0)
        fourier_layout.addWidget(self._create_label("Wave Count"))
        self.fourier_waves_spin = QSpinBox()
        self.fourier_waves_spin.setRange(1, 7)
        self.fourier_waves_spin.setValue(3)
        self.fourier_waves_spin.setMinimumHeight(35)
        self.fourier_waves_spin.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        self.fourier_waves_spin.setStyleSheet(self.SPINBOX_STYLE)
        self.fourier_waves_spin.valueChanged.connect(self._on_fourier_changed)
        fourier_layout.addWidget(self.fourier_waves_spin)
        fourier_layout.addSpacing(8)
        fourier_layout.addWidget(self._create_label("Amplitude"))
        self.fourier_amp_slider = QSlider(Qt.Orientation.Horizontal)
        self.fourier_amp_slider.setRange(5, 40)
        self.fourier_amp_slider.setValue(15)
        self.fourier_amp_slider.setMinimumHeight(30)
        self.fourier_amp_slider.valueChanged.connect(self._on_fourier_changed)
        fourier_layout.addWidget(self.fourier_amp_slider)
        self.fourier_amp_label = QLabel("0.15")
        self.fourier_amp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.fourier_amp_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        fourier_layout.addWidget(self.fourier_amp_label)
        self.fourier_widget.setLayout(fourier_layout)
        self.fourier_widget.setVisible(False)
        layout.addWidget(self.fourier_widget)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_appearance_section(self):
        """Create Appearance card."""
        group = QGroupBox("APPEARANCE")
        group.setMinimumWidth(280)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Tentacle Color
        layout.addWidget(self._create_label("Base Color"))
        self.color_button = ColorButton(self._tentacle_color)
        self.color_button.colorChanged.connect(self._on_color_changed)
        layout.addWidget(self.color_button)

        # Hue Shift
        layout.addWidget(self._create_label("Color Variation"))
        self.hue_slider = QSlider(Qt.Orientation.Horizontal)
        self.hue_slider.setRange(0, 30)
        self.hue_slider.setValue(int(self._hue_shift * 100))
        self.hue_slider.setMinimumHeight(30)
        self.hue_slider.valueChanged.connect(self._on_hue_changed)
        layout.addWidget(self.hue_slider)
        self.hue_label = QLabel("0.10")
        self.hue_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hue_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.hue_label)

        # Thickness
        layout.addWidget(self._create_label("Base Thickness"))
        self.thickness_slider = QSlider(Qt.Orientation.Horizontal)
        self.thickness_slider.setRange(10, 50)
        self.thickness_slider.setValue(25)
        self.thickness_slider.setMinimumHeight(30)
        self.thickness_slider.valueChanged.connect(self._on_thickness_changed)
        layout.addWidget(self.thickness_slider)
        self.thickness_label = QLabel("0.25")
        self.thickness_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thickness_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.thickness_label)

        # Taper
        layout.addWidget(self._create_label("Taper"))
        self.taper_slider = QSlider(Qt.Orientation.Horizontal)
        self.taper_slider.setRange(0, 100)
        self.taper_slider.setValue(60)
        self.taper_slider.setMinimumHeight(30)
        self.taper_slider.valueChanged.connect(self._on_taper_changed)
        layout.addWidget(self.taper_slider)
        self.taper_label = QLabel("0.60")
        self.taper_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.taper_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.taper_label)

        # Body Scale
        layout.addWidget(self._create_label("Body Size"))
        self.body_scale_slider = QSlider(Qt.Orientation.Horizontal)
        self.body_scale_slider.setRange(50, 200)
        self.body_scale_slider.setValue(120)
        self.body_scale_slider.setMinimumHeight(30)
        self.body_scale_slider.valueChanged.connect(self._on_body_scale_changed)
        layout.addWidget(self.body_scale_slider)
        self.body_scale_label = QLabel("1.20")
        self.body_scale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body_scale_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.body_scale_label)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_branching_section(self):
        """Create Branching card."""
        group = QGroupBox("BRANCHING")
        group.setMinimumWidth(280)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Depth
        layout.addWidget(self._create_label("Depth"))
        self.branch_depth_spin = QSpinBox()
        self.branch_depth_spin.setRange(0, 3)
        self.branch_depth_spin.setValue(self._branch_depth)
        self.branch_depth_spin.setMinimumHeight(35)
        self.branch_depth_spin.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        self.branch_depth_spin.setStyleSheet(self.SPINBOX_STYLE)
        self.branch_depth_spin.valueChanged.connect(self._on_branching_changed)
        layout.addWidget(self.branch_depth_spin)
        layout.addSpacing(8)

        # Count
        layout.addWidget(self._create_label("Count Per Level"))
        self.branch_count_spin = QSpinBox()
        self.branch_count_spin.setRange(1, 3)
        self.branch_count_spin.setValue(self._branch_count)
        self.branch_count_spin.setMinimumHeight(35)
        self.branch_count_spin.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        self.branch_count_spin.setStyleSheet(self.SPINBOX_STYLE)
        self.branch_count_spin.valueChanged.connect(self._on_branching_changed)
        layout.addWidget(self.branch_count_spin)
        layout.addSpacing(8)

        # Info
        self.branch_info_label = QLabel("Total: ~24 segments")
        self.branch_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.branch_info_label.setStyleSheet("color: #06b6d4; font-size: 11pt; font-weight: bold; padding: 12px; background-color: #164e63; border-radius: 8px; margin-top: 10px; border: 1px solid #0891b2;")
        layout.addWidget(self.branch_info_label)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_eyes_section(self):
        """Create Eyes card (full width)."""
        group = QGroupBox("EYES")
        layout = QHBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(15, 15, 15, 15)

        # Num Eyes
        eyes_layout = QVBoxLayout()
        eyes_layout.addWidget(self._create_label("Number of Eyes"))
        self.num_eyes_spin = QSpinBox()
        self.num_eyes_spin.setRange(0, 12)
        self.num_eyes_spin.setValue(self._num_eyes)
        self.num_eyes_spin.setMinimumHeight(35)
        self.num_eyes_spin.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        self.num_eyes_spin.setStyleSheet(self.SPINBOX_STYLE)
        self.num_eyes_spin.valueChanged.connect(self._on_num_eyes_changed)
        eyes_layout.addWidget(self.num_eyes_spin)
        layout.addLayout(eyes_layout)

        # Min Eye Size
        min_size_layout = QVBoxLayout()
        min_size_layout.addWidget(self._create_label("Min Size"))
        self.eye_size_min_slider = QSlider(Qt.Orientation.Horizontal)
        self.eye_size_min_slider.setRange(5, 50)
        self.eye_size_min_slider.setValue(10)
        self.eye_size_min_slider.setMinimumHeight(30)
        self.eye_size_min_slider.valueChanged.connect(self._on_eye_size_changed)
        min_size_layout.addWidget(self.eye_size_min_slider)
        self.eye_size_min_label = QLabel("0.10")
        self.eye_size_min_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.eye_size_min_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        min_size_layout.addWidget(self.eye_size_min_label)
        layout.addLayout(min_size_layout)

        # Max Eye Size
        max_size_layout = QVBoxLayout()
        max_size_layout.addWidget(self._create_label("Max Size"))
        self.eye_size_max_slider = QSlider(Qt.Orientation.Horizontal)
        self.eye_size_max_slider.setRange(5, 50)
        self.eye_size_max_slider.setValue(25)
        self.eye_size_max_slider.setMinimumHeight(30)
        self.eye_size_max_slider.valueChanged.connect(self._on_eye_size_changed)
        max_size_layout.addWidget(self.eye_size_max_slider)
        self.eye_size_max_label = QLabel("0.25")
        self.eye_size_max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.eye_size_max_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        max_size_layout.addWidget(self.eye_size_max_label)
        layout.addLayout(max_size_layout)

        # Eyeball Color
        eyeball_color_layout = QVBoxLayout()
        eyeball_color_layout.addWidget(self._create_label("Eyeball Color"))
        self.eyeball_color_button = ColorButton(self._eyeball_color)
        self.eyeball_color_button.colorChanged.connect(self._on_eyeball_color_changed)
        eyeball_color_layout.addWidget(self.eyeball_color_button)
        layout.addLayout(eyeball_color_layout)

        # Pupil Color
        pupil_color_layout = QVBoxLayout()
        pupil_color_layout.addWidget(self._create_label("Pupil Color"))
        self.pupil_color_button = ColorButton(self._pupil_color)
        self.pupil_color_button.colorChanged.connect(self._on_pupil_color_changed)
        pupil_color_layout.addWidget(self.pupil_color_button)
        layout.addLayout(pupil_color_layout)

        group.setLayout(layout)
        return group

    def _create_animation_section(self):
        """Create Animation card (full width)."""
        group = QGroupBox("ANIMATION")
        layout = QHBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(15, 15, 15, 15)

        # Speed
        speed_layout = QVBoxLayout()
        speed_layout.addWidget(self._create_label("Wave Speed"))
        self.anim_speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.anim_speed_slider.setRange(50, 500)
        self.anim_speed_slider.setValue(200)
        self.anim_speed_slider.setMinimumHeight(30)
        self.anim_speed_slider.valueChanged.connect(self._on_anim_speed_changed)
        speed_layout.addWidget(self.anim_speed_slider)
        self.anim_speed_label = QLabel("2.0x")
        self.anim_speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.anim_speed_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        speed_layout.addWidget(self.anim_speed_label)
        layout.addLayout(speed_layout)

        # Wave Amplitude
        wave_layout = QVBoxLayout()
        wave_layout.addWidget(self._create_label("Wave Intensity"))
        self.wave_amp_slider = QSlider(Qt.Orientation.Horizontal)
        self.wave_amp_slider.setRange(0, 20)
        self.wave_amp_slider.setValue(5)
        self.wave_amp_slider.setMinimumHeight(30)
        self.wave_amp_slider.valueChanged.connect(self._on_wave_amp_changed)
        wave_layout.addWidget(self.wave_amp_slider)
        self.wave_amp_label = QLabel("0.05")
        self.wave_amp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.wave_amp_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        wave_layout.addWidget(self.wave_amp_label)
        layout.addLayout(wave_layout)

        # Pulse Speed
        pulse_speed_layout = QVBoxLayout()
        pulse_speed_layout.addWidget(self._create_label("Pulse Speed"))
        self.pulse_speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.pulse_speed_slider.setRange(50, 300)
        self.pulse_speed_slider.setValue(150)
        self.pulse_speed_slider.setMinimumHeight(30)
        self.pulse_speed_slider.valueChanged.connect(self._on_pulse_speed_changed)
        pulse_speed_layout.addWidget(self.pulse_speed_slider)
        self.pulse_speed_label = QLabel("1.5x")
        self.pulse_speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pulse_speed_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        pulse_speed_layout.addWidget(self.pulse_speed_label)
        layout.addLayout(pulse_speed_layout)

        # Pulse Amount
        pulse_amt_layout = QVBoxLayout()
        pulse_amt_layout.addWidget(self._create_label("Pulse Amount"))
        self.pulse_amt_slider = QSlider(Qt.Orientation.Horizontal)
        self.pulse_amt_slider.setRange(0, 15)
        self.pulse_amt_slider.setValue(5)
        self.pulse_amt_slider.setMinimumHeight(30)
        self.pulse_amt_slider.valueChanged.connect(self._on_pulse_amt_changed)
        pulse_amt_layout.addWidget(self.pulse_amt_slider)
        self.pulse_amt_label = QLabel("0.05")
        self.pulse_amt_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pulse_amt_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        pulse_amt_layout.addWidget(self.pulse_amt_label)
        layout.addLayout(pulse_amt_layout)

        group.setLayout(layout)
        return group

    def _create_actions_section(self):
        """Create Presets & Actions (full width)."""
        group = QGroupBox("PRESETS & ACTIONS")
        layout = QHBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Presets
        for name, algo, params in PRESETS:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, a=algo, p=params: self._load_preset(a, p))
            layout.addWidget(btn)

        layout.addStretch()

        # Attack 1 button (prominent)
        self.attack_btn = QPushButton("⚡ ATTACK 1 ⚡")
        self.attack_btn.setMinimumHeight(55)
        self.attack_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #dc2626, stop:1 #ea580c);
                border: 2px solid #f97316;
                font-weight: bold;
                font-size: 14pt;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #ef4444, stop:1 #f97316);
                border: 2px solid #fb923c;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #b91c1c, stop:1 #c2410c);
                border: 2px solid #ea580c;
            }
        """)
        self.attack_btn.clicked.connect(self.attack_requested.emit)
        layout.addWidget(self.attack_btn)

        # Attack 2 button (subtle slash - orange theme)
        self.attack_2_btn = QPushButton("⚔ ATTACK 2 ⚔")
        self.attack_2_btn.setMinimumHeight(55)
        self.attack_2_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #ea580c, stop:1 #f59e0b);
                border: 2px solid #fb923c;
                font-weight: bold;
                font-size: 14pt;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #f97316, stop:1 #fbbf24);
                border: 2px solid #fcd34d;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #c2410c, stop:1 #d97706);
                border: 2px solid #f97316;
            }
        """)
        self.attack_2_btn.clicked.connect(self.attack_2_requested.emit)
        layout.addWidget(self.attack_2_btn)

        # Actions
        self.undo_btn = QPushButton("Undo")
        self.undo_btn.clicked.connect(self.undo_requested.emit)
        self.undo_btn.setEnabled(False)
        layout.addWidget(self.undo_btn)

        self.redo_btn = QPushButton("Redo")
        self.redo_btn.clicked.connect(self.redo_requested.emit)
        self.redo_btn.setEnabled(False)
        layout.addWidget(self.redo_btn)

        self.export_btn = QPushButton("Export JSON")
        self.export_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #10b981, stop:1 #059669);
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #34d399, stop:1 #10b981);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #059669, stop:1 #047857);
            }
        """)
        self.export_btn.clicked.connect(self.export_requested.emit)
        layout.addWidget(self.export_btn)

        group.setLayout(layout)
        return group

    def _create_label(self, text):
        """Create a styled label."""
        label = QLabel(text)
        label.setStyleSheet("color: #d0d0d0; font-size: 9pt; font-weight: 500; padding: 2px 0px;")
        label.setMinimumWidth(100)
        label.setWordWrap(True)
        return label

    # ===== BLOB CREATURE SECTIONS =====

    def _create_blob_shape_section(self):
        """Create Blob Shape card with Fibonacci branching controls."""
        group = QGroupBox("BLOB SHAPE")
        group.setMinimumWidth(280)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Branch Depth
        layout.addWidget(self._create_label("Branch Depth"))
        self.blob_branch_depth_spin = QSpinBox()
        self.blob_branch_depth_spin.setRange(0, 3)
        self.blob_branch_depth_spin.setValue(self._blob_branch_depth)
        self.blob_branch_depth_spin.setMinimumHeight(35)
        self.blob_branch_depth_spin.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        self.blob_branch_depth_spin.setStyleSheet(self.SPINBOX_STYLE)
        self.blob_branch_depth_spin.valueChanged.connect(self._on_blob_branching_changed)
        layout.addWidget(self.blob_branch_depth_spin)
        layout.addSpacing(8)

        # Branch Count
        layout.addWidget(self._create_label("Branches Per Level"))
        self.blob_branch_count_spin = QSpinBox()
        self.blob_branch_count_spin.setRange(1, 3)
        self.blob_branch_count_spin.setValue(self._blob_branch_count)
        self.blob_branch_count_spin.setMinimumHeight(35)
        self.blob_branch_count_spin.setButtonSymbols(QSpinBox.ButtonSymbols.UpDownArrows)
        self.blob_branch_count_spin.setStyleSheet(self.SPINBOX_STYLE)
        self.blob_branch_count_spin.valueChanged.connect(self._on_blob_branching_changed)
        layout.addWidget(self.blob_branch_count_spin)
        layout.addSpacing(8)

        # Branch Info Label (shows total cube count)
        self.blob_branch_info_label = QLabel("Total: ~7 cubes")
        self.blob_branch_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blob_branch_info_label.setStyleSheet("color: #06b6d4; font-size: 11pt; font-weight: bold; padding: 12px; background-color: #164e63; border-radius: 8px; margin-top: 10px; border: 1px solid #0891b2;")
        layout.addWidget(self.blob_branch_info_label)
        layout.addSpacing(8)

        # Cube Spacing
        layout.addWidget(self._create_label("Cube Spacing"))
        self.cube_spacing_slider = QSlider(Qt.Orientation.Horizontal)
        self.cube_spacing_slider.setRange(50, 250)  # 0.5 to 2.5
        self.cube_spacing_slider.setValue(120)  # 1.2 default
        self.cube_spacing_slider.setMinimumHeight(30)
        self.cube_spacing_slider.valueChanged.connect(self._on_cube_spacing_changed)
        layout.addWidget(self.cube_spacing_slider)
        self.cube_spacing_label = QLabel("1.20")
        self.cube_spacing_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cube_spacing_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.cube_spacing_label)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_blob_appearance_section(self):
        """Create Blob Appearance card."""
        group = QGroupBox("BLOB APPEARANCE")
        group.setMinimumWidth(280)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Blob Color
        layout.addWidget(self._create_label("Blob Color"))
        self.blob_color_button = ColorButton(self._blob_color)
        self.blob_color_button.colorChanged.connect(self._on_blob_color_changed)
        layout.addWidget(self.blob_color_button)

        # Transparency
        layout.addWidget(self._create_label("Transparency"))
        self.blob_transparency_slider = QSlider(Qt.Orientation.Horizontal)
        self.blob_transparency_slider.setRange(10, 95)  # 10-95%
        self.blob_transparency_slider.setValue(70)  # 70% default
        self.blob_transparency_slider.setMinimumHeight(30)
        self.blob_transparency_slider.valueChanged.connect(self._on_blob_transparency_changed)
        layout.addWidget(self.blob_transparency_slider)
        self.blob_transparency_label = QLabel("70%")
        self.blob_transparency_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blob_transparency_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.blob_transparency_label)

        # Cube Size Min
        layout.addWidget(self._create_label("Min Cube Size"))
        self.cube_size_min_slider = QSlider(Qt.Orientation.Horizontal)
        self.cube_size_min_slider.setRange(10, 150)  # 0.1 to 1.5
        self.cube_size_min_slider.setValue(30)  # 0.3 default
        self.cube_size_min_slider.setMinimumHeight(30)
        self.cube_size_min_slider.valueChanged.connect(self._on_cube_size_changed)
        layout.addWidget(self.cube_size_min_slider)
        self.cube_size_min_label = QLabel("0.30")
        self.cube_size_min_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cube_size_min_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.cube_size_min_label)

        # Cube Size Max
        layout.addWidget(self._create_label("Max Cube Size"))
        self.cube_size_max_slider = QSlider(Qt.Orientation.Horizontal)
        self.cube_size_max_slider.setRange(10, 150)  # 0.1 to 1.5
        self.cube_size_max_slider.setValue(80)  # 0.8 default
        self.cube_size_max_slider.setMinimumHeight(30)
        self.cube_size_max_slider.valueChanged.connect(self._on_cube_size_changed)
        layout.addWidget(self.cube_size_max_slider)
        self.cube_size_max_label = QLabel("0.80")
        self.cube_size_max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cube_size_max_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.cube_size_max_label)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_blob_animation_section(self):
        """Create Blob Animation card."""
        group = QGroupBox("BLOB ANIMATION")
        group.setMinimumWidth(280)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Jiggle Speed
        layout.addWidget(self._create_label("Jiggle Speed"))
        self.jiggle_speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.jiggle_speed_slider.setRange(50, 500)  # 0.5 to 5.0
        self.jiggle_speed_slider.setValue(200)  # 2.0 default
        self.jiggle_speed_slider.setMinimumHeight(30)
        self.jiggle_speed_slider.valueChanged.connect(self._on_jiggle_speed_changed)
        layout.addWidget(self.jiggle_speed_slider)
        self.jiggle_speed_label = QLabel("2.0x")
        self.jiggle_speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.jiggle_speed_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.jiggle_speed_label)

        # Pulse Amount
        layout.addWidget(self._create_label("Pulse Amount"))
        self.blob_pulse_slider = QSlider(Qt.Orientation.Horizontal)
        self.blob_pulse_slider.setRange(0, 30)  # 0 to 0.3
        self.blob_pulse_slider.setValue(10)  # 0.1 default
        self.blob_pulse_slider.setMinimumHeight(30)
        self.blob_pulse_slider.valueChanged.connect(self._on_blob_pulse_changed)
        layout.addWidget(self.blob_pulse_slider)
        self.blob_pulse_label = QLabel("0.10")
        self.blob_pulse_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blob_pulse_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.blob_pulse_label)

        layout.addStretch()
        group.setLayout(layout)
        return group

    # ===== POLYP CREATURE SECTIONS =====

    def _create_polyp_spine_section(self):
        """Create Polyp Spine Shape card."""
        group = QGroupBox("SPINE SHAPE")
        group.setMinimumWidth(280)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Number of Spheres (3-5)
        layout.addWidget(self._create_label("Spheres in Spine"))
        self.num_spheres_spin = QSpinBox()
        self.num_spheres_spin.setRange(3, 5)
        self.num_spheres_spin.setValue(self._num_spheres)
        self.num_spheres_spin.setMinimumHeight(35)
        self.num_spheres_spin.setStyleSheet(self.SPINBOX_STYLE)
        self.num_spheres_spin.valueChanged.connect(self._on_num_spheres_changed)
        layout.addWidget(self.num_spheres_spin)
        layout.addSpacing(8)

        # Base Sphere Size (0.4-1.5)
        layout.addWidget(self._create_label("Root Sphere Size"))
        self.base_sphere_slider = QSlider(Qt.Orientation.Horizontal)
        self.base_sphere_slider.setRange(40, 150)  # 0.4 to 1.5
        self.base_sphere_slider.setValue(80)  # 0.8 default
        self.base_sphere_slider.setMinimumHeight(30)
        self.base_sphere_slider.valueChanged.connect(self._on_base_sphere_changed)
        layout.addWidget(self.base_sphere_slider)
        self.base_sphere_label = QLabel("0.80")
        self.base_sphere_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.base_sphere_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.base_sphere_label)

        # Curve Intensity (0-1)
        layout.addWidget(self._create_label("Spine Curve Amount"))
        self.curve_intensity_slider = QSlider(Qt.Orientation.Horizontal)
        self.curve_intensity_slider.setRange(0, 100)  # 0 to 1.0
        self.curve_intensity_slider.setValue(40)  # 0.4 default
        self.curve_intensity_slider.setMinimumHeight(30)
        self.curve_intensity_slider.valueChanged.connect(self._on_curve_intensity_changed)
        layout.addWidget(self.curve_intensity_slider)
        self.curve_intensity_label = QLabel("0.40")
        self.curve_intensity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.curve_intensity_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.curve_intensity_label)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_polyp_tentacles_section(self):
        """Create Polyp Tentacles card."""
        group = QGroupBox("TENTACLES")
        group.setMinimumWidth(280)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Tentacles per Sphere (3-12)
        layout.addWidget(self._create_label("Tentacles per Sphere"))
        self.polyp_tentacles_spin = QSpinBox()
        self.polyp_tentacles_spin.setRange(3, 12)
        self.polyp_tentacles_spin.setValue(self._polyp_tentacles_per_sphere)
        self.polyp_tentacles_spin.setMinimumHeight(35)
        self.polyp_tentacles_spin.setStyleSheet(self.SPINBOX_STYLE)
        self.polyp_tentacles_spin.valueChanged.connect(self._on_polyp_tentacles_changed)
        layout.addWidget(self.polyp_tentacles_spin)
        layout.addSpacing(8)

        # Tentacle Segments (5-20)
        layout.addWidget(self._create_label("Tentacle Length (Segments)"))
        self.polyp_segments_spin = QSpinBox()
        self.polyp_segments_spin.setRange(5, 20)
        self.polyp_segments_spin.setValue(self._polyp_segments)
        self.polyp_segments_spin.setMinimumHeight(35)
        self.polyp_segments_spin.setStyleSheet(self.SPINBOX_STYLE)
        self.polyp_segments_spin.valueChanged.connect(self._on_polyp_segments_changed)
        layout.addWidget(self.polyp_segments_spin)
        layout.addSpacing(8)

        # Info label
        self.polyp_info_label = QLabel("More segments = longer tentacles")
        self.polyp_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.polyp_info_label.setStyleSheet("color: #06b6d4; font-size: 10pt; font-style: italic; padding: 8px; background-color: #164e63; border-radius: 8px; margin-top: 10px; border: 1px solid #0891b2;")
        layout.addWidget(self.polyp_info_label)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_polyp_appearance_section(self):
        """Create Polyp Appearance card."""
        group = QGroupBox("APPEARANCE")
        group.setMinimumWidth(280)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Spine Color
        layout.addWidget(self._create_label("Spine & Tentacle Color"))
        self.polyp_color_button = ColorButton(self._polyp_color)
        self.polyp_color_button.colorChanged.connect(self._on_polyp_color_changed)
        layout.addWidget(self.polyp_color_button)

        layout.addStretch()
        group.setLayout(layout)
        return group

    # ===== STARFISH CREATURE SECTIONS =====

    def _create_starfish_arms_section(self):
        """Create Starfish Arms & Body card."""
        group = QGroupBox("ARMS & BODY")
        group.setMinimumWidth(280)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Number of Arms (5-8)
        layout.addWidget(self._create_label("Number of Arms"))
        self.num_arms_spin = QSpinBox()
        self.num_arms_spin.setRange(5, 8)
        self.num_arms_spin.setValue(self._num_arms)
        self.num_arms_spin.setMinimumHeight(35)
        self.num_arms_spin.setStyleSheet(self.SPINBOX_STYLE)
        self.num_arms_spin.valueChanged.connect(self._on_num_arms_changed)
        layout.addWidget(self.num_arms_spin)
        layout.addSpacing(8)

        # Arm Segments (4-10)
        layout.addWidget(self._create_label("Segments Per Arm"))
        self.arm_segments_spin = QSpinBox()
        self.arm_segments_spin.setRange(4, 10)
        self.arm_segments_spin.setValue(self._arm_segments)
        self.arm_segments_spin.setMinimumHeight(35)
        self.arm_segments_spin.setStyleSheet(self.SPINBOX_STYLE)
        self.arm_segments_spin.valueChanged.connect(self._on_arm_segments_changed)
        layout.addWidget(self.arm_segments_spin)
        layout.addSpacing(8)

        # Central Body Size (0.4-1.5)
        layout.addWidget(self._create_label("Central Body Size"))
        self.central_body_slider = QSlider(Qt.Orientation.Horizontal)
        self.central_body_slider.setRange(40, 150)  # 0.4 to 1.5
        self.central_body_slider.setValue(80)  # 0.8 default
        self.central_body_slider.setMinimumHeight(30)
        self.central_body_slider.valueChanged.connect(self._on_central_body_changed)
        layout.addWidget(self.central_body_slider)
        self.central_body_label = QLabel("0.80")
        self.central_body_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.central_body_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.central_body_label)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_starfish_appearance_section(self):
        """Create Starfish Appearance card."""
        group = QGroupBox("APPEARANCE")
        group.setMinimumWidth(280)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Starfish Color
        layout.addWidget(self._create_label("Starfish Color"))
        self.starfish_color_button = ColorButton(self._starfish_color)
        self.starfish_color_button.colorChanged.connect(self._on_starfish_color_changed)
        layout.addWidget(self.starfish_color_button)

        # Arm Base Thickness (0.2-0.6)
        layout.addWidget(self._create_label("Arm Thickness"))
        self.arm_thickness_slider = QSlider(Qt.Orientation.Horizontal)
        self.arm_thickness_slider.setRange(20, 60)  # 0.2 to 0.6
        self.arm_thickness_slider.setValue(40)  # 0.4 default
        self.arm_thickness_slider.setMinimumHeight(30)
        self.arm_thickness_slider.valueChanged.connect(self._on_arm_thickness_changed)
        layout.addWidget(self.arm_thickness_slider)
        self.arm_thickness_label = QLabel("0.40")
        self.arm_thickness_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.arm_thickness_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.arm_thickness_label)

        # Curl Factor (0-0.8)
        layout.addWidget(self._create_label("Arm Curl Amount"))
        self.curl_factor_slider = QSlider(Qt.Orientation.Horizontal)
        self.curl_factor_slider.setRange(0, 80)  # 0 to 0.8
        self.curl_factor_slider.setValue(30)  # 0.3 default
        self.curl_factor_slider.setMinimumHeight(30)
        self.curl_factor_slider.valueChanged.connect(self._on_curl_factor_changed)
        layout.addWidget(self.curl_factor_slider)
        self.curl_factor_label = QLabel("0.30")
        self.curl_factor_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.curl_factor_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.curl_factor_label)

        # Info label
        self.starfish_info_label = QLabel("Higher curl = arms bend downward more")
        self.starfish_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.starfish_info_label.setStyleSheet("color: #06b6d4; font-size: 10pt; font-style: italic; padding: 8px; background-color: #164e63; border-radius: 8px; margin-top: 10px; border: 1px solid #0891b2;")
        layout.addWidget(self.starfish_info_label)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def _create_starfish_animation_section(self):
        """Create Starfish Animation card."""
        group = QGroupBox("ANIMATION")
        group.setMinimumWidth(280)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # Animation Speed
        layout.addWidget(self._create_label("Animation Speed"))
        self.starfish_anim_speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.starfish_anim_speed_slider.setRange(50, 500)  # 0.5 to 5.0
        self.starfish_anim_speed_slider.setValue(150)  # 1.5 default
        self.starfish_anim_speed_slider.setMinimumHeight(30)
        self.starfish_anim_speed_slider.valueChanged.connect(self._on_starfish_anim_speed_changed)
        layout.addWidget(self.starfish_anim_speed_slider)
        self.starfish_anim_speed_label = QLabel("1.5x")
        self.starfish_anim_speed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.starfish_anim_speed_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.starfish_anim_speed_label)

        # Pulse Amount
        layout.addWidget(self._create_label("Pulse Amount"))
        self.starfish_pulse_slider = QSlider(Qt.Orientation.Horizontal)
        self.starfish_pulse_slider.setRange(0, 20)  # 0 to 0.2
        self.starfish_pulse_slider.setValue(6)  # 0.06 default
        self.starfish_pulse_slider.setMinimumHeight(30)
        self.starfish_pulse_slider.valueChanged.connect(self._on_starfish_pulse_changed)
        layout.addWidget(self.starfish_pulse_slider)
        self.starfish_pulse_label = QLabel("0.06")
        self.starfish_pulse_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.starfish_pulse_label.setStyleSheet("color: #a78bfa; font-size: 13pt; font-weight: bold; background-color: #2d1b4e; padding: 6px 14px; border-radius: 12px; border: 1px solid #6366f1;")
        layout.addWidget(self.starfish_pulse_label)

        layout.addStretch()
        group.setLayout(layout)
        return group

    # Event handlers
    def _on_tentacles_changed(self, value):
        if not self._updating:
            self._num_tentacles = value
            self._update_branch_info()
            self.creature_changed.emit()

    def _on_segments_changed(self, value):
        if not self._updating:
            self._segments = value
            self._update_branch_info()
            self.creature_changed.emit()

    def _on_algorithm_changed(self, text):
        if not self._updating:
            self._algorithm = text.lower()
            self.bezier_widget.setVisible(self._algorithm == 'bezier')
            self.fourier_widget.setVisible(self._algorithm == 'fourier')
            self.creature_changed.emit()

    def _on_bezier_changed(self, value):
        if not self._updating:
            self._bezier_control_strength = value / 100.0
            self.bezier_value_label.setText(f"{self._bezier_control_strength:.2f}")
            self.creature_changed.emit()

    def _on_fourier_changed(self):
        if not self._updating:
            self._fourier_waves = self.fourier_waves_spin.value()
            self._fourier_amplitude = self.fourier_amp_slider.value() / 100.0
            self.fourier_amp_label.setText(f"{self._fourier_amplitude:.2f}")
            self.creature_changed.emit()

    def _on_thickness_changed(self, value):
        if not self._updating:
            self._thickness_base = value / 100.0
            self.thickness_label.setText(f"{self._thickness_base:.2f}")
            self.creature_changed.emit()

    def _on_taper_changed(self, value):
        if not self._updating:
            self._taper_factor = value / 100.0
            self.taper_label.setText(f"{self._taper_factor:.2f}")
            self.creature_changed.emit()

    def _on_color_changed(self, rgb_tuple):
        if not self._updating:
            self._tentacle_color = rgb_tuple
            self.creature_changed.emit()

    def _on_hue_changed(self, value):
        if not self._updating:
            self._hue_shift = value / 100.0
            self.hue_label.setText(f"{self._hue_shift:.2f}")
            self.creature_changed.emit()

    def _on_body_scale_changed(self, value):
        if not self._updating:
            self._body_scale = value / 100.0
            self.body_scale_label.setText(f"{self._body_scale:.2f}")
            self.creature_changed.emit()

    def _on_branching_changed(self):
        if not self._updating:
            self._branch_depth = self.branch_depth_spin.value()
            self._branch_count = self.branch_count_spin.value()
            self._update_branch_info()
            self.creature_changed.emit()

    def _on_anim_speed_changed(self, value):
        if not self._updating:
            self._anim_speed = value / 100.0
            self.anim_speed_label.setText(f"{self._anim_speed:.1f}x")
            self.creature_changed.emit()

    def _on_wave_amp_changed(self, value):
        if not self._updating:
            self._wave_amplitude = value / 100.0
            self.wave_amp_label.setText(f"{self._wave_amplitude:.2f}")
            self.creature_changed.emit()

    def _on_pulse_speed_changed(self, value):
        if not self._updating:
            self._pulse_speed = value / 100.0
            self.pulse_speed_label.setText(f"{self._pulse_speed:.1f}x")
            self.creature_changed.emit()

    def _on_pulse_amt_changed(self, value):
        if not self._updating:
            self._pulse_amount = value / 100.0
            self.pulse_amt_label.setText(f"{self._pulse_amount:.2f}")
            self.creature_changed.emit()

    def _on_num_eyes_changed(self, value):
        if not self._updating:
            self._num_eyes = value
            self.creature_changed.emit()

    def _on_eye_size_changed(self):
        if not self._updating:
            self._eye_size_min = self.eye_size_min_slider.value() / 100.0
            self._eye_size_max = self.eye_size_max_slider.value() / 100.0
            self.eye_size_min_label.setText(f"{self._eye_size_min:.2f}")
            self.eye_size_max_label.setText(f"{self._eye_size_max:.2f}")
            self.creature_changed.emit()

    def _on_eyeball_color_changed(self, rgb_tuple):
        if not self._updating:
            self._eyeball_color = rgb_tuple
            self.creature_changed.emit()

    def _on_pupil_color_changed(self, rgb_tuple):
        if not self._updating:
            self._pupil_color = rgb_tuple
            self.creature_changed.emit()

    # ==== BLOB EVENT HANDLERS ====

    def _on_creature_type_changed(self, text):
        """Handle creature type selection change."""
        if not self._updating:
            # Convert display name to internal type
            if text == "Tentacle Creature":
                self._creature_type = 'tentacle'
            elif text == "Blob Creature":
                self._creature_type = 'blob'
            elif text == "Polyp Creature":
                self._creature_type = 'polyp'
            else:  # "Starfish Creature"
                self._creature_type = 'starfish'

            # Show/hide appropriate containers
            self.tentacle_container.setVisible(self._creature_type == 'tentacle')
            self.blob_container.setVisible(self._creature_type == 'blob')
            self.polyp_container.setVisible(self._creature_type == 'polyp')
            self.starfish_container.setVisible(self._creature_type == 'starfish')

            # Emit signals
            self.creature_type_changed.emit(self._creature_type)
            self.creature_changed.emit()

    def _on_blob_branching_changed(self):
        if not self._updating:
            self._blob_branch_depth = self.blob_branch_depth_spin.value()
            self._blob_branch_count = self.blob_branch_count_spin.value()
            self._update_blob_branch_info()
            self.creature_changed.emit()

    def _update_blob_branch_info(self):
        """Calculate and display total cube count from branch parameters."""
        if self._blob_branch_count == 1:
            # Linear: 1 + 1 + 1 + ... = depth + 1
            total_cubes = self._blob_branch_depth + 1
        else:
            # Geometric series: 1 + c + c² + c³ + ... + c^d
            # Sum = (c^(d+1) - 1) / (c - 1)
            total_cubes = (self._blob_branch_count ** (self._blob_branch_depth + 1) - 1) // (self._blob_branch_count - 1)

        self.blob_branch_info_label.setText(f"Total: ~{total_cubes} cubes")

    def _on_cube_spacing_changed(self, value):
        if not self._updating:
            self._cube_spacing = value / 100.0
            self.cube_spacing_label.setText(f"{self._cube_spacing:.2f}")
            self.creature_changed.emit()

    def _on_blob_color_changed(self, rgb_tuple):
        if not self._updating:
            self._blob_color = rgb_tuple
            self.creature_changed.emit()

    def _on_blob_transparency_changed(self, value):
        if not self._updating:
            self._blob_transparency = value / 100.0
            self.blob_transparency_label.setText(f"{int(value)}%")
            self.creature_changed.emit()

    def _on_cube_size_changed(self):
        if not self._updating:
            self._cube_size_min = self.cube_size_min_slider.value() / 100.0
            self._cube_size_max = self.cube_size_max_slider.value() / 100.0
            self.cube_size_min_label.setText(f"{self._cube_size_min:.2f}")
            self.cube_size_max_label.setText(f"{self._cube_size_max:.2f}")
            self.creature_changed.emit()

    def _on_jiggle_speed_changed(self, value):
        if not self._updating:
            self._jiggle_speed = value / 100.0
            self.jiggle_speed_label.setText(f"{self._jiggle_speed:.1f}x")
            self.creature_changed.emit()

    def _on_blob_pulse_changed(self, value):
        if not self._updating:
            self._blob_pulse_amount = value / 100.0
            self.blob_pulse_label.setText(f"{self._blob_pulse_amount:.2f}")
            self.creature_changed.emit()

    # ==== POLYP EVENT HANDLERS ====

    def _on_num_spheres_changed(self, value):
        if not self._updating:
            self._num_spheres = value
            self.creature_changed.emit()

    def _on_base_sphere_changed(self, value):
        if not self._updating:
            self._base_sphere_size = value / 100.0
            self.base_sphere_label.setText(f"{self._base_sphere_size:.2f}")
            self.creature_changed.emit()

    def _on_polyp_color_changed(self, rgb_tuple):
        if not self._updating:
            self._polyp_color = rgb_tuple
            self.creature_changed.emit()

    def _on_curve_intensity_changed(self, value):
        if not self._updating:
            self._curve_intensity = value / 100.0
            self.curve_intensity_label.setText(f"{self._curve_intensity:.2f}")
            self.creature_changed.emit()

    def _on_polyp_tentacles_changed(self, value):
        if not self._updating:
            self._polyp_tentacles_per_sphere = value
            self.creature_changed.emit()

    def _on_polyp_segments_changed(self, value):
        if not self._updating:
            self._polyp_segments = value
            self.creature_changed.emit()

    # ==== STARFISH EVENT HANDLERS ====

    def _on_num_arms_changed(self, value):
        if not self._updating:
            self._num_arms = value
            self.creature_changed.emit()

    def _on_arm_segments_changed(self, value):
        if not self._updating:
            self._arm_segments = value
            self.creature_changed.emit()

    def _on_central_body_changed(self, value):
        if not self._updating:
            self._central_body_size = value / 100.0
            self.central_body_label.setText(f"{self._central_body_size:.2f}")
            self.creature_changed.emit()

    def _on_starfish_color_changed(self, rgb_tuple):
        if not self._updating:
            self._starfish_color = rgb_tuple
            self.creature_changed.emit()

    def _on_arm_thickness_changed(self, value):
        if not self._updating:
            self._arm_base_thickness = value / 100.0
            self.arm_thickness_label.setText(f"{self._arm_base_thickness:.2f}")
            self.creature_changed.emit()

    def _on_curl_factor_changed(self, value):
        if not self._updating:
            self._curl_factor = value / 100.0
            self.curl_factor_label.setText(f"{self._curl_factor:.2f}")
            self.creature_changed.emit()

    def _on_starfish_anim_speed_changed(self, value):
        if not self._updating:
            self._starfish_anim_speed = value / 100.0
            self.starfish_anim_speed_label.setText(f"{self._starfish_anim_speed:.1f}x")
            self.creature_changed.emit()

    def _on_starfish_pulse_changed(self, value):
        if not self._updating:
            self._starfish_pulse = value / 100.0
            self.starfish_pulse_label.setText(f"{self._starfish_pulse:.2f}")
            self.creature_changed.emit()

    def _update_branch_info(self):
        """Update branch info label."""
        if self._branch_count == 1:
            branches_per_main = self._branch_depth + 1
        else:
            branches_per_main = (self._branch_count ** (self._branch_depth + 1) - 1) // (self._branch_count - 1)

        total_tentacles = self._num_tentacles * branches_per_main
        total_segments = total_tentacles * self._segments
        self.branch_info_label.setText(f"Total: ~{total_segments} segments")

    def _load_preset(self, algorithm, params):
        """Load preset."""
        self._updating = True
        self._algorithm = algorithm
        self.algorithm_combo.setCurrentText(algorithm.capitalize())

        if algorithm == 'bezier':
            self._bezier_control_strength = params['control_strength']
            self.bezier_slider.setValue(int(self._bezier_control_strength * 100))
            self.bezier_widget.setVisible(True)
            self.fourier_widget.setVisible(False)
        else:
            self._fourier_waves = params['num_waves']
            self._fourier_amplitude = params['amplitude']
            self.fourier_waves_spin.setValue(self._fourier_waves)
            self.fourier_amp_slider.setValue(int(self._fourier_amplitude * 100))
            self.bezier_widget.setVisible(False)
            self.fourier_widget.setVisible(True)

        self._updating = False
        self.creature_changed.emit()

    def get_state(self):
        """Get current state."""
        return {
            'creature_type': self._creature_type,
            # Tentacle parameters
            'num_tentacles': self._num_tentacles,
            'segments': self._segments,
            'algorithm': self._algorithm,
            'params': self.get_algorithm_params(),
            'thickness_base': self._thickness_base,
            'taper_factor': self._taper_factor,
            'branch_depth': self._branch_depth,
            'branch_count': self._branch_count,
            'body_scale': self._body_scale,
            'tentacle_color': self._tentacle_color,
            'hue_shift': self._hue_shift,
            'anim_speed': self._anim_speed,
            'wave_amplitude': self._wave_amplitude,
            'pulse_speed': self._pulse_speed,
            'pulse_amount': self._pulse_amount,
            'num_eyes': self._num_eyes,
            'eye_size_min': self._eye_size_min,
            'eye_size_max': self._eye_size_max,
            'eyeball_color': self._eyeball_color,
            'pupil_color': self._pupil_color,
            # Blob parameters
            'blob_branch_depth': self._blob_branch_depth,
            'blob_branch_count': self._blob_branch_count,
            'cube_size_min': self._cube_size_min,
            'cube_size_max': self._cube_size_max,
            'cube_spacing': self._cube_spacing,
            'blob_color': self._blob_color,
            'blob_transparency': self._blob_transparency,
            'jiggle_speed': self._jiggle_speed,
            'blob_pulse_amount': self._blob_pulse_amount,
            # Polyp parameters
            'num_spheres': self._num_spheres,
            'base_sphere_size': self._base_sphere_size,
            'polyp_color': self._polyp_color,
            'curve_intensity': self._curve_intensity,
            'polyp_tentacles_per_sphere': self._polyp_tentacles_per_sphere,
            'polyp_segments': self._polyp_segments,
            # Starfish parameters
            'num_arms': self._num_arms,
            'arm_segments': self._arm_segments,
            'central_body_size': self._central_body_size,
            'arm_base_thickness': self._arm_base_thickness,
            'starfish_color': self._starfish_color,
            'curl_factor': self._curl_factor,
            'starfish_anim_speed': self._starfish_anim_speed,
            'starfish_pulse_amount': self._starfish_pulse
        }

    def get_algorithm_params(self):
        """Get algorithm parameters."""
        if self._algorithm == 'bezier':
            return {'control_strength': self._bezier_control_strength}
        else:
            return {
                'num_waves': self._fourier_waves,
                'amplitude': self._fourier_amplitude
            }

    def set_state(self, state):
        """Restore state."""
        self._updating = True

        # Creature type
        self._creature_type = state.get('creature_type', 'tentacle')

        # Tentacle parameters
        self._num_tentacles = state.get('num_tentacles', 2)
        self._segments = state.get('segments', 12)
        self._algorithm = state.get('algorithm', 'bezier')
        self._thickness_base = state.get('thickness_base', 0.25)
        self._taper_factor = state.get('taper_factor', 0.6)
        self._branch_depth = state.get('branch_depth', 0)
        self._branch_count = state.get('branch_count', 1)
        self._body_scale = state.get('body_scale', 1.2)
        self._tentacle_color = state.get('tentacle_color', (0.6, 0.3, 0.7))
        self._hue_shift = state.get('hue_shift', 0.1)
        self._anim_speed = state.get('anim_speed', 2.0)
        self._wave_amplitude = state.get('wave_amplitude', 0.05)
        self._pulse_speed = state.get('pulse_speed', 1.5)
        self._pulse_amount = state.get('pulse_amount', 0.05)
        self._num_eyes = state.get('num_eyes', 3)
        self._eye_size_min = state.get('eye_size_min', 0.1)
        self._eye_size_max = state.get('eye_size_max', 0.25)
        self._eyeball_color = state.get('eyeball_color', (1.0, 1.0, 1.0))
        self._pupil_color = state.get('pupil_color', (0.0, 0.0, 0.0))

        # Blob parameters
        self._blob_branch_depth = state.get('blob_branch_depth', 2)
        self._blob_branch_count = state.get('blob_branch_count', 2)
        self._cube_size_min = state.get('cube_size_min', 0.3)
        self._cube_size_max = state.get('cube_size_max', 0.8)
        self._cube_spacing = state.get('cube_spacing', 1.2)
        self._blob_color = state.get('blob_color', (0.2, 0.8, 0.4))
        self._blob_transparency = state.get('blob_transparency', 0.7)
        self._jiggle_speed = state.get('jiggle_speed', 2.0)
        self._blob_pulse_amount = state.get('blob_pulse_amount', 0.1)

        # Polyp parameters
        self._num_spheres = state.get('num_spheres', 4)
        self._base_sphere_size = state.get('base_sphere_size', 0.8)
        self._polyp_color = state.get('polyp_color', (0.6, 0.3, 0.7))
        self._curve_intensity = state.get('curve_intensity', 0.4)
        self._polyp_tentacles_per_sphere = state.get('polyp_tentacles_per_sphere', 6)
        self._polyp_segments = state.get('polyp_segments', 12)

        # Starfish parameters
        self._num_arms = state.get('num_arms', 5)
        self._arm_segments = state.get('arm_segments', 6)
        self._central_body_size = state.get('central_body_size', 0.8)
        self._arm_base_thickness = state.get('arm_base_thickness', 0.4)
        self._starfish_color = state.get('starfish_color', (0.9, 0.5, 0.3))
        self._curl_factor = state.get('curl_factor', 0.3)
        self._starfish_anim_speed = state.get('starfish_anim_speed', 1.5)
        self._starfish_pulse = state.get('starfish_pulse_amount', 0.06)

        # Update creature type selector
        if self._creature_type == 'tentacle':
            display_name = "Tentacle Creature"
        elif self._creature_type == 'blob':
            display_name = "Blob Creature"
        elif self._creature_type == 'polyp':
            display_name = "Polyp Creature"
        else:  # starfish
            display_name = "Starfish Creature"
        self.creature_type_combo.setCurrentText(display_name)

        # Show/hide appropriate containers
        self.tentacle_container.setVisible(self._creature_type == 'tentacle')
        self.blob_container.setVisible(self._creature_type == 'blob')
        self.polyp_container.setVisible(self._creature_type == 'polyp')
        self.starfish_container.setVisible(self._creature_type == 'starfish')

        # Update tentacle UI
        self.tentacles_spin.setValue(self._num_tentacles)
        self.segments_spin.setValue(self._segments)
        self.algorithm_combo.setCurrentText(self._algorithm.capitalize())
        self.thickness_slider.setValue(int(self._thickness_base * 100))
        self.taper_slider.setValue(int(self._taper_factor * 100))
        self.branch_depth_spin.setValue(self._branch_depth)
        self.branch_count_spin.setValue(self._branch_count)
        self.body_scale_slider.setValue(int(self._body_scale * 100))
        self.color_button.set_color(self._tentacle_color)
        self.hue_slider.setValue(int(self._hue_shift * 100))
        self.anim_speed_slider.setValue(int(self._anim_speed * 100))
        self.wave_amp_slider.setValue(int(self._wave_amplitude * 100))
        self.pulse_speed_slider.setValue(int(self._pulse_speed * 100))
        self.pulse_amt_slider.setValue(int(self._pulse_amount * 100))
        self.num_eyes_spin.setValue(self._num_eyes)
        self.eye_size_min_slider.setValue(int(self._eye_size_min * 100))
        self.eye_size_max_slider.setValue(int(self._eye_size_max * 100))
        self.eyeball_color_button.set_color(self._eyeball_color)
        self.pupil_color_button.set_color(self._pupil_color)

        # Update blob UI
        self.blob_branch_depth_spin.setValue(self._blob_branch_depth)
        self.blob_branch_count_spin.setValue(self._blob_branch_count)
        self.cube_spacing_slider.setValue(int(self._cube_spacing * 100))
        self.blob_color_button.set_color(self._blob_color)
        self.blob_transparency_slider.setValue(int(self._blob_transparency * 100))
        self.cube_size_min_slider.setValue(int(self._cube_size_min * 100))
        self.cube_size_max_slider.setValue(int(self._cube_size_max * 100))
        self.jiggle_speed_slider.setValue(int(self._jiggle_speed * 100))
        self.blob_pulse_slider.setValue(int(self._blob_pulse_amount * 100))

        # Update polyp UI
        self.num_spheres_spin.setValue(self._num_spheres)
        self.base_sphere_slider.setValue(int(self._base_sphere_size * 100))
        self.polyp_color_button.set_color(self._polyp_color)
        self.curve_intensity_slider.setValue(int(self._curve_intensity * 100))
        self.polyp_tentacles_spin.setValue(self._polyp_tentacles_per_sphere)
        self.polyp_segments_spin.setValue(self._polyp_segments)

        # Update starfish UI
        self.num_arms_spin.setValue(self._num_arms)
        self.arm_segments_spin.setValue(self._arm_segments)
        self.central_body_slider.setValue(int(self._central_body_size * 100))
        self.starfish_color_button.set_color(self._starfish_color)
        self.arm_thickness_slider.setValue(int(self._arm_base_thickness * 100))
        self.curl_factor_slider.setValue(int(self._curl_factor * 100))
        self.starfish_anim_speed_slider.setValue(int(self._starfish_anim_speed * 100))
        self.starfish_pulse_slider.setValue(int(self._starfish_pulse * 100))

        # Update branch info label
        self._update_blob_branch_info()

        params = state.get('params', {})
        if self._algorithm == 'bezier':
            self._bezier_control_strength = params.get('control_strength', 0.4)
            self.bezier_slider.setValue(int(self._bezier_control_strength * 100))
        else:
            self._fourier_waves = params.get('num_waves', 3)
            self._fourier_amplitude = params.get('amplitude', 0.15)
            self.fourier_waves_spin.setValue(self._fourier_waves)
            self.fourier_amp_slider.setValue(int(self._fourier_amplitude * 100))

        self._update_branch_info()
        self._updating = False
        self.creature_changed.emit()

    def set_undo_redo_enabled(self, can_undo, can_redo):
        """Update undo/redo buttons."""
        self.undo_btn.setEnabled(can_undo)
        self.redo_btn.setEnabled(can_redo)
