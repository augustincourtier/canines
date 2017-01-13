class brain:
    def __init__(self,map,side):
        self.map = map
        self.side = side #1=werewolf, -1=vampires

    def score(self):
        ww=self.map.werewolf
        vamp=self.map.vamp
        nbww = 0
        nbvamp = 0
        for i in ww:
            nbww=nbww+i[2]
        for j in vamp:
            nbvamp=nbvamp+j[2]
        return side*(nbww-nbvamp)

    def calcPath(self):
        map=self.map
        humans=self.map.humans
        if self.camp==1:
            pawn=self.map.werewolf
            ennemi=self.map.vampire
        else:
            ennemi = self.map.werewolf
            pawn = self.map.vampire



    def buildTree(self):

