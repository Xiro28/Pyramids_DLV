import random
from GameManager import GM
from Option import Options


class PileCards:
    def __init__(self, cm):
        self.cm = cm
        self.reset()
    
    def reset(self):
        self.card_pile_obj = self.cm.getPileCard()
        self.next_p = -1

        self.resetted = 0

        self.removed = True
        self.pileFinished = False

        self.backCard = self.cm.loadDeckCard()
        self.dumpCard = self.cm.loadDumpCard()

        self.___assingCardPos()

    def ___assingCardPos(self):
        for card in self.card_pile_obj:
            card.setCardRect((150, 40))
            card.setPileCard(True)
    
    def getDumpCard(self):
        return self.dumpCard

    def getBackCard(self):
        #TODO cambiare texture quando le carte terminano
        if self.pileFinished:
            return None
        
        return self.backCard 

    def getNextPileCard(self):

        if not self.pileFinished: 
            self.next_p += 1
            self.removed = False

            GM.addMove()

        if (self.next_p >= (len(self.card_pile_obj) - 1)):
            reload_times = Options.getOption("reload")
            self.resetted += 1
            
            if self.resetted > reload_times and reload_times != -1:
                self.pileFinished = True
                return self.card_pile_obj[self.next_p]
            
            do_shuffle = Options.getOption("shuffle")
            self.next_p = -1

            #shuffle cards, alcune regole dicono che si puo' mescolare solo 2 volte
            if do_shuffle:
                random.shuffle(self.card_pile_obj)
            
        return self.card_pile_obj[self.next_p % len(self.card_pile_obj)] 
    
    def canDrawPileCard(self):
        return self.next_p > -1
    
    def getCards(self):
        return self.card_pile_obj

    def getCurrentPileCard(self):

        if self.next_p == -1:
            return None

        if self.removed:
            self.next_p -= 1
            self.removed = False

            if self.next_p < -1:
                self.next_p = -1

            self.card_pile_obj[self.next_p % len(self.card_pile_obj)]
        
        return self.card_pile_obj[self.next_p % len(self.card_pile_obj)]
    
    def removeCard(self, card):
        self.removed = True
        self.card_pile_obj.remove(card)

    def addCard(self, card):
        self.card_pile_obj.append(card)
       