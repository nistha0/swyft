"""
SWYFT - Advanced Terrain Generation with Difficulty Modes
Handles procedural terrain generation with progressive difficulty
"""
import pygame
import math
import random
import config

class Terrain:
    def __init__(self):
        self.points = []
        self.segment_length = config.TERRAIN_SEGMENT_LENGTH
        self.difficulty = getattr(config, 'DIFFICULTY', 'MEDIUM')
        self.distance_traveled = 0
        
        # Random seed for unique terrain each game
        self.seed = random.random() * 10000
        self.phase_offset1 = random.random() * 1000
        self.phase_offset2 = random.random() * 1000
        self.phase_offset3 = random.random() * 1000
        self.phase_offset4 = random.random() * 1000
        
        print(f"[TERRAIN] Generated new terrain with seed: {self.seed:.2f}")
        
        self.generate_initial_terrain()
    
    def generate_initial_terrain(self):
        """Generate initial terrain from -200 to 3000"""
        x = -200
        while x < 3000:
            y = self._calculate_height(x)
            self.points.append([x, y])
            x += self.segment_length
    
    def extend_terrain(self):
        """Extend terrain ahead of current position"""
        last_x = self.points[-1][0]
        x = last_x + self.segment_length
        while x < last_x + 1000:
            y = self._calculate_height(x)
            self.points.append([x, y])
            x += self.segment_length
    
    def _calculate_height(self, x):
        """Calculate terrain height at given x position based on difficulty"""
        base_height = config.TERRAIN_BASE_HEIGHT
        
        # Calculate difficulty multiplier based on distance
        distance_factor = min(x / 5000, 1.5)  # Increases up to 1.5x over 5000m
        
        if self.difficulty == "EASY":
            # Gentle rolling hills with random variation
            amplitude1 = 40 + distance_factor * 20
            amplitude2 = 20 + distance_factor * 10
            freq1 = 0.002
            freq2 = 0.005
            
            height = (base_height + 
                     math.sin((x + self.phase_offset1) * freq1) * amplitude1 + 
                     math.cos((x + self.phase_offset2) * freq2) * amplitude2)
            
        elif self.difficulty == "MEDIUM":
            # Moderate hills with some variation and randomness
            amplitude1 = 60 + distance_factor * 40
            amplitude2 = 30 + distance_factor * 20
            amplitude3 = 15 + distance_factor * 10
            freq1 = 0.003
            freq2 = 0.007
            freq3 = 0.015
            
            # Add occasional steep sections with random offset
            steep_factor = math.sin((x + self.phase_offset3) * 0.0008) * 30
            
            height = (base_height + 
                     math.sin((x + self.phase_offset1) * freq1) * amplitude1 + 
                     math.cos((x + self.phase_offset2) * freq2) * amplitude2 +
                     math.sin((x + self.phase_offset3) * freq3) * amplitude3 +
                     steep_factor)
            
        else:  # HARD
            # Extreme terrain with dangerous slopes but controlled amplitudes, with randomness
            amplitude1 = 60 + distance_factor * 40  # Reduced from 80+60
            amplitude2 = 35 + distance_factor * 25  # Reduced from 45+35
            amplitude3 = 20 + distance_factor * 15  # Reduced from 25+20
            amplitude4 = 12  # Reduced from 15
            freq1 = 0.0025
            freq2 = 0.006
            freq3 = 0.012
            freq4 = 0.025
            
            # Add sharp peaks and valleys with random offset (reduced)
            sharp_peaks = math.sin((x + self.phase_offset1) * 0.001) * 35  # Reduced from 50
            
            # Add dangerous steep sections with random offset (reduced)
            steep_section = math.sin((x + self.phase_offset2) * 0.0005) * 30  # Reduced from 40
            
            # Random bumps with different phase
            bump_factor = math.sin((x + self.phase_offset4) * freq4) * amplitude4
            
            height = (base_height + 
                     math.sin((x + self.phase_offset1) * freq1) * amplitude1 + 
                     math.cos((x + self.phase_offset2) * freq2) * amplitude2 +
                     math.sin((x + self.phase_offset3) * freq3) * amplitude3 +
                     sharp_peaks +
                     steep_section +
                     bump_factor)
        
        return height
    
    def get_height_at(self, x):
        """Get interpolated terrain height at any x position"""
        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]
            if x1 <= x <= x2:
                t = (x - x1) / (x2 - x1)
                return y1 + (y2 - y1) * t
        return config.TERRAIN_BASE_HEIGHT
    
    def get_angle_at(self, x):
        """Get terrain angle at given x position"""
        for i in range(len(self.points) - 1):
            x1, y1 = self.points[i]
            x2, y2 = self.points[i + 1]
            if x1 <= x <= x2:
                angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
                return angle
        return 0
    
    def is_dangerous_slope(self, x):
        """Check if the slope at position x is dangerous (can cause flipping)"""
        angle = abs(self.get_angle_at(x))
        
        # Define danger thresholds based on difficulty
        if self.difficulty == "EASY":
            return angle > 45  # Very steep in easy mode
        elif self.difficulty == "MEDIUM":
            return angle > 35  # Moderately steep
        else:  # HARD
            return angle > 28  # Even moderate slopes are dangerous in hard mode
    
    def draw(self, screen, camera_x):
        """Render terrain on screen"""
        screen_points = []
        for point in self.points:
            sx = point[0] - camera_x
            if -50 <= sx <= config.WIDTH + 50:
                screen_points.append((sx, point[1]))
        
        if len(screen_points) >= 2:
            # Draw grass fill
            ground_polygon = ([(0, config.HEIGHT)] + 
                            screen_points + 
                            [(config.WIDTH, config.HEIGHT)])
            pygame.draw.polygon(screen, config.GRASS_GREEN, ground_polygon)
            
            # Draw terrain outline
            pygame.draw.lines(screen, config.GRASS_DARK, False, screen_points, 3)
    
    def draw_themed(self, screen, camera_x, grass_color):
        """Render terrain with themed grass color"""
        screen_points = []
        
        for i, point in enumerate(self.points):
            sx = point[0] - camera_x
            if -50 <= sx <= config.WIDTH + 50:
                screen_points.append((sx, point[1]))
        
        if len(screen_points) >= 2:
            # Draw grass fill with themed color
            ground_polygon = ([(0, config.HEIGHT)] + 
                            screen_points + 
                            [(config.WIDTH, config.HEIGHT)])
            pygame.draw.polygon(screen, grass_color, ground_polygon)
            
            # Draw terrain outline with darker shade
            dark_grass = tuple(max(0, int(c * 0.7)) for c in grass_color)
            pygame.draw.lines(screen, dark_grass, False, screen_points, 3)
