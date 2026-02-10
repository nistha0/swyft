"""
SWYFT - Enhanced Rendering System with Professional Themes
Handles all drawing operations with beautiful theme support
"""
import pygame
import math
import random
import config

try:
    import cv2
    CV2_OK = True
except:
    CV2_OK = False

class ThemeRenderer:
    """Handles theme-specific rendering"""
    
    def __init__(self):
        # Sunny theme
        self.sunny_sky_top = (135, 206, 250)
        self.sunny_sky_bottom = (220, 240, 255)
        self.sunny_grass = (76, 187, 23)
        
        # Night theme - professional dark blue
        self.night_sky_top = (10, 15, 35)
        self.night_sky_bottom = (30, 40, 70)
        self.night_grass = (20, 40, 30)
        
        # Winter theme - professional white/blue
        self.winter_sky_top = (200, 210, 230)
        self.winter_sky_bottom = (230, 240, 255)
        self.winter_grass = (240, 245, 255)
        
        # Rain theme - professional gray
        self.rain_sky_top = (80, 90, 110)
        self.rain_sky_bottom = (120, 130, 150)
        self.rain_grass = (60, 120, 70)
        
        # Rain/snow particles
        self.weather_particles = []
        self.init_weather_particles()
        
        # Stars for night
        self.stars = [(random.randint(0, 1200), random.randint(0, 400), random.uniform(1, 3)) 
                     for _ in range(150)]
        
        # Snowflakes for winter
        self.snowflakes = []
        self.init_snowflakes()
    
    def init_weather_particles(self):
        """Initialize rain particles"""
        for _ in range(200):
            self.weather_particles.append({
                'x': random.randint(0, config.WIDTH + 500),
                'y': random.randint(-100, config.HEIGHT),
                'speed': random.uniform(8, 12),
                'length': random.randint(10, 20)
            })
    
    def init_snowflakes(self):
        """Initialize snowflakes"""
        for _ in range(100):
            self.snowflakes.append({
                'x': random.randint(0, config.WIDTH),
                'y': random.randint(-100, config.HEIGHT),
                'speed': random.uniform(1, 3),
                'size': random.randint(2, 5),
                'sway': random.uniform(-0.5, 0.5)
            })
    
    def update_weather(self):
        """Update weather effects"""
        theme = config.CURRENT_THEME
        
        if theme == "rain":
            for particle in self.weather_particles:
                particle['y'] += particle['speed']
                particle['x'] += 2
                if particle['y'] > config.HEIGHT:
                    particle['y'] = random.randint(-50, -10)
                    particle['x'] = random.randint(0, config.WIDTH + 500)
        
        elif theme == "winter":
            for flake in self.snowflakes:
                flake['y'] += flake['speed']
                flake['x'] += flake['sway']
                if flake['y'] > config.HEIGHT:
                    flake['y'] = random.randint(-50, -10)
                    flake['x'] = random.randint(0, config.WIDTH)
    
    def draw_sky(self, screen):
        """Draw themed sky"""
        theme = config.CURRENT_THEME
        
        if theme == "sunny":
            sky_top, sky_bottom = self.sunny_sky_top, self.sunny_sky_bottom
        elif theme == "night":
            sky_top, sky_bottom = self.night_sky_top, self.night_sky_bottom
        elif theme == "winter":
            sky_top, sky_bottom = self.winter_sky_top, self.winter_sky_bottom
        else:  # rain
            sky_top, sky_bottom = self.rain_sky_top, self.rain_sky_bottom
        
        for y in range(config.HEIGHT):
            t = y / config.HEIGHT
            r = int(sky_top[0] + (sky_bottom[0] - sky_top[0]) * t)
            g = int(sky_top[1] + (sky_bottom[1] - sky_top[1]) * t)
            b = int(sky_top[2] + (sky_bottom[2] - sky_top[2]) * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (config.WIDTH, y))
    
    def draw_celestial(self, screen, game_time):
        """Draw sun/moon based on theme"""
        theme = config.CURRENT_THEME
        
        if theme == "sunny":
            # Professional sun
            sun_x, sun_y = config.WIDTH - 150, 100
            sun_radius = 45
            
            # Sun glow
            for i in range(5):
                alpha = 30 - i * 5
                glow_surf = pygame.Surface((sun_radius * 2 + i * 20, sun_radius * 2 + i * 20), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (255, 230, 100, alpha), 
                                 (sun_radius + i * 10, sun_radius + i * 10), sun_radius + i * 10)
                screen.blit(glow_surf, (sun_x - sun_radius - i * 10, sun_y - sun_radius - i * 10))
            
            # Sun
            pygame.draw.circle(screen, (255, 220, 0), (sun_x, sun_y), sun_radius)
            pygame.draw.circle(screen, (255, 235, 100), (sun_x, sun_y), sun_radius - 5)
        
        elif theme == "night":
            # Professional moon with craters
            moon_x, moon_y = config.WIDTH - 150, 120
            moon_radius = 40
            
            # Moon glow
            for i in range(4):
                alpha = 40 - i * 10
                glow_surf = pygame.Surface((moon_radius * 2 + i * 15, moon_radius * 2 + i * 15), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (200, 220, 255, alpha),
                                 (moon_radius + i * 7, moon_radius + i * 7), moon_radius + i * 7)
                screen.blit(glow_surf, (moon_x - moon_radius - i * 7, moon_y - moon_radius - i * 7))
            
            # Moon
            pygame.draw.circle(screen, (240, 245, 255), (moon_x, moon_y), moon_radius)
            
            # Craters
            pygame.draw.circle(screen, (220, 225, 235), (moon_x - 10, moon_y - 8), 8)
            pygame.draw.circle(screen, (220, 225, 235), (moon_x + 12, moon_y + 5), 6)
            pygame.draw.circle(screen, (220, 225, 235), (moon_x - 5, moon_y + 12), 5)
    
    def draw_stars(self, screen, game_time):
        """Draw twinkling stars for night theme"""
        if config.CURRENT_THEME == "night":
            for x, y, size in self.stars:
                # Twinkling effect
                twinkle = (math.sin(game_time * 3 + x + y) + 1) / 2
                alpha = int(150 + twinkle * 105)
                
                star_surf = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
                pygame.draw.circle(star_surf, (255, 255, 255, alpha), (int(size), int(size)), int(size))
                screen.blit(star_surf, (x - size, y - size))
    
    def draw_weather_effects(self, screen):
        """Draw rain or snow"""
        theme = config.CURRENT_THEME
        
        if theme == "rain":
            for particle in self.weather_particles:
                # Rain drops - professional look
                pygame.draw.line(screen, (180, 200, 220, 200),
                               (particle['x'], particle['y']),
                               (particle['x'] + 3, particle['y'] + particle['length']), 2)
        
        elif theme == "winter":
            for flake in self.snowflakes:
                # Snowflakes - professional look
                surf = pygame.Surface((flake['size'] * 2, flake['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, (255, 255, 255, 220), 
                                 (flake['size'], flake['size']), flake['size'])
                screen.blit(surf, (flake['x'] - flake['size'], flake['y'] - flake['size']))
    
    def get_grass_color(self):
        """Get grass color based on theme"""
        theme = config.CURRENT_THEME
        if theme == "sunny":
            return self.sunny_grass
        elif theme == "night":
            return self.night_grass
        elif theme == "winter":
            return self.winter_grass
        else:  # rain
            return self.rain_grass

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.hud_font = pygame.font.Font(None, 44)
        self.large_font = pygame.font.Font(None, 72)
        self.title_font = pygame.font.Font(None, 88)  # For GET READY screen
        self.medium_font = pygame.font.Font(None, 56)
        self.small_font = pygame.font.Font(None, 36)
        self.theme_renderer = ThemeRenderer()
    
    def draw_sky(self):
        """Draw themed sky background"""
        self.theme_renderer.draw_sky(self.screen)
    
    def draw_fuel_bar(self, fuel, is_refilling=False):
        """Draw fuel gauge bar with refill animation"""
        bar_width = 250
        bar_height = 30
        bar_x = config.WIDTH - bar_width - 25
        bar_y = 50
        
        # Background
        bg_color = (100, 220, 100) if is_refilling else config.GRAY
        pygame.draw.rect(self.screen, bg_color, 
                        (bar_x - 5, bar_y - 5, bar_width + 10, bar_height + 10))
        pygame.draw.rect(self.screen, config.BLACK, 
                        (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Fuel level
        fuel_percentage = fuel / config.FUEL_INITIAL
        fuel_width = int(bar_width * fuel_percentage)
        
        # Color based on fuel level (brighter when refilling)
        if fuel_percentage > 0.5:
            fuel_color = (0, 255, 0) if is_refilling else config.GREEN
        elif fuel_percentage > 0.25:
            fuel_color = (255, 255, 0) if is_refilling else config.YELLOW
        else:
            fuel_color = (255, 50, 50) if is_refilling else config.FUEL_COLOR_RED
        
        if fuel_width > 0:
            pygame.draw.rect(self.screen, fuel_color,
                           (bar_x, bar_y, fuel_width, bar_height))
        
        # Fuel text with refill indicator
        fuel_label = "FUEL ++" if is_refilling else "FUEL"
        fuel_text = self.hud_font.render(fuel_label, True, config.WHITE)
        self.screen.blit(fuel_text, (bar_x, bar_y - 35))
    
    def draw_hud(self, score_data, is_refilling=False):
        """Draw heads-up display with coins, distance, and fuel"""
        # Semi-transparent background
        hud = pygame.Surface((config.WIDTH, 130), pygame.SRCALPHA)
        hud.fill((0, 0, 0, 100))
        self.screen.blit(hud, (0, 0))
        
        # Coins text
        coins_text = self.hud_font.render(
            f"Coins: {score_data['coins']}", 
            True, 
            config.COIN_GOLD
        )
        self.screen.blit(coins_text, (25, 20))
        
        # Distance text
        distance_text = self.hud_font.render(
            f"Distance: {score_data['distance']}m", 
            True, 
            config.WHITE
        )
        self.screen.blit(distance_text, (25, 60))

        # Fuel bar with refill animation
        self.draw_fuel_bar(score_data['fuel'], is_refilling)
        
        # High Score
        high_score_text = self.hud_font.render(
            f"High Score: {score_data['high_score']}m", 
            True, 
            config.YELLOW
        )
        high_score_rect = high_score_text.get_rect(topright=(config.WIDTH - 25, 90))
        self.screen.blit(high_score_text, high_score_rect)
        
        # Difficulty indicator
        diff_colors = {
            "EASY": (76, 175, 80),
            "MEDIUM": (255, 193, 7),
            "HARD": (244, 67, 54)
        }
        diff_color = diff_colors.get(config.DIFFICULTY, (200, 200, 200))
        diff_text = self.small_font.render(
            f"Mode: {config.DIFFICULTY}", 
            True, 
            diff_color
        )
        diff_rect = diff_text.get_rect(topleft=(25, 100))
        self.screen.blit(diff_text, diff_rect)
    
    def draw_sound_button(self, mouse_pos, is_sound_on):
        """Draw sound toggle button with wooden style below high score on right"""
        # Wooden colors
        WOOD_BROWN = (139, 90, 43)
        WOOD_DARK = (101, 67, 33)
        WOOD_LIGHT = (160, 110, 70)
        TEXT_WHITE = (255, 255, 255)
        
        button_size = 50
        button_x = config.WIDTH - button_size - 80  # Positioned to the right, with more spacing
        button_y = 135  # Below high score (which is at y=90)
        button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
        
        # Check if hovering
        is_hovering = button_rect.collidepoint(mouse_pos)
        
        # Wood grain effect
        button_surf = pygame.Surface((button_size, button_size))
        for i in range(button_size):
            t = i / button_size
            noise = random.randint(-5, 5) if random.random() > 0.9 else 0
            r = int(WOOD_BROWN[0] * (0.9 + t * 0.2) + noise)
            g = int(WOOD_BROWN[1] * (0.9 + t * 0.2) + noise)
            b = int(WOOD_BROWN[2] * (0.9 + t * 0.2) + noise)
            pygame.draw.line(button_surf, (r, g, b), (0, i), (button_size, i))
        
        # Apply hover effect
        if is_hovering:
            button_y -= 2
            button_rect.y = button_y
        
        self.screen.blit(button_surf, (button_x, button_y))
        
        # Wooden border
        pygame.draw.rect(self.screen, WOOD_DARK, (button_x, button_y, button_size, button_size), 
                        3, border_radius=8)
        
        # Highlight
        pygame.draw.rect(self.screen, WOOD_LIGHT, 
                        (button_x + 3, button_y + 3, button_size - 6, 2), border_radius=2)
        
        # Sound icon - speaker shape with wooden style
        center_x = button_x + button_size // 2
        center_y = button_y + button_size // 2
        
        # Speaker base (trapezoid shape)
        speaker_points = [
            (center_x - 12, center_y - 8),
            (center_x - 12, center_y + 8),
            (center_x - 4, center_y + 5),
            (center_x - 4, center_y - 5)
        ]
        pygame.draw.polygon(self.screen, TEXT_WHITE, speaker_points)
        pygame.draw.polygon(self.screen, WOOD_DARK, speaker_points, 2)
        
        # Speaker cone
        cone_points = [
            (center_x - 4, center_y - 5),
            (center_x - 4, center_y + 5),
            (center_x + 4, center_y + 10),
            (center_x + 4, center_y - 10)
        ]
        pygame.draw.polygon(self.screen, TEXT_WHITE, cone_points)
        pygame.draw.polygon(self.screen, WOOD_DARK, cone_points, 2)
        
        if is_sound_on:
            # Sound waves (3 curved lines)
            for i in range(3):
                radius = 8 + i * 5
                start_angle = -math.pi / 4
                end_angle = math.pi / 4
                arc_points = []
                for angle in [start_angle + (end_angle - start_angle) * t / 10 for t in range(11)]:
                    x = center_x + 4 + int(radius * math.cos(angle))
                    y = center_y + int(radius * math.sin(angle))
                    arc_points.append((x, y))
                
                if len(arc_points) > 1:
                    pygame.draw.lines(self.screen, TEXT_WHITE, False, arc_points, 2)
        else:
            # X mark to indicate muted (red)
            x_color = (220, 60, 60)
            pygame.draw.line(self.screen, x_color, 
                           (center_x + 6, center_y - 8), 
                           (center_x + 14, center_y + 8), 3)
            pygame.draw.line(self.screen, x_color, 
                           (center_x + 6, center_y + 8), 
                           (center_x + 14, center_y - 8), 3)
        
        return button_rect
    
    def draw_pause_button(self, mouse_pos):
        """Draw wooden pause button next to sound button on right"""
        # Wooden colors
        WOOD_BROWN = (139, 90, 43)
        WOOD_DARK = (101, 67, 33)
        WOOD_LIGHT = (160, 110, 70)
        TEXT_WHITE = (255, 255, 255)
        
        # Button position and size
        button_size = 50
        button_x = config.WIDTH - button_size - 15  # Far right
        button_y = 135  # Same height as sound button
        button_rect = pygame.Rect(button_x, button_y, button_size, button_size)
        
        # Check if hovering
        is_hovering = button_rect.collidepoint(mouse_pos)
        
        # Wood grain effect
        button_surf = pygame.Surface((button_size, button_size))
        for i in range(button_size):
            t = i / button_size
            noise = random.randint(-5, 5) if random.random() > 0.9 else 0
            r = int(WOOD_BROWN[0] * (0.9 + t * 0.2) + noise)
            g = int(WOOD_BROWN[1] * (0.9 + t * 0.2) + noise)
            b = int(WOOD_BROWN[2] * (0.9 + t * 0.2) + noise)
            pygame.draw.line(button_surf, (r, g, b), (0, i), (button_size, i))
        
        # Apply hover effect
        if is_hovering:
            button_y -= 2
            button_rect.y = button_y
        
        self.screen.blit(button_surf, (button_x, button_y))
        
        # Wooden border
        pygame.draw.rect(self.screen, WOOD_DARK, (button_x, button_y, button_size, button_size), 
                        3, border_radius=8)
        
        # Highlight
        pygame.draw.rect(self.screen, WOOD_LIGHT, 
                        (button_x + 3, button_y + 3, button_size - 6, 2), border_radius=2)
        
        # Pause icon (two vertical bars)
        bar_width = 6
        bar_height = 20
        bar_gap = 8
        icon_x = button_x + (button_size - bar_width * 2 - bar_gap) // 2
        icon_y = button_y + (button_size - bar_height) // 2
        
        # Shadow
        pygame.draw.rect(self.screen, WOOD_DARK, 
                        (icon_x + 1, icon_y + 1, bar_width, bar_height), border_radius=2)
        pygame.draw.rect(self.screen, WOOD_DARK, 
                        (icon_x + bar_width + bar_gap + 1, icon_y + 1, bar_width, bar_height), 
                        border_radius=2)
        
        # Main bars
        pygame.draw.rect(self.screen, TEXT_WHITE, 
                        (icon_x, icon_y, bar_width, bar_height), border_radius=2)
        pygame.draw.rect(self.screen, TEXT_WHITE, 
                        (icon_x + bar_width + bar_gap, icon_y, bar_width, bar_height), 
                        border_radius=2)
        
        return button_rect
    
    def draw_pause_menu(self, mouse_pos):
        """Draw wooden pause menu overlay"""
        # Wooden colors
        PLAIN_BG = (255, 248, 220)
        WOOD_BROWN = (139, 90, 43)
        WOOD_DARK = (101, 67, 33)
        WOOD_LIGHT = (160, 110, 70)
        TEXT_WHITE = (255, 255, 255)
        TEXT_DARK = (70, 40, 20)
        
        # Overlay
        overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        overlay.fill((*PLAIN_BG, 240))
        self.screen.blit(overlay, (0, 0))
        
        # Menu box
        box_width = 500
        box_height = 400
        box_x = (config.WIDTH - box_width) // 2
        box_y = (config.HEIGHT - box_height) // 2
        
        # Wooden box with grain
        box_surf = pygame.Surface((box_width, box_height))
        for i in range(box_height):
            t = i / box_height
            noise = random.randint(-5, 5) if random.random() > 0.9 else 0
            r = int(WOOD_BROWN[0] * (0.9 + t * 0.2) + noise)
            g = int(WOOD_BROWN[1] * (0.9 + t * 0.2) + noise)
            b = int(WOOD_BROWN[2] * (0.9 + t * 0.2) + noise)
            pygame.draw.line(box_surf, (r, g, b), (0, i), (box_width, i))
        
        self.screen.blit(box_surf, (box_x, box_y))
        
        # Border
        pygame.draw.rect(self.screen, WOOD_DARK, (box_x, box_y, box_width, box_height), 
                        6, border_radius=15)
        
        # Highlight
        pygame.draw.rect(self.screen, WOOD_LIGHT, 
                        (box_x + 8, box_y + 8, box_width - 16, 4), border_radius=2)
        
        # Corner screws
        screw_positions = [
            (box_x + 20, box_y + 20),
            (box_x + box_width - 20, box_y + 20),
            (box_x + 20, box_y + box_height - 20),
            (box_x + box_width - 20, box_y + box_height - 20)
        ]
        for pos in screw_positions:
            pygame.draw.circle(self.screen, WOOD_DARK, pos, 5)
            pygame.draw.circle(self.screen, (80, 50, 25), pos, 4)
        
        # "PAUSED" title
        title_shadow = self.large_font.render("PAUSED", True, TEXT_DARK)
        title_text = self.large_font.render("PAUSED", True, TEXT_WHITE)
        title_rect = title_text.get_rect(center=(config.WIDTH // 2, box_y + 70))
        self.screen.blit(title_shadow, title_rect.move(3, 3))
        self.screen.blit(title_text, title_rect)
        
        # Buttons
        button_width = 320
        button_height = 60
        button_x = config.WIDTH // 2 - button_width // 2
        
        # Resume button
        resume_y = box_y + 160
        resume_rect = pygame.Rect(button_x, resume_y, button_width, button_height)
        resume_hover = resume_rect.collidepoint(mouse_pos)
        
        # Resume button wood grain
        resume_surf = pygame.Surface((button_width, button_height))
        for i in range(button_height):
            t = i / button_height
            noise = random.randint(-3, 3) if random.random() > 0.9 else 0
            r = int(WOOD_BROWN[0] * (0.95 + t * 0.1) + noise)
            g = int(WOOD_BROWN[1] * (0.95 + t * 0.1) + noise)
            b = int(WOOD_BROWN[2] * (0.95 + t * 0.1) + noise)
            pygame.draw.line(resume_surf, (r, g, b), (0, i), (button_width, i))
        
        resume_draw_y = resume_y - 3 if resume_hover else resume_y
        self.screen.blit(resume_surf, (button_x, resume_draw_y))
        pygame.draw.rect(self.screen, WOOD_DARK, 
                        (button_x, resume_draw_y, button_width, button_height), 
                        4, border_radius=10)
        pygame.draw.rect(self.screen, WOOD_LIGHT, 
                        (button_x + 4, resume_draw_y + 4, button_width - 8, 3), 
                        border_radius=5)
        
        resume_shadow = self.medium_font.render("RESUME", True, TEXT_DARK)
        resume_text = self.medium_font.render("RESUME", True, TEXT_WHITE)
        resume_text_rect = resume_text.get_rect(center=(config.WIDTH // 2, resume_draw_y + 30))
        self.screen.blit(resume_shadow, resume_text_rect.move(2, 2))
        self.screen.blit(resume_text, resume_text_rect)
        
        # Menu button
        menu_y = box_y + 250
        menu_rect = pygame.Rect(button_x, menu_y, button_width, button_height)
        menu_hover = menu_rect.collidepoint(mouse_pos)
        
        # Menu button wood grain
        menu_surf = pygame.Surface((button_width, button_height))
        for i in range(button_height):
            t = i / button_height
            noise = random.randint(-3, 3) if random.random() > 0.9 else 0
            r = int(WOOD_BROWN[0] * (0.95 + t * 0.1) + noise)
            g = int(WOOD_BROWN[1] * (0.95 + t * 0.1) + noise)
            b = int(WOOD_BROWN[2] * (0.95 + t * 0.1) + noise)
            pygame.draw.line(menu_surf, (r, g, b), (0, i), (button_width, i))
        
        menu_draw_y = menu_y - 3 if menu_hover else menu_y
        self.screen.blit(menu_surf, (button_x, menu_draw_y))
        pygame.draw.rect(self.screen, WOOD_DARK, 
                        (button_x, menu_draw_y, button_width, button_height), 
                        4, border_radius=10)
        pygame.draw.rect(self.screen, WOOD_LIGHT, 
                        (button_x + 4, menu_draw_y + 4, button_width - 8, 3), 
                        border_radius=5)
        
        menu_shadow = self.medium_font.render("MAIN MENU", True, TEXT_DARK)
        menu_text = self.medium_font.render("MAIN MENU", True, TEXT_WHITE)
        menu_text_rect = menu_text.get_rect(center=(config.WIDTH // 2, menu_draw_y + 30))
        self.screen.blit(menu_shadow, menu_text_rect.move(2, 2))
        self.screen.blit(menu_text, menu_text_rect)
        
        return resume_rect, menu_rect
    
    def draw_game_over(self, score_data, death_reason):
        """Draw wooden-themed game over screen"""
        # Plain beige overlay
        PLAIN_BG = (255, 248, 220)
        overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        overlay.fill((*PLAIN_BG, 240))
        self.screen.blit(overlay, (0, 0))
        
        # Wooden colors
        WOOD_BROWN = (139, 90, 43)
        WOOD_DARK = (101, 67, 33)
        WOOD_LIGHT = (160, 110, 70)
        TEXT_WHITE = (255, 255, 255)
        TEXT_DARK = (70, 40, 20)
        
        # Game Over wooden box
        box_width = 650
        box_height = 520
        box_x = (config.WIDTH - box_width) // 2
        box_y = (config.HEIGHT - box_height) // 2
        
        # Wooden box with wood grain effect
        box_surf = pygame.Surface((box_width, box_height))
        for i in range(box_height):
            t = i / box_height
            noise = random.randint(-5, 5) if random.random() > 0.9 else 0
            r = int(WOOD_BROWN[0] * (0.9 + t * 0.2) + noise)
            g = int(WOOD_BROWN[1] * (0.9 + t * 0.2) + noise)
            b = int(WOOD_BROWN[2] * (0.9 + t * 0.2) + noise)
            pygame.draw.line(box_surf, (r, g, b), (0, i), (box_width, i))
        
        # Draw wooden box
        self.screen.blit(box_surf, (box_x, box_y))
        
        # Wooden border
        pygame.draw.rect(self.screen, WOOD_DARK, (box_x, box_y, box_width, box_height), 6, border_radius=15)
        
        # Highlight
        highlight_rect = pygame.Rect(box_x + 8, box_y + 8, box_width - 16, 4)
        pygame.draw.rect(self.screen, WOOD_LIGHT, highlight_rect, border_radius=2)
        
        # Wood screws in corners
        screw_positions = [
            (box_x + 20, box_y + 20),
            (box_x + box_width - 20, box_y + 20),
            (box_x + 20, box_y + box_height - 20),
            (box_x + box_width - 20, box_y + box_height - 20)
        ]
        for pos in screw_positions:
            pygame.draw.circle(self.screen, WOOD_DARK, pos, 5)
            pygame.draw.circle(self.screen, (80, 50, 25), pos, 4)
        
        # "GAME OVER" text with shadow
        game_over_text = "GAME OVER"
        
        # Shadow
        shadow_text = self.large_font.render(game_over_text, True, TEXT_DARK)
        shadow_rect = shadow_text.get_rect(center=(config.WIDTH // 2 + 3, box_y + 73))
        self.screen.blit(shadow_text, shadow_rect)
        
        # Main text
        main_text = self.large_font.render(game_over_text, True, TEXT_WHITE)
        main_rect = main_text.get_rect(center=(config.WIDTH // 2, box_y + 70))
        self.screen.blit(main_text, main_rect)
        
        # Death reason
        reason_color = (255, 200, 100)  # Warm orange-yellow
        reason_shadow = self.medium_font.render(death_reason, True, TEXT_DARK)
        reason_text = self.medium_font.render(death_reason, True, reason_color)
        reason_rect = reason_text.get_rect(center=(config.WIDTH // 2, box_y + 145))
        self.screen.blit(reason_shadow, reason_rect.move(2, 2))
        self.screen.blit(reason_text, reason_rect)
        
        # Separator line
        line_y = box_y + 190
        pygame.draw.line(self.screen, WOOD_DARK, 
                        (box_x + 50, line_y), (box_x + box_width - 50, line_y), 3)
        
        # Final Score section
        score_y = box_y + 230
        
        # Coins with icon
        coin_icon_pos = (config.WIDTH // 2 - 180, score_y + 5)
        pygame.draw.circle(self.screen, (255, 215, 0), coin_icon_pos, 15)
        pygame.draw.circle(self.screen, (255, 165, 0), coin_icon_pos, 12)
        
        coins_shadow = self.hud_font.render(f"Coins: {score_data['coins']}", True, TEXT_DARK)
        coins_text = self.hud_font.render(f"Coins: {score_data['coins']}", True, (255, 215, 0))
        coins_rect = coins_text.get_rect(midleft=(config.WIDTH // 2 - 150, score_y))
        self.screen.blit(coins_shadow, coins_rect.move(2, 2))
        self.screen.blit(coins_text, coins_rect)
        
        # Distance
        distance_shadow = self.hud_font.render(f"Distance: {score_data['distance']}m", True, TEXT_DARK)
        distance_text = self.hud_font.render(f"Distance: {score_data['distance']}m", True, TEXT_WHITE)
        distance_rect = distance_text.get_rect(center=(config.WIDTH // 2, score_y + 55))
        self.screen.blit(distance_shadow, distance_rect.move(2, 2))
        self.screen.blit(distance_text, distance_rect)
        
        # High score comparison - check if current score beats or ties the previous high score
        # Note: high_score has already been updated in game_state if it's a new record
        current_score = score_data['distance']
        saved_high_score = score_data['high_score']
        
        # If current score equals high score, it means we just set a new record
        if current_score >= saved_high_score:
            new_record_shadow = self.small_font.render("★ NEW RECORD! ★", True, TEXT_DARK)
            new_record_text = self.small_font.render("★ NEW RECORD! ★", True, (255, 215, 0))
            new_record_rect = new_record_text.get_rect(center=(config.WIDTH // 2, score_y + 105))
            self.screen.blit(new_record_shadow, new_record_rect.move(2, 2))
            self.screen.blit(new_record_text, new_record_rect)
        else:
            hs_shadow = self.small_font.render(f"Best: {saved_high_score}m", True, TEXT_DARK)
            hs_text = self.small_font.render(f"Best: {saved_high_score}m", True, (200, 180, 140))
            hs_rect = hs_text.get_rect(center=(config.WIDTH // 2, score_y + 105))
            self.screen.blit(hs_shadow, hs_rect.move(2, 2))
            self.screen.blit(hs_text, hs_rect)
        
        # Controls section with wooden button style
        controls_y = box_y + box_height - 150
        
        # Restart button - wooden style
        button_width = 300
        button_height = 60
        button_x = config.WIDTH // 2 - button_width // 2
        
        # Button wood grain
        restart_bg = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        for i in range(button_height):
            t = i / button_height
            noise = random.randint(-3, 3) if random.random() > 0.9 else 0
            r = int(WOOD_BROWN[0] * (0.95 + t * 0.1) + noise)
            g = int(WOOD_BROWN[1] * (0.95 + t * 0.1) + noise)
            b = int(WOOD_BROWN[2] * (0.95 + t * 0.1) + noise)
            pygame.draw.line(restart_bg, (r, g, b), (0, i), (button_width, i))
        
        self.screen.blit(restart_bg, (button_x, controls_y))
        
        # Button border
        pygame.draw.rect(self.screen, WOOD_DARK, (button_x, controls_y, button_width, button_height), 
                        4, border_radius=10)
        
        # Button highlight
        pygame.draw.rect(self.screen, WOOD_LIGHT, (button_x + 4, controls_y + 4, button_width - 8, 3), 
                        border_radius=5)
        
        restart_shadow = self.medium_font.render("Press R to Restart", True, TEXT_DARK)
        restart_text = self.medium_font.render("Press R to Restart", True, TEXT_WHITE)
        restart_rect = restart_text.get_rect(center=(config.WIDTH // 2, controls_y + 30))
        self.screen.blit(restart_shadow, restart_rect.move(2, 2))
        self.screen.blit(restart_text, restart_rect)
        
        # Menu instruction
        menu_shadow = self.small_font.render("Press ESC for Menu", True, TEXT_DARK)
        menu_text = self.small_font.render("Press ESC for Menu", True, (200, 180, 140))
        menu_rect = menu_text.get_rect(center=(config.WIDTH // 2, controls_y + 85))
        self.screen.blit(menu_shadow, menu_rect.move(1, 1))
        self.screen.blit(menu_text, menu_rect)
    
    def draw_ready_screen(self, control_mode="buttons"):
        """Draw ready screen with wooden theme"""
        # Plain beige overlay
        PLAIN_BG = (255, 248, 220)
        overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        overlay.fill((*PLAIN_BG, 240))
        self.screen.blit(overlay, (0, 0))
        
        # Wooden colors
        WOOD_BROWN = (139, 90, 43)
        WOOD_DARK = (101, 67, 33)
        WOOD_LIGHT = (160, 110, 70)
        TEXT_WHITE = (255, 255, 255)
        TEXT_DARK = (70, 40, 20)
        
        # Wooden box for instructions
        box_width = 600
        box_height = 400
        box_x = (config.WIDTH - box_width) // 2
        box_y = (config.HEIGHT - box_height) // 2
        
        # Wooden box with wood grain effect
        box_surf = pygame.Surface((box_width, box_height))
        for i in range(box_height):
            t = i / box_height
            noise = random.randint(-5, 5) if random.random() > 0.9 else 0
            r = int(WOOD_BROWN[0] * (0.9 + t * 0.2) + noise)
            g = int(WOOD_BROWN[1] * (0.9 + t * 0.2) + noise)
            b = int(WOOD_BROWN[2] * (0.9 + t * 0.2) + noise)
            pygame.draw.line(box_surf, (r, g, b), (0, i), (box_width, i))
        
        # Draw wooden box
        self.screen.blit(box_surf, (box_x, box_y))
        
        # Wooden border
        pygame.draw.rect(self.screen, WOOD_DARK, (box_x, box_y, box_width, box_height), 6, border_radius=15)
        
        # Highlight
        pygame.draw.rect(self.screen, WOOD_LIGHT, (box_x + 8, box_y + 8, box_width - 16, 4), border_radius=2)
        
        # Wood screws in corners
        screw_positions = [
            (box_x + 20, box_y + 20),
            (box_x + box_width - 20, box_y + 20),
            (box_x + 20, box_y + box_height - 20),
            (box_x + box_width - 20, box_y + box_height - 20)
        ]
        for pos in screw_positions:
            pygame.draw.circle(self.screen, WOOD_DARK, pos, 5)
            pygame.draw.circle(self.screen, (80, 50, 25), pos, 4)
        
        # "GET READY!" title with shadow
        title_shadow = self.title_font.render("GET READY!", True, TEXT_DARK)
        title_text = self.title_font.render("GET READY!", True, (255, 215, 0))  # Gold color
        title_rect = title_text.get_rect(center=(config.WIDTH // 2, box_y + 70))
        self.screen.blit(title_shadow, title_rect.move(3, 3))
        self.screen.blit(title_text, title_rect)
        
        # Separator line
        line_y = box_y + 130
        pygame.draw.line(self.screen, WOOD_DARK, 
                        (box_x + 50, line_y), (box_x + box_width - 50, line_y), 3)
        
        # Instructions based on control mode
        if control_mode == "gestures":
            instructions = [
                ("3+ fingers", "ACCELERATE"),
                ("Fist", "BRAKE"),
            ]
            start_text = "Make any gesture to start!"
        else:
            instructions = [
                ("UP or W", "ACCELERATE"),
                ("DOWN or S", "BRAKE"),
            ]
            start_text = "Press any key to start!"
        
        # Draw instructions
        y_start = box_y + 170
        for i, (key, action) in enumerate(instructions):
            y_pos = y_start + i * 60
            
            # Key part (left side) - white
            key_shadow = self.hud_font.render(key, True, TEXT_DARK)
            key_text = self.hud_font.render(key, True, TEXT_WHITE)
            key_rect = key_text.get_rect(midright=(config.WIDTH // 2 - 20, y_pos))
            self.screen.blit(key_shadow, key_rect.move(2, 2))
            self.screen.blit(key_text, key_rect)
            
            # "=" symbol
            equals_shadow = self.hud_font.render("=", True, TEXT_DARK)
            equals_text = self.hud_font.render("=", True, (200, 180, 140))
            equals_rect = equals_text.get_rect(center=(config.WIDTH // 2, y_pos))
            self.screen.blit(equals_shadow, equals_rect.move(2, 2))
            self.screen.blit(equals_text, equals_rect)
            
            # Action part (right side) - gold
            action_shadow = self.hud_font.render(action, True, TEXT_DARK)
            action_text = self.hud_font.render(action, True, (255, 215, 0))
            action_rect = action_text.get_rect(midleft=(config.WIDTH // 2 + 20, y_pos))
            self.screen.blit(action_shadow, action_rect.move(2, 2))
            self.screen.blit(action_text, action_rect)
        
        # Start instruction at bottom in wooden button style
        button_y = box_y + box_height - 100
        button_width = 450
        button_height = 60
        button_x = config.WIDTH // 2 - button_width // 2
        
        # Button wood grain
        button_bg = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
        for i in range(button_height):
            t = i / button_height
            noise = random.randint(-3, 3) if random.random() > 0.9 else 0
            r = int(WOOD_BROWN[0] * (0.95 + t * 0.1) + noise)
            g = int(WOOD_BROWN[1] * (0.95 + t * 0.1) + noise)
            b = int(WOOD_BROWN[2] * (0.95 + t * 0.1) + noise)
            pygame.draw.line(button_bg, (r, g, b), (0, i), (button_width, i))
        
        self.screen.blit(button_bg, (button_x, button_y))
        
        # Button border
        pygame.draw.rect(self.screen, WOOD_DARK, (button_x, button_y, button_width, button_height), 
                        4, border_radius=10)
        
        # Button highlight
        pygame.draw.rect(self.screen, WOOD_LIGHT, (button_x + 4, button_y + 4, button_width - 8, 3), 
                        border_radius=5)
        
        # Start text
        start_shadow = self.medium_font.render(start_text, True, TEXT_DARK)
        start_rendered = self.medium_font.render(start_text, True, (100, 255, 100))
        start_rect = start_rendered.get_rect(center=(config.WIDTH // 2, button_y + 30))
        self.screen.blit(start_shadow, start_rect.move(2, 2))
        self.screen.blit(start_rendered, start_rect)
    
    def draw_gesture_feed(self, frame):
        """Draw gesture camera feed"""
        if not CV2_OK or frame is None:
            return
        try:
            w, h = 240, 180
            # Resize frame
            frame_resized = cv2.resize(frame, (w, h))
            # Convert color
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            # Create pygame surface
            surf = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
            # Position in bottom-right corner
            x, y = config.WIDTH - w - 10, config.HEIGHT - h - 10
            # Draw border
            pygame.draw.rect(self.screen, (0, 255, 0), (x-3, y-3, w+6, h+6), 3)
            # Draw frame
            self.screen.blit(surf, (x, y))
            # Draw label
            label = self.small_font.render("GESTURE CONTROL", True, (0, 255, 0))
            r = label.get_rect(centerx=x+w//2, bottom=y-5)
            pygame.draw.rect(self.screen, (0, 0, 0), r.inflate(10, 4))
            self.screen.blit(label, r)
        except Exception as e:
            # If there's an error, show a placeholder
            w, h = 240, 180
            x, y = config.WIDTH - w - 10, config.HEIGHT - h - 10
            pygame.draw.rect(self.screen, (50, 50, 50), (x, y, w, h))
            pygame.draw.rect(self.screen, (255, 0, 0), (x-3, y-3, w+6, h+6), 3)
            error_text = self.small_font.render("CAMERA ERROR", True, (255, 0, 0))
            error_rect = error_text.get_rect(center=(x+w//2, y+h//2))
            self.screen.blit(error_text, error_rect)

    
    def render_scene(self, clouds, terrain, coins, fuel_canisters, car, camera_x, 
                    score_data, game_time, game_over=False, death_reason="", obstacles=None,
                    paused=False, mouse_pos=None, is_sound_on=True, gesture_frame=None,
                    ready_state=False, control_mode="buttons"):
        """Render entire game scene with theme support"""
        # Sky
        self.draw_sky()
        
        # Stars (night theme)
        self.theme_renderer.draw_stars(self.screen, game_time)
        
        # Sun/Moon
        self.theme_renderer.draw_celestial(self.screen, game_time)
        
        # Clouds (only in sunny/rain themes)
        if config.CURRENT_THEME in ["sunny", "rain"]:
            for cloud in clouds:
                cloud.draw(self.screen)
        
        # Terrain with themed grass color
        if hasattr(terrain, 'draw_themed'):
            terrain.draw_themed(self.screen, camera_x, self.theme_renderer.get_grass_color())
        else:
            terrain.draw(self.screen, camera_x)
        
        # Obstacles
        if obstacles:
            for obstacle in obstacles:
                obstacle.draw(self.screen, camera_x)
        
        # Coins
        for coin in coins:
            coin.draw(self.screen, camera_x, game_time)
        
        # Fuel canisters
        for fuel_can in fuel_canisters:
            fuel_can.draw(self.screen, camera_x, game_time)
        
        # Car
        car.draw(self.screen, camera_x)
        
        # Weather effects (rain/snow)
        self.theme_renderer.update_weather()
        self.theme_renderer.draw_weather_effects(self.screen)
        
        # HUD with refill animation
        self.draw_hud(score_data, score_data.get('is_refilling', False))
        
        # Gesture feed
        if gesture_frame is not None:
            self.draw_gesture_feed(gesture_frame)
        
        # Sound button (always visible, even during pause/game over)
        sound_button_rect = None
        if mouse_pos is None:
            mouse_pos = pygame.mouse.get_pos()
        sound_button_rect = self.draw_sound_button(mouse_pos, is_sound_on)
        
        # Pause button (only when not game over)
        pause_button_rect = None
        if not game_over and not paused:
            pause_button_rect = self.draw_pause_button(mouse_pos)
        
        # Pause menu
        resume_rect = None
        menu_rect = None
        if paused and not game_over:
            resume_rect, menu_rect = self.draw_pause_menu(mouse_pos)
        
        # Ready state screen
        if ready_state:
            self.draw_ready_screen(control_mode)
        
        # Game Over screen
        if game_over:
            self.draw_game_over(score_data, death_reason)
        
        # Update display
        pygame.display.flip()
        
        return pause_button_rect, resume_rect, menu_rect, sound_button_rect


