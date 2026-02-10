"""
SWYFT - Obstacles System
Professional obstacles that make the game more challenging
"""
import pygame
import random
import config

class Obstacle:
    """Base obstacle class"""
    def __init__(self, x, y, obstacle_type="rock"):
        self.x = x
        self.y = y
        self.type = obstacle_type
        self.width = 40
        self.height = 40
        self.active = True
        
        if obstacle_type == "rock":
            self.width = 45
            self.height = 40
            self.color = (100, 100, 110)
        elif obstacle_type == "log":
            self.width = 60
            self.height = 25
            self.color = (120, 80, 40)
        elif obstacle_type == "barrier":
            self.width = 15
            self.height = 70
            self.color = (200, 50, 50)
    
    def get_collision_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.width//2, self.y - self.height, 
                          self.width, self.height)
    
    def draw(self, screen, camera_x):
        """Draw obstacle"""
        screen_x = self.x - camera_x
        
        if -100 <= screen_x <= config.WIDTH + 100:
            if self.type == "rock":
                self._draw_rock(screen, screen_x)
            elif self.type == "log":
                self._draw_log(screen, screen_x)
            elif self.type == "barrier":
                self._draw_barrier(screen, screen_x)
    
    def _draw_rock(self, screen, screen_x):
        """Draw a professional rock"""
        # Main rock body - irregular polygon
        points = [
            (screen_x - 20, self.y),
            (screen_x - 15, self.y - 30),
            (screen_x, self.y - 40),
            (screen_x + 18, self.y - 28),
            (screen_x + 22, self.y - 5),
            (screen_x + 10, self.y)
        ]
        
        # Shadow
        shadow_points = [(p[0] + 3, p[1] + 3) for p in points]
        pygame.draw.polygon(screen, (50, 50, 60), shadow_points)
        
        # Main rock
        pygame.draw.polygon(screen, (100, 100, 110), points)
        
        # Highlights for 3D effect
        pygame.draw.polygon(screen, (130, 130, 140), points[:4])
        
        # Cracks/details
        pygame.draw.line(screen, (80, 80, 90), 
                        (screen_x - 8, self.y - 15), 
                        (screen_x + 5, self.y - 20), 2)
        pygame.draw.line(screen, (80, 80, 90),
                        (screen_x + 10, self.y - 25),
                        (screen_x + 15, self.y - 15), 2)
    
    def _draw_log(self, screen, screen_x):
        """Draw a professional log"""
        # Shadow
        shadow_rect = pygame.Rect(screen_x - self.width//2 + 3, 
                                  self.y - self.height + 3, 
                                  self.width, self.height)
        pygame.draw.ellipse(screen, (60, 40, 20), shadow_rect)
        
        # Main log
        log_rect = pygame.Rect(screen_x - self.width//2, 
                              self.y - self.height, 
                              self.width, self.height)
        pygame.draw.ellipse(screen, (120, 80, 40), log_rect)
        
        # Wood grain
        for i in range(3):
            grain_y = self.y - self.height//2 + (i - 1) * 7
            pygame.draw.line(screen, (100, 65, 30),
                           (screen_x - self.width//2 + 5, grain_y),
                           (screen_x + self.width//2 - 5, grain_y), 2)
        
        # Bark texture
        pygame.draw.arc(screen, (90, 60, 30), log_rect, 0, 3.14, 2)
    
    def _draw_barrier(self, screen, screen_x):
        """Draw a professional barrier/sign"""
        # Post
        post_rect = pygame.Rect(screen_x - self.width//2, 
                               self.y - self.height,
                               self.width, self.height)
        
        # Shadow
        shadow_rect = post_rect.move(2, 2)
        pygame.draw.rect(screen, (100, 25, 25), shadow_rect, border_radius=3)
        
        # Main barrier
        pygame.draw.rect(screen, (220, 50, 50), post_rect, border_radius=3)
        pygame.draw.rect(screen, (180, 40, 40), post_rect, 3, border_radius=3)
        
        # Warning stripes
        stripe_width = self.width - 4
        stripe_height = 8
        for i in range(3):
            stripe_y = self.y - self.height + 15 + i * 20
            stripe_rect = pygame.Rect(screen_x - stripe_width//2,
                                     stripe_y,
                                     stripe_width, stripe_height)
            color = (255, 255, 100) if i % 2 == 0 else (220, 50, 50)
            pygame.draw.rect(screen, color, stripe_rect)

class ObstacleManager:
    """Manages obstacle spawning and updates"""
    def __init__(self, terrain):
        self.terrain = terrain
        self.obstacles = []
        self.last_spawn_x = 0
        self.spawn_distance = config.OBSTACLE_SPAWN_MIN_DISTANCE
    
    def spawn_obstacle(self, car_x):
        """Spawn new obstacle ahead of car"""
        if car_x - self.last_spawn_x > self.spawn_distance:
            # Random spawn distance
            spawn_x = car_x + random.randint(config.OBSTACLE_SPAWN_MIN_DISTANCE,
                                            config.OBSTACLE_SPAWN_MAX_DISTANCE)
            spawn_y = self.terrain.get_height_at(spawn_x)
            
            # Random obstacle type
            obstacle_type = random.choice(config.OBSTACLE_TYPES)
            
            obstacle = Obstacle(spawn_x, spawn_y, obstacle_type)
            self.obstacles.append(obstacle)
            
            self.last_spawn_x = car_x
            self.spawn_distance = random.randint(config.OBSTACLE_SPAWN_MIN_DISTANCE,
                                                config.OBSTACLE_SPAWN_MAX_DISTANCE)
    
    def update(self, car_x):
        """Update obstacles and spawn new ones"""
        # Remove obstacles that are far behind
        self.obstacles = [obs for obs in self.obstacles if obs.x > car_x - 500]
        
        # Spawn new obstacles
        if config.OBSTACLE_ENABLED:
            self.spawn_obstacle(car_x)
    
    def check_collision(self, car_rect):
        """Check if car collides with any obstacle"""
        for obstacle in self.obstacles:
            if obstacle.active:
                obs_rect = obstacle.get_collision_rect()
                if car_rect.colliderect(obs_rect):
                    return True, obstacle
        return False, None
    
    def get_visible_obstacles(self):
        """Get all active obstacles"""
        return self.obstacles
