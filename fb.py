import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -6
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
BLUE_SKY = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load assets
try:
    bird_images = [
        pygame.image.load("bird1.png").convert_alpha(),
        pygame.image.load("bird2.png").convert_alpha(),
        pygame.image.load("bird3.png").convert_alpha()
    ]
    background_img = pygame.image.load("background.png").convert()
    pipe_img = pygame.image.load("pipe.png").convert_alpha()
except FileNotFoundError:
    print("Error: Image files not found. Please ensure you have:")
    print("bird1.png, bird2.png, bird3.png, background.png, and pipe.png")
    sys.exit()

class Bird:
    def __init__(self):
        self.images = bird_images
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT//2))
        self.movement = 0
        self.animation_speed = 0.15

    def animate(self):
        self.index += self.animation_speed
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[int(self.index)]

    def flap(self):
        self.movement = FLAP_STRENGTH

    def update(self):
        self.movement += GRAVITY
        self.rect.centery += self.movement
        self.animate()

class Pipe:
    def __init__(self):
        self.image = pipe_img
        self.top_pipe = self.image.get_rect()
        self.bottom_pipe = self.image.get_rect()
        self.passed = False
        self.set_position()

    def set_position(self):
        gap_position = random.randint(100, SCREEN_HEIGHT - 100 - PIPE_GAP)
        self.top_pipe.midbottom = (SCREEN_WIDTH, gap_position - PIPE_GAP//2)
        self.bottom_pipe.midtop = (SCREEN_WIDTH, gap_position + PIPE_GAP//2)

    def update(self):
        self.top_pipe.centerx -= PIPE_SPEED
        self.bottom_pipe.centerx -= PIPE_SPEED

    def offscreen(self):
        return self.top_pipe.right < 0

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.active = True
        self.last_pipe = pygame.time.get_ticks()

    def spawn_pipe(self):
        now = pygame.time.get_ticks()
        if now - self.last_pipe > PIPE_FREQUENCY:
            self.pipes.append(Pipe())
            self.last_pipe = now

    def check_collision(self):
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.top_pipe) or \
               self.bird.rect.colliderect(pipe.bottom_pipe):
                self.active = False
        
        if self.bird.rect.top <= 0 or self.bird.rect.bottom >= SCREEN_HEIGHT:
            self.active = False

    def update_score(self):
        for pipe in self.pipes:
            if not pipe.passed and self.bird.rect.left > pipe.top_pipe.right:
                pipe.passed = True
                self.score += 1

    def reset(self):
        self.active = True
        self.bird.rect.center = (100, SCREEN_HEIGHT//2)
        self.pipes.clear()
        self.score = 0

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.active:
                        self.bird.flap()
                    if event.key == pygame.K_r and not self.active:
                        self.reset()

            screen.blit(background_img, (0, 0))

            if self.active:
                # Game elements
                self.spawn_pipe()
                self.bird.update()
                
                for pipe in self.pipes[:]:
                    pipe.update()
                    if pipe.offscreen():
                        self.pipes.remove(pipe)
                
                self.check_collision()
                self.update_score()

            # Draw elements
            screen.blit(self.bird.image, self.bird.rect)
            for pipe in self.pipes:
                screen.blit(pipe.image, pipe.top_pipe)
                screen.blit(pipe.image, pipe.bottom_pipe)

            # Score display
            font = pygame.font.Font(None, 50)
            text = font.render(str(self.score), True, WHITE)
            screen.blit(text, (SCREEN_WIDTH//2 - 15, 50))

            # Game over screen
            if not self.active:
                game_over_font = pygame.font.Font(None, 70)
                game_over_text = game_over_font.render("Game Over", True, WHITE)
                screen.blit(game_over_text, (80, 200))
                restart_text = font.render("Press R to restart", True, WHITE)
                screen.blit(restart_text, (100, 300))

            pygame.display.update()
            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()