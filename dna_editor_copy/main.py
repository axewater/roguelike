"""
DNA Editor - Creature Tentacle Generator

Interactive 3D editor for creating tentacle creatures using mathematical curves.

Two mathematical algorithms for generating organic tentacles:
1. Bezier Curves - Cubic polynomial curves with control points
2. Fourier Series - Wave composition for organic shapes

FEATURES:
- Real-time parameter sliders for all algorithms
- Thickness & taper controls with live preview
- Preset system (3 built-in presets)
- Undo/Redo system (up to 50 steps)
- Interactive help overlay (Press H)
- Enhanced UI with algorithm-specific controls

Usage:
    python3 dna_editor/main.py

Controls:
    H - Toggle help overlay
    1/2/3 - Set tentacle count
    Q/W - Switch algorithm
    +/- - Adjust segments
    Sliders - Adjust parameters
    Presets - Quick preset buttons
    Ctrl+Z - Undo
    Ctrl+Y - Redo
    Mouse Drag - Orbit camera
    Scroll - Zoom
    R - Reset camera
"""

import sys
import os

# Add parent directory to path to enable package imports when run directly
if __name__ == "__main__":
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

from ursina import Ursina, Entity, camera, color, window
from dna_editor.controllers import EditorController


def main():
    """Main entry point."""
    app = Ursina(
        title="DNA Editor - Creature Tentacle Generator",
        borderless=False,
        fullscreen=False
    )

    window.size = (1400, 900)
    window.position = (100, 50)
    window.color = color.rgb(0.05, 0.05, 0.1)

    camera.fov = 60

    # Create editor controller
    editor = EditorController()

    # Create Entity wrapper to ensure update() is called every frame
    class EditorUpdater(Entity):
        def __init__(self, editor_controller):
            super().__init__()
            self.editor = editor_controller

        def update(self):
            self.editor.update()

    # Instantiate the updater
    updater = EditorUpdater(editor)

    app.run()


if __name__ == "__main__":
    main()
