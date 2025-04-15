"""
Fancy Snake Game - Power-Ups System

This file implements power-ups and special abilities for our fancy Snake game.
"""

import pygame
import random
import math
from pygame import gfxdraw

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

class PowerUp:
    """Power-up class for special abilities and effects"""
    
    # Power-up types and their properties
    TYPES = {
        'speed_boost': {
            'color': (255, 255, 0),  # Yellow
            'glow_color': (255, 255, 0, 100),
            'duration': 5.0,  # seconds
            'spawn_chance': 0.2,
            'effect_strength': 1.5,  # 50% faster
            'description': "Speed Boost: Move 50% faster"
        },
        'slow_motion': {
            'color': (0, 191, 255),  # Deep sky blue
            'glow_color': (0, 191, 255, 100),
            'duration': 5.0,
            'spawn_chance': 0.15,
            'effect_strength': 0.5,  # 50% slower
            'description': "Slow Motion: Move 50% slower"
        },
        'ghost_mode': {
            'color': (200, 200, 255),  # Light blue
            'glow_color': (200, 200, 255, 100),
            'duration': 4.0,
            'spawn_chance': 0.1,
            'effect_strength': 1.0,
            'description': "Ghost Mode: Pass through walls and yourself"
        },
        'double_points': {
            'color': (255, 215, 0),  # Gold
            'glow_color': (255, 215, 0, 100),
            'duration': 7.0,
            'spawn_chance': 0.2,
            'effect_strength': 2.0,  # Double points
            'description': "Double Points: Score twice as many points"
        },
        'magnet': {
            'color': (255, 0, 255),  # Magenta
            'glow_color': (255, 0, 255, 100),
            'duration': 6.0,
            'spawn_chance': 0.15,
            'effect_strength': 1.0,
            'description': "Magnet: Attract food items"
        },
        'size_down': {
            'color': (50, 205, 50),  # Lime green
            'glow_color': (50, 205, 50, 100),
            'duration': 8.0,
            'spawn_chance': 0.1,
            'effect_strength': 0.5,  # Remove half of snake length
            'description': "Size Down: Reduce snake length by half"
        }
    }
    
    def __init__(self):
        # Choose a random power-up type based on spawn chances
        self.type = self.choose_random_type()
        self.properties = self.TYPES[self.type]
        
        self.position = (0, 0)
        self.active = False
        self.collect_time = None
        self.remaining_time = 0
        
        # Animation properties
        self.pulse_time = 0
        self.rotation = 0
        self.particles = []
    
    def choose_random_type(self):
        """Choose a random power-up type based on spawn chances"""
        types = list(self.TYPES.keys())
        chances = [self.TYPES[t]['spawn_chance'] for t in types]
        
        # Normalize chances
        total = sum(chances)
        chances = [c / total for c in chances]
        
        # Cumulative distribution
        cumulative = [sum(chances[:i+1]) for i in range(len(chances))]
        
        # Random selection
        r = random.random()
        for i, threshold in enumerate(cumulative):
            if r <= threshold:
                return types[i]
        
        # Fallback
        return types[0]
    
    def spawn(self, snake_segments, food_position):
        """Spawn power-up at a random position not occupied by the snake or food"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_segments and (x, y) != food_position:
                self.position = (x, y)
                self.active = False
                self.collect_time = None
                self.remaining_time = self.properties['duration']
                break
    
    def collect(self):
        """Collect the power-up"""
        self.active = True
        self.collect_time = pygame.time.get_ticks() / 1000  # Current time in seconds
    
    def is_expired(self, current_time):
        """Check if the power-up effect has expired"""
        if not self.active or self.collect_time is None:
            return False
        
        elapsed = current_time - self.collect_time
        self.remaining_time = max(0, self.properties['duration'] - elapsed)
        return elapsed >= self.properties['duration']
    
    def update(self, dt):
        """Update power-up animation"""
        self.pulse_time += dt
        self.rotation += dt * 60  # Rotate 60 degrees per second
        
        # Update particles
        for particle in self.particles[:]:
            particle['age'] += dt
            if particle['age'] >= particle['lifetime']:
                self.particles.remove(particle)
            else:
                # Update position
                particle['x'] += particle['vx'] * dt
                particle['y'] += particle['vy'] * dt
                # Update alpha
                progress = particle['age'] / particle['lifetime']
                particle['alpha'] = int(255 * (1 - progress))
        
        # Add new particles occasionally
        if not self.active and random.random() < dt * 2:  # Average 2 particles per second
            self.add_ambient_particle()
    
    def add_ambient_particle(self):
        """Add ambient particles around the power-up"""
        x, y = self.position
        center_x = (x + 0.5) * GRID_SIZE
        center_y = (y + 0.5) * GRID_SIZE
        
        angle = random.uniform(0, math.pi * 2)
        distance = random.uniform(0, GRID_SIZE * 0.5)
        start_x = center_x + math.cos(angle) * distance
        start_y = center_y + math.sin(angle) * distance
        
        speed = random.uniform(5, 15)
        lifetime = random.uniform(0.5, 1.0)
        
        self.particles.append({
            'x': start_x,
            'y': start_y,
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
            'size': random.uniform(1, 3),
            'color': self.properties['color'],
            'alpha': 150,
            'lifetime': lifetime,
            'age': 0,
        })
    
    def render(self, surface, dimmed=False):
        """Render power-up with fancy effects"""
        if self.active:
            return  # Don't render if already collected
        
        x, y = self.position
        center_x = (x + 0.5) * GRID_SIZE
        center_y = (y + 0.5) * GRID_SIZE
        
        # Calculate pulsing effect
        pulse = abs(math.sin(self.pulse_time * 3))
        size = int(GRID_SIZE * 0.7 + pulse * GRID_SIZE * 0.2)
        
        # Apply dimming if needed
        color = tuple(c // 2 for c in self.properties['color']) if dimmed else self.properties['color']
        
        # Draw ambient particles
        if not dimmed:
            for particle in self.particles:
                pygame.gfxdraw.filled_circle(
                    surface,
                    int(particle['x']),
                    int(particle['y']),
                    int(particle['size']),
                    (*particle['color'], particle['alpha'])
                )
        
        # Draw glow effect (if not dimmed)
        if not dimmed:
            glow_size = int(size * 1.5 + pulse * size * 0.5)
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.gfxdraw.filled_circle(
                glow_surface,
                glow_size,
                glow_size,
                glow_size,
                self.properties['glow_color']
            )
            surface.blit(
                glow_surface,
                (center_x - glow_size, center_y - glow_size)
            )
        
        # Draw main power-up item
        pygame.draw.circle(surface, color, (center_x, center_y), size // 2)
        
        # Draw power-up specific pattern
        if not dimmed:
            if self.type == 'speed_boost':
                # Draw lightning bolt
                points = [
                    (center_x - size//4, center_y - size//3),
                    (center_x, center_y - size//8),
                    (center_x - size//8, center_y),
                    (center_x + size//4, center_y + size//3),
                    (center_x, center_y + size//8),
                    (center_x + size//8, center_y)
                ]
                pygame.draw.polygon(surface, (255, 255, 200), points)
            
            elif self.type == 'slow_motion':
                # Draw clock face
                pygame.draw.circle(surface, (200, 200, 255), (center_x, center_y), size // 3, 2)
                # Draw clock hands
                angle = math.radians(self.rotation)
                hand_length = size // 4
                pygame.draw.line(
                    surface, 
                    (200, 200, 255), 
                    (center_x, center_y),
                    (center_x + math.cos(angle) * hand_length, center_y + math.sin(angle) * hand_length),
                    2
                )
            
            elif self.type == 'ghost_mode':
                # Draw ghost shape
                ghost_points = []
                for i in range(8):
                    angle = math.pi * 2 * i / 8 + math.radians(self.rotation)
                    r = size // 3
                    x = center_x + math.cos(angle) * r
                    y = center_y + math.sin(angle) * r
                    ghost_points.append((x, y))
                
                pygame.draw.polygon(surface, (255, 255, 255, 150), ghost_points)
            
            elif self.type == 'double_points':
                # Draw dollar sign
                font = pygame.font.Font(None, size // 2)
                text = font.render("$", True, (255, 255, 200))
                text_rect = text.get_rect(center=(center_x, center_y))
                surface.blit(text, text_rect)
            
            elif self.type == 'magnet':
                # Draw magnet shape
                magnet_width = size // 3
                magnet_height = size // 2
                
                # North pole (red)
                pygame.draw.rect(
                    surface,
                    (255, 100, 100),
                    (center_x - magnet_width//2, center_y - magnet_height//2, magnet_width, magnet_height//2)
                )
                
                # South pole (blue)
                pygame.draw.rect(
                    surface,
                    (100, 100, 255),
                    (center_x - magnet_width//2, center_y, magnet_width, magnet_height//2)
                )
            
            elif self.type == 'size_down':
                # Draw shrink arrows
                arrow_size = size // 3
                
                # Left arrow
                pygame.draw.line(
                    surface,
                    (200, 255, 200),
                    (center_x - arrow_size, center_y),
                    (center_x, center_y),
                    2
                )
                pygame.draw.line(
                    surface,
                    (200, 255, 200),
                    (center_x - arrow_size, center_y),
                    (center_x - arrow_size//2, center_y - arrow_size//2),
                    2
                )
                pygame.draw.line(
                    surface,
                    (200, 255, 200),
                    (center_x - arrow_size, center_y),
                    (center_x - arrow_size//2, center_y + arrow_size//2),
                    2
                )
                
                # Right arrow
                pygame.draw.line(
                    surface,
                    (200, 255, 200),
                    (center_x + arrow_size, center_y),
                    (center_x, center_y),
                    2
                )
                pygame.draw.line(
                    surface,
                    (200, 255, 200),
                    (center_x + arrow_size, center_y),
                    (center_x + arrow_size//2, center_y - arrow_size//2),
                    2
                )
                pygame.draw.line(
                    surface,
                    (200, 255, 200),
                    (center_x + arrow_size, center_y),
                    (center_x + arrow_size//2, center_y + arrow_size//2),
                    2
                )
    
    def render_status(self, surface, x, y, width=100, height=20):
        """Render power-up status bar when active"""
        if not self.active or self.remaining_time <= 0:
            return
        
        # Draw background
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, (50, 50, 50), bg_rect, border_radius=height//2)
        
        # Draw progress bar
        progress = self.remaining_time / self.properties['duration']
        progress_width = int(width * progress)
        progress_rect = pygame.Rect(x, y, progress_width, height)
        pygame.draw.rect(surface, self.properties['color'], progress_rect, border_radius=height//2)
        
        # Draw border
        pygame.draw.rect(surface, (200, 200, 200), bg_rect, width=1, border_radius=height//2)
        
        # Draw icon
        icon_size = height - 4
        icon_rect = pygame.Rect(x + 2, y + 2, icon_size, icon_size)
        pygame.draw.rect(surface, self.properties['color'], icon_rect, border_radius=icon_size//2)
        
        # Draw text
        font = pygame.font.Font(None, height - 4)
        text = font.render(f"{self.remaining_time:.1f}s", True, (255, 255, 255))
        text_rect = text.get_rect(midright=(x + width - 5, y + height//2))
        surface.blit(text, text_rect)


class PowerUpManager:
    """Manages multiple power-ups and their effects"""
    
    def __init__(self):
        self.power_ups = []  # Available power-ups on screen
        self.active_effects = []  # Currently active power-up effects
        
        self.spawn_timer = 0
        self.spawn_interval = 15.0  # Seconds between power-up spawns
        self.max_power_ups = 1  # Maximum number of power-ups on screen at once
    
    def update(self, dt, snake, food):
        """Update power-ups and their effects"""
        current_time = pygame.time.get_ticks() / 1000  # Current time in seconds
        
        # Update spawn timer
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval and len(self.power_ups) < self.max_power_ups:
            self.spawn_timer = 0
            self.spawn_power_up(snake.segments, food.position)
        
        # Update existing power-ups
        for power_up in self.power_ups:
            power_up.update(dt)
        
        # Check for expired effects
        for effect in self.active_effects[:]:
            if effect.is_expired(current_time):
                self.active_effects.remove(effect)
        
        # Check for power-up collection
        for power_up in self.power_ups[:]:
            if snake.head_position == power_up.position:
                power_up.collect()
                self.active_effects.append(power_up)
                self.power_ups.remove(power_up)
    
    def spawn_power_up(self, snake_segments, food_position):
        """Spawn a new power-up"""
        power_up = PowerUp()
        power_up.spawn(snake_segments, food_position)
        self.power_ups.append(power_up)
    
    def render(self, surface, dimmed=False):
        """Render all power-ups"""
        for power_up in self.power_ups:
            power_up.render(surface, dimmed)
    
    def render_active_effects(self, surface):
        """Render status bars for active effects"""
        y_offset = 50  # Start below score
        for i, effect in enumerate(self.active_effects):
            effect.render_status(surface, 10, y_offset + i * 25)
    
    def get_effect(self, effect_type):
        """Get the active effect of the specified type, or None if not active"""
        for effect in self.active_effects:
            if effect.type == effect_type:
                return effect
        return None
    
    def has_effect(self, effect_type):
        """Check if an effect of the specified type is active"""
        return self.get_effect(effect_type) is not None
    
    def get_effect_strength(self, effect_type, default=1.0):
        """Get the strength of an effect, or default if not active"""
        effect = self.get_effect(effect_type)
        if effect:
            return effect.properties['effect_strength']
        return default
    
    def apply_effects(self, snake, game):
        """Apply all active effects to the game"""
        # Apply speed effects
        speed_multiplier = 1.0
        if self.has_effect('speed_boost'):
            speed_multiplier *= self.get_effect_strength('speed_boost')
        if self.has_effect('slow_motion'):
            speed_multiplier *= self.get_effect_strength('slow_motion')
        
        # Apply the speed multiplier
        game.move_delay = game.base_move_delay / speed_multiplier
        
        # Apply ghost mode
        snake.ghost_mode = self.has_effect('ghost_mode')
        
        # Apply size down (one-time effect)
        size_down = self.get_effect('size_down')
        if size_down and not hasattr(size_down, 'applied'):
            # Remove half of the snake's segments (but keep at least 3)
            segments_to_remove = max(0, len(snake.segments) // 2 - 3)
            if segments_to_remove > 0:
                snake.segments = snake.segments[:-segments_to_remove]
            size_down.applied = True
    
    def get_score_multiplier(self):
        """Get the current score multiplier from active effects"""
        multiplier = 1.0
        if self.has_effect('double_points'):
            multiplier *= self.get_effect_strength('double_points')
        return multiplier
    
    def apply_magnet_effect(self, food, snake):
        """Apply magnet effect to attract food"""
        if not self.has_effect('magnet'):
            return
        
        # Get head position
        head_x, head_y = snake.head_position
        food_x, food_y = food.position
        
        # Calculate distance
        dx = food_x - head_x
        dy = food_y - head_y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # If food is within range and not too close
        if 2 < distance < 8:
            # Move food slightly closer to snake
            if abs(dx) > abs(dy):
                # Move horizontally
                if dx > 0:
                    food_x -= 1
                elif dx < 0:
                    food_x += 1
            else:
                # Move vertically
                if dy > 0:
                    food_y -= 1
                elif dy < 0:
                    food_y += 1
            
            # Update food position if the new position is valid
            new_pos = (food_x, food_y)
            if new_pos not in snake.segments:
                food.position = new_pos


# Test function
def test_power_ups():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Power-Up Test")
    clock = pygame.time.Clock()
    
    # Create a power-up
    power_up = PowerUp()
    power_up.position = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
    
    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update
        dt = clock.tick(60) / 1000.0
        power_up.update(dt)
        
        # Render
        screen.fill((0, 0, 0))
        power_up.render(screen)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    test_power_ups()
