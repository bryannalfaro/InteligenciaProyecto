import torch
import torch.optim as optim
import torch.nn.functional as F
import torch.nn as nn
import os
import numpy as np


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        # ! usar otro optimizador
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, move, reward, next_state, game_over):
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        move = torch.tensor(move, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            move = torch.unsqueeze(move, 0)
            reward = torch.unsqueeze(reward, 0)
            game_over = (game_over, )

        # predictied Q values
        predicted_q_values = self.model(state)

        # Q new = r + y * max(next predicted Q value)
        target = predicted_q_values.clone()
        for index in range(len(game_over)):
            Q_new = reward[index]
            if not game_over[index]:
                Q_new = reward[index] + self.gamma * \
                    torch.max(self.model(next_state[index]))

            target[index][torch.argmax(move[index]).item()] = Q_new

        # Q_new = r + y * max(next_predicted Q value) -> only do this if not game_over
        self.optimizer.zero_grad()
        loss = self.criterion(target, predicted_q_values)
        loss.backward()

        self.optimizer.step()


class Linear_Qnet(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = F.relu(self.linear1(x))
        x = self.linear2(x)
        return x

    def save(self, file_name='model.pth'):
        location = './NN/model'
        if not os.path.exists(location):
            os.makedirs(location)

        # location lo load the model
        file_name = os.path.join(location, file_name)

        # save with torch
        torch.save(self.state_dict(), file_name)
