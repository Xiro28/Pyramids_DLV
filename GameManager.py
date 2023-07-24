import time

class GM:
    points = 0
    move = 0
    game = 1
    start_time = time.time()

    @staticmethod
    def reset(reset_game = True):
        GM.points = 0
        GM.move = 0
        if reset_game:
            GM.game = 1
        GM.start_time = time.time()


    @staticmethod
    def getGame():
        return GM.game
    
    def addGame():
        GM.game += 1
    
    @staticmethod
    def getElapsedTime():
        return time.time() - GM.start_time
    

    start_time_sc = time.time()
    @staticmethod
    def scheduleAtFixedOne(func):
        if int(time.time()) - int(GM.start_time_sc) >= 1:
            GM.start_time_sc = time.time()
            func()

    @staticmethod
    def addPoints(points):
        GM.points += points

        if GM.points < 0:
            GM.points = 0

        if points > 0:
            GM.move += points//100

    @staticmethod
    def getPoints():
        return GM.points
    
    @staticmethod
    def getMove():
        return GM.move
    
    @staticmethod
    def addMove():
        GM.move += 1

        