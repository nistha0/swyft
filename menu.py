import pygame
import sys
import math
import random
import config
from music_manager import get_music_manager

# Initialize pygame for menu
pygame.init()

# Initialize music manager
music_manager = get_music_manager()

# Color palette - wooden theme
PLAIN_BG = (255, 248, 220)  # Light cream/beige background
WOOD_BROWN = (139, 90, 43)  # Wood color
WOOD_DARK = (101, 67, 33)   # Dark wood color
WOOD_LIGHT = (160, 110, 70)  # Light wood highlight
TEXT_WHITE = (255, 255, 255)
TEXT_DARK = (70, 40, 20)    # Dark brown text

# Fonts
title_font = pygame.font.Font(None, 120)
button_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 28)

class WoodenButton:
    """Wooden sign-style button"""
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        self.hover_offset = 0
        self.target_offset = 0
    
    def update(self):
        self.target_offset = -3 if self.is_hovered else 0
        self.hover_offset += (self.target_offset - self.hover_offset) * 0.2
    
    def draw(self, screen):
        draw_rect = self.rect.move(0, int(self.hover_offset))
        
        # Wooden sign pole
        pole_width = 15
        pole_height = 40
        pole_x = draw_rect.centerx - pole_width // 2
        pole_y = draw_rect.bottom
        
        # Draw pole
        pygame.draw.rect(screen, WOOD_DARK, (pole_x, pole_y, pole_width, pole_height))
        pygame.draw.rect(screen, WOOD_LIGHT, (pole_x, pole_y, 4, pole_height))
        
        # Main wooden sign
        # Shadow
        shadow_rect = draw_rect.move(3, 3)
        pygame.draw.rect(screen, (0, 0, 0, 80), shadow_rect, border_radius=8)
        
        # Wood grain effect
        for i in range(draw_rect.height):
            t = i / draw_rect.height
            noise = random.randint(-5, 5) if random.random() > 0.9 else 0
            r = int(WOOD_BROWN[0] * (0.9 + t * 0.2) + noise)
            g = int(WOOD_BROWN[1] * (0.9 + t * 0.2) + noise)
            b = int(WOOD_BROWN[2] * (0.9 + t * 0.2) + noise)
            pygame.draw.line(screen, (r, g, b), 
                           (draw_rect.left, draw_rect.top + i), 
                           (draw_rect.right, draw_rect.top + i))
        
        # Border and details
        pygame.draw.rect(screen, WOOD_DARK, draw_rect, 5, border_radius=8)
        
        # Highlight
        highlight_rect = pygame.Rect(draw_rect.x + 5, draw_rect.y + 5, 
                                     draw_rect.width - 10, 3)
        pygame.draw.rect(screen, WOOD_LIGHT, highlight_rect, border_radius=2)
        
        # Wood screws/nails
        screw_positions = [
            (draw_rect.left + 15, draw_rect.top + 15),
            (draw_rect.right - 15, draw_rect.top + 15),
            (draw_rect.left + 15, draw_rect.bottom - 15),
            (draw_rect.right - 15, draw_rect.bottom - 15)
        ]
        for pos in screw_positions:
            pygame.draw.circle(screen, WOOD_DARK, pos, 4)
            pygame.draw.circle(screen, (80, 50, 25), pos, 3)
        
        # Text with shadow
        text_surf = button_font.render(self.text, True, TEXT_WHITE)
        text_shadow = button_font.render(self.text, True, TEXT_DARK)
        text_rect = text_surf.get_rect(center=draw_rect.center)
        
        screen.blit(text_shadow, text_rect.move(2, 2))
        screen.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class VolumeSlider:
    """Volume slider control"""
    def __init__(self, x, y, width, height, initial_value=0.3):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = initial_value  # 0.0 to 1.0
        self.dragging = False
        self.handle_radius = 12
    
    def handle_event(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        handle_x = self.rect.x + int(self.value * self.rect.width)
        handle_rect = pygame.Rect(handle_x - self.handle_radius, 
                                   self.rect.centery - self.handle_radius,
                                   self.handle_radius * 2, self.handle_radius * 2)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if handle_rect.collidepoint(mouse_x, mouse_y) or self.rect.collidepoint(mouse_x, mouse_y):
                self.dragging = True
                self.update_value(mouse_x)
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                return True
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.update_value(mouse_x)
                return True
        return False
    
    def update_value(self, mouse_x):
        """Update slider value based on mouse position"""
        relative_x = mouse_x - self.rect.x
        self.value = max(0.0, min(1.0, relative_x / self.rect.width))
    
    def draw(self, screen):
        # Slider track
        track_rect = pygame.Rect(self.rect.x, self.rect.centery - 4, 
                                self.rect.width, 8)
        pygame.draw.rect(screen, WOOD_DARK, track_rect, border_radius=4)
        
        # Filled portion
        filled_width = int(self.value * self.rect.width)
        if filled_width > 0:
            filled_rect = pygame.Rect(self.rect.x, self.rect.centery - 4,
                                     filled_width, 8)
            pygame.draw.rect(screen, WOOD_BROWN, filled_rect, border_radius=4)
        
        # Handle
        handle_x = self.rect.x + int(self.value * self.rect.width)
        handle_y = self.rect.centery
        
        # Handle shadow
        pygame.draw.circle(screen, (0, 0, 0, 80), 
                         (handle_x + 2, handle_y + 2), self.handle_radius)
        
        # Handle
        pygame.draw.circle(screen, WOOD_LIGHT, (handle_x, handle_y), self.handle_radius)
        pygame.draw.circle(screen, WOOD_DARK, (handle_x, handle_y), self.handle_radius, 2)
        pygame.draw.circle(screen, WOOD_BROWN, (handle_x, handle_y), 4)


def draw_plain_background(screen):
    """Plain colored background"""
    screen.fill(PLAIN_BG)

def home_page(screen, clock):
    """Main menu with wooden sign buttons and bouncing title"""
    
    # Wooden buttons
    start_button = WoodenButton(config.WIDTH//2 - 200, 280, 400, 70, "START GAME")
    difficulty_button = WoodenButton(config.WIDTH//2 - 200, 365, 400, 70, "DIFFICULTY: MEDIUM")
    settings_button = WoodenButton(config.WIDTH//2 - 200, 450, 400, 70, "SETTINGS")
    
    running = True
    time = 0
    
    # Current difficulty
    difficulties = ["EASY", "MEDIUM", "HARD"]
    current_diff_index = 1
    config.DIFFICULTY = difficulties[current_diff_index]
    
    while running:
        dt = clock.tick(config.FPS) / 1000.0
        time += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if start_button.handle_event(event):
                return "theme_select"
            if difficulty_button.handle_event(event):
                current_diff_index = (current_diff_index + 1) % len(difficulties)
                config.DIFFICULTY = difficulties[current_diff_index]
                difficulty_button.text = f"DIFFICULTY: {config.DIFFICULTY}"
            if settings_button.handle_event(event):
                return "settings"
        
        start_button.update()
        difficulty_button.update()
        settings_button.update()
        
        # Draw plain background
        draw_plain_background(screen)
        
        # Bouncing SWYFT title
        bounce_offset = math.sin(time * 3) * 15  # Bouncing effect
        title_y = 150 + bounce_offset
        
        # Title shadow
        title_shadow = title_font.render("SWYFT", True, TEXT_DARK)
        title_shadow_rect = title_shadow.get_rect(center=(config.WIDTH//2 + 3, title_y + 3))
        screen.blit(title_shadow, title_shadow_rect)
        
        # Main title
        title = title_font.render("SWYFT", True, WOOD_BROWN)
        title_rect = title.get_rect(center=(config.WIDTH//2, title_y))
        screen.blit(title, title_rect)
        
        # Buttons
        start_button.draw(screen)
        difficulty_button.draw(screen)
        settings_button.draw(screen)
        
        # Difficulty description
        diff_descriptions = {
            "EASY": "Gentle hills, perfect for beginners",
            "MEDIUM": "Moderate challenges, balanced gameplay",
            "HARD": "Extreme terrain, for skilled drivers"
        }
        desc_text = small_font.render(diff_descriptions[config.DIFFICULTY], True, TEXT_DARK)
        desc_rect = desc_text.get_rect(center=(config.WIDTH//2, 545))
        screen.blit(desc_text, desc_rect)
        
        pygame.display.flip()

def theme_select_page(screen, clock):
    """Theme selection page with wooden styling"""
    
    # Theme buttons
    sunny_button = WoodenButton(config.WIDTH//2 - 390, 230, 260, 100, "SUNNY")
    night_button = WoodenButton(config.WIDTH//2 - 110, 230, 260, 100, "NIGHT")
    winter_button = WoodenButton(config.WIDTH//2 - 390, 350, 260, 100, "WINTER")
    rain_button = WoodenButton(config.WIDTH//2 - 110, 350, 260, 100, "RAIN")
    back_button = WoodenButton(50, 50, 150, 60, "← BACK")
    
    running = True
    time = 0
    
    while running:
        dt = clock.tick(config.FPS) / 1000.0
        time += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if sunny_button.handle_event(event):
                config.CURRENT_THEME = "sunny"
                return "control_select"
            if night_button.handle_event(event):
                config.CURRENT_THEME = "night"
                return "control_select"
            if winter_button.handle_event(event):
                config.CURRENT_THEME = "winter"
                return "control_select"
            if rain_button.handle_event(event):
                config.CURRENT_THEME = "rain"
                return "control_select"
            if back_button.handle_event(event):
                return "home"
        
        sunny_button.update()
        night_button.update()
        winter_button.update()
        rain_button.update()
        back_button.update()
        
        draw_plain_background(screen)
        
        # Title
        title = button_font.render("Choose Your Theme", True, WOOD_BROWN)
        title_shadow = button_font.render("Choose Your Theme", True, TEXT_DARK)
        title_rect = title.get_rect(center=(config.WIDTH//2, 130))
        screen.blit(title_shadow, title_rect.move(2, 2))
        screen.blit(title, title_rect)
        
        sunny_button.draw(screen)
        night_button.draw(screen)
        winter_button.draw(screen)
        rain_button.draw(screen)
        back_button.draw(screen)
        
        pygame.display.flip()

def control_select_page(screen, clock):
    """Control selection page"""
    
    button_control = WoodenButton(config.WIDTH//2 - 340, config.HEIGHT//2 - 60, 300, 110, "BUTTONS")
    gesture_control = WoodenButton(config.WIDTH//2 + 40, config.HEIGHT//2 - 60, 300, 110, "GESTURES")
    back_button = WoodenButton(50, 50, 150, 60, "← BACK")
    
    running = True
    time = 0
    
    while running:
        dt = clock.tick(config.FPS) / 1000.0
        time += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if button_control.handle_event(event):
                return "game_buttons"
            if gesture_control.handle_event(event):
                return "game_gestures"
            if back_button.handle_event(event):
                return "theme_select"
        
        button_control.update()
        gesture_control.update()
        back_button.update()
        
        draw_plain_background(screen)
        
        title = button_font.render("Choose Control Method", True, WOOD_BROWN)
        title_shadow = button_font.render("Choose Control Method", True, TEXT_DARK)
        title_rect = title.get_rect(center=(config.WIDTH//2, 120))
        screen.blit(title_shadow, title_rect.move(2, 2))
        screen.blit(title, title_rect)
        
        button_control.draw(screen)
        gesture_control.draw(screen)
        back_button.draw(screen)
        
        pygame.display.flip()

def settings_page(screen, clock):
    """Settings page with volume control only"""
    
    # Get current volume from music manager
    current_volume = music_manager.music_volume
    
    # Volume slider (centered and larger)
    volume_slider = VolumeSlider(config.WIDTH//2 - 250, 280, 500, 50, current_volume)
    
    # Back button
    back_button = WoodenButton(50, 50, 150, 60, "← BACK")
    
    running = True
    time = 0
    
    while running:
        dt = clock.tick(config.FPS) / 1000.0
        time += dt
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle volume slider
            if volume_slider.handle_event(event):
                music_manager.set_music_volume(volume_slider.value)
            
            if back_button.handle_event(event):
                return "home"
        
        back_button.update()
        
        draw_plain_background(screen)
        
        # Title
        bounce_offset = math.sin(time * 3) * 10
        title = title_font.render("SETTINGS", True, WOOD_BROWN)
        title_shadow = title_font.render("SETTINGS", True, TEXT_DARK)
        title_rect = title.get_rect(center=(config.WIDTH//2, 150 + bounce_offset))
        screen.blit(title_shadow, title_rect.move(2, 2))
        screen.blit(title, title_rect)
        
        # Volume section
        volume_label = button_font.render("Music Volume", True, TEXT_DARK)
        volume_label_rect = volume_label.get_rect(center=(config.WIDTH//2, 240))
        screen.blit(volume_label, volume_label_rect)
        
        volume_slider.draw(screen)
        
        # Volume percentage (larger)
        volume_percent_text = button_font.render(f"{int(volume_slider.value * 100)}%", True, WOOD_BROWN)
        volume_percent_rect = volume_percent_text.get_rect(center=(config.WIDTH//2, 350))
        screen.blit(volume_percent_text, volume_percent_rect)
        
        # Instruction
        instruction = small_font.render("Drag the slider to adjust music volume", True, TEXT_DARK)
        instruction_rect = instruction.get_rect(center=(config.WIDTH//2, 410))
        screen.blit(instruction, instruction_rect)
        
        back_button.draw(screen)
        
        pygame.display.flip()

def main():
    """Main navigation controller"""
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("SWYFT - Hill Climb Racing")
    clock = pygame.time.Clock()
    
    # Set defaults
    if not hasattr(config, 'CURRENT_THEME'):
        config.CURRENT_THEME = "sunny"
    if not hasattr(config, 'DIFFICULTY'):
        config.DIFFICULTY = "MEDIUM"
    
    # Start menu music
    music_manager.play_menu_music()
    
    current_page = "home"
    
    while True:
        if current_page == "home":
            current_page = home_page(screen, clock)
        elif current_page == "settings":
            current_page = settings_page(screen, clock)
        elif current_page == "theme_select":
            current_page = theme_select_page(screen, clock)
        elif current_page == "control_select":
            current_page = control_select_page(screen, clock)
        elif current_page == "game_buttons":
            music_manager.play_gameplay_music()
            import game
            result = game.run_game(control_mode="buttons")
            music_manager.play_menu_music()
            if result == "quit":
                pygame.quit()
                sys.exit()
            else:
                current_page = "home"
        elif current_page == "game_gestures":
            music_manager.play_gameplay_music()
            import game
            result = game.run_game(control_mode="gestures")
            music_manager.play_menu_music()
            if result == "quit":
                pygame.quit()
                sys.exit()
            else:
                current_page = "home"

if __name__ == "__main__":
    main()

