import pygame, random

class MapCreator:
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 500
    GRID_SIZE = 10
    SQUARE_SIZE = 50
    GRID_WIDTH = WINDOW_WIDTH // SQUARE_SIZE
    GRID_HEIGHT = WINDOW_HEIGHT // SQUARE_SIZE
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0 , 255)
    green_squares = []
    red_squares = []
    bus_start = []

    def __init__(self):
        self.grid = [[self.BLACK for _ in range(self.GRID_WIDTH)] for _ in range(self.GRID_HEIGHT)]
        self.running = False

    def run(self):
        pygame.init()
        window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Map Creator")

        self.running = True
        while self.running:
            self.handle_events()

            # Draw grid
            window.fill(self.WHITE)
            for row in range(self.GRID_HEIGHT):
                for col in range(self.GRID_WIDTH):
                    x = col * (self.SQUARE_SIZE + 1)  # Add 1 for white space
                    y = row * (self.SQUARE_SIZE + 1)  # Add 1 for white space
                    pygame.draw.rect(window, self.grid[row][col], (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

            # Update the display
            pygame.display.update()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    col = mouse_pos[0] // (self.SQUARE_SIZE + 1)
                    row = mouse_pos[1] // (self.SQUARE_SIZE + 1)
                    self.update_grid(row, col, False)
                if event.button == 3: # Right mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    col = mouse_pos[0] // (self.SQUARE_SIZE + 1)
                    row = mouse_pos[1] // (self.SQUARE_SIZE + 1)
                    self.update_grid(row, col, True)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.save_bus_schedule()
                self.save_map_info()

    def update_grid(self, row, col, bus_start):

        current_color = self.grid[row][col]
        if current_color == self.BLACK and not bus_start:
            self.grid[row][col] = self.GREEN
            self.green_squares.append([col, row])
        elif current_color == self.GREEN and not bus_start:
            self.grid[row][col] = self.RED
            self.red_squares.append([col, row])
            self.green_squares.remove([col, row])
        elif current_color == self.RED and not bus_start:
            self.grid[row][col] = self.BLACK
            self.red_squares.remove([col, row])

        if current_color == self.BLACK and bus_start:
            self.grid[row][col] = self.BLUE
            self.bus_start = [col, row]
        elif current_color == self.BLUE and bus_start:
            self.bus_start = []
            self.grid[row][col] = self.BLACK

    def save_bus_schedule(self):
        filename = "bus_schedule_2.txt"
        with open(filename, "w") as file:
            line = f"id,cords,people_num\n"
            file.write(line)
            for i, square in enumerate(self.green_squares, start=1):
                cord = list(square)
                people_num = [random.randint(0, 10) for _ in range(32)]
                line = f"{i} , {cord} , {people_num}\n"
                file.write(line)

    def save_map_info(self):
        filename = "map_info_2.txt"
        with open(filename, "w") as file:
            line = f"road_blockades,bus_start_position\n"
            file.write(line)
            cord = self.bus_start
            road_blockades = [self.red_squares[i] for i in range(len(self.red_squares))]
            line = f"{road_blockades} , {cord}\n"
            file.write(line)


# Create and run the map creator
map_creator = MapCreator()
map_creator.run()
