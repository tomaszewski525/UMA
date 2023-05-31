import numpy as np
import Environment
import random
import time

def init_q_table(loadFromTextFile, size):
    if loadFromTextFile:
        return np.loadtxt('q_table.txt').reshape(size)
    else:
        return np.zeros(size)


def choose_action(point_interval,state):
    if random.uniform(0, 1) < epsilon:
        return random.randint(0, 3)  # Random action
    else:
        return np.argmax(q_table[point_interval, state[0], state[1]])  # Greedy action


def update_q_table(state, action, next_state, reward, turn):
    q_value = q_table[turn, state[0], state[1], action]
    max_q_value = np.max(q_table[turn, next_state[0], next_state[1]])
    q_table[turn, state[0], state[1], action] = (1 - alpha) * q_value + alpha * (reward + gamma * max_q_value)



env = Environment.Bus_environment

# Get size of environment
env_width, env_height = env.get_actions(env)
env.initialize(env, 'bus_schedule.txt', 'map_info.txt')

# number of different combinations of people on bus stop
max_combinations = env.get_max_combinations(env)

# Q-learning parameters
alpha = 0.6  # Learning rate
gamma = 0.6  # Discount factor
epsilon = 0.5  # Exploration rate
max_iterations = 150000

q_table = init_q_table(True, (max_combinations, env_width, env_height, 4))
print(q_table)


iterations = 0
while iterations < max_iterations and not env.is_finished(env):

    player_position = env.player_position

    action = choose_action(env.point_interval, player_position)
    # Take the action
    if action == 0:  # Up
        new_position = [player_position[0], max(player_position[1] - 1, 0)]
    elif action == 1:  # Down
        new_position = [player_position[0], min(player_position[1] + 1, env_height - 1)]
    elif action == 2:  # Left
        new_position = [max(player_position[0] - 1, 0), player_position[1]]
    elif action == 3:  # Right
        new_position = [min(player_position[0] + 1, env_width - 1), player_position[1]]

    # Calculate the reward
    reward = env.get_reward(env, new_position)



    # Update the Q-table

    update_q_table(player_position, action, new_position, reward, env.point_interval)
    # Update the player position
    env.player_position = new_position

    env.update_env(env)
    if(env.isFinished):
        iterations += 1
        print(iterations)
        print(env.player_points)
        if iterations > max_iterations:
            epsilon = 0
        env.initialize(env, 'bus_schedule.txt', 'map_info.txt')

    if iterations > max_iterations-1:
        np.savetxt('q_table.txt', q_table.reshape(max_combinations, -1))

    time.sleep(0.1)
    env.visualize(env)

print(q_table)

