import numpy as np
import Environment
import random
import os
import matplotlib.pyplot as plt
from scipy import stats
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


def choose_action(point_interval, state, bus_stops_state, t_epsilon):
    """
    This is function choose q_table action based on point interval and state

    Returns:
    action (int, 0-3)
    """

    if random.uniform(0, 1) < t_epsilon:
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


def evaluation(env, t_epsilon):
    """
    Evaluate q table
    """
    # All bus stops states, list length equals to bus stops number
    env_stops_state = [0 for _ in range(len(env.green_squares))]
    last_point_interval = 0
    while not env.is_finished(env):
        # current player position
        player_position = env.player_position

        # current action
        bus_stops_state = int(''.join(map(str, env_stops_state)), 2)
        action = choose_action(env.point_interval, player_position, bus_stops_state, t_epsilon)

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
            env_stops_state = [0 for _ in range(len(env.green_squares))]
        last_point_interval = env.point_interval

    return env.player_points

def plot_goal_values(goal_values, alphas, epsilons, gamma, i):
    # Generate x-axis values (iteration numbers)
    x = range(1, len(goal_values) + 1)

    # Plot the vector values
    plt.scatter(x, goal_values, s=1)

    # Perform linear regression to get the best line of fit
    slope, intercept, _, _, _ = stats.linregress(x, goal_values)
    line = slope * np.array(x) + intercept

    # Plot the best line of fit
    plt.plot(x, line, color='red', label="Best Fit Line")


    # Set the plot title and labels
    plt.title(f"Badanie, gamma={gamma}")
    plt.xlabel("Numer generacji")
    plt.ylabel("Wartości funkcji celu")
    #plt.savefig(f'generacja{i}.png')
    #plt.clf()
    # Display the plot
    #plt.show()
    #
    # plt.plot(x, alphas)
    # # Set the plot title and labels
    # plt.title(f"Wartości alpha")
    # plt.xlabel("Numer generacji")
    # plt.ylabel("alpha")
    # plt.show()
    #
    # plt.plot(x, epsilons)
    # # Set the plot title and labels
    # plt.title(f"Wartości epsilon")
    # plt.xlabel("Numer generacji")
    # plt.ylabel("epsilon")
    # plt.show()


######################################################
# SETTINGS
visualize = True
save_q_table = False
use_q_table = True  # use trained q table
env_number = 10
os.makedirs(f"Q_Tables/{env_number}", exist_ok=True) # Create save directory
save_file_path = f"Q_Tables/{env_number}/q_table.txt" # where  to save q table
trained_q_table_path = f"Q_Tables/{env_number}/q_table.txt" # trained q table path
bus_schedule_path = f"Maps/{env_number}/bus_schedule.txt"  # bus schedule
map_info_path = f"Maps/{env_number}/map_info.txt"  # map info

# Init environment
env = Environment.Bus_environment

# Get size of environment
env_width, env_height = env.get_actions(env)
env.initialize(env, bus_schedule_path, map_info_path)

# number of different combinations of people on bus stop, 6 start time, 22 end time, after each 30 minutes number
# of people on bus stop change
max_combinations = env.get_max_combinations(env)

# Q-learning parameters
alpha = 1.0  # Learning rate
gamma = 0.7  # Discount factor
epsilon = 0.0  # Exploration rate, if epsilon 0 only values from q table, if 1 only exploration
max_iterations = 1  # number of whole training epochs, one epoch is whole environment cycle

# Changing hiperparametersa
alpha_rate_of_decay = 0.002
alpha_decay_time = 200
epsilon_rate_of_decay = 0.002
epsilon_decay_time = 200
alphas = []
epsilons = []

# All bus stops states, list length equals to bus stops number
env_stops_state = [0 for _ in range(len(env.green_squares))]

# Init q_table, 32 = number of different stops states 2^5
q_table = init_q_table(use_q_table, (max_combinations, 2**len(env_stops_state), env_width, env_height, 4), trained_q_table_path)


# Q-learning training
iterations = 0
last_point_interval = 0

# Visualize score
scores = []
while iterations < max_iterations and not env.is_finished(env):

    # current player position
    player_position = env.player_position

    # current action
    bus_stops_state = int(''.join(map(str, env_stops_state)), 2)
    action = choose_action(env.point_interval, player_position, bus_stops_state, epsilon)

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

    # Player has picked up passengers from bus stop
    if new_position in env.green_squares:
        index = env.green_squares.index(new_position)
        env_stops_state[index] = 1

    # Update environment
    env.update_env(env)
    if env.point_interval != last_point_interval:
        env_stops_state = [0 for _ in range(len(env.green_squares))]
    last_point_interval = env.point_interval

    # Finished env iteration
    if env.isFinished:
        alphas.append(alpha)
        epsilons.append(epsilon)
        iterations += 1

        # Tune hiperparameters
        if iterations % alpha_decay_time == 0:
             alpha = alpha - alpha_rate_of_decay
        if iterations % epsilon_decay_time == 0:
            epsilon = epsilon - epsilon_rate_of_decay


        env.initialize(env, bus_schedule_path, map_info_path)
        value = evaluation(env, 0)
        scores.append(value)
        print(f"Iteration: {iterations}, Q TABLE VALUE: {value}")
        #epsilon = temp_epsilon
        env.initialize(env, bus_schedule_path, map_info_path)

    # Save trained q table
    if iterations > max_iterations-1 and save_q_table:
        np.savetxt(save_file_path, q_table.reshape(max_combinations, -1))

    # Viusalize q_table, if you want to have faster training comment out
    if visualize:
        time.sleep(0.1)
        env.visualize(env)

#plot_goal_values(scores, alphas, epsilons, gamma, i+1)
#print(q_table)

