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
        return self.side*(nbww-nbvamp)

    def calcPath(self,camp):
        map=self.map
        humans=map.humans
        if camp==1:
            pawn=map.werewolf
        else:
            pawn = map.vampire
        maps = []
        for i in range(len(pawn)):
            maps += [self.newmapmove(self, map, i, [1, 0], camp)]
            maps += [self.newmapmove(self, map, i, [-1, 0], camp)]
            maps += [self.newmapmove(self, map, i, [0, 1], camp)]
            maps += [self.newmapmove(self, map, i, [0, -1], camp)]
            maps += [self.newmapmove(self, map, i, [1, 1], camp)]
            maps += [self.newmapmove(self, map, i, [-1, 1], camp)]
            maps += [self.newmapmove(self, map, i, [1, -1], camp)]
            maps += [self.newmapmove(self, map, i, [-1, -1], camp)]

        return maps

    def newmapmove(self, map, i, coord, camp):
        newMap=map
        if camp==1 and map.coordX>=map.werewolf[i][1][0]+coord[0]>=1:
            map.werewolf[i][1][0]+=coord[0]
        else if camp==0 and map.coordY>=map.werewolf[i][1][1]+coord[1]>=1:
            map.vampire[i][1][1]+=coord[1]
        return newMap


    def buildTree(self):


