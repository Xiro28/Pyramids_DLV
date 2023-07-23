import sys

from CardManager import CM
from GameManager import GM
from DumpPile import DPManager
from Helper import Helper
from PileCards import PileCards
from RenderingManager import GPManager as gpm

cm = None
pc = None
dp = None


def removeCards(card1, card2 = None):

    global pc
    global cm
    global dp

    dp.dumpCard(card1)

    if card1.isPileCard():
        pc.removeCard(card1)
    else:
        cm.removeCard(card1)

    if card2 != None:
        dp.dumpCard(card2)

        if card2.isPileCard():
            pc.removeCard(card2)
        else:
            cm.removeCard(card2)


def clearScreen():
    global cm
    global pc
    global dp

    cardsToDraw = cm.getCardsPLevels(True).copy()

    cardsToDraw.append([pc.getBackCard()])

    gpm.clearScreen()

    if dp.getNumDumpPile() > 0:
        cardsToDraw.append([pc.getDumpCard()])

    if pc.getCurrentPileCard() != None:
        cardsToDraw.append([pc.getCurrentPileCard()])

    gpm.drawCards(cardsToDraw)
    gpm.drawFooter()
    


#pensa una soluzione stile iteratore
#quando arrivi a 2 carte controlli la loro somma e le rimuovi in caso sia positivo == 13
cardToCheck = []

def addNumberToSum(card):
    global cardToCheck
    global clearFlag

    gpm.highlightCard(card)

    if card.isKing():
        GM.addPoints(100)
        removeCards(card)
        clearFlag = True
        return

    if len(cardToCheck) > 0 and cardToCheck[0] == card:
        cardToCheck = []
        clearFlag = True
        return

    cardToCheck.append(card)
    if len(cardToCheck) == 2:
        if cardToCheck[0].checkSum(cardToCheck[1]):
            GM.addPoints(200)
            removeCards(cardToCheck[0], cardToCheck[1])
        clearFlag = True
        cardToCheck = []

def reset():
    global cm
    global pc
    global dp
    global cardToCheck

    cardToCheck = []

    cm.reset()
    pc.reset()
    dp.reset()


if __name__ == '__main__':
    
    gpm.initGraphics()

    cm = CM()
    pc = PileCards(cm)

    dp = DPManager(cm, pc)

    clearFlag = True

    def modeEndless():
        reset()

    def modeTimed():
        #show win screen and go back to main menu
        pass

    def modeSingle():
        #show win screen and go back to main menu
        clearScreen()
        retVal = gpm.drawScreen("Win")
        reset()
        GM.reset()
        if retVal == 1:
            gpm.drawMenu()


    gameModes = [modeSingle, modeEndless, modeTimed]

    gMode = gpm.drawMenu()

    GM.reset()

    while 1:
        gpm.getEvent()

        if gpm.getEventQuit():
            sys.exit()

        if clearFlag:
            clearScreen()
            clearFlag = False

        currPileCard = pc.getCurrentPileCard()

        if gpm.getCollisionRect(gpm.resetTexture.get_rect()):
            reset()
            GM.reset()
            clearFlag = True
        if gpm.getCollision(pc.getDumpCard()):
            dp.restoreLastMove()
            clearFlag = True
        elif currPileCard != None and gpm.getCollision(currPileCard):
            addNumberToSum(currPileCard)
        elif gpm.getCollision(pc.getBackCard()):
            pc.getNextPileCard()
            clearFlag = True
        else:
            for card in cm.getCardsPLevels():
                if gpm.getCollision(card):
                    addNumberToSum(card)
                    break

        gpm.highlightSuggestedCards(Helper.findSumBetweenCards(cm.getCardsPLevels(), pc.getCurrentPileCard()))

        GM.scheduleAtFixedOne(gpm.drawFooter)

        if cm.getWinState():
            gameModes[gMode]()

        


        
