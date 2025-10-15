"""
Info panel - displays creature stats and algorithm selection buttons.
"""

from ursina import Text, Button, color


class InfoPanel:
    """Top panel showing tentacles, segments, algorithm info and buttons."""

    def __init__(self, on_algorithm_changed):
        """
        Create info panel.

        Args:
            on_algorithm_changed: Callback when algorithm button clicked
        """
        self.on_algorithm_changed = on_algorithm_changed
        self.elements = []

        # Title and info text
        self.info_text = Text(
            text="",
            position=(-0.85, 0.47),
            origin=(0, 0),
            scale=1.0,
            color=color.white,
            background=True
        )
        self.elements.append(self.info_text)

        # Algorithm buttons
        y_pos = 0.40

        self.btn_bezier = Button(
            text='BEZIER',
            color=color.rgb(0.3, 0.3, 0.4),
            scale=(0.15, 0.04),
            position=(-0.55, y_pos),
            on_click=lambda: self.on_algorithm_changed('bezier')
        )
        self.elements.append(self.btn_bezier)

        self.btn_fourier = Button(
            text='FOURIER',
            color=color.rgb(0.3, 0.3, 0.4),
            scale=(0.15, 0.04),
            position=(-0.25, y_pos),
            on_click=lambda: self.on_algorithm_changed('fourier')
        )
        self.elements.append(self.btn_fourier)

    def update(self, num_tentacles, segments, algorithm):
        """
        Update displayed information.

        Args:
            num_tentacles: Current tentacle count
            segments: Current segment count
            algorithm: Current algorithm name
        """
        self.info_text.text = (
            f"Tentacles: {num_tentacles}  |  "
            f"Segments: {segments}  |  "
            f"Algorithm: {algorithm.upper()}"
        )

        # Highlight active button
        self.btn_bezier.color = (
            color.rgb(0.5, 0.7, 0.5) if algorithm == 'bezier'
            else color.rgb(0.3, 0.3, 0.4)
        )
        self.btn_fourier.color = (
            color.rgb(0.5, 0.7, 0.5) if algorithm == 'fourier'
            else color.rgb(0.3, 0.3, 0.4)
        )

    def get_elements(self):
        """Return all UI elements for cleanup."""
        return self.elements
