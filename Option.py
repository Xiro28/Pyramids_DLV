class Options():

    __options = {"reload":  2, "shuffle": 1, "hint": 1}

    @staticmethod
    def getOptions():
        return Options.__options
    
    @staticmethod
    def getOption(option):
        return Options.__options[option]
    
    @staticmethod
    def setOption(option, value):
        Options.__options[option] = value