import pygame as pg

from GameManager import GM

class GPManager():
    CARD_WIDTH = 110
    CARD_HEIGHT = 155

    screen = None
    font = None
    moving = False

    resetTexture = None

    @staticmethod
    def initGraphics():
       pg.init()
       pg.display.set_caption('Pyramids Solitaire')
       GPManager.screen = pg.display.set_mode((1100, 860), pg.SRCALPHA)
       GPManager.font = pg.font.Font(None, 36)
       GPManager.Titlefont = pg.font.Font(None, 100)

       GPManager.resetTexture = GPManager.loadTexture(path = "textures/png/restart.png", resize = (40, 40))

    @staticmethod
    def loadTexture(path, resize = ()):
        
        if resize == ():
            return pg.image.load(path).convert_alpha()
        
        return pg.transform.scale(pg.image.load(path).convert_alpha(),(resize[0], resize[1]))
    
    @staticmethod
    def clearScreen():
        GPManager.screen.fill((0, 100, 40, 255))

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
                pg.draw.rect(GPManager.screen, (255, 255, 255, 0), card.getCardRect(), border_radius=7)
                GPManager.screen.blit(card.getCardImage(), card.getCardRect(), special_flags=pg.BLEND_RGBA_MIN)

        pg.display.flip()

    @staticmethod
    def highlightCard(card):
        if card == None:
            return
        
        pg.draw.rect(GPManager.screen, (80, 80, 160, 255), card.getCardRect(), 4, border_radius=7)
        pg.display.flip()

    def __renderTitle(text, pos, color):
        text = GPManager.Titlefont.render(text, True, color)
        GPManager.screen.blit(text, pos)

    def __renderText(text, pos, color):
        text = GPManager.font.render(text, True, color)
        GPManager.screen.blit(text, pos)

    @staticmethod
    def highlightSuggestedCards(cards):
        if cards == None:
            return
        
        #red, green violet, blue, yellow, orange, white, black, brown, pink, gray, purple, cyan
        #colors = [(255,0,0,255), (0,255,0,255), (238,130,238,255),  \
        #          (0,0,255,255), (255,255,0,255), (255,165,0,255),  \
        #          (255,255,255,255), (0,0,0,255), (165,42,42,255),  \
        #          (255,192,203,255), (128,128,128,255), (128,0,128,255), (0,255,255,255)]

        colors = [(128,0,200,255)]
        
        idx_c = 0
        for card in cards:
            if card == None:
                continue
            c1, c2 = card
            pg.draw.rect(GPManager.screen, colors[idx_c], c1.getCardRect(), 3, border_radius=7)

            if c2 != None:
                pg.draw.rect(GPManager.screen, colors[idx_c], c2.getCardRect(), 3, border_radius=7)
            idx_c += 1
            
        pg.display.flip()

    @staticmethod
    def getEvent():
        GPManager.event = pg.event.wait(100)
    
    @staticmethod
    def getEventQuit():
        return (GPManager.event.type == pg.QUIT or (GPManager.event.type == pg.KEYDOWN and GPManager.event.key in [pg.K_ESCAPE, pg.K_q]))
    
    @staticmethod
    def getCollisionRect(rect):
        if rect == None:
            return False
        return rect.collidepoint(pg.mouse.get_pos()) and GPManager.event.type == pg.MOUSEBUTTONDOWN and GPManager.event.button == 1

    
    @staticmethod
    def getCollision(card):
        if card == None:
            return False
        GPManager.moving = card.getCardRect().collidepoint(pg.mouse.get_pos()) and GPManager.event.type == pg.MOUSEBUTTONDOWN and GPManager.event.button == 1

        return GPManager.moving
    
    @staticmethod
    def getMouseUp(card):
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

    @staticmethod
    def drawMenu():
        while 1:
            GPManager.getEvent()
            GPManager.clearScreen()

            GPManager.__renderTitle("Pyramids Solitaire", (250, 100, 1024, 860), (255, 255, 255))

            single_game = pg.Rect(450, 300, 400, 50)
            endless     = pg.Rect(450, 350, 400, 50)
            aimode      = pg.Rect(450, 400, 400, 50)
            option      = pg.Rect(450, 450, 400, 50)
            _exit       = pg.Rect(450, 500, 400, 50)

            pg.draw.rect(GPManager.screen, (10,120,50,255), (400, 260, 300, 300), border_radius=10)
            GPManager.__renderText("1. Single Game", single_game, (255, 255, 255))
            GPManager.__renderText("2. Endless",     endless,     (255, 255, 255))
            GPManager.__renderText("3. AI (Endless)", aimode,       (255, 255, 255))
            GPManager.__renderText("4. Option",      option,      (255, 255, 255))
            GPManager.__renderText("5. Exit",        _exit,       (255, 255, 255))

            if GPManager.getEventQuit():
                exit()

            if single_game.collidepoint(pg.mouse.get_pos()) and GPManager.event.type == pg.MOUSEBUTTONDOWN and GPManager.event.button == 1:
                return 0
            elif endless.collidepoint(pg.mouse.get_pos()) and GPManager.event.type == pg.MOUSEBUTTONDOWN and GPManager.event.button == 1:
                return 1
            elif aimode.collidepoint(pg.mouse.get_pos()) and GPManager.event.type == pg.MOUSEBUTTONDOWN and GPManager.event.button == 1:
                return 2
            elif option.collidepoint(pg.mouse.get_pos()) and GPManager.event.type == pg.MOUSEBUTTONDOWN and GPManager.event.button == 1:
                pass
            elif _exit.collidepoint(pg.mouse.get_pos()) and GPManager.event.type == pg.MOUSEBUTTONDOWN and GPManager.event.button == 1:
                exit()

            GPManager.Update()

    @staticmethod
    def drawFooter():
        #color wood
        pg.draw.rect(GPManager.screen, (150,42,60,255), (0, 780, 1100, 120))

        str_points =  f"Punteggio: {GM.getPoints()}" 
        str_moves  =  f"Mosse: {GM.getMove()}"
        str_time   =  f"{int(GM.getElapsedTime())//60:02d}:{int(GM.getElapsedTime()%60):02d}" 


        GPManager.__renderText(str_points, (20, 805, 50, 55),  (255, 255, 255))
        GPManager.__renderText(str_moves,  (300, 805, 50, 55), (255, 255, 255))
        GPManager.__renderText(str_time,   (900, 805, 50, 55), (255, 255, 255))

        rect = GPManager.resetTexture.get_rect()

        
        GPManager.screen.blit(GPManager.resetTexture, rect)
        pg.display.flip()


    def drawScreen(str):
        while 1:
            GPManager.getEvent()

            GPManager.__renderTitle(f"You {str}", (400, 200, 1024, 860), (255, 255, 255))

            restart     = pg.Rect(400, 400, 1024, 50)
            goMenu      = pg.Rect(400, 450, 1024, 50)


            GPManager.__renderText("Restart", restart, (255, 255, 255))
            GPManager.__renderText("Menu",     goMenu,  (255, 255, 255))

            if GPManager.getEventQuit():
                exit()

            if restart.collidepoint(pg.mouse.get_pos()) and GPManager.event.type == pg.MOUSEBUTTONDOWN and GPManager.event.button == 1:
                return 0
            elif goMenu.collidepoint(pg.mouse.get_pos()) and GPManager.event.type == pg.MOUSEBUTTONDOWN and GPManager.event.button == 1:
                return 1


            GPManager.Update()