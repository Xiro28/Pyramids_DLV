class GM:
    points = 0
    move = 0

    @staticmethod
    def reset():
        GM.points = 0
        GM.move = 0

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
    

        