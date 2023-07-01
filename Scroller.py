from ObjectInGame import *

class Scroller(ObjectInGame):
    def __init__(self,x,y,objects,crowd_objects,win):
        super().__init__(x,y)
        self.lista_objects = objects
        self.win = win
        self.up_index = 0
        self.crowd_objects = crowd_objects

    def scrollDown(self):
        if (self.up_index + self.crowd_objects) < len(self.lista_objects):
            self.up_index += 1

    def scrollUp(self):
        if self.up_index > 0:
            self.up_index -= 1

    def spawn(self):
        space = 0
        for i in range(self.up_index,self.up_index+self.crowd_objects):
            object_to_spawn = self.lista_objects[i]
            if object_to_spawn.status == True:
                object_to_spawn.x = self.x - int(object_to_spawn.width/2)
                object_to_spawn.y = self.y - int(object_to_spawn.height/2) + space
                object_to_spawn.spawn()
                space += object_to_spawn.height + 100
            else:
                self.lista_objects.append(self.lista_objects.pop(i))