import pygame as pg
import os

class AudioManager():

    @staticmethod
    def init():
        pg.mixer.init()

        pg.mixer.set_num_channels(4)

        AudioManager.background = pg.mixer.Sound(os.path.join("./music/", "background.mp3"))
        AudioManager.card       = pg.mixer.Sound(os.path.join("./music/", "card.wav"))

        AudioManager.channel1 = pg.mixer.Channel(0)
        AudioManager.channel2 = pg.mixer.Channel(1)

        
    @staticmethod
    def playBackground():
        AudioManager.channel1.play(AudioManager.background, -1)

    @staticmethod
    def playCard():
        AudioManager.channel2.play(AudioManager.card)