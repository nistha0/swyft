"""
SWYFT - Game Configuration
Contains all game constants and settings
"""

# Display settings
WIDTH = 1200
HEIGHT = 600
FPS = 60

# Colors - Sky
SKY_TOP = (135, 206, 250)
SKY_BOTTOM = (220, 240, 255)

# Colors - Terrain
GRASS_GREEN = (76, 187, 23)
GRASS_DARK = (54, 140, 16)

# Colors - UI
COIN_GOLD = (255, 215, 0)
COIN_ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 120, 255)
DARK_BLUE = (0, 80, 180)
GREEN = (0, 200, 100)
YELLOW = (255, 215, 0)

# Physics constants
GRAVITY = 980
ACCELERATION = 500
MAX_SPEED = 500
GROUND_FRICTION = 0.985
AIR_FRICTION = 0.995
ROTATION_SMOOTHING = 8.0

# Car settings
CAR_SCALE = 0.25
CAR_GROUND_OFFSET = 0  # FIXED: Set to 0 so car sits properly on ground

# Camera settings
CAMERA_FOLLOW_SPEED = 6.0
CAMERA_OFFSET_X = 0.35  # Car position as fraction of screen width

# Terrain settings
TERRAIN_SEGMENT_LENGTH = 10
TERRAIN_BASE_HEIGHT = 400  # Raised from 480 to give more vertical space for hills

# Car death settings
CAR_MAX_TILT_ANGLE = 85  # Car dies if tilted more than this (degrees)
CAR_FLIP_DEATH_ENABLED = True  # Enable death from flipping

# Difficulty settings (set by menu)
DIFFICULTY = "MEDIUM"  # Options: "EASY", "MEDIUM", "HARD"

# Difficulty-based parameters
DIFFICULTY_SETTINGS = {
    "EASY": {
        "MAX_TILT_ANGLE": 90,  # Very forgiving
        "FUEL_CONSUMPTION_RATE": 25,  # For keyboard
        "FUEL_IDLE_CONSUMPTION": 3.0,  # For keyboard
        "GESTURE_FUEL_CONSUMPTION": 18,  # Easier for gesture controls
        "GESTURE_FUEL_IDLE": 2.2,  # Easier for gesture controls
        "COIN_SPAWN_FREQUENCY": 0.8,  # More coins
        "TERRAIN_DIFFICULTY": 0.5,
    },
    "MEDIUM": {
        "MAX_TILT_ANGLE": 85,  # Standard
        "FUEL_CONSUMPTION_RATE": 35,  # For keyboard
        "FUEL_IDLE_CONSUMPTION": 4.5,  # For keyboard
        "GESTURE_FUEL_CONSUMPTION": 25,  # Easier for gesture controls
        "GESTURE_FUEL_IDLE": 3.0,  # Easier for gesture controls
        "COIN_SPAWN_FREQUENCY": 1.0,  # Normal
        "TERRAIN_DIFFICULTY": 1.0,
    },
    "HARD": {
        "MAX_TILT_ANGLE": 65,  # Much stricter - easier to flip (was 75)
        "FUEL_CONSUMPTION_RATE": 50,  # For keyboard
        "FUEL_IDLE_CONSUMPTION": 7.0,  # For keyboard
        "GESTURE_FUEL_CONSUMPTION": 35,  # Easier for gesture controls
        "GESTURE_FUEL_IDLE": 5.0,  # Easier for gesture controls
        "COIN_SPAWN_FREQUENCY": 1.2,  # Fewer coins
        "TERRAIN_DIFFICULTY": 1.5,
    }
}

# Coin settings
COIN_SIZE = 28
COIN_DETECTION_RADIUS = 35
COIN_BOB_SPEED = 3
COIN_ROTATION_SPEED = 180
COIN_SPAWN_MIN_DISTANCE = 150
COIN_SPAWN_MAX_DISTANCE = 250
COIN_HEIGHT_ABOVE_GROUND = 80

# Fuel settings
FUEL_INITIAL = 100.0
FUEL_CONSUMPTION_RATE = 35  # Increased from 22 - will be overridden by difficulty
FUEL_IDLE_CONSUMPTION = 4.5  # Increased from 2.5 - will be overridden by difficulty
FUEL_CANISTER_SIZE = 35
FUEL_DETECTION_RADIUS = 40
FUEL_REFILL_AMOUNT = 30.0  # Increased from 25
FUEL_SPAWN_MIN_DISTANCE = 250  # Closer spawning (was 300)
FUEL_SPAWN_MAX_DISTANCE = 550  # Closer spawning (was 700)
FUEL_HEIGHT_ABOVE_GROUND = 80
FUEL_COLOR_RED = (220, 20, 60)
FUEL_COLOR_DARK = (180, 10, 40)

# Cloud settings
NUM_CLOUDS = 6
CLOUD_MIN_SPEED = 10
CLOUD_MAX_SPEED = 30
CLOUD_MIN_SIZE = 20
CLOUD_MAX_SIZE = 50

# Theme settings
CURRENT_THEME = "sunny"  # Options: "sunny", "night", "winter", "rain"

# Obstacle settings
OBSTACLE_ENABLED = True
OBSTACLE_TYPES = ["rock", "log", "barrier"]
OBSTACLE_SPAWN_MIN_DISTANCE = 200
OBSTACLE_SPAWN_MAX_DISTANCE = 400

def get_difficulty_setting(setting_name):
    """Get a difficulty-specific setting"""
    difficulty = DIFFICULTY
    if difficulty in DIFFICULTY_SETTINGS:
        return DIFFICULTY_SETTINGS[difficulty].get(setting_name, globals().get(setting_name))
    return globals().get(setting_name)
