"""
SWYFT - Input Handler with WASD Support
"""
import pygame

class InputHandler:
    def __init__(self, gesture_handler=None):
        self.accelerating = False
        self.braking = False
        self.quit_requested = False
        self.restart_requested = False
        self.menu_requested = False
        self.pause_requested = False
        self.pause_button_clicked = False
        self.gesture_handler = gesture_handler
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_requested = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart_requested = True
                elif event.key == pygame.K_ESCAPE:
                    self.menu_requested = True
                elif event.key == pygame.K_p:
                    self.pause_requested = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.pause_button_clicked = True
    
    def update_input(self):
        """Update input state from keyboard and gestures"""
        keys = pygame.key.get_pressed()
        
        # Keyboard controls - Arrow keys, WASD, and Space
        keyboard_accel = (keys[pygame.K_RIGHT] or keys[pygame.K_UP] or 
                         keys[pygame.K_w] or keys[pygame.K_SPACE])
        keyboard_brake = (keys[pygame.K_LEFT] or keys[pygame.K_DOWN] or 
                         keys[pygame.K_s])
        
        # Gesture controls
        gesture_accel = False
        gesture_brake = False
        if self.gesture_handler and self.gesture_handler.is_active():
            gesture_accel = self.gesture_handler.is_accelerating()
            gesture_brake = self.gesture_handler.is_braking()
        
        # Combined input (keyboard OR gestures)
        self.accelerating = keyboard_accel or gesture_accel
        self.braking = keyboard_brake or gesture_brake
    
    def is_accelerating(self):
        return self.accelerating
    
    def is_braking(self):
        return self.braking
    
    def should_quit(self):
        return self.quit_requested
    
    def should_restart(self):
        if self.restart_requested:
            self.restart_requested = False
            return True
        return False
    
    def should_go_to_menu(self):
        if self.menu_requested:
            self.menu_requested = False
            return True
        return False
    
    def should_pause(self):
        if self.pause_requested:
            self.pause_requested = False
            return True
        return False
    
    def was_pause_button_clicked(self):
        if self.pause_button_clicked:
            self.pause_button_clicked = False
            return True
        return False
    
    def get_mouse_pos(self):
        return pygame.mouse.get_pos()
