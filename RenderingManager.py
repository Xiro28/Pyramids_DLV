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
       GPManager.screen = pg.display.set_mode((1024, 860), pg.SRCALPHA)
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
    def highlightSuggestedCards(cards):
        if cards == None:
            return
        
        #red, green violet, blue, yellow, orange, white, black, brown, pink, gray, purple, cyan
        colors = [(255,0,0,255), (0,255,0,255), (238,130,238,255),  \
                  (0,0,255,255), (255,255,0,255), (255,165,0,255),  \
                  (255,255,255,255), (0,0,0,255), (165,42,42,255),  \
                  (255,192,203,255), (128,128,128,255), (128,0,128,255), (0,255,255,255)]
        
        idx_c = 0
        for card in cards:
            if card == None:
                continue
            c1, c2 = card
            pg.draw.rect(GPManager.screen, colors[idx_c], c1.getCardRect(), 3)
            
            if c2 != None:
                pg.draw.rect(GPManager.screen, colors[idx_c], c2.getCardRect(), 3)
            idx_c += 1
            
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