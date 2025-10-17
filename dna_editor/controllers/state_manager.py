"""
State manager - handles undo/redo history.
"""

import copy
from ..core.constants import MAX_HISTORY_SIZE


class StateManager:
    """Manages undo/redo history for editor state."""

    def __init__(self):
        """Initialize state manager."""
        self.history = []
        self.history_index = -1
        self.max_history = MAX_HISTORY_SIZE

    def save_state(self, creature_type='tentacle',
                   # Tentacle parameters
                   num_tentacles=2, segments=12, algorithm='bezier', params=None,
                   thickness_base=0.25, taper_factor=0.6, branch_depth=0, branch_count=1,
                   body_scale=1.2, tentacle_color=(0.6, 0.3, 0.7), hue_shift=0.1,
                   anim_speed=2.0, wave_amplitude=0.05, pulse_speed=1.5, pulse_amount=0.05,
                   num_eyes=3, eye_size_min=0.1, eye_size_max=0.25,
                   eyeball_color=(1.0, 1.0, 1.0), pupil_color=(0.0, 0.0, 0.0),
                   # Blob parameters
                   num_cubes=8, cube_size_min=0.3, cube_size_max=0.8,
                   cube_spacing=1.2, blob_color=(0.2, 0.8, 0.4), blob_transparency=0.7,
                   jiggle_speed=2.0, blob_pulse_amount=0.1):
        """
        Save current state to history.

        Args:
            creature_type: 'tentacle' or 'blob'
            [Tentacle parameters]
            num_tentacles: Number of tentacles
            segments: Segments per tentacle
            algorithm: Current algorithm
            params: Algorithm parameters dict
            thickness_base: Base thickness
            taper_factor: Taper factor
            branch_depth: Branching depth
            branch_count: Number of branches per tentacle
            body_scale: Body sphere scale
            tentacle_color: Base tentacle color (RGB tuple 0-1)
            hue_shift: Color variation between tentacles
            anim_speed: Animation wave speed
            wave_amplitude: Wave motion intensity
            pulse_speed: Body pulse breathing speed
            pulse_amount: Body pulse expansion amount
            num_eyes: Number of eyes on upper hemisphere
            eye_size_min: Minimum eye size
            eye_size_max: Maximum eye size
            eyeball_color: Eyeball color (RGB tuple 0-1)
            pupil_color: Pupil color (RGB tuple 0-1)
            [Blob parameters]
            num_cubes: Number of cubes
            cube_size_min: Minimum cube size
            cube_size_max: Maximum cube size
            cube_spacing: Cube spacing
            blob_color: Blob color (RGB tuple 0-1)
            blob_transparency: Transparency (0-1)
            jiggle_speed: Jiggle animation speed
            blob_pulse_amount: Pulse intensity
        """
        state = {
            'creature_type': creature_type,
            # Tentacle parameters
            'num_tentacles': num_tentacles,
            'segments': segments,
            'algorithm': algorithm,
            'params': copy.deepcopy(params) if params else {},
            'thickness_base': thickness_base,
            'taper_factor': taper_factor,
            'branch_depth': branch_depth,
            'branch_count': branch_count,
            'body_scale': body_scale,
            'tentacle_color': tentacle_color,
            'hue_shift': hue_shift,
            'anim_speed': anim_speed,
            'wave_amplitude': wave_amplitude,
            'pulse_speed': pulse_speed,
            'pulse_amount': pulse_amount,
            'num_eyes': num_eyes,
            'eye_size_min': eye_size_min,
            'eye_size_max': eye_size_max,
            'eyeball_color': eyeball_color,
            'pupil_color': pupil_color,
            # Blob parameters
            'num_cubes': num_cubes,
            'cube_size_min': cube_size_min,
            'cube_size_max': cube_size_max,
            'cube_spacing': cube_spacing,
            'blob_color': blob_color,
            'blob_transparency': blob_transparency,
            'jiggle_speed': jiggle_speed,
            'blob_pulse_amount': blob_pulse_amount
        }

        # Clear future history if we're not at the end
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]

        # Add new state
        self.history.append(state)

        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
        else:
            self.history_index += 1

    def undo(self):
        """
        Undo to previous state.

        Returns:
            Previous state dict or None if can't undo
        """
        if self.history_index > 0:
            self.history_index -= 1
            return self._get_current_state()
        return None

    def redo(self):
        """
        Redo to next state.

        Returns:
            Next state dict or None if can't redo
        """
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            return self._get_current_state()
        return None

    def _get_current_state(self):
        """Get current state with deep copy of params."""
        state = self.history[self.history_index]

        return {
            'creature_type': state.get('creature_type', 'tentacle'),
            # Tentacle parameters
            'num_tentacles': state.get('num_tentacles', 2),
            'segments': state.get('segments', 12),
            'algorithm': state.get('algorithm', 'bezier'),
            'params': copy.deepcopy(state.get('params', {})),
            'thickness_base': state.get('thickness_base', 0.25),
            'taper_factor': state.get('taper_factor', 0.6),
            'branch_depth': state.get('branch_depth', 0),
            'branch_count': state.get('branch_count', 1),
            'body_scale': state.get('body_scale', 1.2),
            'tentacle_color': state.get('tentacle_color', (0.6, 0.3, 0.7)),
            'hue_shift': state.get('hue_shift', 0.1),
            'anim_speed': state.get('anim_speed', 2.0),
            'wave_amplitude': state.get('wave_amplitude', 0.05),
            'pulse_speed': state.get('pulse_speed', 1.5),
            'pulse_amount': state.get('pulse_amount', 0.05),
            'num_eyes': state.get('num_eyes', 3),
            'eye_size_min': state.get('eye_size_min', 0.1),
            'eye_size_max': state.get('eye_size_max', 0.25),
            'eyeball_color': state.get('eyeball_color', (1.0, 1.0, 1.0)),
            'pupil_color': state.get('pupil_color', (0.0, 0.0, 0.0)),
            # Blob parameters
            'num_cubes': state.get('num_cubes', 8),
            'cube_size_min': state.get('cube_size_min', 0.3),
            'cube_size_max': state.get('cube_size_max', 0.8),
            'cube_spacing': state.get('cube_spacing', 1.2),
            'blob_color': state.get('blob_color', (0.2, 0.8, 0.4)),
            'blob_transparency': state.get('blob_transparency', 0.7),
            'jiggle_speed': state.get('jiggle_speed', 2.0),
            'blob_pulse_amount': state.get('blob_pulse_amount', 0.1)
        }

    def can_undo(self):
        """Check if undo is available."""
        return self.history_index > 0

    def can_redo(self):
        """Check if redo is available."""
        return self.history_index < len(self.history) - 1
