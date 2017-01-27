class map:
    def __init__(self,vampire,werewolf,humans,sizeX,sizeY):
        self.sizeX=sizeX
        self.sizeY=sizeY
        self.humans=humans
        self.vampire=vampire
        self.werewolf=werewolf

    def addVampire(self,number,coordX,coordY):
        self.vampire=self.vampire+[number,[coordX,coordY]]

    def addWerewolf(self, number, coordX, coordY):
        self.werewolf = self.vampire + [number, [coordX, coordY]]

    def addHumans(self, number, coordX, coordY):
        self.humans = self.vampire + [number, [coordX, coordY]]

    def moveVampire(self,):