"""
Fancy Snake Game - Game States Design

This file outlines the game states and transitions for our fancy Snake game implementation.
"""

class GameState:
    """
    Base class for all game states.
    
    Each state handles its own events, updates, and rendering.
    """
    
    def __init__(self, game):
        """Initialize with reference to the main game object"""
        self.game = game
        
    def enter(self):
        """Called when entering this state"""
        pass
        
    def exit(self):
        """Called when exiting this state"""
        pass
        
    def handle_events(self, events):
        """Handle input events specific to this state"""
        pass
        
    def update(self, dt):
        """Update game elements specific to this state"""
        pass
        
    def render(self, surface):
        """Render elements specific to this state"""
        pass


class MenuState(GameState):
    """
    Main menu state with options to start game, select difficulty, view high scores, etc.
    """
    
    def __init__(self, game):
        super().__init__(game)
        self.menu_options = ["Start Game", "Difficulty", "High Scores", "Options", "Quit"]
        self.selected_option = 0
        
    def handle_events(self, events):
        """Handle menu navigation and selection"""
        pass
        
    def update(self, dt):
        """Update menu animations and effects"""
        pass
        
    def render(self, surface):
        """Render menu options with fancy effects"""
        pass


class PlayingState(GameState):
    """
    Main gameplay state where the snake moves and interacts with the game world.
    """
    
    def __init__(self, game):
        super().__init__(game)
        
    def enter(self):
        """Initialize snake, food, and game elements"""
        pass
        
    def handle_events(self, events):
        """Handle snake movement controls"""
        pass
        
    def update(self, dt):
        """Update snake, food, power-ups, and check for collisions"""
        pass
        
    def render(self, surface):
        """Render the game world, snake, food, and UI elements"""
        pass


class PausedState(GameState):
    """
    Paused game state where gameplay is temporarily suspended.
    """
    
    def __init__(self, game):
        super().__init__(game)
        self.pause_options = ["Resume", "Restart", "Options", "Quit to Menu"]
        self.selected_option = 0
        
    def handle_events(self, events):
        """Handle pause menu navigation and selection"""
        pass
        
    def update(self, dt):
        """Update pause menu animations"""
        pass
        
    def render(self, surface):
        """Render paused game with overlay and menu options"""
        pass


class GameOverState(GameState):
    """
    Game over state displayed when the player loses.
    """
    
    def __init__(self, game):
        super().__init__(game)
        self.game_over_options = ["Play Again", "High Scores", "Quit to Menu"]
        self.selected_option = 0
        
    def enter(self):
        """Set up game over screen and check for high score"""
        pass
        
    def handle_events(self, events):
        """Handle game over menu navigation and selection"""
        pass
        
    def update(self, dt):
        """Update game over animations and effects"""
        pass
        
    def render(self, surface):
        """Render game over screen with score and options"""
        pass


# State transition diagram:
"""
┌─────────────┐     Start Game     ┌─────────────┐
│             │ ─────────────────> │             │
│  MenuState  │                    │ PlayingState│
│             │ <───────────────── │             │
└─────────────┘     Game Over      └─────────────┘
      ^                                  │ ^
      │                                  │ │
      │                                  │ │
      │                                  ▼ │
      │            ┌─────────────┐        │
      │            │             │        │
      └────────────┤ GameOverState│        │
                   │             │        │
                   └─────────────┘        │
                         ^                │
                         │                │
                         │                │
                         │                │
                   ┌─────────────┐        │
                   │             │        │
                   │ PausedState │ <──────┘
                   │             │  Pause
                   └─────────────┘
                         │
                         │ Resume
                         ▼
                   ┌─────────────┐
                   │             │
                   │ PlayingState│
                   │             │
                   └─────────────┘
"""
