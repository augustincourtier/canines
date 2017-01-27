import Map.map

class Brain:
    def __init__(self, currentmap, side):
        self.currentmap = currentmap
        self.side = side #1=werewolf, -1=vampires

    def score(self):
        ww=self.currentmap.werewolf
        vamp=self.currentmap.vamp
        nbww = 0
        nbvamp = 0
        for i in ww:
            nbww=nbww+i[2]
        for j in vamp:
            nbvamp=nbvamp+j[2]
        return self.side*(nbww-nbvamp)

    def calcPath(self,camp):
        Map=self.currentmap
        if camp==1:
            pawn=Map.werewolf
        else:
            pawn = Map.vampire
        maps = []
        for i in range(len(pawn)):
            maps += self.movegrp(self, i, camp)
        return maps

    def movegrp(self, i, camp):
        maps=[]
        tempmap=self.currentmap
        if camp==1:
            coordX=tempmap.werewolf[i][1][0]
            coordY=tempmap.werewolf[i][1][1]
            for j in range(Map.werewolf[i][0])
                maps+=[tempmap.movewerewolf(tempmap,j,coordX,coordY)]
                maps+=[tempmap.movewerewolf(tempmap,j,coordX,coordY)]
                maps+=[tempmap.movewerewolf(tempmap,j,coordX,coordY)]
                maps+=[tempmap.movewerewolf(tempmap,j,coordX,coordY)]
                maps+=[tempmap.movewerewolf(tempmap,j,coordX,coordY)]
                maps+=[tempmap.movewerewolf(tempmap,j,coordX,coordY)]
                maps+=[tempmap.movewerewolf(tempmap,j,coordX,coordY)]
                maps+=[tempmap.movewerewolf(tempmap,j,coordX,coordY)]
        else:
            coordX = tempmap.vampire[i][1][0]
            coordY = tempmap.vampire[i][1][1]
            for j in range(Map.vampire[i][0])
                maps += [tempmap.movevampire(tempmap, j, coordX, coordY)]
                maps += [tempmap.movevampire(tempmap, j, coordX, coordY)]
                maps += [tempmap.movevampire(tempmap, j, coordX, coordY)]
                maps += [tempmap.movevampire(tempmap, j, coordX, coordY)]
                maps += [tempmap.movevampire(tempmap, j, coordX, coordY)]
                maps += [tempmap.movevampire(tempmap, j, coordX, coordY)]
                maps += [tempmap.movevampire(tempmap, j, coordX, coordY)]
                maps += [tempmap.movevampire(tempmap, j, coordX, coordY)]
        return maps


    def buildTree(self):


