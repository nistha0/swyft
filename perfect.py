import pygame
import math
import random

pygame.init()

# -------------------------
# Screen Setup
# -------------------------
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hill Climb Racing - Ant Position Manual")
clock = pygame.time.Clock()

# Load ant image
ant_image = pygame.image.load("ant.png").convert_alpha()
ant_scale = 0.1  # scale factor for ant size
ant_image = pygame.transform.rotozoom(ant_image, 0, ant_scale)

# -------------------------
# Smooth Terrain Generator
# -------------------------
def generate_smooth_hill(offset_y, amplitude, length=WIDTH, step=4):
    points = []
    for x in range(0, length + 20, step):
        y = offset_y + math.sin(x * 0.01) * amplitude + math.sin(x * 0.03) * (amplitude * 0.3)
        points.append((x, y))
    return points

# -------------------------
# Draw sky gradient
# -------------------------
def draw_sky():
    top = (20, 90, 220)
    middle = (100, 180, 255)
    bottom = (200, 230, 255)

    for y in range(HEIGHT):
        t = y / HEIGHT
        if t < 0.5:
            r = top[0] * (1 - t*2) + middle[0] * (t*2)
            g = top[1] * (1 - t*2) + middle[1] * (t*2)
            b = top[2] * (1 - t*2) + middle[2] * (t*2)
        else:
            t2 = (t-0.5)*2
            r = middle[0] * (1 - t2) + bottom[0] * t2
            g = middle[1] * (1 - t2) + bottom[1] * t2
            b = middle[2] * (1 - t2) + bottom[2] * t2
        pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (WIDTH, y))

# -------------------------
# Draw sun with glow
# -------------------------
def draw_sun():
    sun_x, sun_y = 1000, 120
    sun_radius = 70

    glow_surface = pygame.Surface((300, 300), pygame.SRCALPHA)
    
    for i in range(10, 150, 10):
        alpha = max(0, 80 - i//2)
        pygame.draw.circle(glow_surface, (255, 255, 200, alpha), (150, 150), i)
    
    pygame.draw.circle(glow_surface, (255, 255, 180), (150, 150), sun_radius)
    screen.blit(glow_surface, (sun_x - 150, sun_y - 150))

# -------------------------
# Clouds
# -------------------------
class Cloud:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(50, 200)
        self.speed = random.uniform(10, 30)
        self.size = random.randint(20, 50)

    def update(self, dt):
        self.x -= self.speed * dt
        if self.x < -200:
            self.x = WIDTH + random.randint(50, 150)
            self.y = random.randint(50, 200)

    def draw(self):
        c = (255, 255, 255)
        s = self.size
        pygame.draw.circle(screen, c, (int(self.x), int(self.y)), s)
        pygame.draw.circle(screen, c, (int(self.x + s), int(self.y + 20)), s)
        pygame.draw.circle(screen, c, (int(self.x - s), int(self.y + 15)), s)

clouds = [Cloud() for _ in range(5)]

# -------------------------
# Draw hills
# -------------------------
def draw_hill(points, color):
    poly = [(0, HEIGHT)] + points + [(WIDTH, HEIGHT)]
    pygame.draw.polygon(screen, color, poly)

hill_back = generate_smooth_hill(offset_y=450, amplitude=25)
hill_mid = generate_smooth_hill(offset_y=500, amplitude=40)
hill_front = generate_smooth_hill(offset_y=550, amplitude=55)

# -------------------------
# Manual ant position
# -------------------------
ant_x = WIDTH // 2.5   # Change this to move ant left/right
ant_y = 450        # Change this to move ant up/down

# -------------------------
# Main Loop
# -------------------------
running = True
while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_sky()
    draw_sun()

    for cloud in clouds:
        cloud.update(dt)
        cloud.draw()

    draw_hill(hill_back, (160, 220, 170))
    draw_hill(hill_mid, (100, 190, 120))
    draw_hill(hill_front, (70, 150, 90))

    # Draw ant at manual position
    ant_rect = ant_image.get_rect(midbottom=(ant_x, ant_y))
    screen.blit(ant_image, ant_rect)

    pygame.display.update()

pygame.quit()
