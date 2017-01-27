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

    def calcPath(self,camp):
        map=self.map
        humans=map.humans
        if camp==1:
            pawn=map.werewolf
        else:
            pawn = map.vampire
        maps = []
        for i in len(pawn):
            maps = maps + [self.newMap(self,0,1)]
            maps = maps + [self.newMap(self,0,-1)]
            maps = maps + [self.newMap(self,1,1)]
            maps = maps + [self.newMap(self,1,-1)]
        return maps

    def newMap(self,coord,side):
        tempPawn = pawn
        tempMap = self.map
        tempPawn[i][coord] = tempPawn[i][coord]+side
        if camp == 1:
            tempMap.werewolf = tempPawn
        else:
            tempMap.vampire = tempPawn
        return tempMap


    def buildTree(self):

