import numpy as np
import Environment
import random
import time

################# Q LEARNING FUNCTIONS #################

def init_q_table(loadFromTextFile, size, q_table_file):
    """
    This function initilize q_table

    Parameters:
    loadFromTextFile (bool): if True than load q_table from file, else init with zeros;
    size (4 parametres tuple): shape of q_table in numpy;
    q_table_file (string): file name;

    Returns:
    Q_table
    """
    if loadFromTextFile:
        return np.loadtxt(q_table_file).reshape(size)
    else:
        return np.zeros(size)


def choose_action(point_interval, state, bus_stops_state):
    """
    This is function choose q_table action based on point interval and state

    Returns:
    action (int, 0-3)
    """
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, 3)  # Random action
    else:
        return np.argmax(q_table[point_interval, bus_stops_state, state[0], state[1]])  # Greedy action


def update_q_table(state, action, next_state, reward, point_interval, bus_stops_state):
    """
    This is function updates q_table based on current state, action, next state, reward, and point interval
    """
    q_value = q_table[point_interval, bus_stops_state, state[0], state[1], action]
    max_q_value = np.max(q_table[point_interval, bus_stops_state, next_state[0], next_state[1]])
    q_table[point_interval, bus_stops_state, state[0], state[1], action] = (1 - alpha) * q_value + alpha * (reward + gamma * max_q_value)

######################################################

# Init environment
env = Environment.Bus_environment

# Get size of environment
env_width, env_height = env.get_actions(env)
env.initialize(env, 'bus_schedule.txt', 'map_info.txt')

# number of different combinations of people on bus stop, 6 start time, 22 end time, after each 30 minutes number
# of people on bus stop change
max_combinations = env.get_max_combinations(env)

# Q-learning parameters
alpha = 0.8  # Learning rate
gamma = 0.5  # Discount factor
epsilon = 0.0  # Exploration rate, if epsilon 0 only values from q table, if 1 only exploration
max_iterations = 100000 # number of whole training epochs, one epoch is whole environment cycle

"""
[9, 2] 1
[2, 5] 2
[4, 7] 3
[6, 9] 4
[2, 1] 5
"""

# All bus stops states, list lenght equals to bus stops number
env_stops_state = [0, 0, 0, 0, 0]

# Init q_table, 32 = number of diffrent stops states 2^5
q_table = init_q_table(True, (max_combinations, 32, env_width, env_height, 4), "q_table_Trained.txt")


# Q-learning training
iterations = 0
last_point_interval = 0
while iterations < max_iterations and not env.is_finished(env):

    # current player position
    player_position = env.player_position

    # current action
    bus_stops_state = int(''.join(map(str, env_stops_state)), 2)
    action = choose_action(env.point_interval, player_position, bus_stops_state)

    # Take the action
    if action == 0:  # Up
        new_position = [player_position[0], max(player_position[1] - 1, 0)]
    elif action == 1:  # Down
        new_position = [player_position[0], min(player_position[1] + 1, env_height - 1)]
    elif action == 2:  # Left
        new_position = [max(player_position[0] - 1, 0), player_position[1]]
    elif action == 3:  # Right
        new_position = [min(player_position[0] + 1, env_width - 1), player_position[1]]



    bus_stops_state = int(''.join(map(str, env_stops_state)), 2)

    # Calculate the reward
    reward = env.get_reward(env, new_position)
    # Update the Q-table
    update_q_table(player_position, action, new_position, reward, env.point_interval, bus_stops_state)
    # Update the player position
    env.player_position = new_position

    if new_position in env.green_squares:
        index = env.green_squares.index(new_position)
        env_stops_state[index] = 1

    # Update environment
    env.update_env(env)
    if env.point_interval != last_point_interval:
        env_stops_state = [0, 0, 0, 0, 0]
    last_point_interval = env.point_interval

    if(env.isFinished):
        iterations += 1
        print(iterations)
        print(env.player_points)
        if iterations > max_iterations:
            epsilon = 0
        env.initialize(env, 'bus_schedule.txt', 'map_info.txt')

    # Save trained q table
    if iterations > max_iterations-1:
        np.savetxt('q_table.txt', q_table.reshape(max_combinations, -1))

    # Viusalize q_table, if you want to have faster training comment out
    #time.sleep(0.1)
    #env.visualize(env)

print(q_table)

