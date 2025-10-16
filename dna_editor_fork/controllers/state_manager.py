"""
State manager - handles undo/redo history.
"""

try:
    # Try relative import (for Ursina version)
    from ..core.constants import MAX_HISTORY_SIZE
except ImportError:
    # Fall back to absolute import (for PyQt6 version)
    from dna_editor_copy.core.constants import MAX_HISTORY_SIZE


class StateManager:
    """Manages undo/redo history for editor state."""

    def __init__(self):
        """Initialize state manager."""
        self.history = []
        self.history_index = -1
        self.max_history = MAX_HISTORY_SIZE

    def save_state(self, num_tentacles, segments, algorithm, params,
                   thickness_base, taper_factor):
        """
        Save current state to history.

        Args:
            num_tentacles: Number of tentacles
            segments: Segments per tentacle
            algorithm: Current algorithm
            params: Algorithm parameters dict
            thickness_base: Base thickness
            taper_factor: Taper factor
        """
        # Deep copy params dict (handle both dict and primitive values)
        params_copy = {}
        for k, v in params.items():
            if isinstance(v, dict):
                params_copy[k] = v.copy()
            else:
                params_copy[k] = v

        state = {
            'num_tentacles': num_tentacles,
            'segments': segments,
            'algorithm': algorithm,
            'params': params_copy,
            'thickness_base': thickness_base,
            'taper_factor': taper_factor
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
            print(f"Undo (history {self.history_index + 1}/{len(self.history)})")
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
            print(f"Redo (history {self.history_index + 1}/{len(self.history)})")
            return self._get_current_state()
        return None

    def _get_current_state(self):
        """Get current state with deep copy of params."""
        state = self.history[self.history_index]

        # Deep copy params dict (handle both dict and primitive values)
        params_copy = {}
        for k, v in state['params'].items():
            if isinstance(v, dict):
                params_copy[k] = v.copy()
            else:
                params_copy[k] = v

        return {
            'num_tentacles': state['num_tentacles'],
            'segments': state['segments'],
            'algorithm': state['algorithm'],
            'params': params_copy,
            'thickness_base': state['thickness_base'],
            'taper_factor': state['taper_factor']
        }

    def can_undo(self):
        """Check if undo is available."""
        return self.history_index > 0

    def can_redo(self):
        """Check if redo is available."""
        return self.history_index < len(self.history) - 1
