"""
SWYFT - Physics Engine
Handles physics calculations and car movement
"""
import config as config

class PhysicsEngine:
    def __init__(self):
        self.velocity_x = 0.0
        self.velocity_y = 0.0
    
    def apply_gravity(self, dt):
        """Apply gravity to vertical velocity"""
        self.velocity_y += config.GRAVITY * dt
    
    def apply_ground_friction(self):
        """Apply friction when on ground"""
        self.velocity_x *= config.GROUND_FRICTION
    
    def apply_air_friction(self):
        """Apply friction when in air"""
        self.velocity_x *= config.AIR_FRICTION
    
    def accelerate(self, dt, speed_multiplier=1.0):
        """Apply forward acceleration with optional speed multiplier"""
        self.velocity_x += config.ACCELERATION * dt * speed_multiplier
    
    def brake(self, dt):
        """Apply braking force - prevents backwards movement"""
        # Strong braking deceleration
        self.velocity_x -= config.ACCELERATION * 1.5 * dt
        # Prevent going backwards - stop at zero
        if self.velocity_x < 0:
            self.velocity_x = 0
    
    def clamp_velocity(self):
        """Limit velocity to max speed"""
        # Don't allow negative velocity (backwards movement)
        self.velocity_x = max(0, min(config.MAX_SPEED, self.velocity_x))
    
    def reset_vertical_velocity(self):
        """Reset vertical velocity (when landing)"""
        self.velocity_y = 0
    
    def get_velocity(self):
        """Get current velocity tuple"""
        return (self.velocity_x, self.velocity_y)
