from abc import ABC , abstractclassmethod

class ObjectInGame(ABC):

    win = None

    def __init__(self,x,y):
        self.x = x
        self.y = y

    @abstractclassmethod
    def spawn(self):
        pass
