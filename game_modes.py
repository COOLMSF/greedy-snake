"""
Fancy Snake Game - Game Modes and Difficulty Levels

This file implements different game modes and difficulty settings for our fancy Snake game.
"""

import pygame
import random
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Difficulty levels
EASY = 0
MEDIUM = 1
HARD = 2
EXTREME = 3

# Game modes
CLASSIC = 0
TIME_TRIAL = 1
OBSTACLE = 2
MAZE = 3
ZEN = 4

class GameModeManager:
    """Manages different game modes and difficulty settings"""
    
    def __init__(self):
        # Default settings
        self.difficulty = MEDIUM
        self.game_mode = CLASSIC
        
        # Difficulty settings
        self.difficulty_settings = {
            EASY: {
                'move_delay': 0.12,  # Slower snake
                'power_up_interval': 12.0,  # More frequent power-ups
                'food_value': 15,  # More points per food
                'wall_collision': False,  # No wall collisions
                'description': "Easy: Slower snake, no wall collisions"
            },
            MEDIUM: {
                'move_delay': 0.1,
                'power_up_interval': 15.0,
                'food_value': 10,
                'wall_collision': True,
                'description': "Medium: Standard speed, wall collisions"
            },
            HARD: {
                'move_delay': 0.08,  # Faster snake
                'power_up_interval': 20.0,  # Less frequent power-ups
                'food_value': 8,  # Fewer points per food
                'wall_collision': True,
                'description': "Hard: Faster snake, fewer power-ups"
            },
            EXTREME: {
                'move_delay': 0.06,  # Very fast snake
                'power_up_interval': 30.0,  # Rare power-ups
                'food_value': 5,  # Minimal points per food
                'wall_collision': True,
                'description': "Extreme: Very fast snake, rare power-ups"
            }
        }
        
        # Game mode settings
        self.game_mode_settings = {
            CLASSIC: {
                'name': "Classic",
                'description': "Classic Snake: Eat food, grow longer, don't hit walls or yourself",
                'has_obstacles': False,
                'has_time_limit': False,
                'has_maze': False,
                'has_portals': False
            },
            TIME_TRIAL: {
                'name': "Time Trial",
                'description': "Time Trial: Score as many points as possible before time runs out",
                'has_obstacles': False,
                'has_time_limit': True,
                'time_limit': 60.0,  # 60 seconds
                'has_maze': False,
                'has_portals': False
            },
            OBSTACLE: {
                'name': "Obstacle",
                'description': "Obstacle: Navigate around obstacles while collecting food",
                'has_obstacles': True,
                'obstacle_count': 15,
                'has_time_limit': False,
                'has_maze': False,
                'has_portals': False
            },
            MAZE: {
                'name': "Maze",
                'description': "Maze: Find your way through a maze to collect food",
                'has_obstacles': False,
                'has_time_limit': False,
                'has_maze': True,
                'has_portals': True,
                'portal_count': 2
            },
            ZEN: {
                'name': "Zen",
                'description': "Zen Mode: Relaxed gameplay with no death, just enjoy growing",
                'has_obstacles': False,
                'has_time_limit': False,
                'has_maze': False,
                'has_portals': False,
                'no_death': True
            }
        }
        
        # Obstacles for obstacle mode
        self.obstacles = []
        
        # Maze walls for maze mode
        self.maze_walls = []
        
        # Portals for maze mode
        self.portals = []
        
        # Time remaining for time trial mode
        self.time_remaining = 0
    
    def set_difficulty(self, difficulty):
        """Set the game difficulty"""
        if difficulty in self.difficulty_settings:
            self.difficulty = difficulty
    
    def set_game_mode(self, mode):
        """Set the game mode"""
        if mode in self.game_mode_settings:
            self.game_mode = mode
            
            # Initialize mode-specific elements
            if self.game_mode_settings[mode]['has_time_limit']:
                self.time_remaining = self.game_mode_settings[mode]['time_limit']
            
            if self.game_mode_settings[mode]['has_obstacles']:
                self.generate_obstacles()
            else:
                self.obstacles = []
            
            if self.game_mode_settings[mode]['has_maze']:
                self.generate_maze()
            else:
                self.maze_walls = []
            
            if self.game_mode_settings[mode].get('has_portals', False):
                self.generate_portals()
            else:
                self.portals = []
    
    def get_move_delay(self):
        """Get the move delay based on current difficulty"""
        return self.difficulty_settings[self.difficulty]['move_delay']
    
    def get_power_up_interval(self):
        """Get the power-up spawn interval based on current difficulty"""
        return self.difficulty_settings[self.difficulty]['power_up_interval']
    
    def get_food_value(self):
        """Get the base food value based on current difficulty"""
        return self.difficulty_settings[self.difficulty]['food_value']
    
    def has_wall_collision(self):
        """Check if wall collisions are enabled"""
        return self.difficulty_settings[self.difficulty]['wall_collision']
    
    def has_time_limit(self):
        """Check if the current mode has a time limit"""
        return self.game_mode_settings[self.game_mode]['has_time_limit']
    
    def is_no_death_mode(self):
        """Check if the current mode is no-death (Zen mode)"""
        return self.game_mode_settings[self.game_mode].get('no_death', False)
    
    def update(self, dt):
        """Update mode-specific elements"""
        # Update time remaining for time trial mode
        if self.has_time_limit():
            self.time_remaining -= dt
            if self.time_remaining <= 0:
                self.time_remaining = 0
                return True  # Time's up
        
        return False
    
    def generate_obstacles(self):
        """Generate obstacles for obstacle mode"""
        self.obstacles = []
        obstacle_count = self.game_mode_settings[self.game_mode]['obstacle_count']
        
        # Create random obstacles
        for _ in range(obstacle_count):
            x = random.randint(2, GRID_WIDTH - 3)
            y = random.randint(2, GRID_HEIGHT - 3)
            
            # Avoid center area where snake starts
            if abs(x - GRID_WIDTH // 2) < 3 and abs(y - GRID_HEIGHT // 2) < 3:
                continue
            
            self.obstacles.append((x, y))
    
    def generate_maze(self):
        """Generate a simple maze for maze mode"""
        self.maze_walls = []
        
        # Create border walls
        for x in range(GRID_WIDTH):
            self.maze_walls.append((x, 0))
            self.maze_walls.append((x, GRID_HEIGHT - 1))
        
        for y in range(GRID_HEIGHT):
            self.maze_walls.append((0, y))
            self.maze_walls.append((GRID_WIDTH - 1, y))
        
        # Create internal walls
        # Horizontal walls with gaps
        for y in range(5, GRID_HEIGHT - 5, 5):
            gap_pos = random.randint(5, GRID_WIDTH - 6)
            for x in range(1, GRID_WIDTH - 1):
                if not (gap_pos <= x <= gap_pos + 4):
                    self.maze_walls.append((x, y))
        
        # Vertical walls with gaps
        for x in range(5, GRID_WIDTH - 5, 5):
            gap_pos = random.randint(5, GRID_HEIGHT - 6)
            for y in range(1, GRID_HEIGHT - 1):
                if not (gap_pos <= y <= gap_pos + 4):
                    self.maze_walls.append((x, y))
    
    def generate_portals(self):
        """Generate portals for maze mode"""
        self.portals = []
        portal_count = self.game_mode_settings[self.game_mode].get('portal_count', 2)
        
        # Create portal pairs
        for _ in range(portal_count):
            # First portal
            while True:
                x1 = random.randint(2, GRID_WIDTH - 3)
                y1 = random.randint(2, GRID_HEIGHT - 3)
                if (x1, y1) not in self.maze_walls and (x1, y1) not in self.portals:
                    break
            
            # Second portal
            while True:
                x2 = random.randint(2, GRID_WIDTH - 3)
                y2 = random.randint(2, GRID_HEIGHT - 3)
                if (x2, y2) not in self.maze_walls and (x2, y2) not in self.portals and (x2, y2) != (x1, y1):
                    break
            
            # Add portal pair
            self.portals.append(((x1, y1), (x2, y2)))
    
    def check_portal_teleport(self, position):
        """Check if position is on a portal and return the exit position"""
        for portal_pair in self.portals:
            if position == portal_pair[0]:
                return portal_pair[1]
            elif position == portal_pair[1]:
                return portal_pair[0]
        return None
    
    def is_valid_spawn_position(self, position, snake_segments):
        """Check if a position is valid for spawning food or power-ups"""
        x, y = position
        
        # Check if position is within bounds
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return False
        
        # Check if position is occupied by snake
        if position in snake_segments:
            return False
        
        # Check if position is occupied by obstacle
        if position in self.obstacles:
            return False
        
        # Check if position is occupied by maze wall
        if position in self.maze_walls:
            return False
        
        # Check if position is occupied by portal
        for portal_pair in self.portals:
            if position == portal_pair[0] or position == portal_pair[1]:
                return False
        
        return True
    
    def render(self, surface):
        """Render mode-specific elements"""
        # Render obstacles
        for x, y in self.obstacles:
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, (150, 75, 0), rect)  # Brown obstacles
            
            # Add some texture
            for i in range(3):
                pygame.draw.line(
                    surface,
                    (100, 50, 0),
                    (x * GRID_SIZE + i * 5, y * GRID_SIZE),
                    (x * GRID_SIZE + i * 5, y * GRID_SIZE + GRID_SIZE),
                    1
                )
        
        # Render maze walls
        for x, y in self.maze_walls:
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, (100, 100, 150), rect)  # Blue-gray walls
            
            # Add some texture
            pygame.draw.rect(surface, (80, 80, 120), rect, 1)
            pygame.draw.line(
                surface,
                (120, 120, 170),
                (x * GRID_SIZE, y * GRID_SIZE),
                (x * GRID_SIZE + GRID_SIZE, y * GRID_SIZE + GRID_SIZE),
                1
            )
        
        # Render portals
        for portal_pair in self.portals:
            for i, (x, y) in enumerate(portal_pair):
                # Different colors for each end of the portal pair
                color = (0, 191, 255) if i == 0 else (255, 105, 180)  # Blue and pink
                
                # Draw portal
                center_x = (x + 0.5) * GRID_SIZE
                center_y = (y + 0.5) * GRID_SIZE
                
                # Draw outer circle
                pygame.draw.circle(surface, color, (center_x, center_y), GRID_SIZE // 2)
                
                # Draw inner circle
                pygame.draw.circle(surface, (0, 0, 0), (center_x, center_y), GRID_SIZE // 3)
                
                # Draw swirl
                for j in range(8):
                    angle = j * math.pi / 4 + pygame.time.get_ticks() / 1000
                    radius = GRID_SIZE // 4
                    end_x = center_x + math.cos(angle) * radius
                    end_y = center_y + math.sin(angle) * radius
                    pygame.draw.line(surface, color, (center_x, center_y), (end_x, end_y), 2)
        
        # Render time remaining for time trial mode
        if self.has_time_limit():
            # Draw time bar at the top
            bar_width = SCREEN_WIDTH - 20
            bar_height = 15
            bar_x = 10
            bar_y = 40
            
            # Background
            pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            
            # Progress
            progress = self.time_remaining / self.game_mode_settings[self.game_mode]['time_limit']
            progress_width = int(bar_width * progress)
            
            # Color changes from green to yellow to red as time decreases
            if progress > 0.6:
                color = (0, 255, 0)  # Green
            elif progress > 0.3:
                color = (255, 255, 0)  # Yellow
            else:
                color = (255, 0, 0)  # Red
            
            pygame.draw.rect(surface, color, (bar_x, bar_y, progress_width, bar_height))
            
            # Border
            pygame.draw.rect(surface, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 1)
            
            # Text
            font = pygame.font.Font(None, 20)
            time_text = font.render(f"Time: {int(self.time_remaining)}s", True, (255, 255, 255))
            surface.blit(time_text, (bar_x + 5, bar_y - 2))
    
    def render_mode_info(self, surface, x, y):
        """Render current mode and difficulty info"""
        mode_name = self.game_mode_settings[self.game_mode]['name']
        difficulty_name = ["Easy", "Medium", "Hard", "Extreme"][self.difficulty]
        
        font = pygame.font.Font(None, 24)
        text = font.render(f"Mode: {mode_name} | Difficulty: {difficulty_name}", True, (200, 200, 200))
        surface.blit(text, (x, y))
    
    def render_mode_selection(self, surface, selected_mode, selected_difficulty):
        """Render mode and difficulty selection screen"""
        # Title
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("Game Mode & Difficulty", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title_text, title_rect)
        
        # Mode selection
        mode_font = pygame.font.Font(None, 36)
        mode_title = mode_font.render("Select Game Mode:", True, (255, 255, 255))
        surface.blit(mode_title, (SCREEN_WIDTH // 4 - 100, 150))
        
        for i, mode in enumerate(self.game_mode_settings.keys()):
            mode_name = self.game_mode_settings[mode]['name']
            mode_desc = self.game_mode_settings[mode]['description']
            
            # Highlight selected mode
            if mode == selected_mode:
                color = (255, 255, 0)  # Yellow for selected
                pygame.draw.rect(surface, (50, 50, 50), (SCREEN_WIDTH // 4 - 110, 190 + i * 60, 300, 50), border_radius=5)
            else:
                color = (200, 200, 200)
            
            # Mode name
            mode_text = mode_font.render(mode_name, True, color)
            surface.blit(mode_text, (SCREEN_WIDTH // 4 - 100, 200 + i * 60))
            
            # Mode description
            desc_font = pygame.font.Font(None, 20)
            desc_text = desc_font.render(mode_desc, True, (150, 150, 150))
            surface.blit(desc_text, (SCREEN_WIDTH // 4 - 100, 225 + i * 60))
        
        # Difficulty selection
        diff_title = mode_font.render("Select Difficulty:", True, (255, 255, 255))
        surface.blit(diff_title, (3 * SCREEN_WIDTH // 4 - 100, 150))
        
        for i, diff in enumerate(self.difficulty_settings.keys()):
            diff_desc = self.difficulty_settings[diff]['description']
            
            # Highlight selected difficulty
            if diff == selected_difficulty:
                color = (255, 255, 0)  # Yellow for selected
                pygame.draw.rect(surface, (50, 50, 50), (3 * SCREEN_WIDTH // 4 - 110, 190 + i * 60, 300, 50), border_radius=5)
            else:
                color = (200, 200, 200)
            
            # Difficulty name and description
            diff_text = mode_font.render(diff_desc, True, color)
            surface.blit(diff_text, (3 * SCREEN_WIDTH // 4 - 100, 200 + i * 60))
        
        # Instructions
        inst_font = pygame.font.Font(None, 24)
        inst_text = inst_font.render("Use arrow keys to navigate, Enter to select, Space to start game", True, (200, 200, 200))
        inst_rect = inst_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        surface.blit(inst_text, inst_rect)


# Test function
def test_game_modes():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Modes Test")
    clock = pygame.time.Clock()
    
    # Create game mode manager
    mode_manager = GameModeManager()
    mode_manager.set_game_mode(MAZE)  # Test maze mode
    
    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Change mode
                    current_mode = mode_manager.game_mode
                    mode_manager.set_game_mode((current_mode + 1) % 5)
        
        # Update
        dt = clock.tick(60) / 1000.0
        mode_manager.update(dt)
        
        # Render
        screen.fill((0, 0, 30))
        mode_manager.render(screen)
        mode_manager.render_mode_info(screen, 10, 10)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    test_game_modes()
