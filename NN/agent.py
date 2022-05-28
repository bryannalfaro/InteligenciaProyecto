from pickle import NONE
import random
import torch
import numpy as np
from game import SGNN, Direction, Point
from model import Linear_Qnet, QTrainer
from ploter import plot
from collections import deque

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001  # ! probar con otro lr original 0.001
GAMMA = 0.9  # ! probar con valores entre 0.8 y 0.9
HIDDE_NET_SIZE = 256  # ! probar con otro numero del centro


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SGNN()
    while True:
        # old state
        old_state = agent.get_state(game)

        # move
        finale_move = agent.get_action(old_state)

        # move and get new state
        reward, game_over, score = game.play_step(finale_move)
        new_state = agent.get_state(game)

        # train short memory
        agent.train_short_memory(
            old_state, finale_move, reward, new_state, game_over)

        # remember
        agent.remember(old_state, finale_move, reward, new_state, game_over)

        if game_over:
            # train long memory and plot results
            game.reset()
            agent.number_of_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game: ', agent.number_of_games,
                  ' Score: ', score, ' Best: ', record)

            plot_scores.append(score)
            total_score += score
            plot_mean_scores.append(total_score / agent.number_of_games)
            plot(plot_scores, plot_mean_scores)


class Agent:
    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0  # to control de randomness
        # the discount rate smaller than 1 (around 0.8 or 0.9)
        self.gamma = GAMMA
        self.memory = deque(maxlen=MAX_MEMORY)  # the memory
        # model and trainer
        # 11 because we have 11 states and 3 because we have 3 actions, the hidden can be change
        self.model = Linear_Qnet(11, HIDDE_NET_SIZE, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=GAMMA)

    def get_state(self, game):
        head = game.snake[0]
        left_point = Point(head.x - 20, head.y)
        right_point = Point(head.x + 20, head.y)
        upper_point = Point(head.x, head.y - 20)
        down_point = Point(head.x, head.y + 20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Check if there is a "collision" straight ahead (danger)
            (dir_r and game.is_collision(right_point)) or
            (dir_l and game.is_collision(left_point)) or
            (dir_u and game.is_collision(upper_point)) or
            (dir_d and game.is_collision(down_point)),

            # Check if there is a "collision" on the right direction ahead (danger)
            (dir_u and game.is_collision(right_point)) or
            (dir_d and game.is_collision(left_point)) or
            (dir_l and game.is_collision(upper_point)) or
            (dir_r and game.is_collision(down_point)),

            # Check if there is a "collision" left direction ahead (danger)
            (dir_d and game.is_collision(right_point)) or
            (dir_u and game.is_collision(left_point)) or
            (dir_r and game.is_collision(upper_point)) or
            (dir_l and game.is_collision(down_point)),

            # direction to move
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # gold location
            game.food.x < game.head.x,  # gold left
            game.food.x > game.head.x,  # gold right
            game.food.y < game.head.y,  # gold up
            game.food.y > game.head.y  # gold down
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards,
                                next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        # for start ramdom moves (exploration / exploitation)
        self.epsilon = 80 - self.number_of_games  # cahnge 80
        final_move = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
        else:
            state_initial = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state_initial)
            move = torch.argmax(prediction).item()
        final_move[move] = 1
        return final_move


if __name__ == '__main__':
    train()
