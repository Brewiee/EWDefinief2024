import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Frogger")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Frog properties
frog_width = 40
frog_height = 40
frog_x = screen_width // 2 - frog_width // 2
frog_y = screen_height - frog_height
frog_speed = 5

# Car properties
car_width = 60
car_height = 40
car_speed = 7
cars = []


def create_car():
    car_x = random.randint(0, screen_width - car_width)
    car_y = random.randint(50, screen_height - 100)
    car = pygame.Rect(car_x, car_y, car_width, car_height)
    return car


for _ in range(6):
    cars.append(create_car())

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()


def reset_game():
    global frog_x, frog_y, cars, running, game_over, win, message_time
    frog_x = screen_width // 2 - frog_width // 2
    frog_y = screen_height - frog_height
    cars.clear()
    for _ in range(6):
        cars.append(create_car())
    running = True
    game_over = False
    win = False
    message_time = 0


running = True
game_over = False
win = False
message_time = 0
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running = False
            elif event.key == pygame.K_RETURN:
                if game_over or win:
                    reset_game()

    if not game_over and not win:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            frog_x -= frog_speed
        if keys[pygame.K_RIGHT]:
            frog_x += frog_speed
        if keys[pygame.K_UP]:
            frog_y -= frog_speed
        if keys[pygame.K_DOWN]:
            frog_y += frog_speed

        # Boundaries for the frog
        if frog_x < 0:
            frog_x = 0
        elif frog_x > screen_width - frog_width:
            frog_x = screen_width - frog_width
        if frog_y < 0:
            frog_y = 0
        elif frog_y > screen_height - frog_height:
            frog_y = screen_height - frog_height

        # Draw frog
        pygame.draw.rect(screen, GREEN, (frog_x, frog_y, frog_width, frog_height))

        # Draw cars
        for car in cars:
            pygame.draw.rect(screen, BLACK, car)
            car.x += car_speed
            if car.x > screen_width:
                car.x = 0 - car_width
                car.y = random.randint(50, screen_height - 100)

        # Collision detection
        frog_rect = pygame.Rect(frog_x, frog_y, frog_width, frog_height)
        for car in cars:
            if frog_rect.colliderect(car):
                game_over = True
                message_time = time.time()  # Initialize the timer for message flickering
                break

        # Check if frog reaches the other side
        if frog_y == 0:
            win = True
            message_time = time.time()  # Initialize the timer for message flickering

    # Draw the game-over or win message with flickering effect
    if game_over or win:
        current_time = time.time()
        if int(current_time * 2) % 2 == 0:  # Flicker the message every 0.5 seconds
            if game_over:
                text = font.render("You died. Press Enter to restart.", True, RED)
            elif win:
                text = font.render("You win! Press Enter to restart.", True, RED)
            screen.blit(text, (screen_width // 2 - 180, screen_height // 2))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
