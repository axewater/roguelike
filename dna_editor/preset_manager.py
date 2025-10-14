"""
Preset Manager - Save, load, and manage creature presets

Handles JSON serialization of creature parameters for sharing and reuse.
"""

import json
import os
from datetime import datetime


class PresetManager:
    """
    Manages creature preset storage and retrieval.
    """

    def __init__(self, presets_dir='dna_editor/presets'):
        """
        Initialize preset manager.

        Args:
            presets_dir: Directory to store preset JSON files
        """
        self.presets_dir = presets_dir
        self.presets = {}  # name -> params dict
        self.current_preset_name = None

        # Ensure presets directory exists
        os.makedirs(presets_dir, exist_ok=True)

        # Load existing presets
        self.load_all_presets()

    def load_all_presets(self):
        """
        Load all preset files from presets directory.
        """
        self.presets.clear()

        # Load main examples file if it exists
        examples_file = os.path.join(self.presets_dir, 'examples.json')
        if os.path.exists(examples_file):
            with open(examples_file, 'r') as f:
                examples = json.load(f)
                if isinstance(examples, dict):
                    self.presets.update(examples)

        # Load individual preset files
        if os.path.exists(self.presets_dir):
            for filename in os.listdir(self.presets_dir):
                if filename.endswith('.json') and filename != 'examples.json':
                    filepath = os.path.join(self.presets_dir, filename)
                    try:
                        with open(filepath, 'r') as f:
                            preset_data = json.load(f)
                            preset_name = filename[:-5]  # Remove .json
                            self.presets[preset_name] = preset_data
                    except Exception as e:
                        print(f"Warning: Failed to load preset {filename}: {e}")

        print(f"✓ Loaded {len(self.presets)} presets")

    def save_preset(self, name, params, overwrite=True):
        """
        Save a preset to disk.

        Args:
            name: Preset name
            params: Parameter dictionary
            overwrite: If False, raises error if preset exists

        Returns:
            bool: Success
        """
        if not overwrite and name in self.presets:
            raise ValueError(f"Preset '{name}' already exists")

        # Add metadata
        params_with_meta = params.copy()
        params_with_meta['preset_name'] = name
        params_with_meta['created_at'] = datetime.now().isoformat()

        # Save to memory
        self.presets[name] = params_with_meta

        # Save to disk (individual file)
        filename = f"{name}.json"
        filepath = os.path.join(self.presets_dir, filename)

        try:
            with open(filepath, 'w') as f:
                json.dump(params_with_meta, f, indent=2)
            print(f"✓ Saved preset '{name}' to {filepath}")
            self.current_preset_name = name
            return True
        except Exception as e:
            print(f"✗ Failed to save preset '{name}': {e}")
            return False

    def load_preset(self, name):
        """
        Load a preset by name.

        Args:
            name: Preset name

        Returns:
            dict: Parameter dictionary, or None if not found
        """
        if name in self.presets:
            self.current_preset_name = name
            return self.presets[name].copy()
        else:
            print(f"✗ Preset '{name}' not found")
            return None

    def delete_preset(self, name):
        """
        Delete a preset.

        Args:
            name: Preset name

        Returns:
            bool: Success
        """
        if name not in self.presets:
            print(f"✗ Preset '{name}' not found")
            return False

        # Remove from memory
        del self.presets[name]

        # Remove file
        filename = f"{name}.json"
        filepath = os.path.join(self.presets_dir, filename)

        try:
            if os.path.exists(filepath):
                os.remove(filepath)
            print(f"✓ Deleted preset '{name}'")
            return True
        except Exception as e:
            print(f"✗ Failed to delete preset '{name}': {e}")
            return False

    def duplicate_preset(self, original_name, new_name):
        """
        Duplicate an existing preset with a new name.

        Args:
            original_name: Name of preset to duplicate
            new_name: Name for duplicated preset

        Returns:
            bool: Success
        """
        if original_name not in self.presets:
            print(f"✗ Preset '{original_name}' not found")
            return False

        # Copy parameters
        params = self.presets[original_name].copy()
        params['preset_name'] = new_name

        # Save as new preset
        return self.save_preset(new_name, params)

    def get_preset_names(self):
        """
        Get list of all preset names.

        Returns:
            list: Sorted list of preset names
        """
        return sorted(self.presets.keys())

    def export_all(self, filename='all_presets.json'):
        """
        Export all presets to a single JSON file.

        Args:
            filename: Output filename

        Returns:
            bool: Success
        """
        filepath = os.path.join(self.presets_dir, filename)

        try:
            with open(filepath, 'w') as f:
                json.dump(self.presets, f, indent=2)
            print(f"✓ Exported {len(self.presets)} presets to {filepath}")
            return True
        except Exception as e:
            print(f"✗ Failed to export presets: {e}")
            return False

    def get_default_parameters(self):
        """
        Get default creature parameters.

        Returns:
            dict: Default parameters
        """
        return {
            'preset_name': 'Default Creature',
            'body_size': 0.6,
            'body_hue': 280,
            'body_shape': 'sphere',
            'tentacle_count': 8,
            'base_length': 2.0,
            'length_variation': 20,
            'segments': 10,
            'base_thickness': 0.1,
            'taper': 50,
            'eye_count': 2,
            'eye_pattern': 'dual',
            'eye_size': 0.1,
            'spike_count': 15,
            'spike_length': 0.2,
            'wave_speed': 2.0,
            'wave_amplitude': 20,
            'animate': True
        }
