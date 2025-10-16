"""
Parameters panel - algorithm-specific parameter controls.
"""

from ursina import Text, Slider, color


class ParametersPanel:
    """Panel with algorithm-specific sliders (Bezier/Fourier)."""

    def __init__(self, on_param_changed):
        """
        Create parameters panel.

        Args:
            on_param_changed: Callback when any parameter changes
        """
        self.on_param_changed = on_param_changed
        self.elements = []

        y_pos = 0.32

        # Section label
        self.param_label = Text(
            text="Algorithm Parameters:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.9,
            color=color.rgb(0.7, 0.9, 1.0)
        )
        self.elements.append(self.param_label)

        # Bezier controls
        y_pos -= 0.05
        self._create_bezier_controls(y_pos)

        # Fourier controls
        self._create_fourier_controls(y_pos)

    def _create_bezier_controls(self, y_pos):
        """Create Bezier-specific controls."""
        self.bezier_strength_label = Text(
            text="Control Strength:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.white,
            visible=False
        )
        self.elements.append(self.bezier_strength_label)

        self.bezier_strength_slider = Slider(
            min=0.1, max=0.8, default=0.4, step=0.05,
            position=(-0.6, y_pos - 0.01),
            width=0.2, height=0.02,
            on_value_changed=self.on_param_changed,
            visible=False
        )
        self.elements.append(self.bezier_strength_slider)

        self.bezier_strength_value = Text(
            text="0.40",
            position=(-0.37, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.rgb(0.5, 1.0, 0.5),
            visible=False
        )
        self.elements.append(self.bezier_strength_value)

    def _create_fourier_controls(self, y_pos):
        """Create Fourier-specific controls."""
        # Wave count
        self.fourier_waves_label = Text(
            text="Wave Count:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.white,
            visible=False
        )
        self.elements.append(self.fourier_waves_label)

        self.fourier_waves_slider = Slider(
            min=1, max=7, default=3, step=1,
            position=(-0.6, y_pos - 0.01),
            width=0.2, height=0.02,
            on_value_changed=self.on_param_changed,
            visible=False
        )
        self.elements.append(self.fourier_waves_slider)

        self.fourier_waves_value = Text(
            text="3",
            position=(-0.37, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.rgb(0.5, 1.0, 0.5),
            visible=False
        )
        self.elements.append(self.fourier_waves_value)

        # Amplitude
        y_pos -= 0.05
        self.fourier_amp_label = Text(
            text="Amplitude:",
            position=(-0.85, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.white,
            visible=False
        )
        self.elements.append(self.fourier_amp_label)

        self.fourier_amp_slider = Slider(
            min=0.05, max=0.4, default=0.15, step=0.05,
            position=(-0.6, y_pos - 0.01),
            width=0.2, height=0.02,
            on_value_changed=self.on_param_changed,
            visible=False
        )
        self.elements.append(self.fourier_amp_slider)

        self.fourier_amp_value = Text(
            text="0.15",
            position=(-0.37, y_pos),
            origin=(0, 0),
            scale=0.8,
            color=color.rgb(0.5, 1.0, 0.5),
            visible=False
        )
        self.elements.append(self.fourier_amp_value)

    def update(self, algorithm, params):
        """
        Update visibility and values based on current algorithm.

        Args:
            algorithm: 'bezier' or 'fourier'
            params: Dict of algorithm parameters
        """
        is_bezier = algorithm == 'bezier'
        is_fourier = algorithm == 'fourier'

        # Show/hide Bezier controls
        self.bezier_strength_label.visible = is_bezier
        self.bezier_strength_slider.visible = is_bezier
        self.bezier_strength_value.visible = is_bezier

        # Show/hide Fourier controls
        self.fourier_waves_label.visible = is_fourier
        self.fourier_waves_slider.visible = is_fourier
        self.fourier_waves_value.visible = is_fourier
        self.fourier_amp_label.visible = is_fourier
        self.fourier_amp_slider.visible = is_fourier
        self.fourier_amp_value.visible = is_fourier

        # Update values
        if is_bezier:
            val = params.get('control_strength', 0.4)
            self.bezier_strength_slider.value = val
            self.bezier_strength_value.text = f"{val:.2f}"
        elif is_fourier:
            waves = params.get('num_waves', 3)
            amp = params.get('amplitude', 0.15)
            self.fourier_waves_slider.value = waves
            self.fourier_waves_value.text = f"{int(waves)}"
            self.fourier_amp_slider.value = amp
            self.fourier_amp_value.text = f"{amp:.2f}"

    def get_bezier_params(self):
        """Get current Bezier parameter values."""
        return {'control_strength': self.bezier_strength_slider.value}

    def get_fourier_params(self):
        """Get current Fourier parameter values."""
        return {
            'num_waves': int(self.fourier_waves_slider.value),
            'amplitude': self.fourier_amp_slider.value
        }

    def get_elements(self):
        """Return all UI elements for cleanup."""
        return self.elements
