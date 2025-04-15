"""
Fancy Snake Game - Visual Elements Enhancement

This file implements fancy visual elements for our Snake game.
"""

import pygame
import math
import random
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

class ParticleSystem:
    """Particle system for visual effects"""
    
    def __init__(self):
        self.particles = []
    
    def create_food_particles(self, x, y, color, count=20):
        """Create particles when food is eaten"""
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 3)
            size = random.uniform(2, 5)
            lifetime = random.uniform(0.5, 1.5)
            
            self.particles.append({
                'x': x * GRID_SIZE + GRID_SIZE // 2,
                'y': y * GRID_SIZE + GRID_SIZE // 2,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': size,
                'color': color,
                'alpha': 255,
                'lifetime': lifetime,
                'age': 0,
            })
    
    def create_trail_particles(self, x, y, color, count=3):
        """Create trail particles behind the snake"""
        for _ in range(count):
            offset_x = random.uniform(-GRID_SIZE/4, GRID_SIZE/4)
            offset_y = random.uniform(-GRID_SIZE/4, GRID_SIZE/4)
            size = random.uniform(1, 3)
            lifetime = random.uniform(0.3, 0.8)
            
            self.particles.append({
                'x': x * GRID_SIZE + GRID_SIZE // 2 + offset_x,
                'y': y * GRID_SIZE + GRID_SIZE // 2 + offset_y,
                'vx': 0,
                'vy': 0,
                'size': size,
                'color': color,
                'alpha': 150,
                'lifetime': lifetime,
                'age': 0,
            })
    
    def create_death_particles(self, segments, count_per_segment=10):
        """Create explosion particles when snake dies"""
        for x, y in segments:
            for _ in range(count_per_segment):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(2, 5)
                size = random.uniform(3, 7)
                lifetime = random.uniform(0.8, 2.0)
                
                # Random color variations of green
                r = random.randint(0, 100)
                g = random.randint(180, 255)
                b = random.randint(0, 100)
                
                self.particles.append({
                    'x': x * GRID_SIZE + GRID_SIZE // 2,
                    'y': y * GRID_SIZE + GRID_SIZE // 2,
                    'vx': math.cos(angle) * speed,
                    'vy': math.sin(angle) * speed,
                    'size': size,
                    'color': (r, g, b),
                    'alpha': 255,
                    'lifetime': lifetime,
                    'age': 0,
                })
    
    def update(self, dt):
        """Update all particles"""
        # Update existing particles
        for particle in self.particles[:]:
            # Update position
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Update age
            particle['age'] += dt
            
            # Calculate alpha based on lifetime
            progress = particle['age'] / particle['lifetime']
            particle['alpha'] = int(255 * (1 - progress))
            
            # Remove dead particles
            if particle['age'] >= particle['lifetime']:
                self.particles.remove(particle)
    
    def render(self, surface):
        """Render all particles"""
        for particle in self.particles:
            # Get particle properties
            x, y = int(particle['x']), int(particle['y'])
            size = particle['size']
            color = particle['color']
            alpha = particle['alpha']
            
            # Create surface for this particle
            particle_surface = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
            
            # Draw the particle
            pygame.gfxdraw.filled_circle(
                particle_surface, 
                int(size), 
                int(size), 
                int(size), 
                (*color, alpha)
            )
            
            # Blit to main surface
            surface.blit(particle_surface, (x - size, y - size))


class BackgroundEffect:
    """Background visual effects"""
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.stars = []
        self.grid_lines = []
        self.create_stars(100)
        self.create_grid()
        self.time = 0
    
    def create_stars(self, count):
        """Create starry background effect"""
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.uniform(0.5, 2)
            pulse_speed = random.uniform(1, 3)
            
            self.stars.append({
                'x': x,
                'y': y,
                'size': size,
                'base_size': size,
                'pulse_speed': pulse_speed,
                'phase': random.uniform(0, math.pi * 2),
            })
    
    def create_grid(self):
        """Create grid lines"""
        # Horizontal lines
        for y in range(0, self.height, GRID_SIZE):
            self.grid_lines.append(((0, y), (self.width, y)))
        
        # Vertical lines
        for x in range(0, self.width, GRID_SIZE):
            self.grid_lines.append(((x, 0), (x, self.height)))
    
    def update(self, dt):
        """Update background effects"""
        self.time += dt
        
        # Update stars
        for star in self.stars:
            # Pulsing effect
            pulse = math.sin(self.time * star['pulse_speed'] + star['phase'])
            star['size'] = star['base_size'] * (1 + 0.3 * pulse)
    
    def render(self, surface):
        """Render background effects"""
        # Fill background with dark color
        surface.fill((10, 10, 30))
        
        # Draw stars
        for star in self.stars:
            x, y = int(star['x']), int(star['y'])
            size = star['size']
            
            # Draw with glow effect
            pygame.gfxdraw.filled_circle(surface, x, y, int(size), (200, 200, 255, 100))
            pygame.gfxdraw.filled_circle(surface, x, y, int(size/2), (255, 255, 255, 200))
        
        # Draw grid lines (subtle)
        for start, end in self.grid_lines:
            pygame.draw.line(surface, (30, 30, 60), start, end, 1)


