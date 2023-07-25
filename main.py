import sys

from CardManager import CM
from GameManager import GM
from DumpPile import DPManager
from Helper import Helper
from Option import Options
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

    gpm.clearScreen()

    cardsToDraw = cm.getCardsPLevels(True).copy()

    if pc.getBackCard() != None:
        rect = pc.getBackCard().getCardRect().copy()
        rect.x -= 10
        rect.y -= 10
        gpm.drawRectSurround(rect)
        cardsToDraw.append([pc.getBackCard()])

    if dp.getNumDumpPile() > 0:
        rect = pc.getDumpCard().getCardRect().copy()
        rect.x += 10
        rect.y += 10
        gpm.drawRectSurround(rect)
        cardsToDraw.append([(dp.dumpPile[-1], pc.getDumpCard().getCardRect())])

    if pc.canDrawPileCard():
        cardsToDraw.append([pc.getCurrentPileCard()])

    gpm.drawCards(cardsToDraw, GM.getElapsedTime() < 1)
    gpm.drawFooter()
    
#TODO AI mode

#TODO Timed mode ?
#TODO Animations ?

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
        GM.addGame()
        reset()

    def modeTimed():
        #show win screen and go back to main menu
        pass

    def modeSingle():
        #show win screen and go back to main menu
        clearScreen()
        retVal = gpm.drawScreen("Table cleared!")
        reset()
        GM.reset(False)
        if retVal != 1:
            GM.addGame()
            return False
        return True


    gameModes = [modeSingle, modeEndless, modeTimed]

    while 1:
        selected = gpm.drawMenu()

        #option selected
        while selected == 3:
            gpm.drawOptions()
            selected = gpm.drawMenu()

        GM.reset()

        #AI selected
        if selected == 2:
            pass

        while 1:
            gpm.getEvent()

            if gpm.getEventQuit():
                sys.exit()

            if clearFlag:
                clearScreen()
                clearFlag = False

            currPileCard = pc.getCurrentPileCard()
            if gpm.getCollisionRect(gpm.menuTexture_rect):
                reset()
                GM.reset()
                clearFlag = True
                break
            elif gpm.getCollisionRect(gpm.resetTexture_rect):
                reset()
                GM.reset()
                clearFlag = True
            elif gpm.getCollision(pc.getDumpCard()):
                dp.restoreLastMove()
                clearFlag = True
            elif pc.canDrawPileCard() and gpm.getCollision(currPileCard):
                addNumberToSum(currPileCard)
            elif gpm.getCollision(pc.getBackCard()):
                pc.getNextPileCard()
                clearFlag = True
            else:
                for card in cm.getCardsPLevels():
                    if gpm.getCollision(card):
                        addNumberToSum(card)
                        break

            if Options.getOption("hint"):
                gpm.highlightSuggestedCards(Helper.findSumBetweenCards(cm.getCardsPLevels(), pc.getCurrentPileCard()))

            GM.scheduleAtFixedOne(gpm.drawFooter)

            if cm.getWinState():
                if gameModes[selected]():
                    break
            elif pc.pileFinished and Helper.checkGameOver(cm.getCardsPLevels(), pc.getCards()):
                clearScreen()
                gpm.drawScreen("  Game Over!")
                reset()
                GM.reset()
                break

        


        
