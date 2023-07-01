class Gravita():

    @classmethod
    def apply(cls,oggetto,platforms):
        G = oggetto.gravity_force
        #G = 2
        oggetto.move_collide((0,G),[x.getHitBox() for x in platforms])
            

