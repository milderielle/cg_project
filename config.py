# Configuration file for Animated Billboard Designer

# Canvas settings
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CANVAS_BG_COLOR = (255, 255, 255)

# Shape settings
DEFAULT_CONTROL_POINTS_TARGET = 12  # Default number of control points per shape
MIN_CONTROL_POINTS = 4
MAX_CONTROL_POINTS = 50

# Animation settings
ANIMATION_FPS = 30
ANIMATION_DURATION = 2.0  # seconds per shape-to-shape transition
LOOP_SMOOTHLY = True  # Ensure smooth loop from last to first shape

# Point display settings
POINT_RADIUS = 5
POINT_COLOR = (255, 0, 0)
POINT_SELECTED_COLOR = (0, 255, 0)
CONTROL_POINT_COLOR = (100, 100, 255)

# Curve drawing settings
CURVE_COLOR = (0, 100, 200)
CURVE_WIDTH = 2
CURVE_RESOLUTION = 100  # Number of segments to draw per curve

# UI settings
UI_FONT_SIZE = 12
STATUS_BAR_HEIGHT = 30

# Easing function default
DEFAULT_EASING = 'ease-in-out'

# File settings
SAVE_FORMAT = '.shape'  # Shape file format
ANIMATION_EXPORT_FORMAT = '.mp4'  # Animation export format
