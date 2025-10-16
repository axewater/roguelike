"""
Thickness panel - controls for tentacle thickness and taper.
"""

from ursina import Text, Slider, color, window


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

        y_pos = 0.16

        # Section label
        self.thickness_label = Text(
            text="Thickness:",
            x=window.left[0] + 0.02,
            y=y_pos,
            origin=(0, 0),
            scale=0.9,
            color=color.rgb(0.7, 0.9, 1.0)
        )
        self.elements.append(self.thickness_label)

        # Base thickness
        y_pos -= 0.05
        self.thickness_base_label = Text(
            text="Base:",
            x=window.left[0] + 0.02,
            y=y_pos,
            origin=(0, 0),
            scale=0.8,
            color=color.white
        )
        self.elements.append(self.thickness_base_label)

        self.thickness_base_slider = Slider(
            min=0.1, max=0.5, default=0.25, step=0.05,
            x=window.left[0] + 0.22,
            y=y_pos - 0.01,
            width=0.2, height=0.02,
            on_value_changed=self.on_thickness_changed
        )
        self.elements.append(self.thickness_base_slider)

        # Taper
        y_pos -= 0.06
        self.taper_label = Text(
            text="Taper:",
            x=window.left[0] + 0.02,
            y=y_pos,
            origin=(0, 0),
            scale=0.8,
            color=color.white
        )
        self.elements.append(self.taper_label)

        self.taper_slider = Slider(
            min=0.0, max=1.0, default=0.6, step=0.1,
            x=window.left[0] + 0.22,
            y=y_pos - 0.01,
            width=0.2, height=0.02,
            on_value_changed=self.on_thickness_changed
        )
        self.elements.append(self.taper_slider)

    def update(self, thickness_base, taper_factor):
        """
        Update slider values.

        Args:
            thickness_base: Base thickness value
            taper_factor: Taper factor value
        """
        self.thickness_base_slider.value = thickness_base
        self.taper_slider.value = taper_factor

    def get_values(self):
        """Get current thickness values."""
        return {
            'thickness_base': self.thickness_base_slider.value,
            'taper_factor': self.taper_slider.value
        }
