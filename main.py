import sys
from AI.player import Player
from AudioManager import AudioManager

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

def removeCards(card1, card2 = None):

    global pc
    global cm
    global dp

    if card1 == None and card2 == None:
        return

    dp.dumpCard(card1)

    AudioManager.playCard()

    if card1.isPileCard():
        pc.removeCard(card1)
    else:
        cm.removeCard(card1)

    if card2 != None:
        dp.dumpCard(card2)

        AudioManager.playCard()

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
    gpm.drawFooter(True)
    
#TODO AI mode
#TODO Timed mode ?

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


def aiLoopNoRicerca():

    PILE_CARD_ID = 999
    clearFlag = True

    global cm
    global pc
    global dp
    global gpm
    global gameModes

    while 1:
        gpm.getEvent()

        if gpm.getEventQuit():
            sys.exit()

        if clearFlag:
            clearScreen()
            clearFlag = False

        if gpm.getCollisionRect(gpm.menuTexture_rect):
            reset()
            GM.reset()
            clearFlag = True
            break
        elif gpm.getCollisionRect(gpm.resetTexture_rect):
            reset()
            GM.reset()
            clearFlag = True

        for card in cm.getCardsPLevels():
            Player.addCard(card.getLevel(), card.getIndex(), card.getCardValue())

        if pc.getCurrentPileCard() != None:
            Player.addPileCard(pc.getCurrentPileCard().getCardValue())

        actions = Player.get_next_actionsOptimal()

        gpm.highlightSuggestedCards(Helper.findSumBetweenCards(cm.getCardsPLevels(), pc.getCurrentPileCard()))

        #limit to one 
        for action in actions:
            if "dumpKing" in action:
                card_id = int(action.split("(")[1].split(")")[0])
                card =  None

                if card_id != PILE_CARD_ID:
                    card = cm.getCardByID(card_id)
                else:
                    card = pc.getCurrentPileCard()

                GM.addPoints(100)

                removeCards(card)
                clearFlag = True
                pass

            elif "dump" in action:
                card1_id = int(action.split("(")[1].split(",")[0])
                card2_id = int(action.split(",")[1].split(")")[0])

                card1 = None
                card2 = None

                

                if card1_id == PILE_CARD_ID:
                    card1 = pc.getCurrentPileCard()
                else:
                    card1 = cm.getCardByID(int(card1_id))
                    
                if card2_id == PILE_CARD_ID:
                    card2 = pc.getCurrentPileCard()
                else:
                    card2 = cm.getCardByID(int(card2_id))
                
                GM.addPoints(200)
                removeCards(card1, card2)
                clearFlag = True
            elif action == "nextCardPile":
                pc.getNextPileCard()
                clearFlag = True

            AudioManager.playCard()

            if cm.getWinState():
                clearScreen()
                reset()
                GM.addWin()
                GM.addGame()
                gpm.drawScreen("Table Cleared!", True)
            elif pc.pileFinished and Helper.checkGameOver(cm.getCardsPLevels(), [pc.getCurrentPileCard()]):
                clearScreen()
                reset()
                GM.addGame()
                GM.addLose()
                GM.reset(False)
                gpm.drawScreen("  Game Over!", True)

    return False



#forse voglio complicarmi un po la vita ma ci provo lo stesso

#problema: siccome le probabilità di vincita sono statisticamente basse
#cerchiamo di massimizzarle implementando un algoritmo di ricerca
#per trovare la soluzione migliore.

#quindi prendiamo tutti gli answer set anche se non sono ottimali per quel stato in cui si trova il gioco
#Meglio termiare il gioco con qualche mossa in piu che finire in game over...

#possibile soluzione: far iterare l'algoritmo fino a quando si trova in una situazione di stallo
#una volta qui eliminiamo tutte le mosse eseguite e riporviamo prendendo decisioni diverse.
#se anche prendendo decisioni diverse ci troviamo davanti una situazione di stallo, a questo punto 
#la piramide è irrisolvibile e quindi siamo in game over
#altrimenti WIN

#La struttura dati formata dovrebbe essere quella di un albero (:D)

#la classe player attraverso la funzione get_next_actions ci torna una lista di answer set
#inseriamo cosi tutti gli answer set in una lista e li iteriamo uno alla volta

