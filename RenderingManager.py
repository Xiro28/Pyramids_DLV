import pygame as pg

class GPManager():
    CARD_WIDTH = 100
    CARD_HEIGHT = 150

    screen = None
    moving = False

    @staticmethod
    def initGraphics():
       pg.init()
       pg.display.set_caption('Pyramids Solitaire')
       GPManager.screen = pg.display.set_mode((1280, 860), pg.SRCALPHA)
       GPManager.screen.fill((0, 128, 40, 255))

    @staticmethod
    def loadTexture(path, resize = ()):
        
        if resize == ():
            return pg.image.load(path).convert()
        
        return pg.transform.scale(pg.image.load(path).convert(),(resize[0], resize[1]))
    
    @staticmethod
    def clearScreen():
        GPManager.screen.fill((0, 128, 40, 255))

    @staticmethod
    def Update():
        pg.display.flip()

    @staticmethod
    def drawCards(cards):
        if cards == None:
            return
        
        for cards_level in cards:
            for card in cards_level:
                if card == None:
                    continue
                GPManager.screen.blit(card.getCardImage(), card.getCardRect())
        pg.display.flip()

    @staticmethod
    def highlightCard(card):
        if card == None:
            return
        
        pg.draw.rect(GPManager.screen, (80, 80, 180, 255), card.getCardRect(), 3)
        pg.display.flip()

    @staticmethod
    def getEvent():
        GPManager.event = pg.event.wait()
    
    @staticmethod
    def getEventQuit():
        return (GPManager.event.type == pg.QUIT or (GPManager.event.type == pg.KEYDOWN and GPManager.event.key in [pg.K_ESCAPE, pg.K_q]))
    
    @staticmethod
    def getCollision(card):
        if card == None:
            return False
        GPManager.moving = card.getCardRect().collidepoint(pg.mouse.get_pos()) and GPManager.event.type == pg.MOUSEBUTTONDOWN and GPManager.event.button == 1

        return GPManager.moving
    
    @staticmethod
    def getMouseUp(self, card):
        if card == None:
            return False
        return GPManager.event.type == pg.MOUSEBUTTONUP and GPManager.event.button == 1
    
    @staticmethod
    def getMouseMotion(card):
        if card == None:
            return False
        return GPManager.event.type == pg.MOUSEMOTION and GPManager.moving
    
    @staticmethod
    def moveCard(card):
        if card == None:
            return
        
        mx,my=pg.mouse.get_pos()
        card.setCardRect((mx - GPManager.CARD_WIDTH//2, my - GPManager.CARD_HEIGHT//2))