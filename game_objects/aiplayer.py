import pygame
import numpy as np
from pygame.locals import *
from sklearn.externals import joblib
from keras.models import load_model
from game_objects.player import Player
from game_objects.mlp_model import MLP_model


class AIPlayer(Player):
    def __init__(self, name, screen, screen_height, screen_width):
        Player.__init__(self, name, screen, screen_height, screen_width)
        self.predictive_model = joblib.load('ElasticNet.pkl')
        self.y_mean = joblib.load('ymean.pkl')
        self.x_mean = joblib.load('x_mean.pkl')

    def scoring(self):
        scoreBlit = self.scoreFont.render(str(self.score),
                                          1, (255, 255, 255))
        if self.name == "player1":
            self.screen.blit(scoreBlit, (32, 16))
            if self.score == 5:
                print ("player 1 wins!")
                exit()
        elif self.name == "player2":
            self.screen.blit(scoreBlit, (self.SCR_HEI + 92, 16))
            if self.score == 5:
                print ("Player 2 wins!")
                exit()

    def movement(self, screen_np):
        if screen_np is not None:
            model = self.predictive_model
            centered_data = (screen_np - self.x_mean).reshape(1, -1)
            prediction = model.predict(centered_data)
            print("centered", centered_data.mean())
            self.y = prediction + self.y_mean
            print(self.y)


class MLPlayer(Player):
    def __init__(self, name, screen, screen_height, screen_width):
        Player.__init__(self, name, screen, screen_height, screen_width)
        self.predictive_model = MLP_model
        self.y_mean = joblib.load('ymean.pkl')
        self.x_mean = joblib.load('x_mean.pkl')

    def scoring(self):
        scoreBlit = self.scoreFont.render(str(self.score),
                                          1, (255, 255, 255))
        if self.name == "player1":
            self.screen.blit(scoreBlit, (32, 16))
            if self.score == 5:
                print ("player 1 wins!")
                exit()
        elif self.name == "player2":
            self.screen.blit(scoreBlit, (self.SCR_HEI + 92, 16))
            if self.score == 5:
                print ("Player 2 wins!")
                exit()

    def movement(self, screen_np):
        if screen_np is not None:
            model = self.predictive_model
            centered_data = (screen_np - self.x_mean)
            prediction = model.predict(centered_data)
            self.y = prediction + self.y_mean
            print("predicted pos ",  self.y)


class Conv2DPlayer(Player):
    def __init__(self, name, screen, screen_height, screen_width):
        Player.__init__(self, name, screen, screen_height, screen_width)
        self.predictive_model = load_model('pong_conv2d.h5')
        self.y_mean = joblib.load('ymean.pkl')
        self.x_mean = joblib.load('x_mean.pkl')

    def scoring(self):
        scoreBlit = self.scoreFont.render(str(self.score),
                                          1, (255, 255, 255))
        if self.name == "player1":
            self.screen.blit(scoreBlit, (32, 16))
            if self.score == 5:
                print ("player 1 wins!")
                exit()
        elif self.name == "player2":
            self.screen.blit(scoreBlit, (self.SCR_HEI + 92, 16))
            if self.score == 5:
                print ("Player 2 wins!")
                exit()

    def movement(self, screen_np):
        if screen_np is not None:
            centered_data = (screen_np - self.x_mean)
            centered_data = np.reshape(centered_data, (1, 400, 400, 1))
            model = self.predictive_model
            prediction = model.predict(centered_data)
            self.y = prediction + self.y_mean
            print("predicted pos ",  self.y)
