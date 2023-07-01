from ObjectInGame import *
from InteractiveImageButton import *

class Slider(ObjectInGame):
    def __init__(self,x,y,lista_objects):
        self.x = x
        self.y = y
        self.lista_objects = lista_objects
        self.index = 0

    def swipeRight(self):
        self.index += 1

    def swipeLeft(self):
        self.index -= 1

    @abstractclassmethod
    def conditionToSwipeRight(self):
        pass

    @abstractclassmethod
    def conditionToSwipeLeft(self):
        pass

    def getIndex(self):
        return self.index

    def spawn(self):
        self.index = self.index % len(self.lista_objects)

        image = self.lista_objects[self.getIndex()]
        center_of_image_to_spawn = image.get_rect(center = (self.x,self.y))
        self.win.blit(image,center_of_image_to_spawn)

        if self.conditionToSwipeLeft():
            self.swipeLeft()

        if self.conditionToSwipeRight():
            self.swipeRight()



class ButtonSlider(Slider):
    def __init__(self,x,y,lista_objects,leftButton,rightButton):
        super().__init__(x,y,lista_objects)
        self.leftButton = leftButton
        self.rightButton = rightButton
        self.index_to_spawn = 0

    def spawn(self):
        self.index = self.index % len(self.lista_objects)

        image = self.lista_objects[self.getIndex()]

        if type(image) is list:
            if self.index_to_spawn >= len(image):
                self.index_to_spawn = 0
            center_of_image_to_spawn = image[self.index_to_spawn].get_rect(center = (self.x,self.y))
            self.win.blit(image[self.index_to_spawn],center_of_image_to_spawn)
            self.index_to_spawn += 1
        else:
            center_of_image_to_spawn = image.get_rect(center = (self.x,self.y))
            self.win.blit(image,center_of_image_to_spawn)

        self.leftButton.spawn()

        self.rightButton.spawn()

        if self.conditionToSwipeLeft():
            self.swipeLeft()

        if self.conditionToSwipeRight():
            self.swipeRight()

    def conditionToSwipeLeft(self):
        if self.leftButton.clicked():
            return True
        return False
    
    def conditionToSwipeRight(self): 
        if self.rightButton.clicked():
            return True
        return False




    

