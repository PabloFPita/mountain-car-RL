import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import pickle
import sys
import time

def run(episodes, is_training=True, render=False):
    """
    Run the Mountain Car RL algorithm.

    Args:
        episodes (int): The number of episodes to run.
        is_training (bool, optional): Whether to run in training mode or not. Defaults to True.
        render (bool, optional): Whether to render the environment. Defaults to False.
    """

    env = gym.make('MountainCar-v0', render_mode='human' if render else None)

    # Divide position and velocity into segments. To discretize the state space.
    pos_space = np.linspace(env.observation_space.low[0], env.observation_space.high[0], 40)    # Between -1.2 and 0.6
    vel_space = np.linspace(env.observation_space.low[1], env.observation_space.high[1], 40)    # Between -0.07 and 0.07

    if(is_training):
        q = np.zeros((len(pos_space), len(vel_space), env.action_space.n)) # init a 40x40x3 array
    else:
        f = open(f'models\mountain_car.pkl', 'rb')
        q = pickle.load(f)
        f.close()

    learning_rate_a = 0.9 # alpha or learning rate. If we increase this, the agent will learn faster but may not converge.
    discount_factor_g = 0.9 # gamma or discount factor. If we increase this, the agent will care more about future rewards.

    epsilon = 1         # 1 = 100% random actions
    epsilon_decay_rate = 2/episodes # epsilon decay rate. If we increase this, the agent will explore more initially.
    rng = np.random.default_rng()   # random number generator

    rewards_per_episode = np.zeros(episodes)
    
    start_time = time.time()  # Start timing

    for i in range(episodes):
        state = env.reset()[0]      # Starting position, starting velocity always 0
        state_p = np.digitize(state[0], pos_space)
        state_v = np.digitize(state[1], vel_space)

        terminated = False          # True when reached goal

        rewards=0

        while(not terminated and rewards>-1000):

            if is_training and rng.random() < epsilon:
                # Choose random action (0=drive left, 1=stay neutral, 2=drive right)
                action = env.action_space.sample()
            else:
                action = np.argmax(q[state_p, state_v, :])

            new_state,reward,terminated,_,_ = env.step(action)
            new_state_p = np.digitize(new_state[0], pos_space)
            new_state_v = np.digitize(new_state[1], vel_space)

            if is_training:
                q[state_p, state_v, action] = q[state_p, state_v, action] + learning_rate_a * (
                    reward + discount_factor_g*np.max(q[new_state_p, new_state_v,:]) - q[state_p, state_v, action]
                ) # Q-learning update rule

            state = new_state
            state_p = new_state_p
            state_v = new_state_v

            rewards+=reward

        epsilon = max(epsilon - epsilon_decay_rate, 0)

        rewards_per_episode[i] = rewards

        # Print the current state of the process every 5 episodes
        if  is_training and i % 100 == 0:
            print(f"Episode: {i}, Rewards: {rewards}, Epsilon: {epsilon}")

    env.close()

    # Save Q table to file
    if is_training:
        f = open(f'models\mountain_car.pkl','wb')
        pickle.dump(q, f)
        f.close()

    mean_rewards = np.zeros(episodes)
    for t in range(episodes):
        mean_rewards[t] = np.mean(rewards_per_episode[max(0, t-100):(t+1)])
        

    plt.plot(mean_rewards)

    # Add labels and title
    plt.xlabel('Episodes')
    plt.ylabel('Mean Rewards')
    plt.title('Mean Rewards per Episode')

    if is_training:
        plt.savefig(f'plots-rewards\mountain_car_train.png')
    else:
        plt.savefig(f'plots-rewards\mountain_car_test.png')
    end_time = time.time()  # End timing

    if is_training:
        print(f"Training finished in {end_time - start_time} seconds")  # Print the time taken for training
    else:
        print(f"Testing finished in {end_time - start_time} seconds")


if __name__ == '__main__':
    mode = sys.argv[1]

    if mode == 'train':
        run(5000, is_training=True, render=False)
    elif mode == 'test':
        run(10, is_training=False, render=True)
    else:
        print("Invalid mode. Please specify 'train' or 'test'.")