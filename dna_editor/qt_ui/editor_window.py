"""
Main editor window - orchestrates control panel and 3D renderer.

Handles undo/redo, file export, and coordinate updates between UI and 3D.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QFileDialog, QMessageBox
)
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt
import json
import sys
import os

from .control_panel import ControlPanel
from .ursina_renderer import UrsinaRenderer
from ..controllers.state_manager import StateManager


class EditorWindow(QMainWindow):
    """Main DNA Editor window."""

    def __init__(self):
        """Initialize editor window."""
        super().__init__()

        self.state_manager = StateManager()

        self.setWindowTitle("DNA Editor - Controls")
        self.setFixedSize(360, 750)
        self.move(50, 100)

        self._init_ui()
        self._init_menu()

        # Initial creature build
        self._on_creature_changed()

        print("✓ Editor window initialized")

    def _init_ui(self):
        """Initialize UI layout."""
        # Central widget with vertical layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Control panel
        self.control_panel = ControlPanel()
        self.control_panel.creature_changed.connect(self._on_creature_changed)
        self.control_panel.undo_requested.connect(self._on_undo)
        self.control_panel.redo_requested.connect(self._on_redo)
        self.control_panel.export_requested.connect(self._on_export)
        layout.addWidget(self.control_panel)

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
        self.renderer.rebuild_creature(
            num_tentacles=state['num_tentacles'],
            segments=state['segments'],
            algorithm=state['algorithm'],
            params=state['params'],
            thickness_base=state['thickness_base'],
            taper_factor=state['taper_factor']
        )

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
            taper_factor=state['taper_factor']
        )

    def _on_undo(self):
        """Handle undo request."""
        state = self.state_manager.undo()
        if state:
            self.control_panel.set_state(state)
            self._update_undo_redo_state()

            # Rebuild creature
            self.renderer.rebuild_creature(
                num_tentacles=state['num_tentacles'],
                segments=state['segments'],
                algorithm=state['algorithm'],
                params=state['params'],
                thickness_base=state['thickness_base'],
                taper_factor=state['taper_factor']
            )

    def _on_redo(self):
        """Handle redo request."""
        state = self.state_manager.redo()
        if state:
            self.control_panel.set_state(state)
            self._update_undo_redo_state()

            # Rebuild creature
            self.renderer.rebuild_creature(
                num_tentacles=state['num_tentacles'],
                segments=state['segments'],
                algorithm=state['algorithm'],
                params=state['params'],
                thickness_base=state['thickness_base'],
                taper_factor=state['taper_factor']
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
            'taper_factor': state['taper_factor']
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
                print(f"✓ Exported DNA to: {file_path}")

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Export Failed",
                    f"Failed to export DNA:\n{str(e)}"
                )
                print(f"✗ Export failed: {e}")

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
        print("Closing editor...")

        # Cleanup renderer
        self.renderer.cleanup()

        # Accept close
        event.accept()
        print("✓ Editor closed")
