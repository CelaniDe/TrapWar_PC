class RecvDataFactory():
    
    @classmethod
    def getRecvData(cls,lista,Type,old):
        for i in  range(len(lista)):
            if len(lista[i]) > 0:
                if isinstance(lista[i][0],Type):
                    return lista[i]
            else:
                if(not RecvDataFactory().__hasNext(lista,i)):
                    return list()
                old = list()
        return old

    def __hasNext(self,lista,index):
        for i in range(index,len(lista)):
            if lista[i] != []:
                return True
        return False
