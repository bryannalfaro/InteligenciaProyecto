# -*- coding: utf-8 -*-

from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import random


sizeOfSquare = 10


class board:
    def __init__(self):
        intPosition = -2
        self.squares = []
        self.score = 0
        for x in range(0, 50):
            intPosition = intPosition + 1
            for y in range(0, 50):
                intPosition = intPosition + 1
                self.squares.append(square(x*sizeOfSquare, y*sizeOfSquare,
                                           "WHITE", intPosition))

    def getSquare(self, squareNumber):
        squareHere = self.squares[squareNumber]
        return squareHere

    def addScore(self):
        self.score = self.score + 1


class snake:
    def __init__(self, head, tail, direction):
        self.head = head  # use this to find the next square
        # use this to store all the squares that currently make
        self.body = [self.head]
        # up the snake
        self.tail = tail  # use this to reset squares to white
        self.direction = direction

    def setDirection(self, direction):
        self.direction = direction

    def updateSnake(self, point):
        newHead = 1225
        #newHead = None
        self.tail = self.body[-1]
        eaten = False
        if self.direction == "UP":
            if self.body[0] - 1 == point:
                self.body.insert(0, point)
                eaten = True
            else:
                newHead = self.body[0] - 1
        if self.direction == "DOWN":
            if self.body[0] + 1 == point:
                self.body.insert(0, point)
                eaten = True
            else:
                newHead = self.body[0] + 1
        if self.direction == "LEFT":
            if self.body[0] - 50 == point:
                self.body.insert(0, point)
                eaten = True
            else:
                newHead = self.body[0] - 50
        if self.direction == "RIGHT":
            if self.body[0] + 50 == point:
                self.body.insert(0, point)
                eaten = True
            else:
                newHead = self.body[0] + 50
        if newHead <= 0:
            newHead = 2500 + newHead
        if newHead >= 2500:
            newHead = newHead - 2500

        if eaten == False:
            self.body.insert(0, newHead)
            del(self.body[-1])
        return eaten

    def checkColision(self):
        collide = False
        for bodyPart in self.body:
            if self.body[0] == bodyPart and bodyPart is not self.body[0]:
                collide = True
        return collide


class square:
    def __init__(self, x, y, colourState, intPosition):
        self.positionX = x
        self.positionY = y
        self.colourState = colourState
        self.size = sizeOfSquare
        self.intPosition = intPosition

    def getColourState(self):
        return self.colourState

    def getX(self):
        return self.positionX

    def getY(self):
        return self.positionY

    def getSize(self):
        return self.size

    def setColourState(self, colour):
        self.colourState = colour


class Agent:
    def __init__(self, initial_games=100, test_games=100, goal_steps=100, lr=1e-2,):
        self.model = self.network()
        self.initial_games = initial_games
        self.test_games = test_games
        self.goal_steps = goal_steps
        self.lr = lr
        self.filename = 'snake_nn.tflearn'

    def network(self):
        model = Sequential()
        model.add(Dense(12, input_dim=4, activation='relu'))
        model.add(Dense(1, activation='linear'))

        model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])

        return model

    def getPossibles(self, snake):
        direction = snake.direction
        eatSelfDirection = ""
        if direction == "UP":
            eatSelfDirection = "DOWN"
        if direction == "DOWN":
            eatSelfDirection = "UP"
        if direction == "LEFT":
            eatSelfDirection = "RIGHT"
        if direction == "RIGHT":
            eatSelfDirection = "LEFT"
        possibles = ["UP", "DOWN", "LEFT", "RIGHT"]
        possibles.remove(eatSelfDirection)
        return possibles

    def get_random_move(self, snake):
        direction = snake.direction
        eatSelfDirection = "UP"
        if direction == "UP":
            eatSelfDirection = "DOWN"
        if direction == "DOWN":
            eatSelfDirection = "UP"
        if direction == "LEFT":
            eatSelfDirection = "RIGHT"
        if direction == "RIGHT":
            eatSelfDirection = "LEFT"
        possibles = ["UP", "DOWN", "LEFT", "RIGHT"]
        possibles.remove(eatSelfDirection)
        index = random.randint(0, 2)
        move = possibles[index]

        return move

    def getState(self, board, snake, point):
        boardLength = 50

        snakeY = snake.body[0] // boardLength
        foodY = point // boardLength
        snakeX = snake.body[0] - (snake.body[0] // boardLength * 50)
        foodX = point - (point // boardLength * 50)

        yDif = snakeX-foodX
        xDif = snakeY-foodY
        direction = snake.direction

        xChange = 0
        yChange = 0
        if direction == "UP":
            yChange = -1
        if direction == "DOWN":
            yChange = 1
        if direction == "LEFT":
            xChange = -1
        if direction == "RIGHT":
            xChange = 1

        state = [xDif, yDif, xChange, yChange]
        return state

    def getReward(self, state, eaten):
        reward = 0
        if eaten == True:
            reward = 1000
        xDif = state[0]
        yDif = state[1]
        pyth = (np.sqrt((yDif*yDif)+(xDif*xDif)))/100
        reward = reward - pyth
        return reward

    def getDirection(self, snake, dataModel, point):
        possibles = self.getPossibles(snake)
        state = self.getState(dataModel, snake, point)
        state0 = state[0]
        state1 = state[1]
        paired = []
        predictions = []
        for move in possibles:
            xChange = 0
            yChange = 0
            if move == "UP":
                yChange = -1
            if move == "DOWN":
                yChange = 1
            if move == "LEFT":
                xChange = -1
            if move == "RIGHT":
                xChange = 1
            thisList = [state0, state1, xChange, yChange]
            X = np.array([thisList])
            pred = self.model.predict(X)
            predictions.append(pred[0][0])
            pair = [pred[0][0], move]
            paired.append(pair)

        # print(possibles)

        Max = -10000000000
        for pair in paired:
            if pair[0] > Max:
                snake.setDirection(pair[1])
                Max = pair[0]
                # print(snake.direction)

        # print(paired)
        # print("-------------------------")
        #print("SNAKE:", snake.direction)

    def getDirections(self, snake, dataModel, point):
        possibles = self.getPossibles(snake)
        state = self.getState(dataModel, snake, point)
        state0 = state[0]
        state1 = state[1]
        paired = []
        predictions = []
        for move in possibles:
            xChange = 0
            yChange = 0
            if move == "UP":
                yChange = -1
            if move == "DOWN":
                yChange = 1
            if move == "LEFT":
                xChange = -1
            if move == "RIGHT":
                xChange = 1
            thisList = [state0, state1, xChange, yChange]
            X = np.array([thisList])
            pred = self.model.predict(X)
            predictions.append(pred[0][0])
            pair = [pred[0][0], move]
            paired.append(pair)

        # print(possibles)

        Max = -10000000000
        for pair in paired:
            if pair[0] > Max:
                snake.setDirection(pair[1])
                Max = pair[0]
                # print(snake.direction)

        # print(paired)
        # print("-------------------------")
        #print("SNAKE:", snake.direction)

    def train_model(self, training_data):

        X = np.array([i[0:4] for i in training_data])
        y = np.array([i[4] for i in training_data])
        self.model.fit(X, y)
        # self.model.save(self.filename)
