class PileCards:
    def __init__(self, cm):
        self.cm = cm
        self.reset()
    
    def reset(self):
        self.card_pile_obj = self.cm.getPileCard()
        self.next_p = -1

        self.resetted = 0

        self.removed = True

        self.backCard = self.cm.loadDeckCard()
        self.dumpCard = self.cm.loadDumpCard()

        self.___assingCardPos()

    def ___assingCardPos(self):
        for card in self.card_pile_obj:
            card.setCardRect((140, 10))
            card.setPileCard(True)
    
    def getDumpCard(self):
        return self.dumpCard

    def getBackCard(self):
        #TODO cambiare texture quando le carte terminano
        return  self.backCard 

    def getNextPileCard(self):
        if (self.next_p % len(self.card_pile_obj)) == 0:
            self.resetted += 1

            if self.resetted == 3:
                print("Game Over")

        self.next_p += 1
        self.removed = False
        return self.card_pile_obj[self.next_p % len(self.card_pile_obj)] 

    def getCurrentPileCard(self):
        if self.removed:
            return None
        
        return self.card_pile_obj[self.next_p % len(self.card_pile_obj)]
    
    def removeCard(self, card):
        self.removed = True
        self.card_pile_obj.remove(card)

    def addCard(self, card):
        self.card_pile_obj.append(card)
       