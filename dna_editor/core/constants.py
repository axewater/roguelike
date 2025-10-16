"""
Constants and configuration for DNA Editor.
"""

# Default algorithm parameters
DEFAULT_PARAMS = {
    'bezier': {'control_strength': 0.4},
    'fourier': {'num_waves': 3, 'amplitude': 0.15}
}

# Preset configurations (name, algorithm, params)
PRESETS = [
    ('Default', 'bezier', {'control_strength': 0.4}),
    ('Wavy', 'fourier', {'num_waves': 4, 'amplitude': 0.25}),
    ('Tight', 'bezier', {'control_strength': 0.2}),
]

# Default values
DEFAULT_NUM_TENTACLES = 2
DEFAULT_SEGMENTS = 12
DEFAULT_THICKNESS_BASE = 0.25
DEFAULT_TAPER_FACTOR = 0.6
DEFAULT_ALGORITHM = 'bezier'

# Limits
MIN_TENTACLES = 1
MAX_TENTACLES = 12
MIN_SEGMENTS = 5
MAX_SEGMENTS = 20

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
