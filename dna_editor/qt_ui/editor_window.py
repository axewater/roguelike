"""
Main editor window - orchestrates control panel and 3D renderer.

Handles undo/redo, file export, and coordinate updates between UI and 3D.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QFileDialog, QMessageBox, QScrollArea
)
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt
import json
import sys
import os

from .control_panel_modern import ModernControlPanel
from .ursina_renderer import UrsinaRenderer
from ..controllers.state_manager import StateManager


class EditorWindow(QMainWindow):
    """Main DNA Editor window."""

    def __init__(self):
        """Initialize editor window."""
        super().__init__()

        self.state_manager = StateManager()

        self.setWindowTitle("DNA Editor - Creature Designer")
        self.setFixedSize(1300, 850)  # Modern wide layout with breathing room
        self.move(100, 100)

        # Apply modern dark theme stylesheet with enhanced visuals
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #1a1a1a, stop:1 #1e1e1e);
            }
            QGroupBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #2d2d2d, stop:1 #252525);
                border: 1px solid #3a3a3a;
                border-radius: 10px;
                margin-top: 16px;
                padding: 20px;
                font-weight: bold;
                color: #e5e5e5;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 8px 16px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                           stop:0 #6366f1, stop:1 #8b5cf6);
                border-radius: 6px;
                color: white;
                font-size: 11pt;
                font-weight: bold;
            }
            QLabel {
                color: #e5e5e5;
                font-size: 11pt;
            }
            QSpinBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #3a3a3a, stop:1 #323232);
                border: 2px solid #4a4a4a;
                border-radius: 8px;
                padding: 10px;
                color: #e5e5e5;
                font-size: 12pt;
                min-height: 45px;
                selection-background-color: #6366f1;
            }
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #3a3a3a, stop:1 #323232);
                border: 2px solid #4a4a4a;
                border-radius: 8px;
                padding: 10px;
                padding-right: 35px;
                color: #e5e5e5;
                font-size: 12pt;
                min-height: 45px;
                selection-background-color: #6366f1;
            }
            QSpinBox:focus, QComboBox:focus {
                border: 2px solid #6366f1;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #424242, stop:1 #3a3a3a);
            }
            QSpinBox:hover, QComboBox:hover {
                border: 2px solid #8b5cf6;
            }
            QSpinBox::up-button {
                background: #4a4a4a;
                border-radius: 4px;
                border: none;
                width: 24px;
                subcontrol-origin: border;
                subcontrol-position: top right;
            }
            QSpinBox::down-button {
                background: #4a4a4a;
                border-radius: 4px;
                border: none;
                width: 24px;
                subcontrol-origin: border;
                subcontrol-position: bottom right;
            }
            QSpinBox::up-button:hover {
                background: #6366f1;
            }
            QSpinBox::down-button:hover {
                background: #6366f1;
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
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #7c3aed, stop:1 #6366f1);
                border: none;
                border-radius: 8px;
                color: white;
                padding: 12px 20px;
                font-size: 11pt;
                font-weight: bold;
                min-height: 45px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #8b5cf6, stop:1 #7c3aed);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #6d28d9, stop:1 #5b21b6);
                padding-top: 14px;
                padding-bottom: 10px;
            }
            QPushButton:disabled {
                background: #333333;
                color: #666666;
            }
            QSlider::groove:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                           stop:0 #3a3a3a, stop:1 #2d2d2d);
                height: 10px;
                border-radius: 5px;
                border: 1px solid #4a4a4a;
            }
            QSlider::handle:horizontal {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                                           fx:0.3, fy:0.3,
                                           stop:0 #a78bfa, stop:1 #6366f1);
                width: 24px;
                height: 24px;
                margin: -8px 0;
                border-radius: 12px;
                border: 2px solid #8b5cf6;
            }
            QSlider::handle:horizontal:hover {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                                           fx:0.3, fy:0.3,
                                           stop:0 #c4b5fd, stop:1 #8b5cf6);
                border: 2px solid #a78bfa;
            }
            QSlider::handle:horizontal:pressed {
                background: qradialgradient(cx:0.5, cy:0.5, radius:0.8,
                                           fx:0.3, fy:0.3,
                                           stop:0 #ddd6fe, stop:1 #a78bfa);
            }
        """)

        self._init_ui()
        self._init_menu()

        # Initial creature build
        self._on_creature_changed()

    def _init_ui(self):
        """Initialize UI layout."""
        # Central widget with vertical layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Control panel
        self.control_panel = ModernControlPanel()
        self.control_panel.creature_changed.connect(self._on_creature_changed)
        self.control_panel.undo_requested.connect(self._on_undo)
        self.control_panel.redo_requested.connect(self._on_redo)
        self.control_panel.export_requested.connect(self._on_export)
        self.control_panel.attack_requested.connect(self._on_attack)

        # Wrap control panel in scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.control_panel)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #6366f1;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: #8b5cf6;
            }
        """)
        layout.addWidget(scroll_area)

        # Status label at bottom
        status_label = QLabel("3D Preview: Separate Window")
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_label.setStyleSheet(
            "color: #888; "
            "font-size: 10px; "
            "padding: 8px; "
            "background-color: #2a2a2a;"
        )
        layout.addWidget(status_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Initialize Ursina renderer (separate window)
        self.renderer = UrsinaRenderer()

    def _init_menu(self):
        """Initialize menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        export_action = QAction("&Export JSON", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(self._on_export)
        file_menu.addAction(export_action)

        file_menu.addSeparator()

        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")

        self.undo_action = QAction("&Undo", self)
        self.undo_action.setShortcut(QKeySequence("Ctrl+Z"))
        self.undo_action.setEnabled(False)
        self.undo_action.triggered.connect(self._on_undo)
        edit_menu.addAction(self.undo_action)

        self.redo_action = QAction("&Redo", self)
        self.redo_action.setShortcut(QKeySequence("Ctrl+Y"))
        self.redo_action.setEnabled(False)
        self.redo_action.triggered.connect(self._on_redo)
        edit_menu.addAction(self.redo_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _on_creature_changed(self):
        """Handle creature parameter changes."""
        # Save current state for undo
        state = self.control_panel.get_state()
        self._save_state(state)

        # Rebuild creature in renderer
        self._rebuild_creature_from_state(state)

        # Update undo/redo button states
        self._update_undo_redo_state()

    def _save_state(self, state):
        """Save state for undo/redo."""
        self.state_manager.save_state(
            num_tentacles=state['num_tentacles'],
            segments=state['segments'],
            algorithm=state['algorithm'],
            params=state['params'],
            thickness_base=state['thickness_base'],
            taper_factor=state['taper_factor'],
            branch_depth=state.get('branch_depth', 0),
            branch_count=state.get('branch_count', 1),
            body_scale=state.get('body_scale', 1.2),
            tentacle_color=state.get('tentacle_color', (0.6, 0.3, 0.7)),
            hue_shift=state.get('hue_shift', 0.1),
            anim_speed=state.get('anim_speed', 2.0),
            wave_amplitude=state.get('wave_amplitude', 0.05),
            pulse_speed=state.get('pulse_speed', 1.5),
            pulse_amount=state.get('pulse_amount', 0.05)
        )

    def _on_undo(self):
        """Handle undo request."""
        state = self.state_manager.undo()
        if state:
            self.control_panel.set_state(state)
            self._update_undo_redo_state()
            self._rebuild_creature_from_state(state)

    def _on_redo(self):
        """Handle redo request."""
        state = self.state_manager.redo()
        if state:
            self.control_panel.set_state(state)
            self._update_undo_redo_state()
            self._rebuild_creature_from_state(state)

    def _rebuild_creature_from_state(self, state):
        """Rebuild creature from state dict."""
        self.renderer.rebuild_creature(
            num_tentacles=state['num_tentacles'],
            segments=state['segments'],
            algorithm=state['algorithm'],
            params=state['params'],
            thickness_base=state['thickness_base'],
            taper_factor=state['taper_factor'],
            branch_depth=state.get('branch_depth', 0),
            branch_count=state.get('branch_count', 1),
            body_scale=state.get('body_scale', 1.2),
            tentacle_color=state.get('tentacle_color', (0.6, 0.3, 0.7)),
            hue_shift=state.get('hue_shift', 0.1),
            anim_speed=state.get('anim_speed', 2.0),
            wave_amplitude=state.get('wave_amplitude', 0.05),
            pulse_speed=state.get('pulse_speed', 1.5),
            pulse_amount=state.get('pulse_amount', 0.05)
        )

    def _update_undo_redo_state(self):
        """Update undo/redo button and menu enabled states."""
        can_undo = self.state_manager.can_undo()
        can_redo = self.state_manager.can_redo()

        # Update control panel buttons
        self.control_panel.set_undo_redo_enabled(can_undo, can_redo)

        # Update menu actions
        self.undo_action.setEnabled(can_undo)
        self.redo_action.setEnabled(can_redo)

    def _on_attack(self):
        """Handle attack button press."""
        self.renderer.trigger_attack()

    def _on_export(self):
        """Handle export to JSON."""
        # Get current state
        state = self.control_panel.get_state()

        # Create DNA config dict
        dna_config = {
            'num_tentacles': state['num_tentacles'],
            'segments_per_tentacle': state['segments'],
            'algorithm': state['algorithm'],
            'algorithm_params': state['params'],
            'thickness_base': state['thickness_base'],
            'taper_factor': state['taper_factor'],
            'branch_depth': state.get('branch_depth', 0),
            'branch_count': state.get('branch_count', 1),
            'body_scale': state.get('body_scale', 1.2),
            'tentacle_color': state.get('tentacle_color', (0.6, 0.3, 0.7)),
            'hue_shift': state.get('hue_shift', 0.1),
            'anim_speed': state.get('anim_speed', 2.0),
            'wave_amplitude': state.get('wave_amplitude', 0.05),
            'pulse_speed': state.get('pulse_speed', 1.5),
            'pulse_amount': state.get('pulse_amount', 0.05)
        }

        # Open save dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export DNA Configuration",
            "creature_dna.json",
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(dna_config, f, indent=2)

                QMessageBox.information(
                    self,
                    "Export Successful",
                    f"DNA configuration exported to:\n{file_path}"
                )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Failed",
                    f"Failed to export DNA:\n{str(e)}"
                )

    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About DNA Editor",
            "<h2>DNA Editor - Creature Tentacle Generator</h2>"
            "<p>Interactive 3D tool for designing procedural tentacle creatures "
            "using mathematical curve algorithms.</p>"
            "<p><b>Algorithms:</b></p>"
            "<ul>"
            "<li><b>Bezier Curves</b> - Smooth cubic polynomial curves</li>"
            "<li><b>Fourier Series</b> - Wave composition for organic shapes</li>"
            "</ul>"
            "<p><b>Controls:</b></p>"
            "<ul>"
            "<li>Adjust parameters with sliders</li>"
            "<li>Use presets for quick configurations</li>"
            "<li>Undo/Redo (Ctrl+Z / Ctrl+Y)</li>"
            "<li>Export to JSON (Ctrl+E)</li>"
            "</ul>"
            "<p><b>Camera:</b></p>"
            "<ul>"
            "<li>Mouse Drag - Rotate view</li>"
            "<li>Scroll - Zoom in/out</li>"
            "<li>R - Reset camera</li>"
            "</ul>"
            "<p>Built with PyQt6 and Ursina Engine</p>"
        )

    def closeEvent(self, event):
        """Handle window close event."""
        # Cleanup renderer
        self.renderer.cleanup()

        # Accept close
        event.accept()
