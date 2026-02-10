"""
SWYFT - Car Entity
Handles car state, movement, and rendering
"""
import pygame
import config as config

class Car:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y
        self.rotation = 0.0
        self.target_rotation = 0.0
        
        # Load or create car image
        self._load_image()
    
    def _load_image(self):
        """Load car image or create placeholder"""
        try:
            self.original_img = pygame.image.load("car.png").convert_alpha()
            self.original_img = pygame.transform.rotozoom(
                self.original_img, 0, config.CAR_SCALE
            )
        except:
            # Create placeholder car
            self.original_img = pygame.Surface((80, 40), pygame.SRCALPHA)
            pygame.draw.rect(self.original_img, (220, 20, 60), (0, 0, 80, 40))
        
        self.height = self.original_img.get_height()
    
    def update_rotation(self, target_angle, dt, velocity_x=0):
        """Smoothly rotate car to match terrain"""
        # Only use terrain angle - no speed-based tilt
        self.target_rotation = target_angle
        
        # Smooth rotation to match terrain
        self.rotation += (self.target_rotation - self.rotation) * config.ROTATION_SMOOTHING * dt
    
    def update_position(self, velocity_x, velocity_y, dt):
        """Update car position based on velocity"""
        self.x += velocity_x * dt
        self.y += velocity_y * dt
    
    def align_to_ground(self, ground_y):
        """Align car to ground level with offset"""
        self.y = ground_y - self.height / 2 + config.CAR_GROUND_OFFSET
    
    def draw(self, screen, camera_x):
        """Render car on screen"""
        rotated = pygame.transform.rotate(self.original_img, -self.rotation)
        rect = rotated.get_rect(center=(self.x - camera_x, self.y))
        screen.blit(rotated, rect)
    
    def get_position(self):
        """Get current car position"""
        return (self.x, self.y)
    
    def get_height(self):
        """Get car image height"""
        return self.height
