while len(green_squares) < 5:
    square = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
    if square != player_position and square not in red_squares and square not in green_squares:
        green_squares.append(square)

        # in our env number of points will change in 30 min intervals so 32 points values
        square_set_points = []
        for i in range(0, 32):
            square_set_points.append(random.randint(0, 10))

        green_square_points[str(square)] = square_set_points

while len(red_squares) < 5:
    square = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
    if square != player_position and square not in red_squares:
        red_squares.append(square)
print(red_squares)

player_position = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]