"""Global configuration: dimensions, colors, timings and scoring tables."""

# --- Grid geometry ---------------------------------------------------------
COLS = 10                # number of columns in the playfield
ROWS = 20                # number of visible rows in the playfield
CELL = 30                # pixel size of a single cell
BORDER = 4               # thickness of the wall/border in pixels

# --- Side panel & window ---------------------------------------------------
PANEL_WIDTH = 220        # width of the info panel on the right
MARGIN = 24              # outer margin around everything

PLAY_WIDTH = COLS * CELL
PLAY_HEIGHT = ROWS * CELL

WINDOW_WIDTH = MARGIN * 3 + PLAY_WIDTH + PANEL_WIDTH
WINDOW_HEIGHT = MARGIN * 2 + PLAY_HEIGHT

FPS = 60

# --- Colors (R, G, B) ------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
BG_COLOR = (18, 18, 26)
GRID_COLOR = (40, 40, 55)
BORDER_COLOR = (90, 90, 120)
PANEL_COLOR = (28, 28, 40)
TEXT_COLOR = (230, 230, 240)
GHOST_COLOR = (70, 70, 90)

# A vibrant, high-contrast color for each tetromino type.
PIECE_COLORS = {
    "I": (0, 240, 240),     # cyan
    "O": (240, 240, 0),     # yellow
    "T": (160, 0, 240),     # purple
    "S": (0, 240, 0),       # green
    "Z": (240, 0, 0),       # red
    "J": (0, 0, 240),       # blue
    "L": (240, 160, 0),     # orange
}

# --- Timing ----------------------------------------------------------------
# Gravity delay (ms) per level. Falls faster as the level increases.
BASE_FALL_MS = 800
MIN_FALL_MS = 80
FALL_STEP_MS = 65        # subtracted per level (clamped to MIN_FALL_MS)

LINES_PER_LEVEL = 10     # lines cleared to advance one level

# --- Scoring ---------------------------------------------------------------
# Points awarded for clearing N lines at once (before level multiplier).
LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}
SOFT_DROP_POINTS = 1     # per cell soft-dropped
HARD_DROP_POINTS = 2     # per cell hard-dropped
