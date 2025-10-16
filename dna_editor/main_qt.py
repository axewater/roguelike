"""
DNA Editor - PyQt6 Version

Interactive 3D editor for creating tentacle creatures using mathematical curves.

Usage:
    python3 dna_editor_copy/main_qt.py

Features:
- PyQt6 controls with precise layout
- Real-time 3D preview (Ursina in separate window)
- Undo/Redo system (50 steps)
- Export DNA to JSON
- Preset configurations
"""

import sys
import os

# Add parent directory to path for imports
if __name__ == "__main__":
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from dna_editor_copy.qt_ui import EditorWindow


def main():
    """Main entry point."""
    print("=" * 70)
    print("DNA EDITOR - PYQT6 VERSION")
    print("=" * 70)
    print("Starting DNA Editor with PyQt6 UI...")
    print()
    print("Features:")
    print("  - PyQt6 control panel with sliders and spinboxes")
    print("  - Ursina 3D viewport (separate window)")
    print("  - Undo/Redo (Ctrl+Z / Ctrl+Y)")
    print("  - Export to JSON (Ctrl+E)")
    print("  - Preset configurations")
    print()
    print("Camera Controls (in 3D window):")
    print("  - Mouse Drag - Rotate camera")
    print("  - Scroll - Zoom in/out")
    print("  - R - Reset camera")
    print("=" * 70)
    print()

    # Create Qt application
    app = QApplication(sys.argv)

    # Set application style
    app.setStyle("Fusion")

    # Create main window
    window = EditorWindow()
    window.show()

    print("✓ Application started")
    print("✓ Use the control panel to adjust creature parameters")
    print()

    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
