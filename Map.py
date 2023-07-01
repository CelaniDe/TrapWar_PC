import pickle

class Map:
    def __init__(self,name):
        self.__map = {
            "name" : str(name),
            "Player" : list(),
            "Platform" : list(),
            "Pickup" : list(),
            "Bullet" : list(),
            "Trigger": list(),
            "Ghosts" : list()
        }

    def addPlayer(self,player):
        self.__map["Player"].append(player)

    def addPlatform(self,platform):
        self.__map["Platform"].append(platform)
    
    def addPickup(self,pickup):
        self.__map["Pickup"].append(pickup)

    def addBullet(self,bullet):
        self.__map["Bullet"].append(bullet)

    def addTrigger(self,trigger):
        self.__map["Trigger"].append(trigger)

    def addGhot(self,ghost):
        self.__map["Ghosts"].append(ghost)

    def returnAllObjects(self):
        all_objects_list = list()
        for lista_objects in self.__map.values():
            if type(lista_objects) == list:
                for objects in lista_objects:
                    all_objects_list.append(objects)
        return all_objects_list

    def isInLista(self,object_):
        object_x = object_.x
        object_y = object_.y
        for objects in self.returnAllObjects():
            if object_x == objects.x and object_y == objects.y:
                return True
        return False

    def returnObjectXY(self,x,y):
        for objects in self.returnAllObjects():
            if objects.hitBox.collidepoint((x,y)):
                return objects
        return None
        
    def removeObject(self,object_to_remove):
        for objects in self.__map['Player']:
            if object_to_remove == objects:
                self.__map['Player'].remove(object_to_remove)
                break
        for objects in self.__map['Platform']:
            if object_to_remove == objects:
                self.__map['Platform'].remove(object_to_remove)
                break
        for objects in self.__map['Pickup']:
            if object_to_remove == objects:
                self.__map['Pickup'].remove(object_to_remove)
                break
        for objects in self.__map['Bullet']:
            if object_to_remove == objects:
                self.__map['Bullet'].remove(object_to_remove)
                break
        for objects in self.__map['Trigger']:
            if object_to_remove == objects:
                self.__map['Trigger'].remove(object_to_remove)
                break
        for objects in self.__map['Ghosts']:
            if object_to_remove == objects:
                self.__map['Ghosts'].remove(object_to_remove)
                break
        

    def save(self):
        with open(f"maps/{self.__map['name']}.pickle", 'wb') as handle:
            pickle.dump(self.__map, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def openMap(self,map_name):
        self.__map = __class__.loadMap(map_name)

    @classmethod
    def loadMap(cls,map_name):
        with open(f'maps/{map_name}.pickle', 'rb') as handle:
            return pickle.load(handle)


