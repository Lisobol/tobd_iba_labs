import gym
import numpy as np
from Cartpole import CartPole


def run(epochs: int, epsilon, min_epsilon, decay):
    cp = gym.make('CartPole-v0')
    cart_pole = CartPole(states_count=cp.observation_space.shape[0],
                         actions_count=cp.action_space.n)

    count = 0
    avg_reward = []

    for epoch in range(epochs):
        state = cp.reset()
        total_reward = 0
        while True:
            cp.render()

            if count == 0:
                action = cp.action_space.sample()
            else:
                action = cart_pole.choose_action(state, epsilon)

            next_state, reward, terminated, _ = cp.step(action)
            total_reward += reward

            cart_pole.save_to_memory([state, reward, action, next_state, terminated])
            state = next_state

            if count > cart_pole.batch_size:
                cart_pole.train()
            count += 1

            if epsilon > min_epsilon:
                epsilon *= decay

            if terminated:
                avg_reward.append(total_reward)
                break

        if len(avg_reward) > 100:
            del avg_reward[0]

        if np.mean(avg_reward) > 195:
            break

        print("Epoch: ", epoch, "reward: ", total_reward, "avg: ", np.mean(avg_reward))
    print('Всего ', epochs, ' эпох')


if __name__ == 'main':
    run(epochs=1000, epsilon=0.9, min_epsilon=0.01, decay=0.995)
