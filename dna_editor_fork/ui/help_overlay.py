"""
Help overlay - displays keyboard controls and usage instructions.
"""

from ursina import Text, color


class HelpOverlay:
    """Full-screen help overlay with controls documentation."""

    def __init__(self):
        """Create help overlay (initially hidden)."""
        self.visible = False
        self.elements = []

        help_text = """DNA EDITOR - CONTROLS

CAMERA:
  Mouse Drag - Orbit camera
  Scroll - Zoom in/out
  R - Reset camera

TENTACLES:
  1/2/3 - Set tentacle count
  +/- - Adjust segment count (5-20)

ALGORITHM:
  Q - Bezier (smooth curves)
  W - Fourier (wave composition)
  Sliders - Adjust parameters

EDITING:
  Ctrl+Z - Undo
  Ctrl+Y - Redo
  Presets - Click preset buttons

OTHER:
  H - Toggle this help
  ESC - Quit"""

        self.overlay = Text(
            text=help_text,
            x=0,
            y=0,
            origin=(0, 0),
            scale=0.8,
            color=color.white,
            background=True,
            visible=False
        )
        self.elements.append(self.overlay)

    def toggle(self):
        """Toggle help overlay visibility."""
        self.visible = not self.visible
        self.overlay.visible = self.visible
        return self.visible
