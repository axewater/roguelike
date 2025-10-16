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

    def save_state(self, num_tentacles, segments, algorithm, params,
                   thickness_base, taper_factor, branch_depth=0, branch_count=1,
                   body_scale=1.2, tentacle_color=(0.6, 0.3, 0.7), hue_shift=0.1,
                   anim_speed=2.0, wave_amplitude=0.05, pulse_speed=1.5, pulse_amount=0.05):
        """
        Save current state to history.

        Args:
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
        """
        state = {
            'num_tentacles': num_tentacles,
            'segments': segments,
            'algorithm': algorithm,
            'params': copy.deepcopy(params),
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
            'pulse_amount': pulse_amount
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
            'num_tentacles': state['num_tentacles'],
            'segments': state['segments'],
            'algorithm': state['algorithm'],
            'params': copy.deepcopy(state['params']),
            'thickness_base': state['thickness_base'],
            'taper_factor': state['taper_factor'],
            'branch_depth': state.get('branch_depth', 0),
            'branch_count': state.get('branch_count', 1),
            'body_scale': state.get('body_scale', 1.2),
            'tentacle_color': state.get('tentacle_color', (0.6, 0.3, 0.7)),
            'hue_shift': state.get('hue_shift', 0.1),
            'anim_speed': state.get('anim_speed', 2.0),
            'wave_amplitude': state.get('wave_amplitude', 0.05),
            'pulse_speed': state.get('pulse_speed', 1.5),
            'pulse_amount': state.get('pulse_amount', 0.05)
        }

    def can_undo(self):
        """Check if undo is available."""
        return self.history_index > 0

    def can_redo(self):
        """Check if redo is available."""
        return self.history_index < len(self.history) - 1
