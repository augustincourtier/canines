class Map:
    def __init__(self,vampire,werewolf,humans,sizeX,sizeY):
        self.sizeX=sizeX
        self.sizeY=sizeY
        self.humans=humans
        self.vampire=vampire
        self.werewolf=werewolf

    def addvampire(self,number,coordX,coordY):
        self.vampire += [number, [coordX, coordY]]

    def addwerewolf(self, number, coordX, coordY):
        self.werewolf = self.vampire + [number, [coordX, coordY]]

    def addhumans(self, number, coordX, coordY):
        self.humans = self.vampire + [number, [coordX, coordY]]

    def movevampire(self,number,coordX,coordY,idgrp):
        if self.vampire[idgrp][0]<=number:
            self.vampire[idgrp][1]=[coordX,coordY]
        else:
            self.vampire[idgrp][0]-=number
            self.addVampire(map,number,coordX,coordY)

    def movewerewolf(self,number,coordX,coordY,idgrp):
        if self.werewolf[idgrp][0]<=number:
            self.werewolf[idgrp][1]=[coordX,coordY]
        else:
            self.werewolf[idgrp][0]-=number
            self.addWerewolf(map,number,coordX,coordY)

    def findgrp(self,coordX,coordY):
        for i in range(len(self.vampire)):
            if self.vampire[1]==[coordX,coordY]:
                return [i,"vampire"]
        for i in range(len(self.werewolf)):
            if self.vampire[1] == [coordX, coordY]:
                return [i, "werewolf"]
        for i in range(len(self.humans)):
            if self.vampire[1] == [coordX, coordY]:
                return [i, "humans"]

