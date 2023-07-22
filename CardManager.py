import random
import itertools

from RenderingManager import GPManager as gpm
from CardInfo import CardInfo

class CM:
    CARD_WIDTH = 100
    CARD_HEIGHT = 150

    CARDS_TYPE = ["spades", "hearts", "diamonds", "clubs"]
    CARDS_VALUE = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]
    CARD_INTVALUE = [1,2,3,4,5,6,7,8,9,10,11,12,13]

    GAME_STARTLEVEL = 6

    def __init__(self):

        self.cards_p_levels = list()
        self.cards_enabled = list()
        self.cards_pile = list()

        self.level = CM.GAME_STARTLEVEL
        self.cards = list(itertools.product([0, 1, 2, 3], CM.CARD_INTVALUE))


        random.shuffle(self.cards)
       
        self.___buildDeck()
        self.___assingCardPos()

    def getPileCard(self):
        return self.cards_pile
    
    def getCardsPLevels(self, all = False):
        
        if all:
            return self.cards_p_levels
        else:
            self.UpdateEnabled()

            return self.cards_enabled
    
    def loadDeckCard(self):
        texture = gpm.loadTexture(path = "textures/png/back.jpg", resize = (CM.CARD_WIDTH, CM.CARD_HEIGHT))
        texture_rect = texture.get_rect()
        texture_rect.x = 10
        texture_rect.y = 10
        return CardInfo(cardImage=texture, cardRect=texture_rect)
    
    def loadDumpCard(self):
        texture = gpm.loadTexture(path = "textures/png/back.jpg", resize = (CM.CARD_WIDTH, CM.CARD_HEIGHT))
        texture_rect = texture.get_rect()
        texture_rect.x = CM.CARD_WIDTH * 8 + CM.CARD_WIDTH//2
        texture_rect.y = 10
        return CardInfo(cardImage=texture, cardRect=texture_rect)

    def loadCardByID(self, type, value, level):
        card_type = CM.CARDS_TYPE[type % 4]
        card_value = CM.CARDS_VALUE[value % 13]
        texture = gpm.loadTexture(path = "textures/png/" + card_value + "_of_" + card_type + ".png", resize = (CM.CARD_WIDTH, CM.CARD_HEIGHT))
        texture_rect = texture.get_rect()
        return CardInfo(card_type, card_value, self.getCardValue(value), level, texture, texture_rect)
    
    def getCardValue(self, value):
        return CM.CARD_INTVALUE[value % 13]
    
    def UpdateEnabled(self):
        self.cards_enabled = list()

        for curr_level in range(CM.GAME_STARTLEVEL):
            cards = self.cards_p_levels[curr_level]
            cards_next_level = self.cards_p_levels[curr_level+1]

            for i in range(len(cards)):

                if cards[i] == None:
                    continue

                if cards_next_level[i] == None and cards_next_level[i+1] == None:
                    self.cards_enabled.append(cards[i])
                    cards[i].setEnabled(True)
                else:
                    cards[i].setEnabled(False)

        #last level always true
        for card in self.cards_p_levels[CM.GAME_STARTLEVEL]:
            if card != None:
                card.setEnabled(True)
                self.cards_enabled.append(card)

    def removeCard(self, card):
        #replace card with None
        self.cards_p_levels[card.getLevel()][card.getIndex()] = None
    
    def addCard(self, card):
        self.cards_p_levels[card.getLevel()][card.getIndex()] = card
    
    def ___buildDeck(self):
        level = 0
        nextLevel = 1

        self.cards_p_levels.append([])

        #shuffle again to have a a more random deck
        random.shuffle(self.cards[:28])

        for card_type, num in self.cards[:28]:
            self.cards_p_levels[level].append(self.loadCardByID(card_type, num, level))
            self.cards_p_levels[level][-1].setIndex(len(self.cards_p_levels[level])-1)
        
            if len(self.cards_p_levels[level]) >= nextLevel:
                self.cards_p_levels.append([])
                level += 1
                nextLevel = level+1

        
        random.shuffle(self.cards[28:])
        for card_type, num in self.cards[28:]:
            self.cards_pile.append(self.loadCardByID(card_type, num, -1))

    def ___assingCardPos(self):
        x = 0
        y = CM.CARD_HEIGHT / 2

        max_width = CM.CARD_WIDTH * 7
        for i in range(0, 7):
            starting_x = (((max_width / 2) - (len(self.cards_p_levels[i]) * CM.CARD_WIDTH) / 2) + CM.CARD_WIDTH / 2) + CM.CARD_WIDTH
            for card in self.cards_p_levels[i]:
                card.getCardRect().x = starting_x + x
                card.getCardRect().y = y
                x += CM.CARD_WIDTH
            y += CM.CARD_HEIGHT / 2
            x = 0