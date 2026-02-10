"""
SWYFT - Game Entities
Contains Coin and Cloud classes
"""
import pygame
import math
import random
import config

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.rotation = 0
        self.bob_offset = random.random() * math.pi * 2
    
    def update(self, dt, game_time):
        """Update coin animation"""
        self.rotation += config.COIN_ROTATION_SPEED * dt
    
    def draw(self, screen, camera_x, game_time):
        """Render coin with 3D rotation effect"""
        if self.collected:
            return
        
        # Calculate screen position with bobbing
        sx = self.x - camera_x
        sy = self.y + math.sin(game_time * config.COIN_BOB_SPEED + self.bob_offset) * 4
        
        # 3D rotation effect
        scale = abs(math.cos(math.radians(self.rotation)))
        width = int(config.COIN_SIZE * max(scale, 0.2))
        height = config.COIN_SIZE
        
        # Draw outer circle
        pygame.draw.ellipse(screen, config.COIN_GOLD, 
                          (sx - width//2, sy - height//2, width, height))
        
        # Draw inner circle
        pygame.draw.ellipse(screen, config.COIN_ORANGE,
                          (sx - int(width*0.7)//2, sy - int(height*0.7)//2,
                           int(width*0.7), int(height*0.7)))
    
    def check_collision(self, car_x, car_y):
        """Check if car collected this coin"""
        if self.collected:
            return False
        if math.hypot(self.x - car_x, self.y - car_y) < config.COIN_DETECTION_RADIUS:
            self.collected = True
            return True
        return False


class Cloud:
    def __init__(self):
        self.x = random.randint(0, config.WIDTH)
        self.y = random.randint(50, 200)
        self.speed = random.uniform(config.CLOUD_MIN_SPEED, config.CLOUD_MAX_SPEED)
        self.size = random.randint(config.CLOUD_MIN_SIZE, config.CLOUD_MAX_SIZE)
    
    def update(self, dt):
        """Update cloud position"""
        self.x -= self.speed * dt
        if self.x < -200:
            self.x = config.WIDTH + random.randint(50, 150)
            self.y = random.randint(50, 200)
    
    def draw(self, screen):
        """Render cloud with multiple circles"""
        c = config.WHITE
        s = self.size
        pygame.draw.circle(screen, c, (int(self.x), int(self.y)), s)
        pygame.draw.circle(screen, c, (int(self.x + s), int(self.y + 20)), s)
        pygame.draw.circle(screen, c, (int(self.x - s), int(self.y + 15)), s)


class FuelCanister:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.bob_offset = random.random() * math.pi * 2
    
    def update(self, dt, game_time):
        """Update fuel canister animation"""
        pass
    
    def draw(self, screen, camera_x, game_time):
        """Render fuel canister"""
        if self.collected:
            return
        
        # Calculate screen position with bobbing
        sx = self.x - camera_x
        sy = self.y + math.sin(game_time * config.COIN_BOB_SPEED + self.bob_offset) * 4
        
        # Draw fuel canister (jerry can shape)
        size = config.FUEL_CANISTER_SIZE
        
        # Main body
        pygame.draw.rect(screen, config.FUEL_COLOR_RED, 
                        (sx - size//2, sy - size//2, size, size))
        
        # Handle/spout
        pygame.draw.rect(screen, config.FUEL_COLOR_DARK,
                        (sx - size//2 + 5, sy - size//2 - 8, size//3, 8))
        
        # Highlight
        pygame.draw.rect(screen, (255, 100, 100),
                        (sx - size//2 + 5, sy - size//2 + 5, size//4, size//2))
        
        # Border
        pygame.draw.rect(screen, config.BLACK,
                        (sx - size//2, sy - size//2, size, size), 2)
    
    def check_collision(self, car_x, car_y):
        """Check if car collected this fuel canister"""
        if self.collected:
            return False
        if math.hypot(self.x - car_x, self.y - car_y) < config.FUEL_DETECTION_RADIUS:
            self.collected = True
            return True
        return False