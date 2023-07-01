import os
import pygame
import weakref

class ResourceController(object):
    def __init__(self, loader):
        self.__dict__.update(dict(
            names = {},
            cache = weakref.WeakValueDictionary(),
            loader = loader
        ))
        
    def __setattr__(self, name, value):
        self.names[name] = value

        
    def __getattr__(self, name):
        try:
            img = self.cache[name]
        except KeyError:
            img = self.loader(self.names[name])
            self.cache[name] = img
        return img

        
    
class ImageController(ResourceController):
    def __init__(self):
        ResourceController.__init__(self, pygame.image.load)


class Loader():
    def __init__(self,nome_percorso):
        self.new_path = os.getcwd()+nome_percorso
        self.old_path = os.getcwd()
        self.length = 0
        self.img_controller = self.__ricevi_foto()

    def __ricevi_foto(self):
        #old_directory = os.getcwd()
        img_controller = ImageController()
        os.chdir(self.new_path)
        nomi_foto = os.listdir()
        nomi_foto = sorted(nomi_foto)
        for name_foto in nomi_foto:
            if "png" in name_foto or "celani" in name_foto:
                img_controller.__setattr__(str(self.length),name_foto)
                self.length += 1
        os.chdir(self.old_path)
        return img_controller

    def get_item(self,index): 
        os.chdir(self.new_path)
        item = self.img_controller.__getattr__(str(index))
        os.chdir(self.old_path)
        return item
    def get_length(self): return self.length

