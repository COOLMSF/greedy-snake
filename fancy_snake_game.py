"""
Fancy Snake Game - Integration and Testing

This file integrates all components and provides a complete game implementation.
"""

import pygame
import sys
import random
import math
import time
import os
from pygame import gfxdraw

# Import our custom modules
from visual_elements import ParticleSystem, BackgroundEffect, EnhancedSnake, EnhancedFood
from sound_manager import SoundManager
from power_ups import PowerUpManager
from game_modes import GameModeManager, CLASSIC, MEDIUM

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
MODE_SELECT = 1
PLAYING = 2
PAUSED = 3
GAME_OVER = 4

class FancySnakeGame:
    def __init__(self):
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fancy Snake Game")
        self.clock = pygame.time.Clock()
        
        # Create directories if they don't exist
        os.makedirs('sounds', exist_ok=True)
        
        # Game state
        self.state = MENU
        self.score = 0
        self.high_score = 0
        
        # Initialize managers
        self.sound_manager = SoundManager()
        self.power_up_manager = PowerUpManager()
        self.game_mode_manager = GameModeManager()
        
        # Set initial game mode and difficulty
        self.game_mode_manager.set_game_mode(CLASSIC)
        self.game_mode_manager.set_difficulty(MEDIUM)
        
        # Mode selection variables
        self.selected_mode = CLASSIC
        self.selected_difficulty = MEDIUM
        
        # Initialize visual elements
        self.background = BackgroundEffect(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.particles = ParticleSystem()
        
        # Initialize game objects
        self.reset_game()
        
        # Font for text rendering
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 72)
        
        # Game timing
        self.last_update_time = time.time()
        self.move_timer = 0
        self.base_move_delay = self.game_mode_manager.get_move_delay()
        self.move_delay = self.base_move_delay
        
        # Menu animation
        self.menu_time = 0
        self.menu_particles = []
        
        # Game over animation
        self.game_over_time = 0
        self.death_particles_created = False
        
        # Play menu music
        self.sound_manager.play_music('menu')
    
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
                    self.sound_manager.play_sound('menu_select')
                    self.state = MODE_SELECT
                elif event.key == pygame.K_SPACE:
                    self.sound_manager.play_sound('menu_select')
                    # Quick start with default settings
                    self.reset_game()
                    self.state = PLAYING
                    self.sound_manager.stop_music()
                    self.sound_manager.play_music('gameplay')
            
            elif self.state == MODE_SELECT:
                if event.key == pygame.K_RETURN:
                    self.sound_manager.play_sound('menu_select')
                    # Apply selected mode and difficulty
                    self.game_mode_manager.set_game_mode(self.selected_mode)
                    self.game_mode_manager.set_difficulty(self.selected_difficulty)
                    self.reset_game()
                    self.state = PLAYING
                    self.sound_manager.stop_music()
                    self.sound_manager.play_music('gameplay')
                elif event.key == pygame.K_SPACE:
                    self.sound_manager.play_sound('menu_select')
                    # Start game with current selections
                    self.game_mode_manager.set_game_mode(self.selected_mode)
                    self.game_mode_manager.set_difficulty(self.selected_difficulty)
                    self.reset_game()
                    self.state = PLAYING
                    self.sound_manager.stop_music()
                    self.sound_manager.play_music('gameplay')
                elif event.key == pygame.K_ESCAPE:
                    self.sound_manager.play_sound('menu_navigate')
                    self.state = MENU
                elif event.key == pygame.K_UP:
                    self.sound_manager.play_sound('menu_navigate')
                    if self.selected_mode > 0:
                        self.selected_mode -= 1
                elif event.key == pygame.K_DOWN:
                    self.sound_manager.play_sound('menu_navigate')
                    if self.selected_mode < 4:  # 5 game modes (0-4)
                        self.selected_mode += 1
                elif event.key == pygame.K_LEFT:
                    self.sound_manager.play_sound('menu_navigate')
                    if self.selected_difficulty > 0:
                        self.selected_difficulty -= 1
                elif event.key == pygame.K_RIGHT:
                    self.sound_manager.play_sound('menu_navigate')
                    if self.selected_difficulty < 3:  # 4 difficulty levels (0-3)
                        self.selected_difficulty += 1
            
            elif self.state == PLAYING:
                if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                    self.snake.change_direction((0, -1))
                    self.sound_manager.play_sound('move')
                elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                    self.snake.change_direction((0, 1))
                    self.sound_manager.play_sound('move')
                elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                    self.snake.change_direction((-1, 0))
                    self.sound_manager.play_sound('move')
                elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                    self.snake.change_direction((1, 0))
                    self.sound_manager.play_sound('move')
                elif event.key == pygame.K_ESCAPE:
                    self.sound_manager.play_sound('menu_select')
                    self.state = PAUSED
            
            elif self.state == PAUSED:
                if event.key == pygame.K_RETURN:
                    self.sound_manager.play_sound('menu_select')
                    self.state = PLAYING
                elif event.key == pygame.K_ESCAPE:
                    self.sound_manager.play_sound('menu_select')
                    self.state = MENU
                    self.sound_manager.stop_music()
                    self.sound_manager.play_music('menu')
            
            elif self.state == GAME_OVER:
                if event.key == pygame.K_RETURN:
                    self.sound_manager.play_sound('menu_select')
                    self.reset_game()
                    self.state = PLAYING
                    self.sound_manager.stop_music()
                    self.sound_manager.play_music('gameplay')
                elif event.key == pygame.K_ESCAPE:
                    self.sound_manager.play_sound('menu_select')
                    self.reset_game()
                    self.state = MENU
                    self.sound_manager.stop_music()
                    self.sound_manager.play_music('menu')
    
    def update(self, dt):
        # Always update background
        self.background.update(dt)
        
        # Update particles
        self.particles.update(dt)
        
        if self.state == MENU:
            # Update menu animations
            self.menu_time += dt
            self.update_menu_particles(dt)
            
        elif self.state == MODE_SELECT:
            # No special updates needed for mode selection
            pass
            
        elif self.state == PLAYING:
            # Update snake animation
            self.snake.update_animation(dt, self.particles)
            
            # Update food animation
            self.food.update(dt)
            
            # Update power-ups
            self.power_up_manager.update(dt, self.snake, self.food)
            
            # Apply power-up effects
            self.power_up_manager.apply_effects(self.snake, self)
            
            # Apply magnet effect if active
            self.power_up_manager.apply_magnet_effect(self.food, self.snake)
            
            # Update game mode specific elements
            if self.game_mode_manager.update(dt):
                # Time's up in time trial mode
                self.state = GAME_OVER
                self.game_over_time = 0
                self.death_particles_created = False
                self.sound_manager.play_sound('game_over')
                self.sound_manager.stop_music()
                self.sound_manager.play_music('game_over')
                return
            
            # Update move timer
            self.move_timer += dt
            if self.move_timer >= self.move_delay:
                self.move_timer = 0
                
                # Move snake
                self.snake.move()
                
                # Check for portal teleportation
                portal_exit = self.game_mode_manager.check_portal_teleport(self.snake.head_position)
                if portal_exit:
                    # Teleport snake head
                    self.snake.segments[0] = portal_exit
                    self.sound_manager.play_sound('power_up')  # Reuse power-up sound for teleport
                
                # Check for collisions with food
                if self.snake.head_position == self.food.position:
                    # Create particles at food position
                    x, y = self.food.position
                    self.particles.create_food_particles(x, y, self.food.color)
                    
                    # Play sound
                    self.sound_manager.play_sound('eat')
                    
                    # Grow snake and update score
                    self.snake.grow()
                    
                    # Calculate score with power-up multiplier
                    score_value = self.game_mode_manager.get_food_value() * 10
                    score_multiplier = self.power_up_manager.get_score_multiplier()
                    self.score += int(score_value * score_multiplier)
                    
                    # Update high score
                    self.high_score = max(self.score, self.high_score)
                    
                    # Spawn new food
                    self.spawn_food()
                
                # Check for collisions with obstacles or maze walls
                if self.snake.head_position in self.game_mode_manager.obstacles or \
                   self.snake.head_position in self.game_mode_manager.maze_walls:
                    if not self.game_mode_manager.is_no_death_mode():
                        self.state = GAME_OVER
                        self.game_over_time = 0
                        self.death_particles_created = False
                        self.sound_manager.play_sound('game_over')
                        self.sound_manager.stop_music()
                        self.sound_manager.play_music('game_over')
                
                # Check for collisions with walls
                head_x, head_y = self.snake.head_position
                if self.game_mode_manager.has_wall_collision() and \
                   (head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT):
                    if not self.game_mode_manager.is_no_death_mode() and not self.snake.ghost_mode:
                        self.state = GAME_OVER
                        self.game_over_time = 0
                        self.death_particles_created = False
                        self.sound_manager.play_sound('game_over')
                        self.sound_manager.stop_music()
                        self.sound_manager.play_music('game_over')
                
                # Check for collisions with self
                if self.snake.head_position in self.snake.segments[1:]:
                    if not self.game_mode_manager.is_no_death_mode() and not self.snake.ghost_mode:
                        self.state = GAME_OVER
                        self.game_over_time = 0
                        self.death_particles_created = False
                        self.sound_manager.play_sound('game_over')
                        self.sound_manager.stop_music()
                        self.sound_manager.play_music('game_over')
                
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
        elif self.state == MODE_SELECT:
            self.game_mode_manager.render_mode_selection(self.screen, self.selected_mode, self.selected_difficulty)
        elif self.state == PLAYING:
            # Draw game mode specific elements
            self.game_mode_manager.render(self.screen)
            
            # Draw game elements
            self.power_up_manager.render(self.screen)
            self.food.render(self.screen)
            self.snake.render(self.screen, self.particles)
            self.particles.render(self.screen)
            
            # Draw UI elements
            self.render_hud()
            self.power_up_manager.render_active_effects(self.screen)
            self.game_mode_manager.render_mode_info(self.screen, 10, SCREEN_HEIGHT - 30)
        elif self.state == PAUSED:
            # Draw game mode specific elements (dimmed)
            self.game_mode_manager.render(self.screen)
            
            # Draw game elements (dimmed)
            self.power_up_manager.render(self.screen, dimmed=True)
            self.food.render(self.screen, dimmed=True)
            self.snake.render(self.screen, self.particles, dimmed=True)
            
            # Draw UI elements
            self.render_hud(dimmed=True)
            self.game_mode_manager.render_mode_info(self.screen, 10, SCREEN_HEIGHT - 30)
            
            # Draw pause menu
            self.render_pause_menu()
        elif self.state == GAME_OVER:
            # Draw game mode specific elements (dimmed)
            self.game_mode_manager.render(self.screen)
            
            # Draw game elements (dimmed)
            self.power_up_manager.render(self.screen, dimmed=True)
            self.food.render(self.screen, dimmed=True)
            self.snake.render(self.screen, self.particles, dimmed=True)
            self.particles.render(self.screen)  # Death particles
            
            # Draw UI elements
            self.render_hud(dimmed=True)
            self.game_mode_manager.render_mode_info(self.screen, 10, SCREEN_HEIGHT - 30)
            
            # Draw game over screen
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
        options = [
            {"text": "Press ENTER for Game Modes", "y_offset": 50},
            {"text": "Press SPACE for Quick Start", "y_offset": 100},
            {"text": "High Score: " + str(self.high_score), "y_offset": 170, "color": GOLD}
        ]
        
        for option in options:
            pulse_start = (math.sin(self.menu_time * 3) + 1) * 0.5
            color = option.get("color", self.lerp_color(WHITE, GOLD, pulse_start))
            text = self.font.render(option["text"], True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + option["y_offset"]))
            self.screen.blit(text, text_rect)
        
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
        # Reset game objects
        self.snake = EnhancedSnake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.food = EnhancedFood()
        
        # Reset score
        self.score = 0
        
        # Reset timers
        self.move_timer = 0
        self.base_move_delay = self.game_mode_manager.get_move_delay()
        self.move_delay = self.base_move_delay
        
        # Reset power-ups
        self.power_up_manager = PowerUpManager()
        self.power_up_manager.spawn_interval = self.game_mode_manager.get_power_up_interval()
        
        # Reset particles
        self.particles = ParticleSystem()
        
        # Spawn initial food
        self.spawn_food()
    
    def spawn_food(self):
        """Spawn food at a valid position"""
        valid_positions = []
        
        # Find all valid positions
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pos = (x, y)
                if self.game_mode_manager.is_valid_spawn_position(pos, self.snake.segments):
                    valid_positions.append(pos)
        
        # If there are valid positions, choose one randomly
        if valid_positions:
            self.food.position = random.choice(valid_positions)
        else:
            # If no valid positions, try to find any position not occupied by snake
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                if (x, y) not in self.snake.segments:
                    self.food.position = (x, y)
                    break
    
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
    game = FancySnakeGame()
    game.run()

if __name__ == "__main__":
    main()
