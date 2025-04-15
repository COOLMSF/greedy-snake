"""
Fancy Snake Game - Main Game with Enhanced Visuals

This file integrates the core game mechanics with fancy visual elements.
"""

import pygame
import sys
import random
import math
import time
from pygame import gfxdraw

# Import our visual elements
from visual_elements import ParticleSystem, BackgroundEffect, EnhancedSnake, EnhancedFood

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

class FancyGame:
    def __init__(self):
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fancy Snake Game")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.state = MENU
        self.score = 0
        self.high_score = 0
        
        # Initialize visual elements
        self.background = BackgroundEffect(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.particles = ParticleSystem()
        
        # Initialize game objects
        self.snake = EnhancedSnake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.food = EnhancedFood()
        self.food.spawn(self.snake.segments)
        
        # Font for text rendering
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 72)
        
        # Game timing
        self.last_update_time = time.time()
        self.move_timer = 0
        self.move_delay = 0.1  # seconds between snake movements
        
        # Menu animation
        self.menu_time = 0
        self.menu_particles = []
        
        # Game over animation
        self.game_over_time = 0
        self.death_particles_created = False
        
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
        # Always update background
        self.background.update(dt)
        
        # Update particles
        self.particles.update(dt)
        
        if self.state == MENU:
            # Update menu animations
            self.menu_time += dt
            self.update_menu_particles(dt)
            
        elif self.state == PLAYING:
            # Update snake animation
            self.snake.update_animation(dt, self.particles)
            
            # Update food animation
            self.food.update(dt)
            
            # Update move timer
            self.move_timer += dt
            if self.move_timer >= self.move_delay:
                self.move_timer = 0
                
                # Move snake
                self.snake.move()
                
                # Check for collisions with food
                if self.snake.head_position == self.food.position:
                    # Create particles at food position
                    x, y = self.food.position
                    self.particles.create_food_particles(x, y, self.food.color)
                    
                    # Grow snake and update score
                    self.snake.grow()
                    self.score += self.food.value * 10
                    self.high_score = max(self.score, self.high_score)
                    
                    # Spawn new food
                    self.food.spawn(self.snake.segments)
                
                # Check for collisions with walls or self
                if self.snake.check_collision():
                    self.state = GAME_OVER
                    self.game_over_time = 0
                    self.death_particles_created = False
                    
        elif self.state == GAME_OVER:
            # Update game over animations
            self.game_over_time += dt
            
            # Create death particles once
            if not self.death_particles_created:
                self.particles.create_death_particles(self.snake.segments)
                self.death_particles_created = True
    
    def update_menu_particles(self, dt):
        # Update existing menu particles
        for particle in self.menu_particles[:]:
            particle['age'] += dt
            if particle['age'] >= particle['lifetime']:
                self.menu_particles.remove(particle)
            else:
                # Update position
                particle['x'] += particle['vx'] * dt
                particle['y'] += particle['vy'] * dt
                # Update alpha
                progress = particle['age'] / particle['lifetime']
                particle['alpha'] = int(255 * (1 - progress))
        
        # Add new particles occasionally
        if random.random() < dt * 5:  # Average 5 particles per second
            self.add_menu_particle()
    
    def add_menu_particle(self):
        """Add ambient particles in the menu screen"""
        # Random position near the edges
        side = random.randint(0, 3)
        if side == 0:  # Top
            x = random.randint(0, SCREEN_WIDTH)
            y = 0
            vx = random.uniform(-20, 20)
            vy = random.uniform(20, 50)
        elif side == 1:  # Right
            x = SCREEN_WIDTH
            y = random.randint(0, SCREEN_HEIGHT)
            vx = random.uniform(-50, -20)
            vy = random.uniform(-20, 20)
        elif side == 2:  # Bottom
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT
            vx = random.uniform(-20, 20)
            vy = random.uniform(-50, -20)
        else:  # Left
            x = 0
            y = random.randint(0, SCREEN_HEIGHT)
            vx = random.uniform(20, 50)
            vy = random.uniform(-20, 20)
        
        # Random color (green/blue hues)
        r = random.randint(0, 100)
        g = random.randint(150, 255)
        b = random.randint(100, 255)
        color = (r, g, b)
        
        self.menu_particles.append({
            'x': x,
            'y': y,
            'vx': vx,
            'vy': vy,
            'size': random.uniform(2, 5),
            'color': color,
            'alpha': 200,
            'lifetime': random.uniform(1.0, 3.0),
            'age': 0,
        })
    
    def render(self):
        # Render background
        self.background.render(self.screen)
        
        if self.state == MENU:
            self.render_menu()
        elif self.state == PLAYING:
            # Draw game elements
            self.food.render(self.screen)
            self.snake.render(self.screen, self.particles)
            self.particles.render(self.screen)
            self.render_hud()
        elif self.state == PAUSED:
            # Draw game elements (dimmed)
            self.food.render(self.screen, dimmed=True)
            self.snake.render(self.screen, self.particles, dimmed=True)
            self.render_hud(dimmed=True)
            self.render_pause_menu()
        elif self.state == GAME_OVER:
            # Draw game elements (dimmed)
            self.food.render(self.screen, dimmed=True)
            self.snake.render(self.screen, self.particles, dimmed=True)
            self.particles.render(self.screen)  # Death particles
            self.render_game_over()
        
        # Update the display
        pygame.display.flip()
    
    def render_menu(self):
        # Render menu particles
        for particle in self.menu_particles:
            pygame.gfxdraw.filled_circle(
                self.screen,
                int(particle['x']),
                int(particle['y']),
                int(particle['size']),
                (*particle['color'], particle['alpha'])
            )
        
        # Title with pulsing effect
        pulse = (math.sin(self.menu_time * 2) + 1) * 0.1
        title_scale = 1.0 + pulse
        title_text = self.title_font.render("FANCY SNAKE", True, GOLD)
        title_rect = title_text.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        
        # Create a slightly larger surface for the title to accommodate the scaling
        scaled_width = int(title_rect.width * title_scale)
        scaled_height = int(title_rect.height * title_scale)
        scaled_surface = pygame.transform.scale(title_text, (scaled_width, scaled_height))
        scaled_rect = scaled_surface.get_rect(center=title_rect.center)
        
        # Draw title with glow effect
        glow_surface = pygame.Surface((scaled_width + 20, scaled_height + 20), pygame.SRCALPHA)
        glow_text = self.title_font.render("FANCY SNAKE", True, (255, 215, 0, 100))
        glow_scaled = pygame.transform.scale(glow_text, (scaled_width + 10, scaled_height + 10))
        glow_rect = glow_scaled.get_rect(center=(glow_surface.get_width()//2, glow_surface.get_height()//2))
        glow_surface.blit(glow_scaled, glow_rect)
        
        # Apply blur effect to glow (simple approximation)
        for i in range(5):
            blur_offset = i + 1
            for offset_x, offset_y in [(blur_offset, 0), (-blur_offset, 0), (0, blur_offset), (0, -blur_offset)]:
                self.screen.blit(glow_surface, (scaled_rect.x - 10 + offset_x, scaled_rect.y - 10 + offset_y))
        
        # Draw the actual title
        self.screen.blit(scaled_surface, scaled_rect)
        
        # Subtitle with color cycling
        hue = (self.menu_time * 50) % 360  # Cycle through hues
        r, g, b = self.hsv_to_rgb(hue, 0.7, 0.9)
        subtitle_text = self.font.render("A Very Fancy Snake Game", True, (r, g, b))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 80))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Menu options with pulsing effect
        pulse_start = (math.sin(self.menu_time * 3) + 1) * 0.5
        start_color = self.lerp_color(WHITE, GOLD, pulse_start)
        start_text = self.font.render("Press ENTER to Start", True, start_color)
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
        
        # Draw animated snake in the background
        self.render_menu_snake()
    
    def render_menu_snake(self):
        """Render an animated snake in the menu background"""
        # Calculate snake path based on time
        t = self.menu_time * 0.5
        points = []
        
        # Create a spiral path
        for i in range(20):
            angle = t + i * 0.3
            radius = 100 + i * 5
            x = SCREEN_WIDTH // 2 + math.cos(angle) * radius
            y = SCREEN_HEIGHT // 2 + math.sin(angle) * radius
            points.append((x, y))
        
        # Draw snake segments along the path
        for i, (x, y) in enumerate(points):
            # Calculate color based on position in snake
            hue = (t * 50 + i * 10) % 360
            r, g, b = self.hsv_to_rgb(hue, 0.8, 0.8)
            
            # Draw segment
            size = 15 - i * 0.5  # Gradually smaller toward tail
            pygame.draw.circle(self.screen, (r, g, b), (int(x), int(y)), max(5, int(size)))
            
            # Draw eyes on the head
            if i == 0:
                # Eyes
                eye_offset = 5
                pygame.draw.circle(self.screen, WHITE, (int(x - eye_offset), int(y - eye_offset)), 3)
                pygame.draw.circle(self.screen, WHITE, (int(x + eye_offset), int(y - eye_offset)), 3)
                
                # Pupils
                pygame.draw.circle(self.screen, BLACK, (int(x - eye_offset), int(y - eye_offset)), 1)
                pygame.draw.circle(self.screen, BLACK, (int(x + eye_offset), int(y - eye_offset)), 1)
    
    def render_hud(self, dimmed=False):
        color = (150, 150, 150) if dimmed else WHITE
        
        # Score with fancy background
        score_bg = pygame.Surface((150, 40), pygame.SRCALPHA)
        pygame.draw.rect(score_bg, (0, 0, 0, 128), score_bg.get_rect(), border_radius=10)
        self.screen.blit(score_bg, (10, 10))
        
        score_text = self.font.render(f"Score: {self.score}", True, color)
        self.screen.blit(score_text, (20, 15))
        
        # High score with fancy background
        high_score_text = self.font.render(f"High: {self.high_score}", True, color)
        high_score_rect = high_score_text.get_rect()
        
        high_score_bg = pygame.Surface((high_score_rect.width + 20, 40), pygame.SRCALPHA)
        pygame.draw.rect(high_score_bg, (0, 0, 0, 128), high_score_bg.get_rect(), border_radius=10)
        self.screen.blit(high_score_bg, (SCREEN_WIDTH - high_score_rect.width - 30, 10))
        
        self.screen.blit(high_score_text, (SCREEN_WIDTH - high_score_rect.width - 20, 15))
    
    def render_pause_menu(self):
        # Semi-transparent overlay with radial gradient
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Create radial gradient
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        max_radius = math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2) / 2
        
        for radius in range(0, int(max_radius), 2):
            alpha = int(128 * (radius / max_radius))
            pygame.gfxdraw.filled_circle(overlay, center[0], center[1], int(max_radius) - radius, (0, 0, 0, alpha))
        
        self.screen.blit(overlay, (0, 0))
        
        # Pause title with glow
        pause_text = self.title_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        
        # Glow effect
        glow_surface = pygame.Surface((pause_rect.width + 20, pause_rect.height + 20), pygame.SRCALPHA)
        glow_text = self.title_font.render("PAUSED", True, (255, 255, 255, 100))
        glow_rect = glow_text.get_rect(center=(glow_surface.get_width()//2, glow_surface.get_height()//2))
        glow_surface.blit(glow_text, glow_rect)
        
        # Apply blur effect to glow (simple approximation)
        for i in range(5):
            blur_offset = i + 1
            for offset_x, offset_y in [(blur_offset, 0), (-blur_offset, 0), (0, blur_offset), (0, -blur_offset)]:
                self.screen.blit(glow_surface, (pause_rect.x - 10 + offset_x, pause_rect.y - 10 + offset_y))
        
        # Draw the actual text
        self.screen.blit(pause_text, pause_rect)
        
        # Menu options with fancy backgrounds
        options = [
            {"text": "Press ENTER to Resume", "y_offset": 0},
            {"text": "Press ESC to Quit to Menu", "y_offset": 60}
        ]
        
        for option in options:
            text = self.font.render(option["text"], True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + option["y_offset"]))
            
            # Background with rounded corners
            bg_rect = text_rect.inflate(40, 20)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(bg_surface, (0, 0, 0, 150), bg_surface.get_rect(), border_radius=10)
            
            # Draw subtle border
            pygame.draw.rect(bg_surface, (100, 100, 100, 100), bg_surface.get_rect(), width=2, border_radius=10)
            
            self.screen.blit(bg_surface, bg_rect)
            self.screen.blit(text, text_rect)
    
    def render_game_over(self):
        # Semi-transparent overlay with radial gradient that expands over time
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Calculate expanding radius based on game over time
        expansion_duration = 1.0  # seconds
        progress = min(1.0, self.game_over_time / expansion_duration)
        
        # Create radial gradient
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        max_radius = math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2) / 2
        current_radius = max_radius * progress
        
        for radius in range(0, int(current_radius), 2):
            alpha = int(192 * (radius / current_radius))
            pygame.gfxdraw.filled_circle(overlay, center[0], center[1], int(current_radius) - radius, (0, 0, 0, alpha))
        
        self.screen.blit(overlay, (0, 0))
        
        # Only show text after the overlay animation is complete
        if progress >= 1.0:
            # Game over title with animation
            title_scale = 1.0 + 0.1 * math.sin(self.game_over_time * 3)
            game_over_text = self.title_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect()
            game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            
            # Scale the text
            scaled_width = int(game_over_rect.width * title_scale)
            scaled_height = int(game_over_rect.height * title_scale)
            scaled_surface = pygame.transform.scale(game_over_text, (scaled_width, scaled_height))
            scaled_rect = scaled_surface.get_rect(center=game_over_rect.center)
            
            # Draw with glow effect
            glow_surface = pygame.Surface((scaled_width + 20, scaled_height + 20), pygame.SRCALPHA)
            glow_text = self.title_font.render("GAME OVER", True, (255, 0, 0, 100))
            glow_scaled = pygame.transform.scale(glow_text, (scaled_width + 10, scaled_height + 10))
            glow_rect = glow_scaled.get_rect(center=(glow_surface.get_width()//2, glow_surface.get_height()//2))
            glow_surface.blit(glow_scaled, glow_rect)
            
            # Apply blur effect to glow
            for i in range(5):
                blur_offset = i + 1
                for offset_x, offset_y in [(blur_offset, 0), (-blur_offset, 0), (0, blur_offset), (0, -blur_offset)]:
                    self.screen.blit(glow_surface, (scaled_rect.x - 10 + offset_x, scaled_rect.y - 10 + offset_y))
            
            # Draw the actual text
            self.screen.blit(scaled_surface, scaled_rect)
            
            # Score with fancy background
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            
            score_bg = pygame.Surface((score_rect.width + 40, score_rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(score_bg, (0, 0, 0, 150), score_bg.get_rect(), border_radius=10)
            self.screen.blit(score_bg, score_rect.inflate(40, 20))
            self.screen.blit(score_text, score_rect)
            
            # Menu options with fancy backgrounds
            options = [
                {"text": "Press ENTER to Play Again", "y_offset": 80},
                {"text": "Press ESC to Return to Menu", "y_offset": 130}
            ]
            
            for option in options:
                text = self.font.render(option["text"], True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + option["y_offset"]))
                
                # Background with rounded corners
                bg_rect = text_rect.inflate(40, 20)
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(bg_surface, (0, 0, 0, 150), bg_surface.get_rect(), border_radius=10)
                
                # Draw subtle border
                pygame.draw.rect(bg_surface, (100, 100, 100, 100), bg_surface.get_rect(), width=2, border_radius=10)
                
                self.screen.blit(bg_surface, bg_rect)
                self.screen.blit(text, text_rect)
    
    def reset_game(self):
        self.snake = EnhancedSnake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.food.spawn(self.snake.segments)
        self.score = 0
        self.move_timer = 0
        self.particles = ParticleSystem()
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV color to RGB"""
        h = h / 360
        i = math.floor(h * 6)
        f = h * 6 - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        
        if i % 6 == 0:
            r, g, b = v, t, p
        elif i % 6 == 1:
            r, g, b = q, v, p
        elif i % 6 == 2:
            r, g, b = p, v, t
        elif i % 6 == 3:
            r, g, b = p, q, v
        elif i % 6 == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q
        
        return int(r * 255), int(g * 255), int(b * 255)
    
    def lerp_color(self, color1, color2, t):
        """Linear interpolation between two colors"""
        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)
        return (r, g, b)


# Main function
def main():
    game = FancyGame()
    game.run()

if __name__ == "__main__":
    main()
