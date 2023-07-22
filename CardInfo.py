class CardInfo:
    def __init__(self, cardType = -1, cardClass = -1, cardValue = -1, cardLevel = -1, cardImage = None, cardRect = None, pileCard = False):
        self.cardType = cardType
        self.cardClass = cardClass
        self.cardValue = cardValue
        self.cardLevel = cardLevel
        self.cardImage = cardImage
        self.cardRect = cardRect
        self.pileCard = pileCard
        self.enabled = False
        self.pIndex = -1

    def setEnabled(self, enabled):
        self.enabled = enabled

    def setIndex(self, index):
        self.pIndex = index

    def getIndex(self):
        return self.pIndex

    def isPileCard(self):
        return self.pileCard
    
    def setPileCard(self, pileCard):
        self.pileCard = pileCard

    def getCardType(self):
        return self.cardType
    
    def getCardClass(self):
        return self.cardClass
    
    def getCardValue(self):
        return self.cardValue
    
    def getCardImage(self):
        return self.cardImage

    def getCardRect(self):
        return self.cardRect
    
    def getLevel(self):
        return self.cardLevel
    
    def setCardRect(self, cardRect):
        self.cardRect.x = cardRect[0]
        self.cardRect.y = cardRect[1]

    def isKing(self):
        return self.cardValue == 13
    
    def checkSum(self, card1):
        return (self.cardValue + card1.getCardValue()) == 13
    
    def highlightCard(self):
        pass
    