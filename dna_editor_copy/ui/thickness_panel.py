"""
Thickness panel - controls for tentacle thickness and taper.
"""

from ursina import Text, Slider, color


class ThicknessPanel:
    """Panel for thickness and taper controls."""

    def __init__(self, on_thickness_changed):
        """
        Create thickness panel.

        Args:
            on_thickness_changed: Callback when thickness values change
        """
        self.on_thickness_changed = on_thickness_changed
        self.elements = []

        y_pos = 0.19

        # Section label
        self.thickness_label = Text(
            text="Thickness:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.9,
            color=color.rgb(0.7, 0.9, 1.0)
        )
        self.elements.append(self.thickness_label)

        # Base thickness
        y_pos -= 0.05
        self.thickness_base_label = Text(
            text="Base:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.white
        )
        self.elements.append(self.thickness_base_label)

        self.thickness_base_slider = Slider(
            min=0.1, max=0.5, default=0.25, step=0.05,
            position=(-0.65, y_pos - 0.01),
            width=0.2, height=0.02,
            on_value_changed=self.on_thickness_changed
        )
        self.elements.append(self.thickness_base_slider)

        self.thickness_base_value = Text(
            text="0.25",
            position=(-0.42, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.rgb(0.5, 1.0, 0.5)
        )
        self.elements.append(self.thickness_base_value)

        # Taper
        y_pos -= 0.05
        self.taper_label = Text(
            text="Taper:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.white
        )
        self.elements.append(self.taper_label)

        self.taper_slider = Slider(
            min=0.0, max=1.0, default=0.6, step=0.1,
            position=(-0.65, y_pos - 0.01),
            width=0.2, height=0.02,
            on_value_changed=self.on_thickness_changed
        )
        self.elements.append(self.taper_slider)

        self.taper_value = Text(
            text="0.6",
            position=(-0.42, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.rgb(0.5, 1.0, 0.5)
        )
        self.elements.append(self.taper_value)

    def update(self, thickness_base, taper_factor):
        """
        Update slider values and text.

        Args:
            thickness_base: Base thickness value
            taper_factor: Taper factor value
        """
        self.thickness_base_slider.value = thickness_base
        self.thickness_base_value.text = f"{thickness_base:.2f}"
        self.taper_slider.value = taper_factor
        self.taper_value.text = f"{taper_factor:.1f}"

    def get_values(self):
        """Get current thickness values."""
        return {
            'thickness_base': self.thickness_base_slider.value,
            'taper_factor': self.taper_slider.value
        }

    def get_elements(self):
        """Return all UI elements for cleanup."""
        return self.elements
