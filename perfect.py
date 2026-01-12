import pygame
import math
import random

pygame.init()

# -------------------------
# Screen Setup
# -------------------------
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hill Climb Racing - car Position Manual")
clock = pygame.time.Clock()

# Load ant image
car_image = pygame.image.load("car.png").convert_alpha()
car_scale = 0.2 # scale factor for ant size
car_image = pygame.transform.rotozoom(car_image, 0, car_scale)

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
# Manual car position
# -------------------------
car_x = WIDTH // 2.5   # Change this to move car left/right
car_y = 457      # Change this to move car up/down

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
    

    for cloud in clouds:
        cloud.update(dt)
        cloud.draw()

    draw_hill(hill_back, (0, 130, 0))
    draw_hill(hill_mid, (0, 130, 0))
    draw_hill(hill_front, (0, 130, 0))

    # Draw ant at manual position
    car_rect = car_image.get_rect(midbottom=(car_x, car_y))
    screen.blit(car_image, car_rect)

    pygame.display.update()

pygame.quit()
