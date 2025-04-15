"""
Fancy Snake Game - Main Game Implementation

This file implements the core game mechanics for our fancy Snake game.
"""

import pygame
import sys
import random
import math
import time
from pygame import gfxdraw

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)
TEAL = (0, 128, 128)

# Game states
MENU = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3

class Game:
    def __init__(self):
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fancy Snake Game")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = MENU
        self.score = 0
        self.high_score = 0
        
        # Initialize game objects
        self.snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.food = Food()
        self.food.spawn(self.snake.segments)
        
        # Font for text rendering
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Background
        self.bg_color = BLACK
        
        # Game timing
        self.last_update_time = time.time()
        self.move_timer = 0
        self.move_delay = 0.1  # seconds between snake movements
        
    def run(self):
        running = True
        while running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - self.last_update_time
            self.last_update_time = current_time
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_events(event)
            
            # Update game state
            self.update(dt)
            
            # Render
            self.render()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if self.state == MENU:
                if event.key == pygame.K_RETURN:
                    self.state = PLAYING
            elif self.state == PLAYING:
                if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                    self.snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                    self.snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                    self.snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                    self.snake.change_direction((1, 0))
                elif event.key == pygame.K_ESCAPE:
                    self.state = PAUSED
            elif self.state == PAUSED:
                if event.key == pygame.K_RETURN:
                    self.state = PLAYING
                elif event.key == pygame.K_ESCAPE:
                    self.state = MENU
            elif self.state == GAME_OVER:
                if event.key == pygame.K_RETURN:
                    self.reset_game()
                    self.state = PLAYING
                elif event.key == pygame.K_ESCAPE:
                    self.reset_game()
                    self.state = MENU
    
    def update(self, dt):
        if self.state == PLAYING:
            # Update move timer
            self.move_timer += dt
            if self.move_timer >= self.move_delay:
                self.move_timer = 0
                
                # Move snake
                self.snake.move()
                
                # Check for collisions with food
                if self.snake.head_position == self.food.position:
                    self.snake.grow()
                    self.score += 10
                    self.high_score = max(self.score, self.high_score)
                    self.food.spawn(self.snake.segments)
                
                # Check for collisions with walls or self
                if self.snake.check_collision():
                    self.state = GAME_OVER
    
    def render(self):
        # Clear the screen
        self.screen.fill(self.bg_color)
        
        # Draw grid lines (subtle)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (30, 30, 30), (0, y), (SCREEN_WIDTH, y))
        
        if self.state == MENU:
            self.render_menu()
        elif self.state == PLAYING:
            # Draw game elements
            self.snake.render(self.screen)
            self.food.render(self.screen)
            self.render_hud()
        elif self.state == PAUSED:
            # Draw game elements (dimmed)
            self.snake.render(self.screen, dimmed=True)
            self.food.render(self.screen, dimmed=True)
            self.render_hud(dimmed=True)
            self.render_pause_menu()
        elif self.state == GAME_OVER:
            # Draw game elements (dimmed)
            self.snake.render(self.screen, dimmed=True)
            self.food.render(self.screen, dimmed=True)
            self.render_game_over()
        
        # Update the display
        pygame.display.flip()
    
    def render_menu(self):
        # Title
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("FANCY SNAKE", True, GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font.render("A Very Fancy Snake Game", True, TEAL)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 50))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Menu options
        start_text = self.font.render("Press ENTER to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(start_text, start_rect)
        
        # High score
        if self.high_score > 0:
            high_score_text = self.font.render(f"High Score: {self.high_score}", True, GOLD)
            high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(high_score_text, high_score_rect)
        
        # Controls
        controls_text = self.small_font.render("Controls: Arrow Keys to move, ESC to pause", True, WHITE)
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(controls_text, controls_rect)
    
    def render_hud(self, dimmed=False):
        color = (150, 150, 150) if dimmed else WHITE
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, color)
        self.screen.blit(score_text, (10, 10))
        
        # High score
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, color)
        high_score_rect = high_score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        self.screen.blit(high_score_text, high_score_rect)
    
    def render_pause_menu(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Pause title
        pause_text = self.font.render("GAME PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(pause_text, pause_rect)
        
        # Menu options
        resume_text = self.font.render("Press ENTER to Resume", True, WHITE)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(resume_text, resume_rect)
        
        quit_text = self.font.render("Press ESC to Quit to Menu", True, WHITE)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(quit_text, quit_rect)
    
    def render_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 192))
        self.screen.blit(overlay, (0, 0))
        
        # Game over title
        game_over_text = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(game_over_text, game_over_rect)
        
        # Score
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(score_text, score_rect)
        
        # Menu options
        restart_text = self.font.render("Press ENTER to Play Again", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font.render("Press ESC to Return to Menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        self.screen.blit(menu_text, menu_rect)
    
    def reset_game(self):
        self.snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.food.spawn(self.snake.segments)
        self.score = 0
        self.move_timer = 0


class Snake:
    def __init__(self, x, y):
        self.segments = [(x, y), (x-1, y), (x-2, y)]  # Head is first element
        self.direction = (1, 0)  # Moving right initially
        self.growth_pending = 0
        self.colors = [
            (0, 255, 0),      # Head color
            (0, 220, 0),      # Body color 1
            (0, 200, 0),      # Body color 2
        ]
    
    @property
    def head_position(self):
        return self.segments[0]
    
    def move(self):
        # Calculate new head position
        head_x, head_y = self.head_position
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
        
        # Add new head
        self.segments.insert(0, new_head)
        
        # Remove tail if no growth is pending
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.segments.pop()
    
    def grow(self):
        self.growth_pending += 1
    
    def check_collision(self):
        # Check for collision with self
        if self.head_position in self.segments[1:]:
            return True
        return False
    
    def change_direction(self, new_direction):
        self.direction = new_direction
    
    def render(self, surface, dimmed=False):
        alpha = 128 if dimmed else 255
        
        # Draw each segment
        for i, (x, y) in enumerate(self.segments):
            # Calculate color based on segment position
            if i == 0:  # Head
                color = self.colors[0]
            else:  # Body
                color_index = (i % 2) + 1
                color = self.colors[color_index]
            
            # Apply dimming if needed
            if dimmed:
                color = (color[0] // 2, color[1] // 2, color[2] // 2)
            
            # Calculate position and size
            rect = pygame.Rect(
                x * GRID_SIZE, 
                y * GRID_SIZE, 
                GRID_SIZE, 
                GRID_SIZE
            )
            
            # Draw rounded rectangle for each segment
            self.draw_rounded_rect(surface, rect, color, 5)
            
            # Draw eyes on the head
            if i == 0:
                self.draw_eyes(surface, x, y, dimmed)
    
    def draw_rounded_rect(self, surface, rect, color, radius):
        """Draw a rounded rectangle"""
        if radius < 1:
            pygame.draw.rect(surface, color, rect)
            return
        
        # Ensure radius is not too large for the rectangle
        radius = min(radius, rect.width // 2, rect.height // 2)
        
        # Draw the main rectangle
        pygame.draw.rect(surface, color, rect, border_radius=radius)
    
    def draw_eyes(self, surface, x, y, dimmed=False):
        """Draw eyes on the snake's head"""
        eye_color = (50, 50, 50) if dimmed else (0, 0, 0)
        pupil_color = (200, 200, 200) if dimmed else WHITE
        
        # Eye positions depend on direction
        dx, dy = self.direction
        
        # Base positions
        left_eye_x = x * GRID_SIZE + GRID_SIZE // 4
        right_eye_x = x * GRID_SIZE + 3 * GRID_SIZE // 4
        left_eye_y = y * GRID_SIZE + GRID_SIZE // 3
        right_eye_y = y * GRID_SIZE + GRID_SIZE // 3
        
        # Adjust based on direction
        if dx == 1:  # Right
            pass  # Default position is for right direction
        elif dx == -1:  # Left
            left_eye_y = y * GRID_SIZE + 2 * GRID_SIZE // 3
            right_eye_y = y * GRID_SIZE + 2 * GRID_SIZE // 3
        elif dy == -1:  # Up
            left_eye_x = x * GRID_SIZE + GRID_SIZE // 3
            right_eye_x = x * GRID_SIZE + 2 * GRID_SIZE // 3
            left_eye_y = y * GRID_SIZE + GRID_SIZE // 4
            right_eye_y = y * GRID_SIZE + GRID_SIZE // 4
        elif dy == 1:  # Down
            left_eye_x = x * GRID_SIZE + GRID_SIZE // 3
            right_eye_x = x * GRID_SIZE + 2 * GRID_SIZE // 3
            left_eye_y = y * GRID_SIZE + 2 * GRID_SIZE // 3
            right_eye_y = y * GRID_SIZE + 2 * GRID_SIZE // 3
        
        # Draw eyes
        pygame.draw.circle(surface, eye_color, (left_eye_x, left_eye_y), GRID_SIZE // 6)
        pygame.draw.circle(surface, eye_color, (right_eye_x, right_eye_y), GRID_SIZE // 6)
        
        # Draw pupils
        pupil_offset_x = dx * GRID_SIZE // 12
        pupil_offset_y = dy * GRID_SIZE // 12
        pygame.draw.circle(surface, pupil_color, 
                          (left_eye_x + pupil_offset_x, left_eye_y + pupil_offset_y), 
                          GRID_SIZE // 10)
        pygame.draw.circle(surface, pupil_color, 
                          (right_eye_x + pupil_offset_x, right_eye_y + pupil_offset_y), 
                          GRID_SIZE // 10)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.pulse_speed = 2  # Speed of pulsing animation
        self.pulse_time = 0   # Time counter for pulsing
        self.glow_radius = GRID_SIZE // 2  # Base radius for glow effect
    
    def spawn(self, snake_segments):
        # Find a position not occupied by the snake
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_segments:
                self.position = (x, y)
                break
    
    def render(self, surface, dimmed=False):
        x, y = self.position
        
        # Calculate pulsing effect
        self.pulse_time += 0.1
        pulse = abs(math.sin(self.pulse_time * self.pulse_speed))
        size = int(GRID_SIZE * 0.6 + pulse * GRID_SIZE * 0.2)
        
        # Apply dimming if needed
        color = (self.color[0] // 2, self.color[1] // 2, self.color[2] // 2) if dimmed else self.color
        
        # Draw food with glow effect
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        
        # Draw glow (if not dimmed)
        if not dimmed:
            glow_size = self.glow_radius + int(pulse * GRID_SIZE * 0.3)
            for i in range(glow_size, 0, -2):
                alpha = 100 - (i * 100 // glow_size)
                glow_color = (color[0], color[1], color[2], alpha)
                pygame.gfxdraw.filled_circle(surface, center_x, center_y, i, glow_color)
        
        # Draw main food item
        pygame.draw.circle(surface, color, (center_x, center_y), size // 2)
        
        # Draw highlight
        highlight_size = size // 4
        highlight_pos = (center_x - size // 6, center_y - size // 6)
        pygame.draw.circle(surface, (255, 255, 255, 180), highlight_pos, highlight_size)


# Main function
def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
