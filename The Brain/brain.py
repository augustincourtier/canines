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
            maps = maps + [self.newMapMove(self,map,i,[1,0],camp)]
            maps = maps + [self.newMapMove(self,map,i,[-1,0],camp)]
            maps = maps + [self.newMapMove(self,map,i,[0,1],camp)]
            maps = maps + [self.newMapMove(self,map,i,[0,-1],camp)]
            maps = maps + [self.newMapMove(self,map,i,[1,1],camp)]
            maps = maps + [self.newMapMove(self,map,i,[-1,1],camp)]
            maps = maps + [self.newMapMove(self,map,i,[1,-1],camp)]
            maps = maps + [self.newMapMove(self,map,i,[-1,-1],camp)]

        return maps

    def newMapMove(self,map,i,coord,camp):
        newMap=map
        if camp==1:
            map.werewolf[i][1]=coord;
        else if camp==0:
            map.vampire[i][1]=coord;
        return map




    def buildTree(self):


