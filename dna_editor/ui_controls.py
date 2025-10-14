"""
UI Controls - User interface for creature parameter editing

Provides an overlay UI for adjusting creature parameters in real-time.
Uses Ursina's built-in UI components.
"""

from ursina import Entity, Text, Button, camera, color as ursina_color, destroy
from ursina import ButtonList


class ControlPanel(Entity):
    """
    UI overlay panel for creature parameter controls.
    """

    def __init__(self, preset_manager, on_parameters_changed):
        """
        Initialize control panel.

        Args:
            preset_manager: PresetManager instance
            on_parameters_changed: Callback function(params_dict)
        """
        super().__init__()
        self.preset_manager = preset_manager
        self.on_parameters_changed = on_parameters_changed
        self.current_params = preset_manager.get_default_parameters()
        self.ui_elements = []

        # Create UI
        self._create_title()
        self._create_preset_selector()
        self._create_quick_controls()
        self._create_stats_display()

        # Initially hidden
        self.enabled = False

    def _create_title(self):
        """Create title text"""
        title = Text(
            text="DNA CREATURE EDITOR",
            position=(-0.85, 0.45),
            origin=(-0.5, 0.5),
            scale=1.5,
            color=ursina_color.rgb(0.9, 0.7, 1.0),
            parent=camera.ui
        )
        self.ui_elements.append(title)

        subtitle = Text(
            text="Tentacle Horror Designer v1.0",
            position=(-0.85, 0.42),
            origin=(-0.5, 0.5),
            scale=0.8,
            color=ursina_color.rgb(0.7, 0.7, 0.8),
            parent=camera.ui
        )
        self.ui_elements.append(subtitle)

    def _create_preset_selector(self):
        """Create preset dropdown and management buttons"""
        # Preset label
        label = Text(
            text="PRESET:",
            position=(-0.85, 0.35),
            origin=(-0.5, 0.5),
            scale=1.0,
            color=ursina_color.rgb(0.9, 0.9, 0.9),
            parent=camera.ui
        )
        self.ui_elements.append(label)

        # Current preset name display
        self.preset_name_text = Text(
            text=self.current_params.get('preset_name', 'None'),
            position=(-0.85, 0.31),
            origin=(-0.5, 0.5),
            scale=0.9,
            color=ursina_color.rgb(0.8, 0.9, 1.0),
            parent=camera.ui
        )
        self.ui_elements.append(self.preset_name_text)

        # Preset management buttons
        button_y = 0.25
        button_x = -0.85

        # Load preset buttons (cycle through presets)
        prev_button = Button(
            text="< PREV",
            scale=(0.08, 0.04),
            position=(button_x, button_y),
            parent=camera.ui,
            on_click=self._load_previous_preset,
            color=ursina_color.rgb(0.3, 0.3, 0.4)
        )
        self.ui_elements.append(prev_button)

        next_button = Button(
            text="NEXT >",
            scale=(0.08, 0.04),
            position=(button_x + 0.09, button_y),
            parent=camera.ui,
            on_click=self._load_next_preset,
            color=ursina_color.rgb(0.3, 0.3, 0.4)
        )
        self.ui_elements.append(next_button)

        # New preset button
        new_button = Button(
            text="NEW",
            scale=(0.08, 0.04),
            position=(button_x + 0.18, button_y),
            parent=camera.ui,
            on_click=self._new_preset,
            color=ursina_color.rgb(0.2, 0.5, 0.3)
        )
        self.ui_elements.append(new_button)

        # Randomize button
        random_button = Button(
            text="RANDOM",
            scale=(0.08, 0.04),
            position=(button_x + 0.27, button_y),
            parent=camera.ui,
            on_click=self._randomize_creature,
            color=ursina_color.rgb(0.5, 0.3, 0.5)
        )
        self.ui_elements.append(random_button)

    def _create_quick_controls(self):
        """Create quick adjustment controls for key parameters"""
        controls_y = 0.15
        label_x = -0.85
        button_x = -0.60

        # Helper function to create a parameter control row
        def create_control_row(label_text, param_key, y_pos, min_val, max_val, step, format_str="{:.1f}"):
            # Label
            label = Text(
                text=label_text,
                position=(label_x, y_pos),
                origin=(-0.5, 0.5),
                scale=0.7,
                color=ursina_color.rgb(0.8, 0.8, 0.8),
                parent=camera.ui
            )
            self.ui_elements.append(label)

            # Value display
            value_text = Text(
                text=format_str.format(self.current_params.get(param_key, 0)),
                position=(button_x, y_pos),
                origin=(0, 0.5),
                scale=0.7,
                color=ursina_color.rgb(0.9, 1.0, 0.9),
                parent=camera.ui
            )
            self.ui_elements.append(value_text)

            # - button
            minus_btn = Button(
                text="-",
                scale=(0.03, 0.03),
                position=(button_x + 0.05, y_pos),
                parent=camera.ui,
                on_click=lambda: self._adjust_parameter(param_key, -step, min_val, max_val, value_text, format_str),
                color=ursina_color.rgb(0.4, 0.2, 0.2)
            )
            self.ui_elements.append(minus_btn)

            # + button
            plus_btn = Button(
                text="+",
                scale=(0.03, 0.03),
                position=(button_x + 0.09, y_pos),
                parent=camera.ui,
                on_click=lambda: self._adjust_parameter(param_key, step, min_val, max_val, value_text, format_str),
                color=ursina_color.rgb(0.2, 0.4, 0.2)
            )
            self.ui_elements.append(plus_btn)

            return value_text

        # Create controls for key parameters
        current_y = controls_y

        # Body parameters
        self._create_section_header("BODY", current_y)
        current_y -= 0.04
        self.value_texts = {}
        self.value_texts['body_size'] = create_control_row("Size:", 'body_size', current_y, 0.3, 1.2, 0.1)
        current_y -= 0.04
        self.value_texts['body_hue'] = create_control_row("Hue:", 'body_hue', current_y, 0, 360, 20, "{:.0f}")
        current_y -= 0.05

        # Tentacle parameters
        self._create_section_header("TENTACLES", current_y)
        current_y -= 0.04
        self.value_texts['tentacle_count'] = create_control_row("Count:", 'tentacle_count', current_y, 4, 12, 1, "{:.0f}")
        current_y -= 0.04
        self.value_texts['base_length'] = create_control_row("Length:", 'base_length', current_y, 0.8, 3.0, 0.2)
        current_y -= 0.04
        self.value_texts['segments'] = create_control_row("Segments:", 'segments', current_y, 5, 15, 1, "{:.0f}")
        current_y -= 0.05

        # Animation parameters
        self._create_section_header("ANIMATION", current_y)
        current_y -= 0.04
        self.value_texts['wave_speed'] = create_control_row("Speed:", 'wave_speed', current_y, 0.5, 5.0, 0.5)
        current_y -= 0.04
        self.value_texts['wave_amplitude'] = create_control_row("Amplitude:", 'wave_amplitude', current_y, 5, 40, 5, "{:.0f}")
        current_y -= 0.05

        # Decorations
        self._create_section_header("DECORATIONS", current_y)
        current_y -= 0.04
        self.value_texts['eye_count'] = create_control_row("Eyes:", 'eye_count', current_y, 0, 8, 1, "{:.0f}")
        current_y -= 0.04
        self.value_texts['spike_count'] = create_control_row("Spikes:", 'spike_count', current_y, 0, 30, 5, "{:.0f}")

    def _create_section_header(self, text, y_pos):
        """Create a section header"""
        header = Text(
            text=text,
            position=(-0.85, y_pos),
            origin=(-0.5, 0.5),
            scale=0.8,
            color=ursina_color.rgb(1.0, 0.9, 0.6),
            parent=camera.ui
        )
        self.ui_elements.append(header)

    def _create_stats_display(self):
        """Create stats/info display at bottom"""
        self.stats_text = Text(
            text="Entities: 0 | Press 'H' to toggle help",
            position=(-0.85, -0.45),
            origin=(-0.5, 0.5),
            scale=0.6,
            color=ursina_color.rgb(0.7, 0.7, 0.7),
            parent=camera.ui
        )
        self.ui_elements.append(self.stats_text)

    def _adjust_parameter(self, param_key, delta, min_val, max_val, value_text, format_str):
        """Adjust a parameter value"""
        current = self.current_params.get(param_key, 0)
        new_value = max(min_val, min(max_val, current + delta))

        # Handle integer parameters
        if isinstance(self.current_params.get(param_key, 0), int):
            new_value = int(new_value)

        self.current_params[param_key] = new_value
        value_text.text = format_str.format(new_value)

        # Trigger rebuild
        self.on_parameters_changed(self.current_params)

    def _load_previous_preset(self):
        """Load previous preset in list"""
        names = self.preset_manager.get_preset_names()
        if not names:
            return

        current_name = self.current_params.get('preset_name', '')
        try:
            current_index = names.index(current_name)
            prev_index = (current_index - 1) % len(names)
        except ValueError:
            prev_index = 0

        self._load_preset_by_name(names[prev_index])

    def _load_next_preset(self):
        """Load next preset in list"""
        names = self.preset_manager.get_preset_names()
        if not names:
            return

        current_name = self.current_params.get('preset_name', '')
        try:
            current_index = names.index(current_name)
            next_index = (current_index + 1) % len(names)
        except ValueError:
            next_index = 0

        self._load_preset_by_name(names[next_index])

    def _load_preset_by_name(self, name):
        """Load a specific preset"""
        params = self.preset_manager.load_preset(name)
        if params:
            self.current_params = params
            self.preset_name_text.text = name
            # Update value displays
            for param_key, value_text in self.value_texts.items():
                value = self.current_params.get(param_key, 0)
                if isinstance(value, int):
                    value_text.text = f"{value:.0f}"
                else:
                    value_text.text = f"{value:.1f}"
            # Trigger rebuild
            self.on_parameters_changed(self.current_params)

    def _new_preset(self):
        """Create new preset with default parameters"""
        self.current_params = self.preset_manager.get_default_parameters()
        self.preset_name_text.text = "New Creature"
        # Update value displays
        for param_key, value_text in self.value_texts.items():
            value = self.current_params.get(param_key, 0)
            if isinstance(value, int):
                value_text.text = f"{value:.0f}"
            else:
                value_text.text = f"{value:.1f}"
        # Trigger rebuild
        self.on_parameters_changed(self.current_params)

    def _randomize_creature(self):
        """Randomize creature parameters"""
        import random

        self.current_params.update({
            'body_size': random.uniform(0.4, 1.0),
            'body_hue': random.randint(0, 360),
            'tentacle_count': random.randint(4, 12),
            'base_length': random.uniform(1.5, 2.8),
            'segments': random.randint(7, 13),
            'eye_count': random.randint(0, 8),
            'spike_count': random.randint(0, 30),
            'wave_speed': random.uniform(1.0, 4.0),
            'wave_amplitude': random.randint(10, 35)
        })

        self.preset_name_text.text = "Random Creature"

        # Update value displays
        for param_key, value_text in self.value_texts.items():
            value = self.current_params.get(param_key, 0)
            if isinstance(value, int):
                value_text.text = f"{value:.0f}"
            else:
                value_text.text = f"{value:.1f}"

        # Trigger rebuild
        self.on_parameters_changed(self.current_params)

    def update_stats(self, stats_dict):
        """Update stats display"""
        entity_count = stats_dict.get('entity_count', 0)
        self.stats_text.text = f"Entities: {entity_count} | Press 'H' to toggle help"

    def show(self):
        """Show the control panel"""
        self.enabled = True
        for element in self.ui_elements:
            element.enabled = True

    def hide(self):
        """Hide the control panel"""
        self.enabled = False
        for element in self.ui_elements:
            element.enabled = False

    def cleanup(self):
        """Clean up UI elements"""
        for element in self.ui_elements:
            destroy(element)
        self.ui_elements.clear()
