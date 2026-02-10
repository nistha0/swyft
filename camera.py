"""
SWYFT - Camera System
Handles smooth camera following
"""
import config as config

class Camera:
    def __init__(self):
        self.x = 0.0
        self.target_x = 0.0
    
    def follow(self, car_x, dt):
        """Smoothly follow the car"""
        self.target_x = car_x - config.WIDTH * config.CAMERA_OFFSET_X
        self.x += (self.target_x - self.x) * config.CAMERA_FOLLOW_SPEED * dt
    
    def get_x(self):
        """Get camera x position"""
        return self.x