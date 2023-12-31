import pygame as pg

from GameManager import GM
from Option import Options

class GPManager():
    CARD_WIDTH = 110
    CARD_HEIGHT = 155

    screen = None
    font = None
    moving = False

    resetTexture = None
    resetTexture_rect = None

    menuTexture = None
    menuTexture_rect = None

    @staticmethod
    def initGraphics():
       pg.init()
       pg.display.set_caption('Pyramids Solitaire')
       GPManager.screen = pg.display.set_mode((1100, 860), pg.SRCALPHA)
       GPManager.font = pg.font.Font(None, 36)
       GPManager.Titlefont = pg.font.Font(None, 100)

       GPManager.resetTexture = GPManager.loadTexture(path = "textures/png/restart.png", resize = (40, 40))
       GPManager.resetTexture_rect = GPManager.resetTexture.get_rect()
       GPManager.resetTexture_rect.x = 950
       GPManager.resetTexture_rect.y = 800

       GPManager.menuTexture = GPManager.loadTexture(path = "textures/png/menu.png", resize = (50, 50))
       GPManager.menuTexture_rect = GPManager.menuTexture.get_rect()
       GPManager.menuTexture_rect.x = 1020
       GPManager.menuTexture_rect.y = 795

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
    def drawCard(card, rect = None, direct = False, animated = True):
        if card == None:
            return
        
        if rect == None:
            pg.draw.rect(GPManager.screen, (255, 255, 255, 0), card.getCardRect(), border_radius=7)
            GPManager.screen.blit(card.getCardImage(), card.getCardRect(), special_flags=pg.BLEND_RGBA_MIN)
        else:
            pg.draw.rect(GPManager.screen, (255, 255, 255, 0), rect, border_radius=7)
            GPManager.screen.blit(card, rect, special_flags=pg.BLEND_RGBA_MIN)

        if direct:

            if animated:
                GPManager.Update()
                pg.time.delay(70)
            else:
                GPManager.Update()

    @staticmethod
    def drawRectSurround(rect):
        pg.draw.rect(GPManager.screen, (80, 80, 140, 255), rect, 5, border_radius=8)

    @staticmethod
    def drawCards(cards, animated = True):
        if cards == None:
            return
        
        for cards_level in cards:
            for card in cards_level:
                if card == None:
                    continue

                #used only by the dump cards
                if isinstance(card, tuple):
                    GPManager.drawCard(card[0].getCardImage(), card[1])

                elif animated:
                    GPManager.drawCard(card, None, True, True)
                else:
                    GPManager.drawCard(card)
                    
        if not animated:
            GPManager.Update()

    @staticmethod
    def highlightCard(card):
        if card == None:
            return
        
        pg.draw.rect(GPManager.screen, (80, 80, 160, 255), card.getCardRect(), 4, border_radius=7)
        GPManager.Update()

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
            
        GPManager.Update()

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


    def __getRotatedTexture(texture, angle, coords):
        rotated_rect = texture.get_rect().move(coords[0], coords[1])
        rotated_size = (300, 300)
        rotated_surface = pg.Surface(rotated_size, pg.SRCALPHA)

        rotated_surface.fill((0, 0, 0, 0))  # Fill with transparent color
        rotated_surface.blit(pg.transform.rotate(texture, angle), (0, 0))

        return rotated_surface, rotated_rect
    
    
    @staticmethod
    def drawMenu():
        GPManager.clearScreen()
        GPManager.__renderTitle("Pyramids Solitaire", (200, 200, 1024, 860), (255, 255, 255))

        single_game = pg.Rect(450, 400, 400, 50)
        endless     = pg.Rect(450, 450, 400, 50)
        aimode      = pg.Rect(450, 500, 400, 50)
        option      = pg.Rect(450, 550, 400, 50)
        _exit       = pg.Rect(450, 600, 400, 50)

        GPManager.Update()

        # Create a surface with the desired size and draw something on it
        card1 = GPManager.loadTexture(path = "textures/png/ace_of_clubs.png", resize = (150, 195))
        card2 = GPManager.loadTexture(path = "textures/png/jack_of_hearts.png", resize = (150, 195))
        
        pg.draw.rect(GPManager.screen, (10,110,50,255), (400, 360, 300, 300), border_radius=10)
        pg.draw.rect(GPManager.screen, (0,60,00,255),  (400, 360, 300, 300), 2, border_radius=10)
        GPManager.__renderText("1. Single Game", single_game, (255, 255, 255))
        GPManager.__renderText("2. Endless",     endless,     (255, 255, 255))
        GPManager.__renderText("3. AI (Endless)", aimode,     (255, 255, 255))
        GPManager.__renderText("4. Option",      option,      (255, 255, 255))
        GPManager.__renderText("5. Exit",        _exit,       (255, 255, 255))

        GPManager.Update()

        rotatedCard1, rotatedCard1_rect = GPManager.__getRotatedTexture(card1, 340, (870, 140))
        GPManager.screen.blit(rotatedCard1, rotatedCard1_rect.topleft)
        pg.time.delay(100)
        GPManager.Update()

        rotatedCard2, rotatedCard2_rect = GPManager.__getRotatedTexture(card2, 355, (830, 150))
        GPManager.screen.blit(rotatedCard2, rotatedCard2_rect.topleft)
        pg.time.delay(100)
        GPManager.Update()
        
        while 1:

            GPManager.getEvent()

            if GPManager.getEventQuit():
                exit()

            if GPManager.event.type == pg.MOUSEBUTTONDOWN and GPManager.event.button == 1:
                if single_game.collidepoint(pg.mouse.get_pos()):
                    return 0
                elif endless.collidepoint(pg.mouse.get_pos()):
                    return 1
                elif aimode.collidepoint(pg.mouse.get_pos()):
                    return 2
                elif option.collidepoint(pg.mouse.get_pos()):
                    return 3
                elif _exit.collidepoint(pg.mouse.get_pos()):
                    exit()

            

    @staticmethod
    def drawFooter(flip = False):
        #color wood
        pg.draw.rect(GPManager.screen, (150,42,60,255), (0, 780, 1100, 120))

        str_points =  f"Punteggio: {GM.getPoints()}" 
        str_moves  =  f"Mosse: {GM.getMove()}"
        str_games  =  f"Gioco: {GM.getGame()}"
        str_time   =  f"{int(GM.getElapsedTime())//60:02d}:{int(GM.getElapsedTime()%60):02d}" 


        GPManager.__renderText(str_points, (20, 805, 50, 55),  (255, 255, 255))
        GPManager.__renderText(str_moves,  (300, 805, 50, 55), (255, 255, 255))
        GPManager.__renderText(str_games,  (500, 805, 50, 55), (255, 255, 255))
        GPManager.__renderText(str_time,   (750, 805, 50, 55), (255, 255, 255))

        GPManager.screen.blit(GPManager.menuTexture, GPManager.menuTexture_rect)
        GPManager.screen.blit(GPManager.resetTexture, GPManager.resetTexture_rect)
        
        if flip:
            GPManager.Update()


    def __drawPlusMinusButton(plus_button_rect, minus_button_rect):

        white = (255, 255, 255)

        pg.draw.rect(GPManager.screen, (0, 80, 0, 128), plus_button_rect, border_radius=8)

        # disegnamo prima |
        pg.draw.line(GPManager.screen, white, (plus_button_rect.centerx, plus_button_rect.top + 5), (plus_button_rect.centerx, plus_button_rect.bottom - 5), 3)

        # disegnamo poi ----
        pg.draw.line(GPManager.screen, white, (plus_button_rect.left + 5, plus_button_rect.centery), (plus_button_rect.right - 5, plus_button_rect.centery), 3)

        pg.draw.rect(GPManager.screen, (0, 80, 0, 128), minus_button_rect, border_radius=8)

        #per il meno disegnamo solo -----
        pg.draw.line(GPManager.screen, white, (minus_button_rect.left + 5, minus_button_rect.centery), (minus_button_rect.right - 5, minus_button_rect.centery), 3)

        return plus_button_rect, minus_button_rect
    
    
    
    @staticmethod
    def drawOptions():

        shuffle_value = Options.getOption("shuffle")
        reload_times_value = Options.getOption("reload")
        hint_value = Options.getOption("hint")   

        white = (255, 255, 255)
        red = (255, 0, 0) 
        
        while 1:
            GPManager.getEvent()
            GPManager.clearScreen()

            pg.draw.rect(GPManager.screen, (10,110,50,255), (270, 250, 520, 300), border_radius=10)
            pg.draw.rect(GPManager.screen, (0,60,00,255),  (270, 250, 520, 300), 2, border_radius=10)

            if GPManager.getEventQuit():
                exit()

            options_text = GPManager.font.render("Options", True, white)
            GPManager.screen.blit(options_text, (300, 260))

            reload_times_text = GPManager.font.render("Reload Times: " + str(reload_times_value), True, white)
            GPManager.screen.blit(reload_times_text, (380, 330))

            shuffle_text = GPManager.font.render("Shuffle: " + ("On" if shuffle_value else "Off"), True, white if shuffle_value else red)
            GPManager.screen.blit(shuffle_text, (380, 380))

            hint_text = GPManager.font.render("Hint: " + ("On" if hint_value else "Off"), True, white if hint_value else red)
            GPManager.screen.blit(hint_text, (380, 420))

            confirm_text = GPManager.font.render("Confirm changes", True, white)
            GPManager.screen.blit(confirm_text, (420, 500))

            plus_button_rect_r, minus_button_rect_r = GPManager.__drawPlusMinusButton(pg.Rect(680, 325, 30, 30), pg.Rect(630, 325, 30, 30))

            if GPManager.event.type == pg.MOUSEBUTTONDOWN and GPManager.event.button == 1:
                if plus_button_rect_r.collidepoint(GPManager.event.pos):
                    reload_times_value += 1
                elif minus_button_rect_r.collidepoint(GPManager.event.pos):
                    reload_times_value -= 1 if reload_times_value > 1 else 0
                elif shuffle_text.get_rect(topleft=(380, 380)).collidepoint(GPManager.event.pos):
                    shuffle_value = (shuffle_value + 1) % 2
                elif hint_text.get_rect(topleft=(380, 420)).collidepoint(GPManager.event.pos):
                    hint_value = (hint_value + 1) % 2
                elif confirm_text.get_rect(topleft=(420, 500)).collidepoint(GPManager.event.pos):
                    Options.setOption("shuffle", shuffle_value)
                    Options.setOption("reload", reload_times_value)
                    Options.setOption("hint", hint_value)
                    return

            GPManager.Update()


    def drawScreen(str, continue_game = False):

        pg.draw.rect(GPManager.screen, (10,110,50,255), (300, 250, 520, 300), border_radius=10)
        pg.draw.rect(GPManager.screen, (0,60,00,255),  (300, 250, 520, 300), 2, border_radius=10)

        GPManager.__renderTitle(f"{str}", (320, 300, 1024, 860), (255, 255, 255))

        restart     = pg.Rect(500, 400, 1024, 50)
        goMenu      = pg.Rect(500, 450, 1024, 50)


        if continue_game:
            GPManager.__renderText(f"Win : {GM.getWins()}",  restart, (255, 255, 255))
            GPManager.__renderText(f"Lose : {GM.getLoses()}", goMenu,  (255, 255, 255))
            GPManager.Update()
            pg.time.delay(500)
        else:
            GPManager.__renderText("Restart", restart, (255, 255, 255))
            GPManager.__renderText("Menu",     goMenu,  (255, 255, 255))
            GPManager.Update()
            

        while not continue_game:
            GPManager.getEvent()

            if GPManager.getEventQuit():
                exit()

            if GPManager.event.type == pg.MOUSEBUTTONDOWN and GPManager.event.button == 1:
                if restart.collidepoint(pg.mouse.get_pos()):
                    return 0
                elif goMenu.collidepoint(pg.mouse.get_pos()):
                    return 1
        return 0