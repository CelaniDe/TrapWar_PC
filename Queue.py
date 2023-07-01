class Queue(object):
    def __init__(self):
        self.lista = list()

    def add(self,element):
        if type(element) != type((0,0)):
            raise Exception("Element is not a tuple")
        self.lista.append(element)

    def pick(self , index = 0): 
        if len(self.lista) > 0:
            return self.lista.pop(index)
        return None

    def have_tail(self):
        if len(self.lista) > 0:
            return True
        return False

    def find_first(self,host): 
        for i in range(len(self.lista)):
            if self.lista[i][1] == host: 
                return i
        return None       

    def remove(self):
        pass