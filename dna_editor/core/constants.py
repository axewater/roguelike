"""
Constants and configuration for DNA Editor.
"""

import math

# Default algorithm parameters
DEFAULT_PARAMS = {
    'bezier': {'control_strength': 0.4},
    'fourier': {'num_waves': 3, 'amplitude': 0.15}
}

# Preset configurations (name, algorithm, params)
PRESETS = [
    ('Default', 'bezier', {'control_strength': 0.4}),
    ('Tight', 'bezier', {'control_strength': 0.2}),
]

# Default values
DEFAULT_NUM_TENTACLES = 2
DEFAULT_SEGMENTS = 12
DEFAULT_THICKNESS_BASE = 0.25
DEFAULT_TAPER_FACTOR = 0.6
DEFAULT_ALGORITHM = 'bezier'

# Appearance defaults
DEFAULT_BODY_SCALE = 1.2
DEFAULT_TENTACLE_COLOR = (0.6, 0.3, 0.7)  # Purple
DEFAULT_HUE_SHIFT = 0.1  # Color variation between tentacles

# Animation defaults
DEFAULT_ANIM_SPEED = 2.0  # Wave motion speed
DEFAULT_WAVE_AMPLITUDE = 0.05  # Animation intensity
DEFAULT_BODY_PULSE_SPEED = 1.5  # Breathing rate
DEFAULT_BODY_PULSE_AMOUNT = 0.05  # Breathing expansion

# Limits
MIN_TENTACLES = 1
MAX_TENTACLES = 12
MIN_SEGMENTS = 5
MAX_SEGMENTS = 20

# Appearance limits
MIN_BODY_SCALE = 0.5
MAX_BODY_SCALE = 2.0
MIN_HUE_SHIFT = 0.0
MAX_HUE_SHIFT = 0.3

# Animation limits
MIN_ANIM_SPEED = 0.5
MAX_ANIM_SPEED = 5.0
MIN_WAVE_AMPLITUDE = 0.0
MAX_WAVE_AMPLITUDE = 0.2
MIN_PULSE_SPEED = 0.5
MAX_PULSE_SPEED = 3.0
MIN_PULSE_AMOUNT = 0.0
MAX_PULSE_AMOUNT = 0.15

# Branching (Fibonacci-based)
GOLDEN_RATIO = 1.618033988749895  # φ
GOLDEN_ANGLE = math.pi * (3 - math.sqrt(5))  # ~137.508 degrees in radians
DEFAULT_BRANCH_DEPTH = 0
DEFAULT_BRANCH_COUNT = 1
MIN_BRANCH_DEPTH = 0
MAX_BRANCH_DEPTH = 3
MIN_BRANCH_COUNT = 1
MAX_BRANCH_COUNT = 3

# History
MAX_HISTORY_SIZE = 50

# Camera defaults
DEFAULT_CAMERA_DISTANCE = 6
DEFAULT_CAMERA_HEIGHT = 2
DEFAULT_CAMERA_ANGLE = 0
MIN_CAMERA_DISTANCE = 2
MAX_CAMERA_DISTANCE = 15
MIN_CAMERA_HEIGHT = 0.5
MAX_CAMERA_HEIGHT = 5

# Scene positioning
GROUND_Y = -3.5  # Floor position (below tentacles at y=-2.5)
SHADOW_Y = -3.45  # Shadow plane just above floor

# Colors
BODY_COLOR = (0.6, 0.3, 0.7)  # Purple
GROUND_COLOR = (0.1, 0.1, 0.15)
SKY_COLOR = (0.05, 0.05, 0.1)  # Legacy single color (not used with gradient)
SKY_GRADIENT_BOTTOM = (0.02, 0.02, 0.08)  # Dark blue-purple at horizon
SKY_GRADIENT_TOP = (0.08, 0.08, 0.15)  # Lighter blue at top
DEBUG_MARKER_COLOR = (1, 1, 0)  # Yellow

# Shadow (layered circles for soft shadow effect)
SHADOW_LAYERS = 5  # Number of shadow layers
SHADOW_BASE_SIZE = 3.5  # Size of largest (outermost) shadow layer
SHADOW_SIZE_STEP = 0.6  # Size reduction per layer (creates gradient effect)
SHADOW_BASE_OPACITY = 25  # Opacity of darkest (innermost) layer (0-255) - SUBTLE!
SHADOW_OPACITY_STEP = 4  # Opacity reduction per layer - small steps to prevent accumulation

# Body
BODY_SCALE = 1.2
BODY_PULSE_AMOUNT = 0.05
BODY_PULSE_SPEED = 1.5
