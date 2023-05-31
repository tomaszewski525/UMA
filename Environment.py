import pygame
import random
import numpy as np
import resource
import time

class Bus_environment:
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

    isFinished = False
    # Read road blockades and bus start position from file
    red_squares = []
    # Read bus stops positions and passenger amount information
    green_squares = []
    green_square_points = {}
    player_points = 0
    player_position = [0,0]

    # Game Time ticks
    turn = 0
    point_interval = 0
    turn_time = 1
    point_interval_time = 30

    start_time = 6
    finish_time = 22
    elapsed_time = 0
    hours = 0
    minutes = 0
    current_time = ""

    running = False

    def get_actions(self):
        return self.GRID_WIDTH, self.GRID_HEIGHT

    def is_finished(self):
        return self.isFinished

    def get_max_combinations(self):
        return (self.finish_time - self.start_time)*2

    def initialize(self, bush_schedule, map_info):
        self.isFinished = False
        # Read road blockades and bus start position from file
        self.red_squares = []
        # Read bus stops positions and passenger amount information
        self.green_squares = []
        self.green_square_points = {}
        self.player_points = 0
        self.player_position = [0, 0]

        # Game Time ticks
        self.turn = 0
        self.point_interval = 0
        self.turn_time = 1
        self.point_interval_time = 30

        self.start_time = 6
        self.finish_time = 22
        self.elapsed_time = 0
        self.hours = 0
        self.minutes = 0
        self.current_time = ""
        self.player_points = 0
        self.turn = 0
        self.init_pygame_once = False

        self.initialize_map(self, bush_schedule, map_info)


    def get_reward(self, new_position):
        if new_position in self.red_squares:
            return -1000 # Penalty for moving to a red square
        if new_position in self.green_squares:
            square_points_temp = self.green_square_points[str(new_position)][self.point_interval]
            self.player_points += square_points_temp
            # modify point interval to 0 points if they were collected
            copy = self.green_square_points[str(new_position)]
            copy[self.point_interval] = 0
            self.green_square_points[str(new_position)] = copy

            return square_points_temp
        return 0

    def initialize_map(self, bush_schedule, map_info):
        self.red_squares, self.player_position = resource.read_map_info(map_info)
        self.green_squares, self.green_square_points = resource.read_bus_schedule(bush_schedule)

    init_pygame_once = False
    def visualize(self):
        running = True
        if not self.init_pygame_once:
            # Initialize Pygame
            pygame.init()
            window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            pygame.display.set_caption("Grid Example")
            font = pygame.font.Font(None, self.FONT_SIZE)
        # Fill the window with black
        window.fill(self.BLACK)

        # Draw grid
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                x = col * self.SQUARE_SIZE
                y = row * self.SQUARE_SIZE
                if [col, row] == self.player_position:
                    pygame.draw.rect(window, self.BLUE, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))
                elif [col, row] in self.red_squares:
                    pygame.draw.rect(window, self.RED, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))
                elif [col, row] in self.green_squares:
                    pygame.draw.rect(window, self.GREEN, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))
                    square_points = self.green_square_points[str([col, row])][self.point_interval]
                    text_surface = font.render(str(square_points), True, self.BLACK)
                    text_rect = text_surface.get_rect(center=(x + self.SQUARE_SIZE // 2, y + self.SQUARE_SIZE // 2))
                    window.blit(text_surface, text_rect)
                else:
                    pygame.draw.rect(window, self.WHITE, (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE), 1)

        # Display current time in the upper-left corner
        text_surface = font.render(self.current_time, True, self.WHITE)
        window.blit(text_surface, (10, 10))
        points_text = f"Points: {self.player_points}"
        points_surface = font.render(points_text, True, self.WHITE)
        window.blit(points_surface, (10, 50))

        # Update the display
        pygame.display.update()

    def manual_check_reward(self, new_position):
        if new_position in self.green_squares:
            square_points = self.green_square_points[str(new_position)][self.point_interval]
            self.player_points += square_points
            # modify point interval to 0 points if they were collected
            copy = self.green_square_points[str(new_position)]
            copy[self.point_interval] = 0
            self.green_square_points[str(new_position)] = copy

    def update_env(self):
        # Calculate game time
        self.turn += 1
        self.elapsed_time = self.turn * self.turn_time
        self.hours = self.start_time + self.elapsed_time // 60
        self.minutes = (self.elapsed_time % 60)
        self.current_time = f"{self.hours:02d}:{self.minutes:02d}"

        # calculate which point interval should be visible
        self.point_interval = self.elapsed_time // self.point_interval_time

        if self.hours == self.finish_time:
            self.isFinished = True
            # Quit the game
            pygame.quit()

    def manual_steering(self):

        # Handle events
        for event in pygame.event.get():
            # Quit env
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:

                # move up one square
                if event.key == pygame.K_UP:
                    new_position = [self.player_position[0], max(self.player_position[1] - 1, 0)]

                    if new_position not in self.red_squares:
                        self.player_position = new_position
                        self.manual_check_reward(new_position)

                # move down one square
                elif event.key == pygame.K_DOWN:
                    new_position = [self.player_position[0], min(self.player_position[1] + 1, self.GRID_HEIGHT - 1)]
                    if new_position not in self.red_squares:
                        self.player_position = new_position
                        self.manual_check_reward(new_position)

                elif event.key == pygame.K_LEFT:
                    new_position = [max(self.player_position[0] - 1, 0), self.player_position[1]]
                    if new_position not in self.red_squares:
                        self.player_position = new_position
                        self.manual_check_reward(new_position)

                elif event.key == pygame.K_RIGHT:
                    new_position = [min(self.player_position[0] + 1, self.GRID_WIDTH - 1), self.player_position[1]]
                    if new_position not in self.red_squares:
                        self.player_position = new_position
                        self.manual_check_reward(new_position)

            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN]:
                    if new_position not in self.red_squares:
                        self.turn += 1


