"""
Presets panel - quick preset buttons for common configurations.
"""

from ursina import Text, Button, color
from ..core.constants import PRESETS


class PresetsPanel:
    """Panel with preset buttons."""

    def __init__(self, on_preset_clicked):
        """
        Create presets panel.

        Args:
            on_preset_clicked: Callback(algorithm, params) when preset clicked
        """
        self.on_preset_clicked = on_preset_clicked
        self.elements = []

        y_pos = 0.01

        # Section label
        self.presets_label = Text(
            text="Presets:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.9,
            color=color.rgb(0.7, 0.9, 1.0)
        )
        self.elements.append(self.presets_label)

        # Create preset buttons from constants
        y_pos -= 0.05
        self.preset_buttons = []
        x_offset = 0

        for name, algo, params in PRESETS:
            btn = Button(
                text=name,
                color=color.rgb(0.3, 0.4, 0.3),
                scale=(0.12, 0.035),
                position=(-0.85 + x_offset, y_pos),
                on_click=lambda a=algo, p=params: self.on_preset_clicked(a, p)
            )
            self.preset_buttons.append(btn)
            self.elements.append(btn)
            x_offset += 0.30

        # Help text (bottom corner)
        self.help_text = Text(
            text="Press H for help",
            position=(-0.95, -0.45),
            origin=(0, 0),
            scale=0.8,
            color=color.rgb(0.5, 0.5, 0.6)
        )
        self.elements.append(self.help_text)

    def get_elements(self):
        """Return all UI elements for cleanup."""
        return self.elements