#RES: Non ne vale la pena, la versione senza ricerca è piu veloce e non ci sono differenze sostanziali
#     tra le due versioni. Rimane qui solo per dimostrare che effettivamente c'ho provato.
#     va anche sistemato perchè nl tentativo di ottimizzare il codice ho fatto un po di casino

stackActions = []

def aiLoop(action_todo = None, _id = 0):

    PILE_CARD_ID = 999
    clearFlag = True

    global cm
    global pc
    global dp
    global gpm
    global stackActions
    global gameModes


    while 1:
        gpm.getEvent()

        if gpm.getEventQuit():
            sys.exit()

        if clearFlag:
            clearScreen()
            clearFlag = False

        if gpm.getCollisionRect(gpm.menuTexture_rect):
            reset()
            GM.reset()
            clearFlag = True
            break
        elif gpm.getCollisionRect(gpm.resetTexture_rect):
            reset()
            GM.reset()
            clearFlag = True


        if action_todo == None:

            for card in cm.getCardsPLevels():
                Player.addCard(card.getLevel(), card.getIndex(), card.getCardValue())

            if pc.getCurrentPileCard() != None:
                Player.addPileCard(pc.getCurrentPileCard().getCardValue())

            actions = Player.get_next_actions()

            actions = actions[0].get_answer_set()

            stackActions.append(actions)

            while len(stackActions[_id]) > 0:
                action = stackActions[_id].pop()
                old_dp_len = dp.getNumDumpPile() 

                aiLoop(action, _id)

                for _ in range(dp.getNumDumpPile() - old_dp_len):
                    dp.restoreLastMove()

            if id == 0 and pc.pileFinished and Helper.checkGameOver(cm.getCardsPLevels(), [pc.getCurrentPileCard()]):
                clearScreen()
                goBackMenu = gpm.drawScreen("  Game Over!")
                reset()
                GM.reset()
                if goBackMenu:
                    return True

        else:

            action = action_todo

            gpm.highlightSuggestedCards(Helper.findSumBetweenCards(cm.getCardsPLevels(), pc.getCurrentPileCard()))

            #limit to one 
            #for action in actions:
            #action = actions[0]
            if "dumpKing" in action:
                card_id = int(action.split("(")[1].split(")")[0])
                card =  None

                if card_id != PILE_CARD_ID:
                    card = cm.getCardByID(card_id)
                else:
                    card = pc.getCurrentPileCard()

                removeCards(card)
                clearFlag = True
                pass

            elif "dump" in action:
                card1_id = int(action.split("(")[1].split(",")[0])
                card2_id = int(action.split(",")[1].split(")")[0])

                card1 = None
                card2 = None

                if card1_id == PILE_CARD_ID:
                    card1 = pc.getCurrentPileCard()
                else:
                    card1 = cm.getCardByID(int(card1_id))
                    
                if card2_id == PILE_CARD_ID:
                    card2 = pc.getCurrentPileCard()
                else:
                    card2 = cm.getCardByID(int(card2_id))
                
                removeCards(card1, card2)
                clearFlag = True
            elif action == "nextCardPile":
                pc.getNextPileCard()
                clearFlag = True

            if cm.getWinState():
                if gameModes[0]():
                    return True
            elif pc.pileFinished and Helper.checkGameOver(cm.getCardsPLevels(), [pc.getCurrentPileCard()]):
                print ("Curr_State: Game Over")
                return True
            
            aiLoop(None, _id + 1)

    return False

if __name__ == '__main__':
    
    gpm.initGraphics()

    AudioManager.init()
    AudioManager.playBackground()

    cm = CM()
    pc = PileCards(cm)

    dp = DPManager(cm, pc)


    clearFlag = True

    while 1:
        selected = gpm.drawMenu()

        #option selected
        while selected == 3:
            gpm.drawOptions()
            selected = gpm.drawMenu()

        GM.reset()

        #AI selected
        if selected == 2:
            Player.init()

            if aiLoopNoRicerca():
                continue

        else:
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
                elif pc.pileFinished and Helper.checkGameOver(cm.getCardsPLevels(), [pc.getCurrentPileCard()]):
                    clearScreen()
                    goBackMenu = gpm.drawScreen("  Game Over!")
                    reset()
                    GM.reset()
                    if goBackMenu:
                        break

        


        
