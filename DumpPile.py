
from GameManager import GM


class DPManager:
 
    def __init__(self, cm, pc):
        self.cm = cm
        self.pc = pc
        self.reset()

    def reset(self):
        self.dumpPile = list()

    def getDumpPile(self):
        return self.dumpPile
    
    def getNumDumpPile(self):
        return len(self.dumpPile)
    
    def dumpCard(self, card):
        self.dumpPile.append(card)

    def __addToDeck(self, card):
        if card.isPileCard():
            self.pc.addCard(card)
        else:
            self.cm.addCard(card)
            

    def restoreLastMove(self):
        if len(self.dumpPile) > 0:
            card1 = self.dumpPile.pop()

            GM.addPoints(-105)

            if not card1.isKing():
                card2 = self.dumpPile.pop()
                self.__addToDeck(card2)

                GM.addPoints(-105)

            self.__addToDeck(card1)