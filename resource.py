def read_bus_schedule(file_name):
    green_squares = []
    green_square_points = {}

    with open(file_name, 'r') as file:
        lines = file.readlines()[1:]

    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        if line:
            values = line.split(' , ')  # Split the line by comma and space
            id_ = int(values[0])
            cords = [int(coord) for coord in values[1].strip('[]').split(',')]
            people_num = [int(num) for num in values[2].strip('[]').split(',')]

            green_squares.append(cords)  # Append cords to green_squares
            green_square_points[str(cords)] = people_num  # Add an entry to green_square_points dictionary
    return green_squares, green_square_points


def read_map_info(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()[1:]
    for line in lines:
        line = line.strip()
        if line:
            red_squares_str, bus_start_position_str = line.split(' , ')
            red_squares = eval(red_squares_str)
            bus_start_position = eval(bus_start_position_str)

    return red_squares, bus_start_position
