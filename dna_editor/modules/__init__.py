"""
Creature module system for procedural generation.

Each module handles creation of a specific creature part:
- body: Central body (sphere/ellipsoid)
- tentacle: Segmented articulated tentacles
- eyes: Eye decorations with placement patterns
- spikes: Surface spike decorations
"""

from .body import create_body
from .tentacle import create_tentacle
from .eyes import create_eyes
from .spikes import create_spikes

__all__ = ['create_body', 'create_tentacle', 'create_eyes', 'create_spikes']
