"""
UI Controls - User interface for creature parameter editing

Provides an overlay UI for adjusting creature parameters in real-time.
Uses Ursina's built-in UI components with centralized layout constants.
"""

from ursina import Entity, Text, Button, camera, destroy
from ui_constants import *


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
        self.value_texts = {}  # Track value displays for updates
        self.choice_texts = {}  # Track choice displays for updates
        self.save_input = None  # Save dialog input field

        # Create UI sections
        self._create_title()
        self._create_preset_selector()
        self._create_parameter_controls()
        self._create_stats_display()

        # Initially hidden
        self.enabled = False

    def _create_title(self):
        """Create title section"""
        title = Text(
            text="DNA CREATURE EDITOR",
            position=(UI_LEFT_MARGIN, UI_TOP_MARGIN),
            origin=(-0.5, 0.5),
            scale=TITLE_SCALE,
            color=COLOR_TITLE,
            parent=camera.ui
        )
        self.ui_elements.append(title)

        subtitle = Text(
            text="Tentacle Horror Designer v1.2",
            position=(UI_LEFT_MARGIN, UI_TOP_MARGIN - TITLE_SPACING),
            origin=(-0.5, 0.5),
            scale=SUBTITLE_SCALE,
            color=COLOR_SUBTITLE,
            parent=camera.ui
        )
        self.ui_elements.append(subtitle)

    def _create_preset_selector(self):
        """Create preset management section"""
        # Starting Y position (below title)
        preset_y = UI_TOP_MARGIN - TITLE_SPACING - 0.06

        # Preset label
        label = Text(
            text="PRESET:",
            position=(UI_LEFT_MARGIN, preset_y),
            origin=(-0.5, 0.5),
            scale=1.0,
            color=COLOR_LABEL,
            parent=camera.ui
        )
        self.ui_elements.append(label)

        # Current preset name display
        self.preset_name_text = Text(
            text=self.current_params.get('preset_name', 'None'),
            position=(UI_LEFT_MARGIN, preset_y - 0.04),
            origin=(-0.5, 0.5),
            scale=0.9,
            color=COLOR_VALUE_HIGHLIGHT,
            parent=camera.ui
        )
        self.ui_elements.append(self.preset_name_text)

        # Preset management buttons (two rows for better spacing)
        button_y1 = preset_y - 0.10
        button_y2 = button_y1 - 0.06  # Increased vertical spacing
        button_x = UI_LEFT_MARGIN
        button_gap = 0.28  # MASSIVE GAP (button width 0.07 + 0.21 space = super spacious!)

        # Row 1: PREV, NEXT
        prev_button = Button(
            text="< PREV",
            scale=BUTTON_MEDIUM,
            position=(button_x, button_y1),
            parent=camera.ui,
            on_click=self._load_previous_preset,
            color=COLOR_BUTTON_DEFAULT,
            highlight_color=COLOR_BUTTON_DEFAULT_HOVER,
            pressed_color=COLOR_BUTTON_DEFAULT_PRESSED
        )
        self.ui_elements.append(prev_button)

        next_button = Button(
            text="NEXT >",
            scale=BUTTON_MEDIUM,
            position=(button_x + button_gap, button_y1),
            parent=camera.ui,
            on_click=self._load_next_preset,
            color=COLOR_BUTTON_DEFAULT,
            highlight_color=COLOR_BUTTON_DEFAULT_HOVER,
            pressed_color=COLOR_BUTTON_DEFAULT_PRESSED
        )
        self.ui_elements.append(next_button)

        # Row 2: NEW, RANDOM, SAVE
        new_button = Button(
            text="NEW",
            scale=BUTTON_MEDIUM,
            position=(button_x, button_y2),
            parent=camera.ui,
            on_click=self._new_preset,
            color=COLOR_BUTTON_ACTION,
            highlight_color=COLOR_BUTTON_ACTION_HOVER,
            pressed_color=COLOR_BUTTON_ACTION_PRESSED
        )
        self.ui_elements.append(new_button)

        random_button = Button(
            text="RANDOM",
            scale=BUTTON_MEDIUM,
            position=(button_x + button_gap, button_y2),
            parent=camera.ui,
            on_click=self._randomize_creature,
            color=COLOR_BUTTON_SPECIAL,
            highlight_color=COLOR_BUTTON_SPECIAL_HOVER,
            pressed_color=COLOR_BUTTON_SPECIAL_PRESSED
        )
        self.ui_elements.append(random_button)

        # SAVE button
        save_button = Button(
            text="SAVE",
            scale=BUTTON_MEDIUM,
            position=(button_x + (button_gap * 2), button_y2),
            parent=camera.ui,
            on_click=self._show_save_dialog,
            color=COLOR_BUTTON_SAVE,
            highlight_color=COLOR_BUTTON_SAVE_HOVER,
            pressed_color=COLOR_BUTTON_SAVE_PRESSED
        )
        self.ui_elements.append(save_button)

    def _create_parameter_controls(self):
        """Create parameter adjustment controls using constants"""
        # Calculate starting Y position
        start_y = 0.12  # Below preset section (more space for presets)

        current_y = start_y

        # Create sections in order
        for section_key in SECTIONS:
            section_name = SECTION_NAMES[section_key]
            params = PARAMETERS.get(section_key, [])
            choice_params = CHOICE_PARAMETERS.get(section_key, [])

            # Section header
            self._create_section_header(section_name, current_y)
            current_y -= SECTION_HEADER_GAP

            # Create numeric parameter rows
            for param_data in params:
                label_text, param_key, min_val, max_val, step, format_str = param_data
                self._create_parameter_row(
                    label_text, param_key, current_y,
                    min_val, max_val, step, format_str
                )
                current_y -= ROW_SPACING

            # Create choice parameter rows
            for choice_data in choice_params:
                label_text, param_key, choices = choice_data
                self._create_choice_parameter_row(
                    label_text, param_key, current_y, choices
                )
                current_y -= ROW_SPACING

            # Add section gap
            current_y -= (SECTION_GAP - ROW_SPACING)

    def _create_section_header(self, text, y_pos):
        """Create a section header"""
        header = Text(
            text=text,
            position=(LABEL_X, y_pos),
            origin=(-0.5, 0.5),
            scale=SECTION_HEADER_SCALE,
            color=COLOR_SECTION_HEADER,
            parent=camera.ui
        )
        self.ui_elements.append(header)

    def _create_parameter_row(self, label_text, param_key, y_pos,
                            min_val, max_val, step, format_str):
        """
        Create a parameter control row with proper alignment.

        Args:
            label_text: Display label
            param_key: Parameter key in params dict
            y_pos: Y position for this row
            min_val: Minimum value
            max_val: Maximum value
            step: Increment/decrement step
            format_str: Format string for display
        """
        # Label (left-aligned)
        label = Text(
            text=label_text,
            position=(LABEL_X, y_pos),
            origin=(-0.5, 0.5),
            scale=PARAMETER_LABEL_SCALE,
            color=COLOR_LABEL,
            parent=camera.ui
        )
        self.ui_elements.append(label)

        # Value display (RIGHT-ALIGNED to end before minus button)
        # This fixes the alignment issue!
        value_text = Text(
            text=format_str.format(self.current_params.get(param_key, 0)),
            position=(VALUE_X, y_pos),
            origin=(0.5, 0.5),  # Right-aligned!
            scale=PARAMETER_VALUE_SCALE,
            color=COLOR_VALUE,
            parent=camera.ui
        )
        self.ui_elements.append(value_text)
        self.value_texts[param_key] = (value_text, format_str)  # Store for updates

        # Minus button
        minus_btn = Button(
            text="-",
            scale=BUTTON_SMALL,
            position=(BUTTON_X_START, y_pos),
            parent=camera.ui,
            on_click=lambda: self._adjust_parameter(
                param_key, -step, min_val, max_val
            ),
            color=COLOR_BUTTON_MINUS,
            highlight_color=COLOR_BUTTON_MINUS_HOVER,
            pressed_color=COLOR_BUTTON_MINUS_PRESSED
        )
        self.ui_elements.append(minus_btn)

        # Plus button
        plus_btn = Button(
            text="+",
            scale=BUTTON_SMALL,
            position=(BUTTON_X_START + BUTTON_WIDTH + BUTTON_SPACING, y_pos),
            parent=camera.ui,
            on_click=lambda: self._adjust_parameter(
                param_key, step, min_val, max_val
            ),
            color=COLOR_BUTTON_PLUS,
            highlight_color=COLOR_BUTTON_PLUS_HOVER,
            pressed_color=COLOR_BUTTON_PLUS_PRESSED
        )
        self.ui_elements.append(plus_btn)

    def _create_choice_parameter_row(self, label_text, param_key, y_pos, choices):
        """
        Create a choice parameter row with cycle button.

        Args:
            label_text: Display label
            param_key: Parameter key in params dict
            y_pos: Y position for this row
            choices: List of choice values
        """
        # Label (left-aligned)
        label = Text(
            text=label_text,
            position=(LABEL_X, y_pos),
            origin=(-0.5, 0.5),
            scale=PARAMETER_LABEL_SCALE,
            color=COLOR_LABEL,
            parent=camera.ui
        )
        self.ui_elements.append(label)

        # Cycle button (between label and value)
        cycle_btn = Button(
            text="CYCLE",
            scale=(0.06, BUTTON_SMALL[1]),  # Compact button
            position=(CYCLE_BUTTON_X, y_pos),
            parent=camera.ui,
            on_click=lambda: self._cycle_choice_parameter(param_key, choices),
            color=COLOR_BUTTON_TOGGLE,
            highlight_color=COLOR_BUTTON_TOGGLE_HOVER,
            pressed_color=COLOR_BUTTON_TOGGLE_PRESSED
        )
        self.ui_elements.append(cycle_btn)

        # Current value display (to the right of CYCLE button)
        current_value = self.current_params.get(param_key, choices[0])
        value_text = Text(
            text=str(current_value),
            position=(VALUE_X + 0.02, y_pos),
            origin=(-0.5, 0.5),  # Left-aligned after CYCLE button
            scale=PARAMETER_VALUE_SCALE,
            color=COLOR_VALUE_HIGHLIGHT,
            parent=camera.ui
        )
        self.ui_elements.append(value_text)
        self.choice_texts[param_key] = (value_text, choices)  # Store for updates

    def _create_stats_display(self):
        """Create stats/info display at bottom"""
        self.stats_text = Text(
            text="Entities: 0 | Press 'H' to toggle help",
            position=(UI_LEFT_MARGIN, UI_BOTTOM_MARGIN),
            origin=(-0.5, 0.5),
            scale=STATS_SCALE,
            color=COLOR_STATS,
            parent=camera.ui
        )
        self.ui_elements.append(self.stats_text)

    def _adjust_parameter(self, param_key, delta, min_val, max_val):
        """
        Adjust a parameter value with error handling.

        Args:
            param_key: Parameter to adjust
            delta: Change amount
            min_val: Minimum allowed value
            max_val: Maximum allowed value
        """
        try:
            current = self.current_params.get(param_key, 0)
            new_value = max(min_val, min(max_val, current + delta))

            # Handle integer parameters
            if isinstance(self.current_params.get(param_key, 0), int):
                new_value = int(new_value)

            self.current_params[param_key] = new_value

            # Update display
            if param_key in self.value_texts:
                value_text, format_str = self.value_texts[param_key]
                value_text.text = format_str.format(new_value)

            # Trigger rebuild
            self.on_parameters_changed(self.current_params)

        except Exception as e:
            print(f"Error adjusting parameter {param_key}: {e}")

    def _cycle_choice_parameter(self, param_key, choices):
        """
        Cycle through choice parameter values.

        Args:
            param_key: Parameter to cycle
            choices: List of possible values
        """
        try:
            current_value = self.current_params.get(param_key, choices[0])

            # Find current index and cycle to next
            try:
                current_index = choices.index(current_value)
                next_index = (current_index + 1) % len(choices)
            except ValueError:
                next_index = 0

            new_value = choices[next_index]
            self.current_params[param_key] = new_value

            # Update display
            if param_key in self.choice_texts:
                value_text, _ = self.choice_texts[param_key]
                value_text.text = str(new_value)

            # Trigger rebuild
            self.on_parameters_changed(self.current_params)

        except Exception as e:
            print(f"Error cycling choice parameter {param_key}: {e}")

    def _load_previous_preset(self):
        """Load previous preset in list"""
        try:
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

        except Exception as e:
            print(f"Error loading previous preset: {e}")

    def _load_next_preset(self):
        """Load next preset in list"""
        try:
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

        except Exception as e:
            print(f"Error loading next preset: {e}")

    def _load_preset_by_name(self, name):
        """Load a specific preset"""
        try:
            params = self.preset_manager.load_preset(name)
            if params:
                self.current_params = params
                self.preset_name_text.text = name
                self._update_all_value_displays()
                # Trigger rebuild
                self.on_parameters_changed(self.current_params)

        except Exception as e:
            print(f"Error loading preset '{name}': {e}")

    def _new_preset(self):
        """Create new preset with default parameters"""
        try:
            self.current_params = self.preset_manager.get_default_parameters()
            self.preset_name_text.text = "New Creature"
            self._update_all_value_displays()
            # Trigger rebuild
            self.on_parameters_changed(self.current_params)

        except Exception as e:
            print(f"Error creating new preset: {e}")

    def _randomize_creature(self):
        """Randomize creature parameters"""
        try:
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
            self._update_all_value_displays()

            # Trigger rebuild
            self.on_parameters_changed(self.current_params)

        except Exception as e:
            print(f"Error randomizing creature: {e}")

    def _show_save_dialog(self):
        """Show save dialog for naming and saving preset"""
        print("\n" + "=" * 60)
        print("SAVE PRESET")
        print("=" * 60)
        print("Enter a name for this preset (or press Enter to cancel):")
        print("Current name:", self.current_params.get('preset_name', 'Unnamed'))
        print()

        # For now, use console input (Ursina InputField has some quirks)
        # This will be improved with a proper dialog in Phase 4
        import threading

        def get_input():
            try:
                name = input("Preset name: ").strip()
                if name:
                    success = self.preset_manager.save_preset(name, self.current_params)
                    if success:
                        self.preset_name_text.text = name
                        self.current_params['preset_name'] = name
                        print(f"✓ Saved as '{name}'")
                    else:
                        print("✗ Failed to save preset")
                else:
                    print("Save cancelled")
                print("=" * 60)
            except Exception as e:
                print(f"Error saving: {e}")

        # Run input in thread to avoid blocking Ursina
        thread = threading.Thread(target=get_input, daemon=True)
        thread.start()

    def _update_all_value_displays(self):
        """Update all parameter value displays"""
        # Update numeric parameters
        for param_key, (value_text, format_str) in self.value_texts.items():
            value = self.current_params.get(param_key, 0)
            value_text.text = format_str.format(value)

        # Update choice parameters
        for param_key, (value_text, choices) in self.choice_texts.items():
            value = self.current_params.get(param_key, choices[0])
            value_text.text = str(value)

    def update_stats(self, stats_dict):
        """Update stats display"""
        entity_count = stats_dict.get('entity_count', 0)
        self.stats_text.text = f"Entities: {entity_count} | Press 'H' to toggle help | Press 'S' to save"

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
