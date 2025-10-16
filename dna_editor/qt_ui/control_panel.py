"""
Control panel with all DNA editor controls.

Provides sliders, spinboxes, buttons for creature parameters.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QLabel, QSlider,
    QSpinBox, QComboBox, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class ControlPanel(QWidget):
    """Left panel with all creature parameter controls."""

    # Signals emitted when parameters change
    creature_changed = pyqtSignal()  # Any parameter changed
    undo_requested = pyqtSignal()
    redo_requested = pyqtSignal()
    export_requested = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize control panel."""
        super().__init__(parent)

        # Initialize state
        self._num_tentacles = 2
        self._segments = 12
        self._algorithm = 'bezier'
        self._bezier_control_strength = 0.4
        self._fourier_waves = 3
        self._fourier_amplitude = 0.15
        self._thickness_base = 0.25
        self._taper_factor = 0.6

        # Block signals during programmatic updates
        self._updating = False

        self._init_ui()

    def _init_ui(self):
        """Initialize UI components."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QLabel("DNA Editor Controls")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Creature Settings
        layout.addWidget(self._create_creature_settings())

        # Algorithm Parameters
        layout.addWidget(self._create_algorithm_params())

        # Thickness Settings
        layout.addWidget(self._create_thickness_settings())

        # Presets
        layout.addWidget(self._create_presets())

        # Actions (Undo/Redo/Export)
        layout.addWidget(self._create_actions())

        layout.addStretch()
        self.setLayout(layout)
        self.setFixedWidth(340)

    def _create_creature_settings(self):
        """Create creature settings group."""
        group = QGroupBox("Creature Settings")
        group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout = QVBoxLayout()

        # Tentacle count
        tent_layout = QHBoxLayout()
        tent_layout.addWidget(QLabel("Tentacles:"))
        self.tentacles_spin = QSpinBox()
        self.tentacles_spin.setRange(1, 3)
        self.tentacles_spin.setValue(self._num_tentacles)
        self.tentacles_spin.valueChanged.connect(self._on_tentacles_changed)
        tent_layout.addWidget(self.tentacles_spin)
        layout.addLayout(tent_layout)

        # Segments
        seg_layout = QHBoxLayout()
        seg_layout.addWidget(QLabel("Segments:"))
        self.segments_spin = QSpinBox()
        self.segments_spin.setRange(5, 20)
        self.segments_spin.setValue(self._segments)
        self.segments_spin.valueChanged.connect(self._on_segments_changed)
        seg_layout.addWidget(self.segments_spin)
        layout.addLayout(seg_layout)

        # Algorithm
        algo_layout = QHBoxLayout()
        algo_layout.addWidget(QLabel("Algorithm:"))
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(["Bezier", "Fourier"])
        self.algorithm_combo.setCurrentText("Bezier")
        self.algorithm_combo.currentTextChanged.connect(self._on_algorithm_changed)
        algo_layout.addWidget(self.algorithm_combo)
        layout.addLayout(algo_layout)

        group.setLayout(layout)
        return group

    def _create_algorithm_params(self):
        """Create algorithm-specific parameters group."""
        group = QGroupBox("Algorithm Parameters")
        group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout = QVBoxLayout()

        # Bezier controls
        self.bezier_widget = QWidget()
        bezier_layout = QVBoxLayout()
        bezier_layout.setContentsMargins(0, 0, 0, 0)

        bezier_layout.addWidget(QLabel("Control Strength:"))
        self.bezier_slider = QSlider(Qt.Orientation.Horizontal)
        self.bezier_slider.setRange(10, 80)  # 0.1 to 0.8 (x100)
        self.bezier_slider.setValue(40)  # 0.4
        self.bezier_slider.valueChanged.connect(self._on_bezier_changed)
        bezier_layout.addWidget(self.bezier_slider)

        self.bezier_value_label = QLabel("0.40")
        self.bezier_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bezier_layout.addWidget(self.bezier_value_label)

        self.bezier_widget.setLayout(bezier_layout)
        layout.addWidget(self.bezier_widget)

        # Fourier controls
        self.fourier_widget = QWidget()
        fourier_layout = QVBoxLayout()
        fourier_layout.setContentsMargins(0, 0, 0, 0)

        fourier_layout.addWidget(QLabel("Wave Count:"))
        self.fourier_waves_spin = QSpinBox()
        self.fourier_waves_spin.setRange(1, 7)
        self.fourier_waves_spin.setValue(3)
        self.fourier_waves_spin.valueChanged.connect(self._on_fourier_changed)
        fourier_layout.addWidget(self.fourier_waves_spin)

        fourier_layout.addWidget(QLabel("Amplitude:"))
        self.fourier_amp_slider = QSlider(Qt.Orientation.Horizontal)
        self.fourier_amp_slider.setRange(5, 40)  # 0.05 to 0.4 (x100)
        self.fourier_amp_slider.setValue(15)  # 0.15
        self.fourier_amp_slider.valueChanged.connect(self._on_fourier_changed)
        fourier_layout.addWidget(self.fourier_amp_slider)

        self.fourier_amp_label = QLabel("0.15")
        self.fourier_amp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fourier_layout.addWidget(self.fourier_amp_label)

        self.fourier_widget.setLayout(fourier_layout)
        self.fourier_widget.setVisible(False)  # Hidden by default
        layout.addWidget(self.fourier_widget)

        group.setLayout(layout)
        return group

    def _create_thickness_settings(self):
        """Create thickness settings group."""
        group = QGroupBox("Thickness")
        group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout = QVBoxLayout()

        # Base thickness
        layout.addWidget(QLabel("Base:"))
        self.thickness_slider = QSlider(Qt.Orientation.Horizontal)
        self.thickness_slider.setRange(10, 50)  # 0.1 to 0.5 (x100)
        self.thickness_slider.setValue(25)  # 0.25
        self.thickness_slider.valueChanged.connect(self._on_thickness_changed)
        layout.addWidget(self.thickness_slider)

        self.thickness_value_label = QLabel("0.25")
        self.thickness_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.thickness_value_label)

        # Taper
        layout.addWidget(QLabel("Taper:"))
        self.taper_slider = QSlider(Qt.Orientation.Horizontal)
        self.taper_slider.setRange(0, 100)  # 0.0 to 1.0 (x100)
        self.taper_slider.setValue(60)  # 0.6
        self.taper_slider.valueChanged.connect(self._on_taper_changed)
        layout.addWidget(self.taper_slider)

        self.taper_value_label = QLabel("0.60")
        self.taper_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.taper_value_label)

        group.setLayout(layout)
        return group

    def _create_presets(self):
        """Create presets group."""
        group = QGroupBox("Presets")
        group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout = QVBoxLayout()

        # Preset buttons
        presets = [
            ("Default", 'bezier', {'control_strength': 0.4}),
            ("Wavy", 'fourier', {'num_waves': 4, 'amplitude': 0.25}),
            ("Tight", 'bezier', {'control_strength': 0.2}),
        ]

        for name, algo, params in presets:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, a=algo, p=params: self._load_preset(a, p))
            layout.addWidget(btn)

        group.setLayout(layout)
        return group

    def _create_actions(self):
        """Create action buttons."""
        group = QGroupBox("Actions")
        group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        layout = QVBoxLayout()

        # Undo/Redo
        undo_redo_layout = QHBoxLayout()

        self.undo_btn = QPushButton("Undo")
        self.undo_btn.clicked.connect(self.undo_requested.emit)
        self.undo_btn.setEnabled(False)
        undo_redo_layout.addWidget(self.undo_btn)

        self.redo_btn = QPushButton("Redo")
        self.redo_btn.clicked.connect(self.redo_requested.emit)
        self.redo_btn.setEnabled(False)
        undo_redo_layout.addWidget(self.redo_btn)

        layout.addLayout(undo_redo_layout)

        # Export
        self.export_btn = QPushButton("Export JSON")
        self.export_btn.clicked.connect(self.export_requested.emit)
        layout.addWidget(self.export_btn)

        group.setLayout(layout)
        return group

    # Getters for current state
    def get_state(self):
        """Get current creature parameters as dict."""
        return {
            'num_tentacles': self._num_tentacles,
            'segments': self._segments,
            'algorithm': self._algorithm,
            'params': self.get_algorithm_params(),
            'thickness_base': self._thickness_base,
            'taper_factor': self._taper_factor
        }

    def get_algorithm_params(self):
        """Get parameters for current algorithm."""
        if self._algorithm == 'bezier':
            return {'control_strength': self._bezier_control_strength}
        else:
            return {
                'num_waves': self._fourier_waves,
                'amplitude': self._fourier_amplitude
            }

    # Setters for restoring state (e.g., undo/redo)
    def set_state(self, state):
        """Restore state from dict (for undo/redo)."""
        self._updating = True

        self._num_tentacles = state['num_tentacles']
        self._segments = state['segments']
        self._algorithm = state['algorithm']
        self._thickness_base = state['thickness_base']
        self._taper_factor = state['taper_factor']

        # Update UI widgets
        self.tentacles_spin.setValue(self._num_tentacles)
        self.segments_spin.setValue(self._segments)
        self.algorithm_combo.setCurrentText(self._algorithm.capitalize())
        self.thickness_slider.setValue(int(self._thickness_base * 100))
        self.taper_slider.setValue(int(self._taper_factor * 100))

        # Update algorithm params
        params = state['params']
        if self._algorithm == 'bezier':
            self._bezier_control_strength = params.get('control_strength', 0.4)
            self.bezier_slider.setValue(int(self._bezier_control_strength * 100))
        else:
            self._fourier_waves = params.get('num_waves', 3)
            self._fourier_amplitude = params.get('amplitude', 0.15)
            self.fourier_waves_spin.setValue(self._fourier_waves)
            self.fourier_amp_slider.setValue(int(self._fourier_amplitude * 100))

        self._updating = False
        self.creature_changed.emit()

    def set_undo_redo_enabled(self, can_undo, can_redo):
        """Update undo/redo button states."""
        self.undo_btn.setEnabled(can_undo)
        self.redo_btn.setEnabled(can_redo)

    # Event handlers
    def _on_tentacles_changed(self, value):
        """Handle tentacle count change."""
        if not self._updating:
            self._num_tentacles = value
            self.creature_changed.emit()

    def _on_segments_changed(self, value):
        """Handle segment count change."""
        if not self._updating:
            self._segments = value
            self.creature_changed.emit()

    def _on_algorithm_changed(self, text):
        """Handle algorithm change."""
        if not self._updating:
            self._algorithm = text.lower()

            # Show/hide appropriate parameter widgets
            self.bezier_widget.setVisible(self._algorithm == 'bezier')
            self.fourier_widget.setVisible(self._algorithm == 'fourier')

            self.creature_changed.emit()

    def _on_bezier_changed(self, value):
        """Handle Bezier parameter change."""
        if not self._updating:
            self._bezier_control_strength = value / 100.0
            self.bezier_value_label.setText(f"{self._bezier_control_strength:.2f}")
            self.creature_changed.emit()

    def _on_fourier_changed(self):
        """Handle Fourier parameter change."""
        if not self._updating:
            self._fourier_waves = self.fourier_waves_spin.value()
            self._fourier_amplitude = self.fourier_amp_slider.value() / 100.0
            self.fourier_amp_label.setText(f"{self._fourier_amplitude:.2f}")
            self.creature_changed.emit()

    def _on_thickness_changed(self, value):
        """Handle thickness change."""
        if not self._updating:
            self._thickness_base = value / 100.0
            self.thickness_value_label.setText(f"{self._thickness_base:.2f}")
            self.creature_changed.emit()

    def _on_taper_changed(self, value):
        """Handle taper change."""
        if not self._updating:
            self._taper_factor = value / 100.0
            self.taper_value_label.setText(f"{self._taper_factor:.2f}")
            self.creature_changed.emit()

    def _load_preset(self, algorithm, params):
        """Load a preset configuration."""
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
