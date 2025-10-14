"""
UI Constants - Centralized layout and styling constants

Defines all UI positioning, spacing, colors, and dimensions for consistent layout.
"""

from ursina import color as ursina_color


# ============================================================================
# LAYOUT CONSTANTS
# ============================================================================

# Screen margins and positioning
UI_LEFT_MARGIN = -0.95      # Left edge of UI panels (actually at the left edge!)
UI_TOP_MARGIN = 0.48        # Top edge of UI
UI_BOTTOM_MARGIN = -0.48    # Bottom edge of UI

# Section spacing
SECTION_GAP = 0.12          # Vertical gap between major sections (increased for clarity)
SECTION_HEADER_GAP = 0.045  # Gap after section headers
ROW_SPACING = 0.055         # Spacing between parameter rows (increased for clarity)
TITLE_SPACING = 0.03        # Spacing between title and subtitle

# Horizontal layout
LABEL_X = UI_LEFT_MARGIN    # Parameter label X position
VALUE_X = -0.64             # Parameter value X position (right-aligned)
BUTTON_X_START = -0.58      # First button (minus) X position
BUTTON_SPACING = 0.045      # Spacing between buttons
CYCLE_BUTTON_X = -0.68      # Cycle button X position (between label and value)

# Component widths
LABEL_WIDTH = 0.20          # Width allocated for labels
VALUE_WIDTH = 0.06          # Width allocated for values
BUTTON_WIDTH = 0.032        # Individual button width (matches BUTTON_SMALL)

# ============================================================================
# BUTTON SIZES
# ============================================================================

# Standard button dimensions
BUTTON_SMALL = (0.032, 0.032)   # Small square buttons (+/-)
BUTTON_MEDIUM = (0.07, 0.036)   # Medium rectangular buttons (PREV/NEXT) - compact for better spacing
BUTTON_LARGE = (0.12, 0.04)     # Large rectangular buttons (SAVE)

# ============================================================================
# TEXT SCALES
# ============================================================================

TITLE_SCALE = 1.5           # Main title
SUBTITLE_SCALE = 0.8        # Subtitle text
SECTION_HEADER_SCALE = 0.8  # Section headers
PARAMETER_LABEL_SCALE = 0.7 # Parameter labels
PARAMETER_VALUE_SCALE = 0.7 # Parameter values
STATS_SCALE = 0.6           # Stats/info text

# ============================================================================
# COLOR PALETTE
# ============================================================================

# Text colors
COLOR_TITLE = ursina_color.rgb(0.9, 0.7, 1.0)         # Purple-ish title
COLOR_SUBTITLE = ursina_color.rgb(0.7, 0.7, 0.8)      # Gray subtitle
COLOR_SECTION_HEADER = ursina_color.rgb(1.0, 0.9, 0.6) # Yellow headers
COLOR_LABEL = ursina_color.rgb(0.8, 0.8, 0.8)         # Light gray labels
COLOR_VALUE = ursina_color.rgb(0.9, 1.0, 0.9)         # Light green values
COLOR_VALUE_HIGHLIGHT = ursina_color.rgb(0.8, 0.9, 1.0) # Light blue highlight
COLOR_STATS = ursina_color.rgb(0.7, 0.7, 0.7)         # Gray stats text

# Button colors
COLOR_BUTTON_DEFAULT = ursina_color.rgb(0.3, 0.3, 0.4)  # Dark gray
COLOR_BUTTON_ACTION = ursina_color.rgb(0.2, 0.5, 0.3)   # Green (NEW)
COLOR_BUTTON_SPECIAL = ursina_color.rgb(0.5, 0.3, 0.5)  # Purple (RANDOM)
COLOR_BUTTON_SAVE = ursina_color.rgb(0.2, 0.4, 0.6)     # Blue (SAVE)
COLOR_BUTTON_MINUS = ursina_color.rgb(0.4, 0.2, 0.2)    # Red (-)
COLOR_BUTTON_PLUS = ursina_color.rgb(0.2, 0.4, 0.2)     # Green (+)
COLOR_BUTTON_TOGGLE = ursina_color.rgb(0.4, 0.4, 0.2)   # Olive (toggle)

# ============================================================================
# PARAMETER DEFINITIONS
# ============================================================================

# Parameter metadata: (label, key, min, max, step, format_string)
PARAMETERS = {
    'body': [
        ('Size:', 'body_size', 0.3, 1.2, 0.1, '{:.1f}'),
        ('Hue:', 'body_hue', 0, 360, 20, '{:.0f}'),
    ],
    'tentacles': [
        ('Count:', 'tentacle_count', 4, 12, 1, '{:.0f}'),
        ('Length:', 'base_length', 0.8, 3.0, 0.2, '{:.1f}'),
        ('Segments:', 'segments', 5, 15, 1, '{:.0f}'),
    ],
    'animation': [
        ('Speed:', 'wave_speed', 0.5, 5.0, 0.5, '{:.1f}'),
        ('Amplitude:', 'wave_amplitude', 5, 40, 5, '{:.0f}'),
    ],
    'decorations': [
        ('Eyes:', 'eye_count', 0, 8, 1, '{:.0f}'),
        ('Spikes:', 'spike_count', 0, 30, 5, '{:.0f}'),
    ]
}

# Choice parameters (cycle buttons) - (label, key, choices)
CHOICE_PARAMETERS = {
    'body': [
        ('Shape:', 'body_shape', ['sphere', 'ellipsoid']),
    ],
    'decorations': [
        ('Eye Pattern:', 'eye_pattern', ['dual', 'spider', 'ring']),
    ]
}

# Section names (in display order)
SECTIONS = ['body', 'tentacles', 'animation', 'decorations']

# Section display names
SECTION_NAMES = {
    'body': 'BODY',
    'tentacles': 'TENTACLES',
    'animation': 'ANIMATION',
    'decorations': 'DECORATIONS'
}

# ============================================================================
# LAYOUT HELPERS
# ============================================================================

def calculate_section_y(section_index, params_before=0):
    """
    Calculate Y position for a section header.

    Args:
        section_index: Index of this section (0-based)
        params_before: Number of parameter rows before this section

    Returns:
        float: Y position
    """
    # Start from preset area
    start_y = 0.20

    # Account for previous sections
    offset = section_index * SECTION_GAP
    offset += params_before * ROW_SPACING

    return start_y - offset


def calculate_param_y(base_y, row_index):
    """
    Calculate Y position for a parameter row.

    Args:
        base_y: Base Y position (usually section header Y)
        row_index: Index of parameter within section (0-based)

    Returns:
        float: Y position
    """
    return base_y - SECTION_HEADER_GAP - (row_index * ROW_SPACING)


def get_button_x(button_index):
    """
    Get X position for a button in a horizontal row.

    Args:
        button_index: Index of button (0 = first, 1 = second, etc.)

    Returns:
        float: X position
    """
    return BUTTON_X_START + (button_index * (BUTTON_WIDTH + BUTTON_SPACING))
