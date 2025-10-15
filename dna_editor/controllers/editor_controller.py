"""
Editor controller - main application orchestrator.

Coordinates all components: models, UI, camera, and state.
"""

from ursina import Entity, Sky, color, held_keys, time as ursina_time
from ..models import TentacleCreature
from ..ui import InfoPanel, ParametersPanel, ThicknessPanel, PresetsPanel, HelpOverlay
from .state_manager import StateManager
from .camera_controller import CameraController
from ..core.constants import (
    DEFAULT_NUM_TENTACLES, DEFAULT_SEGMENTS, DEFAULT_THICKNESS_BASE,
    DEFAULT_TAPER_FACTOR, DEFAULT_ALGORITHM, DEFAULT_PARAMS,
    MIN_TENTACLES, MAX_TENTACLES, MIN_SEGMENTS, MAX_SEGMENTS,
    GROUND_COLOR, SKY_COLOR, DEBUG_MARKER_COLOR
)


class EditorController:
    """Main editor application controller."""

    def __init__(self):
        """Initialize editor with scene, creature, UI, and controllers."""
        # Create scene
        self._create_scene()

        # Initialize state
        self.num_tentacles = DEFAULT_NUM_TENTACLES
        self.segments = DEFAULT_SEGMENTS
        self.algorithm = DEFAULT_ALGORITHM
        self.params = {k: v.copy() for k, v in DEFAULT_PARAMS.items()}
        self.thickness_base = DEFAULT_THICKNESS_BASE
        self.taper_factor = DEFAULT_TAPER_FACTOR

        # Create controllers
        self.state_manager = StateManager()
        self.camera_controller = CameraController()

        # Create creature
        self.creature = None
        self.rebuild_creature()

        # Create UI
        self._create_ui()

        # Animation time
        self.time = 0

        # Print startup info
        self._print_startup_info()

    def _create_scene(self):
        """Create scene elements (ground, sky, debug marker)."""
        self.ground = Entity(
            model='plane',
            scale=20,
            color=color.rgb(*GROUND_COLOR),
            position=(0, -1, 0)
        )

        self.sky = Sky(color=color.rgb(*SKY_COLOR))

        # DEBUG: Add a bright marker at origin to verify rendering works
        self.debug_marker = Entity(
            model='sphere',
            color=color.rgb(*DEBUG_MARKER_COLOR),
            scale=0.3,
            position=(0, 0, 0)
        )
        print("DEBUG: Yellow marker created at origin (0, 0, 0)")

    def _create_ui(self):
        """Create all UI panels."""
        self.info_panel = InfoPanel(on_algorithm_changed=self.set_algorithm)
        self.parameters_panel = ParametersPanel(on_param_changed=self.on_param_changed)
        self.thickness_panel = ThicknessPanel(on_thickness_changed=self.on_thickness_changed)
        self.presets_panel = PresetsPanel(on_preset_clicked=self.load_preset)
        self.help_overlay = HelpOverlay()

        # Initial UI update
        self.update_ui()

    def _print_startup_info(self):
        """Print startup information to console."""
        print("\n" + "=" * 70)
        print("DNA EDITOR - CREATURE TENTACLE GENERATOR")
        print("=" * 70)
        print("FEATURES:")
        print("  - Real-time parameter sliders for algorithms")
        print("  - Thickness & taper controls")
        print("  - Preset system (3 presets)")
        print("  - Undo/Redo (Ctrl+Z / Ctrl+Y)")
        print("  - Help overlay (Press H)")
        print("")
        print("Quick Controls:")
        print("  H - Help  |  1/2/3 - Tentacles  |  Q/W - Algorithm")
        print("  +/- - Segments  |  R - Reset camera")
        print("  Use sliders for fine control!")
        print("=" * 70)
        print()

    def rebuild_creature(self):
        """Rebuild creature with current parameters."""
        if self.creature:
            self.creature.destroy()

        self.creature = TentacleCreature(
            num_tentacles=self.num_tentacles,
            segments_per_tentacle=self.segments,
            algorithm=self.algorithm,
            algorithm_params=self.params[self.algorithm],
            thickness_base=self.thickness_base,
            taper_factor=self.taper_factor
        )

        print(f"Built: {self.num_tentacles} tentacles, {self.segments} segments, {self.algorithm}")
        print(f"Params: {self.params[self.algorithm]}")
        print(f"Thickness: base={self.thickness_base}, taper={self.taper_factor}")
        print(f"Creature root parent: {self.creature.root.parent}")

    def update_ui(self):
        """Update all UI panels with current state."""
        self.info_panel.update(self.num_tentacles, self.segments, self.algorithm)
        self.parameters_panel.update(self.algorithm, self.params[self.algorithm])
        self.thickness_panel.update(self.thickness_base, self.taper_factor)

    def set_algorithm(self, algo):
        """
        Change algorithm.

        Args:
            algo: 'bezier' or 'fourier'
        """
        self._save_state()
        self.algorithm = algo
        self.rebuild_creature()
        self.update_ui()

    def set_tentacles(self, count):
        """
        Change tentacle count.

        Args:
            count: Number of tentacles (1-3)
        """
        self._save_state()
        self.num_tentacles = max(MIN_TENTACLES, min(MAX_TENTACLES, count))
        self.rebuild_creature()
        self.update_ui()

    def adjust_segments(self, delta):
        """
        Adjust segment count.

        Args:
            delta: Change in segments (+/- 1)
        """
        self._save_state()
        self.segments = max(MIN_SEGMENTS, min(MAX_SEGMENTS, self.segments + delta))
        self.rebuild_creature()
        self.update_ui()

    def on_param_changed(self):
        """Callback when algorithm parameter slider changes."""
        self._save_state()

        # Update the parameter based on which algorithm is active
        if self.algorithm == 'bezier':
            self.params['bezier'] = self.parameters_panel.get_bezier_params()
        elif self.algorithm == 'fourier':
            self.params['fourier'] = self.parameters_panel.get_fourier_params()

        # Rebuild creature with new parameters
        self.rebuild_creature()
        self.update_ui()

    def on_thickness_changed(self):
        """Callback when thickness slider changes."""
        self._save_state()

        values = self.thickness_panel.get_values()
        self.thickness_base = values['thickness_base']
        self.taper_factor = values['taper_factor']

        self.rebuild_creature()
        self.update_ui()

    def load_preset(self, algo, params):
        """
        Load a parameter preset.

        Args:
            algo: Algorithm name
            params: Parameter dict
        """
        self._save_state()

        self.algorithm = algo
        self.params[algo].update(params)

        self.rebuild_creature()
        self.update_ui()

        print(f"Loaded preset: {algo} with params {params}")

    def _save_state(self):
        """Save current state for undo/redo."""
        self.state_manager.save_state(
            self.num_tentacles,
            self.segments,
            self.algorithm,
            self.params,
            self.thickness_base,
            self.taper_factor
        )

    def undo(self):
        """Undo to previous state."""
        state = self.state_manager.undo()
        if state:
            self._restore_state(state)

    def redo(self):
        """Redo to next state."""
        state = self.state_manager.redo()
        if state:
            self._restore_state(state)

    def _restore_state(self, state):
        """Restore a saved state."""
        self.num_tentacles = state['num_tentacles']
        self.segments = state['segments']
        self.algorithm = state['algorithm']
        self.params = state['params']
        self.thickness_base = state['thickness_base']
        self.taper_factor = state['taper_factor']

        self.rebuild_creature()
        self.update_ui()

    def toggle_help(self):
        """Toggle help overlay."""
        self.help_overlay.toggle()

    def handle_keyboard_input(self):
        """Handle keyboard input for all controls."""
        # Tentacle count
        if held_keys['1']:
            self.set_tentacles(1)
            held_keys['1'] = False
        if held_keys['2']:
            self.set_tentacles(2)
            held_keys['2'] = False
        if held_keys['3']:
            self.set_tentacles(3)
            held_keys['3'] = False

        # Algorithm
        if held_keys['q']:
            self.set_algorithm('bezier')
            held_keys['q'] = False
        if held_keys['w']:
            self.set_algorithm('fourier')
            held_keys['w'] = False

        # Segments
        if held_keys['+'] or held_keys['=']:
            self.adjust_segments(1)
            held_keys['+'] = False
            held_keys['='] = False
        if held_keys['-']:
            self.adjust_segments(-1)
            held_keys['-'] = False

        # Help
        if held_keys['h']:
            self.toggle_help()
            held_keys['h'] = False

        # Undo/Redo
        if held_keys['control']:
            if held_keys['z']:
                self.undo()
                held_keys['z'] = False
            if held_keys['y']:
                self.redo()
                held_keys['y'] = False

        # Camera reset
        self.camera_controller.handle_reset_key()

    def update(self):
        """Main update loop."""
        dt = ursina_time.dt
        self.time += dt

        # Update camera
        self.camera_controller.update()

        # Update creature animation
        if self.creature:
            self.creature.update_animation(self.time)

        # Handle keyboard input
        self.handle_keyboard_input()
