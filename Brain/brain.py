import Map.map

class Brain:
    def __init__(self, currentmap, side):
        self.currentmap = currentmap
        self.side = side #1=werewolf, -1=vampires

    def minIndex(self, list):
        index=0
        min=0
        for i in range(len(list)):
            if list[i]<min:
                index=i
                min=list[i]
        return index

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
            for j in range(Map.werewolf[i][0]):
                for k in [-1,0,1]:
                    for l in [-1,0,1]:
                        maps += [tempmap.movewerewolf(tempmap, j, coordX+k, coordY+l)]
        else:
            coordX = tempmap.vampire[i][1][0]
            coordY = tempmap.vampire[i][1][1]
            for j in range(Map.vampire[i][0]):
                for k in [-1,0,1]:
                    for l in [-1,0,1]:
                        maps += [tempmap.movevampire(tempmap, j, coordX+k, coordY+l)]
        return maps

    def movegrpCond(self, i, camp):
        maps=[]
        H=self.map.humans
        tempmap=self.currentmap
        if camp==1:
            coordX=tempmap.werewolf[i][1][0]
            coordY=tempmap.werewolf[i][1][1]
            for j in range(Map.werewolf[i][0]):
                for k in [-1,0,1]:
                    for l in [-1,0,1]:
                        for h in H:
                            if max(abs(coordX-h[1][0]),abs(coordY-h[1][1]))>max(abs(coordX+k-h[1][0]),abs(coordY+l-h[1][1])):
                                maps.append([tempmap.movewerewolf(tempmap, j, coordX+k, coordY+l)])
        else:
            coordX = tempmap.vampire[i][1][0]
            coordY = tempmap.vampire[i][1][1]
            for j in range(Map.vampire[i][0]):
                for k in [-1,0,1]:
                    for l in [-1,0,1]:
                        for h in H:
                            if max(abs(coordX - h[1][0]),abs(coordY - h[1][1])) > max(abs(coordX + k - h[1][0]), abs(coordY + l - h[1][1])):
                                maps.append([tempmap.movevampire(tempmap, j, coordX + k, coordY + l)])
        return maps

    def createMapsfromMap(self,camp):
        maps=[]
        if camp==1:
            for i in range(len(self.map.werewolves)):
                maps.append(self.moveGrpCond(i,camp))
        elif camp==0:
            for i in range(len(self.map.vampires)):
                maps.append(self.moveGrpCond(i,camp))
        return maps

    def probaH(self, grp1, grp2):
        if grp1<grp2:
            return grp1/(2*grp2)
        elif grp1>=grp2:
            return 1
        else:
            return 0

    def heuristic(self, map,camp):
        H=map.humans
        V=map.vampires
        W=map.werewolves
        nombreH=len(H)
        nombreV=len(V)
        nombreW=len(W)

        #calcul des distances entre tous les groupes
        distHW=[]
        distVW=[]
        distHV=[]
        for i in range(nombreH):
            distHW[i]=[]
            for j in range(nombreW):
                distHW[i][j]=max(abs(H[i][1][0]-W[i][1][0]),abs(H[i][1][1]-W[i][1][1]))
        for i in range(nombreV):
            distVW[i]=[]
            for j in range(nombreW):
                distVW[i][j] = max(abs(V[i][1][0] - W[i][1][0]), abs(V[i][1][1] - W[i][1][1]))
        for i in range(nombreH):
            distHV[i]=[]
            for j in range(nombreV):
                distHV[i][j] = max(abs(H[i][1][0] - V[i][1][0]), abs(H[i][1][1] - V[i][1][1]))

        # calcul des proba de gagner les humains
        probaW = []
        probaV = []
        for i in range(nombreH):
            probaW[i] = []
            for j in range(nombreW):
                probaW[i][j]=self.probaH(W[i][0],H[j][0])
        for i in range(nombreH):
            probaV[i] = []
            for j in range(nombreV):
                probaV[i][j]=self.probaH(V[i][0],H[j][0])

        #calcul des score
        captureH=[]
        for i in range(nombreH):
            captureH[i]=[]
            if min(distHV[i])<min(distHW):
                captureH[i][0]='V'
                index=self.minIndex(distHV[i])
                captureH[i][1]=min(distHV[i])*pow(probaV[i][index],2)
            elif min(distHV[i])>min(distHW):
                captureH[i][0]='W'
                index=self.minIndex(distHW[i])
                captureH[i][1]=min(distHW[i])*pow(probaW[i][index],2)
            else:
                captureH[i][0]='E'