class EnhancedSnake:
    """Enhanced snake with fancy visuals"""
    
    def __init__(self, x, y):
        self.segments = [(x, y), (x-1, y), (x-2, y)]  # Head is first element
        self.direction = (1, 0)  # Moving right initially
        self.growth_pending = 0
        
        # Visual properties
        self.gradient_colors = self.generate_gradient((0, 255, 100), (0, 100, 255), 10)
        self.glow_colors = self.generate_gradient((100, 255, 100, 150), (0, 100, 255, 50), 10)
        self.pulse_time = 0
        self.trail_time = 0
        
        # Movement animation
        self.move_progress = 0  # 0 to 1 for smooth movement
        self.prev_segments = self.segments.copy()
    
    def generate_gradient(self, start_color, end_color, steps):
        """Generate a gradient between two colors"""
        result = []
        
        # Check if we're dealing with RGBA or RGB
        if len(start_color) == 4:  # RGBA
            for i in range(steps):
                t = i / (steps - 1)
                r = int(start_color[0] * (1 - t) + end_color[0] * t)
                g = int(start_color[1] * (1 - t) + end_color[1] * t)
                b = int(start_color[2] * (1 - t) + end_color[2] * t)
                a = int(start_color[3] * (1 - t) + end_color[3] * t)
                result.append((r, g, b, a))
        else:  # RGB
            for i in range(steps):
                t = i / (steps - 1)
                r = int(start_color[0] * (1 - t) + end_color[0] * t)
                g = int(start_color[1] * (1 - t) + end_color[1] * t)
                b = int(start_color[2] * (1 - t) + end_color[2] * t)
                result.append((r, g, b))
        
        return result
    
    @property
    def head_position(self):
        return self.segments[0]
    
    def move(self):
        """Move the snake with animation"""
        # Save previous positions for animation
        self.prev_segments = self.segments.copy()
        self.move_progress = 0
        
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
    
    def update_animation(self, dt, particle_system=None):
        """Update snake animation"""
        # Update pulse time
        self.pulse_time += dt
        
        # Update movement animation
        self.move_progress = min(1.0, self.move_progress + dt * 10)  # 10 = animation speed
        
        # Update trail particles
        self.trail_time += dt
        if particle_system and self.trail_time >= 0.05:  # Every 0.05 seconds
            self.trail_time = 0
            # Add trail particles behind the snake
            for i, (x, y) in enumerate(self.segments[1:4]):  # Just a few segments behind head
                color_idx = min(i, len(self.gradient_colors) - 1)
                particle_system.create_trail_particles(x, y, self.gradient_colors[color_idx])
    
    def grow(self):
        self.growth_pending += 1
    
    def check_collision(self):
        # Check for collision with self
        if self.head_position in self.segments[1:]:
            return True
        return False
    
    def change_direction(self, new_direction):
        self.direction = new_direction
    
    def render(self, surface, particle_system=None, dimmed=False):
        """Render the snake with fancy effects"""
        alpha = 128 if dimmed else 255
        
        # Draw each segment with interpolation for smooth movement
        for i in range(len(self.segments)):
            # Get current and previous positions
            curr_x, curr_y = self.segments[i]
            
            # For animation, interpolate between previous and current position
            if i < len(self.prev_segments) and self.move_progress < 1.0:
                prev_x, prev_y = self.prev_segments[i]
                # Interpolate position
                x = prev_x + (curr_x - prev_x) * self.move_progress
                y = prev_y + (curr_y - prev_y) * self.move_progress
            else:
                x, y = curr_x, curr_y
            
            # Calculate color based on segment position
            color_idx = min(i, len(self.gradient_colors) - 1)
            color = self.gradient_colors[color_idx]
            
            # Apply pulsing effect to head
            if i == 0:
                pulse = (math.sin(self.pulse_time * 3) + 1) * 0.1
                size_factor = 1.0 + pulse
            else:
                size_factor = 1.0
            
            # Apply dimming if needed
            if dimmed:
                color = tuple(c // 2 for c in color)
            
            # Calculate position and size
            rect = pygame.Rect(
                x * GRID_SIZE, 
                y * GRID_SIZE, 
                GRID_SIZE * size_factor, 
                GRID_SIZE * size_factor
            )
            
            # Center the rectangle
            rect.center = (
                (x + 0.5) * GRID_SIZE, 
                (y + 0.5) * GRID_SIZE
            )
            
            # Draw glow effect (if not dimmed)
            if not dimmed and i < 5:  # Only for first few segments
                glow_color = self.glow_colors[min(i, len(self.glow_colors) - 1)]
                glow_size = int(GRID_SIZE * (1.2 + pulse * 0.5))
                glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                pygame.gfxdraw.filled_circle(
                    glow_surface, 
                    glow_size, 
                    glow_size, 
                    glow_size, 
                    glow_color
                )
                surface.blit(
                    glow_surface, 
                    (rect.centerx - glow_size, rect.centery - glow_size)
                )
            
            # Draw rounded rectangle for each segment
            self.draw_rounded_rect(surface, rect, color, 8)
            
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
        """Draw eyes on the snake's head with fancy effects"""
        eye_color = (50, 50, 50) if dimmed else (0, 0, 0)
        pupil_color = (200, 200, 200) if dimmed else WHITE
        
        # Eye positions depend on direction
        dx, dy = self.direction
        
        # Calculate center of the grid cell
        center_x = (x + 0.5) * GRID_SIZE
        center_y = (y + 0.5) * GRID_SIZE
        
        # Eye offsets based on direction
        if dx == 1:  # Right
            left_eye_pos = (center_x - GRID_SIZE * 0.15, center_y - GRID_SIZE * 0.2)
            right_eye_pos = (center_x - GRID_SIZE * 0.15, center_y + GRID_SIZE * 0.2)
        elif dx == -1:  # Left
            left_eye_pos = (center_x + GRID_SIZE * 0.15, center_y - GRID_SIZE * 0.2)
            right_eye_pos = (center_x + GRID_SIZE * 0.15, center_y + GRID_SIZE * 0.2)
        elif dy == -1:  # Up
            left_eye_pos = (center_x - GRID_SIZE * 0.2, center_y + GRID_SIZE * 0.15)
            right_eye_pos = (center_x + GRID_SIZE * 0.2, center_y + GRID_SIZE * 0.15)
        else:  # Down
            left_eye_pos = (center_x - GRID_SIZE * 0.2, center_y - GRID_SIZE * 0.15)
            right_eye_pos = (center_x + GRID_SIZE * 0.2, center_y - GRID_SIZE * 0.15)
        
        # Draw eyes with glow
        eye_radius = GRID_SIZE * 0.18
        pupil_radius = GRID_SIZE * 0.08
        
        # Draw eye whites with subtle glow
        if not dimmed:
            # Glow
            glow_radius = int(eye_radius * 1.5)
            for eye_pos in [left_eye_pos, right_eye_pos]:
                glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                pygame.gfxdraw.filled_circle(
                    glow_surface, 
                    glow_radius, 
                    glow_radius, 
                    glow_radius, 
                    (255, 255, 255, 40)
                )
                surface.blit(
                    glow_surface, 
                    (eye_pos[0] - glow_radius, eye_pos[1] - glow_radius)
                )
        
        # Draw eye whites
        for eye_pos in [left_eye_pos, right_eye_pos]:
            pygame.draw.circle(surface, eye_color, eye_pos, eye_radius)
        
        # Draw pupils with direction bias
        pupil_offset_x = dx * GRID_SIZE * 0.06
        pupil_offset_y = dy * GRID_SIZE * 0.06
        
        for eye_pos in [left_eye_pos, right_eye_pos]:
            pupil_pos = (eye_pos[0] + pupil_offset_x, eye_pos[1] + pupil_offset_y)
            pygame.draw.circle(surface, pupil_color, pupil_pos, pupil_radius)
            
            # Add highlight
            highlight_pos = (pupil_pos[0] - pupil_radius * 0.3, pupil_pos[1] - pupil_radius * 0.3)
            pygame.draw.circle(surface, (255, 255, 255), highlight_pos, pupil_radius * 0.4)


class EnhancedFood:
    """Enhanced food with fancy visuals"""
    
    def __init__(self):
        self.position = (0, 0)
        self.type = random.choice(['regular', 'bonus', 'special'])
        self.set_properties_by_type()
        self.pulse_time = 0
        self.rotation = 0
        self.particles = []
    
    def set_properties_by_type(self):
        """Set food properties based on type"""
        if self.type == 'regular':
            self.color = (255, 50, 50)  # Red
            self.value = 1
            self.pulse_speed = 2
            self.glow_color = (255, 100, 100, 100)
            self.particle_color = (255, 100, 100)
            self.size_factor = 0.6
        elif self.type == 'bonus':
            self.color = (255, 215, 0)  # Gold
            self.value = 3
            self.pulse_speed = 3
            self.glow_color = (255, 215, 100, 120)
            self.particle_color = (255, 215, 0)
            self.size_factor = 0.7
        else:  # special
            self.color = (0, 191, 255)  # Deep sky blue
            self.value = 5
            self.pulse_speed = 4
            self.glow_color = (100, 200, 255, 150)
            self.particle_color = (100, 200, 255)
            self.size_factor = 0.8
    
    def spawn(self, snake_segments):
        """Spawn food at a random position not occupied by the snake"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in snake_segments:
                self.position = (x, y)
                # Randomly choose a new type
                self.type = random.choice(['regular'] * 7 + ['bonus'] * 2 + ['special'])
                self.set_properties_by_type()
                break
    
    def update(self, dt):
        """Update food animation"""
        self.pulse_time += dt
        self.rotation += dt * 50  # Rotate 50 degrees per second
        
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
        if random.random() < dt * 2:  # Average 2 particles per second
            self.add_ambient_particle()
    
    def add_ambient_particle(self):
        """Add ambient particles around the food"""
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
            'color': self.particle_color,
            'alpha': 150,
            'lifetime': lifetime,
            'age': 0,
        })
    
    def render(self, surface, dimmed=False):
        """Render food with fancy effects"""
        x, y = self.position
        center_x = (x + 0.5) * GRID_SIZE
        center_y = (y + 0.5) * GRID_SIZE
        
        # Calculate pulsing effect
        pulse = abs(math.sin(self.pulse_time * self.pulse_speed))
        size = int(GRID_SIZE * self.size_factor + pulse * GRID_SIZE * 0.2)
        
        # Apply dimming if needed
        color = tuple(c // 2 for c in self.color) if dimmed else self.color
        
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
                self.glow_color
            )
            surface.blit(
                glow_surface,
                (center_x - glow_size, center_y - glow_size)
            )
        
        # Draw main food item
        pygame.draw.circle(surface, color, (center_x, center_y), size // 2)
        
        # Draw pattern based on food type
        if self.type == 'regular':
            # Simple food - just a circle with highlight
            highlight_size = size // 4
            highlight_pos = (center_x - size // 6, center_y - size // 6)
            pygame.draw.circle(surface, (255, 255, 255, 180), highlight_pos, highlight_size)
        
        elif self.type == 'bonus':
            # Star pattern for bonus food
            if not dimmed:
                points = 5
                inner_radius = size // 4
                outer_radius = size // 2
                
                # Calculate star points
                star_points = []
                for i in range(points * 2):
                    angle = math.pi * 2 * i / (points * 2) + math.radians(self.rotation)
                    radius = outer_radius if i % 2 == 0 else inner_radius
                    x = center_x + math.cos(angle) * radius
                    y = center_y + math.sin(angle) * radius
                    star_points.append((x, y))
                
                # Draw star
                pygame.draw.polygon(surface, (255, 255, 200), star_points)
        
        elif self.type == 'special':
            # Spiral pattern for special food
            if not dimmed:
                spiral_points = []
                spiral_radius = size // 2
                spiral_turns = 2
                
                for i in range(20):
                    angle = i / 20 * math.pi * 2 * spiral_turns + math.radians(self.rotation)
                    radius = spiral_radius * (i / 20)
                    x = center_x + math.cos(angle) * radius
                    y = center_y + math.sin(angle) * radius
                    spiral_points.append((x, y))
                
                # Draw spiral
                if len(spiral_points) > 1:
                    pygame.draw.lines(surface, (200, 255, 255), False, spiral_points, 2)


# Main function to test the visual elements
def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fancy Snake - Visual Test")
    clock = pygame.time.Clock()
    
    # Create objects
    background = BackgroundEffect(SCREEN_WIDTH, SCREEN_HEIGHT)
    snake = EnhancedSnake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
    food = EnhancedFood()
    food.spawn(snake.segments)
    particles = ParticleSystem()
    
    # Main loop
    running = True
    last_time = time.time()
    
    while running:
        # Calculate delta time
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, 1):
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                    snake.change_direction((1, 0))
                elif event.key == pygame.K_SPACE:
                    # Test particle effects
                    x, y = food.position
                    particles.create_food_particles(x, y, food.color)
        
        # Update
        background.update(dt)
        snake.update_animation(dt, particles)
        food.update(dt)
        particles.update(dt)
        
        # Render
        background.render(screen)
        food.render(screen)
        snake.render(screen, particles)
        particles.render(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
