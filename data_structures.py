"""
Fancy Snake Game - Data Structures Design

This file outlines the data structures used for the snake, food, and other game elements.
"""

# Snake Data Structure
"""
The snake is represented as a list of positions (segments), where each position is a tuple (x, y).
The first element in the list is the head of the snake.

Example:
snake_segments = [(10, 10), (9, 10), (8, 10)]  # Snake of length 3 facing right

Direction is represented as a tuple (dx, dy) where:
- UP = (0, -1)
- DOWN = (0, 1)
- LEFT = (-1, 0)
- RIGHT = (1, 0)

The snake moves by adding a new head position and removing the tail segment,
unless it has eaten food, in which case the tail segment is not removed.

Snake properties include:
- segments: List of (x, y) positions
- direction: Current movement direction
- speed: Movement speed in grid units per second
- color: Base color of the snake
- special_effects: List of active effects from power-ups
- growth_pending: Number of segments to add (after eating food)
"""

# Food Data Structure
"""
Food items are represented as objects with position and type.

Example:
food = {
    'position': (15, 15),  # (x, y) coordinates
    'type': 'regular',     # or 'bonus', 'special', etc.
    'value': 1,            # points or growth amount
    'color': (255, 0, 0),  # RGB color
    'sprite_index': 0,     # Index in sprite sheet
    'effect': None         # Special effect when eaten
}

Different food types provide different point values and may trigger special effects.
"""

# Power-Up Data Structure
"""
Power-ups are represented as objects with position, type, and duration.

Example:
power_up = {
    'position': (20, 15),       # (x, y) coordinates
    'type': 'speed_boost',      # Type of power-up
    'duration': 5.0,            # Duration in seconds
    'active': False,            # Whether currently active
    'collect_time': None,       # When it was collected
    'color': (0, 255, 255),     # RGB color
    'sprite_index': 2,          # Index in sprite sheet
    'effect_strength': 1.5      # Strength of the effect (e.g., speed multiplier)
}

Power-up types include:
- speed_boost: Increases snake speed
- slow_motion: Decreases snake speed
- invincibility: Snake can pass through itself
- double_points: Doubles points from food
- ghost_mode: Snake can pass through walls
"""

# Particle Data Structure
"""
Particles are used for visual effects and are represented as objects.

Example:
particle = {
    'position': (12, 12),       # (x, y) coordinates
    'velocity': (0.5, -0.5),    # Movement direction and speed
    'size': 3,                  # Size in pixels
    'color': (255, 255, 0),     # RGB color
    'lifetime': 1.0,            # Total lifetime in seconds
    'age': 0.0,                 # Current age in seconds
    'alpha': 255                # Transparency (0-255)
}

Particles are created in bursts for effects like:
- Food collection
- Power-up activation
- Snake movement trail
- Game over explosion
"""

# Grid System
"""
The game uses a grid system for positioning elements.

Grid properties:
- cell_size: Size of each grid cell in pixels (e.g., 20x20)
- grid_width: Number of horizontal cells
- grid_height: Number of vertical cells

Converting between grid and pixel coordinates:
- pixel_x = grid_x * cell_size
- pixel_y = grid_y * cell_size
- grid_x = pixel_x // cell_size
- grid_y = pixel_y // cell_size

The grid system simplifies collision detection and movement logic.
"""

# Score System
"""
The scoring system tracks player performance.

Score components:
- base_score: Points accumulated from eating food
- time_bonus: Bonus points based on game duration
- difficulty_multiplier: Score multiplier based on game difficulty
- combo_multiplier: Temporary multiplier for eating food in quick succession

High scores are stored as a list of dictionaries:
high_scores = [
    {'name': 'Player1', 'score': 1000, 'length': 25, 'difficulty': 'Hard', 'date': '2025-04-10'},
    {'name': 'Player2', 'score': 800, 'length': 20, 'difficulty': 'Medium', 'date': '2025-04-09'},
    # ...
]
"""
