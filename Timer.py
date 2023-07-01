class Timer():
    def __init__(self,durata):
        self.count = 0
        self.durata = durata


    def apply(self):
        if(self.count <= self.durata): self.count += 1
        else: 
            self.count = 0
            self.isStart = False
            return True
        return False        


