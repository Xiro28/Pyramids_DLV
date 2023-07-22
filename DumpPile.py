
class DPManager:
 
    def __init__(self, cm, pc):
        self.dumpPile = list()
        self.cm = cm
        self.pc = pc

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

            if not card1.isKing():
                card2 = self.dumpPile.pop()
                self.__addToDeck(card2)

            self.__addToDeck(card1)