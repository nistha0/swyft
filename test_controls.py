#!/usr/bin/env python3
"""
Quick test to verify keyboard controls work
"""
import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Control Test")
clock = pygame.time.Clock()

font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 32)

accelerating = False
braking = False

print("="*60)
print("CONTROL TEST")
print("="*60)
print("Press keys to test:")
print("  W, ↑, Space = Accelerate")
print("  S, ↓ = Brake")
print("  ESC = Quit")
print("="*60)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Check keys
    keys = pygame.key.get_pressed()
    accelerating = keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]
    braking = keys[pygame.K_s] or keys[pygame.K_DOWN]
    
    # Draw
    screen.fill((30, 30, 30))
    
    title = font.render("Keyboard Test", True, (255, 255, 255))
    screen.blit(title, (250, 50))
    
    # Accelerate status
    accel_color = (0, 255, 0) if accelerating else (100, 100, 100)
    accel_text = small_font.render("ACCELERATE (W/↑/Space)", True, accel_color)
    screen.blit(accel_text, (200, 200))
    
    if accelerating:
        status1 = font.render(">>> ACCELERATING >>>", True, (0, 255, 0))
        screen.blit(status1, (150, 250))
    
    # Brake status
    brake_color = (255, 100, 0) if braking else (100, 100, 100)
    brake_text = small_font.render("BRAKE (S/↓)", True, brake_color)
    screen.blit(brake_text, (250, 350))
    
    if braking:
        status2 = font.render("<<< BRAKING <<<", True, (255, 100, 0))
        screen.blit(status2, (200, 400))
    
    # Instructions
    inst = small_font.render("Press ESC to exit", True, (150, 150, 150))
    screen.blit(inst, (250, 550))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("\nTest complete!")
print("If keys worked here, they'll work in the game!")
