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
GROUND_COLOR = (0.15, 0.2, 0.25)  # Lighter blue-gray ground
SKY_COLOR = (0.05, 0.05, 0.1)  # Legacy single color (not used with gradient)
SKY_GRADIENT_BOTTOM = (0.9, 0.5, 0.65)  # Bright warm pink/coral at horizon
SKY_GRADIENT_TOP = (0.35, 0.65, 0.95)  # Bright cyan/sky blue at top
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

# Toon Shader / Cel-Shading
TOON_CONTACT_SHADOW_SIZE = 0.6  # Shadow sphere size as fraction of segment (0.6 = 60%)
TOON_CONTACT_SHADOW_OPACITY = 60  # Shadow opacity 0-255 (60 = semi-transparent)
TOON_LIGHTING_BANDS = 4  # Number of discrete lighting bands (4 = full, medium, dark, shadow)

# Attack Animation (Whip Physics)
ATTACK_DURATION = 1.2  # Total attack cycle duration in seconds
ATTACK_WIND_UP_END = 0.2  # Wind-up phase ends at this time (pull back)
ATTACK_STRIKE_END = 0.5  # Strike phase ends at this time (forward lash)
ATTACK_FOLLOW_END = 0.8  # Follow-through phase ends at this time (continue motion)
ATTACK_RETURN_END = 1.2  # Return phase ends (ease back to idle)

# Whip wave propagation (exponential traveling wave)
WHIP_SPEED = 8.0  # Angular frequency (higher = faster wave travel)
WHIP_ACCELERATION = 3.5  # Exponential growth factor (higher = more tip acceleration)
WHIP_AMPLITUDE = 0.8  # Base amplitude of whip wave motion

# Dynamic stretching (distance-based extension)
STRETCH_THRESHOLD = 3.0  # Distance to camera before stretching kicks in
STRETCH_MULTIPLIER = 0.5  # How much to extend (0.5 = 50% of excess distance)
STRETCH_MAX = 2.0  # Maximum stretch factor (2.0 = can extend to 200% original length)

# Helical curl (spiral slash motion at tips)
CURL_INTENSITY = 0.3  # Spiral radius multiplier
CURL_SPEED = 10.0  # Spiral rotation speed (radians per second)
CURL_TWIST_FACTOR = 0.5  # How much twist increases per segment

# Wind-up motion (pull back before strike)
WIND_UP_DISTANCE = 0.3  # How far to pull back during wind-up phase

# Segment distance constraints (keep tentacles connected)
SEGMENT_STRETCH_MAX = 1.8  # Maximum distance multiplier (180% of original spacing)
SEGMENT_COMPRESS_MIN = 0.4  # Minimum distance multiplier (40% of original spacing)
CONSTRAINT_ITERATIONS = 2  # Number of constraint solver passes (more = stiffer)

# Exploration Animation (Coordinated Tentacle Reaching)
EXPLORATION_REACH_DURATION = 4.0  # Seconds to reach target (smooth ease-out)
EXPLORATION_RETURN_DURATION = 0.5  # Seconds to spring back (fast return)
EXPLORATION_IDLE_GAP = 0.5  # Pause between cycles
EXPLORATION_TENTACLE_RATIO = (0.25, 0.40)  # 25-40% of tentacles reach together
EXPLORATION_TARGET_MIN_RADIUS = 1.5  # Minimum target distance from body center
EXPLORATION_TARGET_MAX_RADIUS = 2.5  # Maximum target distance from body center
EXPLORATION_REACH_STRENGTH = 1.5  # How far tentacles stretch toward target
