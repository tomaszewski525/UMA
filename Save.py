import pygame
import random
import time

# Constants
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
GRID_SIZE = 10
SQUARE_SIZE = 50
GRID_WIDTH = WINDOW_WIDTH // SQUARE_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // SQUARE_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT_SIZE = 32

# Game Time ticks
turn = 0
point_interval = 0
turn_time = 2
point_interval_time = 30

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Grid Example")
font = pygame.font.Font(None, FONT_SIZE)

# 6-22 -> 32 przedzialy
# Randomly select a starting position for the player
player_position = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]

# Randomly select five positions for the red squares
red_squares = []
while len(red_squares) < 5:
    square = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
    if square != player_position and square not in red_squares:
        red_squares.append(square)

# Randomly select five positions for the green squares with random point values
green_squares = []
green_square_points = {}
while len(green_squares) < 5:
    square = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
    if square != player_position and square not in red_squares and square not in green_squares:
        green_squares.append(square)

        # in our env number of points will change in 30 min intervals so 32 points values
        square_set_points = []
        for i in range(0, 32):
            square_set_points.append(random.randint(0, 10))

        green_square_points[str(square)] = square_set_points


# Player points
player_points = 0


# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        # Quit env
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:

            # move up one square
            if event.key == pygame.K_UP:
                new_position = [player_position[0], max(player_position[1] - 1, 0)]

                if new_position not in red_squares:
                    player_position = new_position

                    if new_position in green_squares:
                        square_points = green_square_points[str(new_position)][point_interval]
                        player_points += square_points
                        # modify point interval to 0 points if they were collected
                        copy = green_square_points[str(new_position)]
                        copy[point_interval] = 0
                        green_square_points[str(new_position)] = copy

            # move down one square
            elif event.key == pygame.K_DOWN:
                new_position = [player_position[0], min(player_position[1] + 1, GRID_HEIGHT - 1)]
                if new_position not in red_squares:
                    player_position = new_position

                    if new_position in green_squares:
                        square_points = green_square_points[str(new_position)][point_interval]
                        player_points += square_points
                        # modify point interval to 0 points if they were collected
                        copy = green_square_points[str(new_position)]
                        copy[point_interval] = 0
                        green_square_points[str(new_position)] = copy

            elif event.key == pygame.K_LEFT:
                new_position = [max(player_position[0] - 1, 0), player_position[1]]
                if new_position not in red_squares:
                    player_position = new_position

                    if new_position in green_squares:
                        square_points = green_square_points[str(new_position)][point_interval]
                        player_points += square_points
                        # modify point interval to 0 points if they were collected
                        copy = green_square_points[str(new_position)]
                        copy[point_interval] = 0
                        green_square_points[str(new_position)] = copy

            elif event.key == pygame.K_RIGHT:
                new_position = [min(player_position[0] + 1, GRID_WIDTH - 1), player_position[1]]
                if new_position not in red_squares:
                    player_position = new_position

                    if new_position in green_squares:
                        square_points = green_square_points[str(new_position)][point_interval]
                        player_points += square_points
                        # modify point interval to 0 points if they were collected
                        copy = green_square_points[str(new_position)]
                        copy[point_interval] = 0
                        green_square_points[str(new_position)] = copy

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN]:
                if new_position not in red_squares:
                    turn += 1

    # Calculate game time
    elapsed_time = turn*turn_time
    hours = 6 + elapsed_time // 60
    minutes = (elapsed_time % 60)
    current_time = f"{hours:02d}:{minutes:02d}"

    # calculate which point interval should be visible
    point_interval = elapsed_time // point_interval_time

    # Check if the hour is 22 (10 PM)
    if hours == 22:
        # Reset game state
        player_position = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
        red_squares = []
        while len(red_squares) < 5:
            square = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
            if square != player_position and square not in red_squares:
                red_squares.append(square)
        green_squares = []
        while len(green_squares) < 5:
            square = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
            if square != player_position and square not in red_squares and square not in green_squares:
                green_squares.append(square)
        turn = 0

    # Fill the window with black
    window.fill(BLACK)

    # Draw grid
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            if [col, row] == player_position:
                pygame.draw.rect(window, BLUE, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            elif [col, row] in red_squares:
                pygame.draw.rect(window, RED, (x, y, SQUARE_SIZE, SQUARE_SIZE))
            elif [col, row] in green_squares:
                pygame.draw.rect(window, GREEN, (x, y, SQUARE_SIZE, SQUARE_SIZE))
                square_points = green_square_points[str([col, row])][point_interval]
                text_surface = font.render(str(square_points), True, BLACK)
                text_rect = text_surface.get_rect(center=(x + SQUARE_SIZE // 2, y + SQUARE_SIZE // 2))
                window.blit(text_surface, text_rect)
            else:
                pygame.draw.rect(window, WHITE, (x, y, SQUARE_SIZE, SQUARE_SIZE), 1)

    # Display current time in the upper-left corner
    text_surface = font.render(current_time, True, WHITE)
    window.blit(text_surface, (10, 10))
    points_text = f"Points: {player_points}"
    points_surface = font.render(points_text, True, WHITE)
    window.blit(points_surface, (10, 50))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    pygame.time.Clock().tick(30)

# Quit the game
pygame.quit()
