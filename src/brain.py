import map
import numpy as np
from copy import deepcopy
from random import randint

class Brain:
    def __init__(self, currentmap, side):
        self.currentmap = currentmap
        self.side = side #1=werewolf, -1=vampires

    ####
    # GENERAL FUNCTIONS OF BRAIN
    ####

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

    def createMOV(self, newmap):
        map=self.currentmap
        H=map.humans
        V=map.vampires
        W=map.werewolves
        newH=newmap.humans
        newV=newmap.vampires
        newW=newmap.werewolves
        for human in H:
            if human in newH:
                H.remove(human)
                newH.remove(human)
        for vampire in V:
            if vampire in newV:
                V.remove(vampire)
                newV.remove(vampire)
        for werewolve in W:
            if werewolve in newW:
                W.remove(werewolve)
                newW.remove(werewolve)

        for i in H:
            mov=[]
            for j in newH:
                if max(abs(i[1][0]-j[1][0]),abs(i[1][1]-j[1][1]))<=1:
                    mov.append(j)
                if len(mov)==1:
                    #voir MOV
                    return 0

    ####
    # ALEX AND PIERRE tests
    ####

    def movegrpCond(self, i, camp):
        maps=[]
        H=self.currentmap.humans
        map=self.currentmap
        if camp==1:
            playerPawns = map.werewolves[i]
        else:
            playerPawns = map.vampires[i]

        coordX = playerPawns[1][0]
        coordY = playerPawns[1][1]
        for j in range(1,playerPawns[0]+1):
            for k in [-1,0,1]:
                for l in [-1,0,1]:
                    for h in H:
                        if max(abs(coordX - h[1][0]),abs(coordY - h[1][1])) > max(abs(coordX + k - h[1][0]), abs(coordY + l - h[1][1])):
                            tempmap=deepcopy(map)
                            #TODO: Rassembler les fonctions move_vampires/move_werewolves add_vampires/add_werewolves etc en une avec param
                            if camp==1:
                                tempmap.move_vampires(j, coordX + k, coordY + l, i)
                            else:
                                tempmap.move_werewolves(j, coordX + k, coordY + l, i)
                            if not self.arrayIsInList(tempmap,maps):
                                maps.append(tempmap)

        return maps


    def createMapsfromMap(self,camp):
        maps=[]
        if camp==1:
            for i in range(len(self.currentmap.werewolves)):
                maps+=(self.movegrpCond(i,camp))
        elif camp==0:
            for i in range(len(self.currentmap.vampires)):
                maps+=(self.movegrpCond(i,camp))
        return maps

    ####
    # ALEX AND ELIE tests
    ####

    # this function gives interesting boxes around one group
    def generateValueBoxes(self, i):
        boxes=[] # this arrays stores interesting boxes around a group
        H=self.currentmap.humans
        map=self.currentmap
        if self.side==1:
            group = map.werewolves[i]
        else:
            group = map.vampires[i]

        coordX = group[1][0]
        coordY = group[1][1]

        for j in range(1,group[0]+1):
            for k in [-1,0,1]:
                for l in [-1,0,1]:
                    for h in H:
                        # box is interesting if going there make a group closer to humans TODO: also to ennemies or allies
                        if max(abs(coordX - h[1][0]),abs(coordY - h[1][1])) > max(abs(coordX + k - h[1][0]), abs(coordY + l - h[1][1])):
                            if coordX + k <= map.size_x-1 and coordX + k >= 0 and coordY + l <= map.size_y-1 and coordY + l >= 0:
                                if not self.arrayIsInList([coordX + k, coordY + l], boxes):
                                    boxes += [[coordX + k, coordY + l]]
        return boxes

    # this function generates all possibles subgroups from one original group and then choose valid possibilities (n subgroups with a total of people =  sizeOfOriginalGroup)
    def generateValueMoves(self, valueBoxes, sizeOfOriginalGroup):
        possibleTuples = [] #this will store each possible tuples for one valid box (ex 1 guy on the box, 2 guys etc..)
        for i in range(len(valueBoxes)):
            possibleTuplesForOneBox = []

            for j in range(0, sizeOfOriginalGroup+1):
                possibleTuplesForOneBox += [[j, [valueBoxes[i][0], valueBoxes[i][1]]]]
            possibleTuples += [possibleTuplesForOneBox]

        # this array contains the list of possibilities for each valueBoxes (0 on the first box, or 1 or 2 and so on..)
        possibleTuples = Brain.standardizeArray(possibleTuples)

        # this array represents "possibleTuples" with index (integers) instead of tuples
        indexArray = Brain.generateIndexArray(len(valueBoxes), sizeOfOriginalGroup)
        # this array still contains indexes
        possibleMoves = Brain.generateMoves(indexArray)

        valueMoves = []
        for indexMove in possibleMoves:
            # eliminating with sumOfMove() combinations that don't give exactly sizeOfOriginalGroup characters in total
            if Brain.sumOfMove(indexMove, possibleTuples) == sizeOfOriginalGroup:
                realMove = []
                # converting indexes into tuples [n, [x,y]]
                for index in indexMove:
                    realMove += [possibleTuples[index]]
                valueMoves += [realMove]

        return valueMoves

    def chooseMove(self, valueMoves, boxes, group):
        # TODO: choose the move to do based on the result of findTargetHumans() and other input
        # first heuristic
        newMoves1 = []
        scoreMax = 0
        for move in valueMoves:
            # print Brain.deleteZeroMoves([move])
            # print self.heuristic1(move)
            if scoreMax == 0:
                scoreMax = self.heuristic1(move)
                newMoves1 = [move]
            else:
                if scoreMax == self.heuristic1(move):
                    newMoves1.append(move)
                elif scoreMax < self.heuristic1(move):
                    scoreMax = self.heuristic1(move)
                    newMoves1 = [move]

        # second heuristic
        newMoves2 = []
        scoreMax = 0
        for move in newMoves1:
            # print Brain.deleteZeroMoves([move])
            # print self.heuristic2(move, boxes, group[1])
            if scoreMax == 0:
                scoreMax = self.heuristic2(move, boxes, group[1])
                newMoves2 = [move]
            else:
                if scoreMax == self.heuristic2(move, boxes, group[1]):
                    newMoves2.append(move)
                elif scoreMax < self.heuristic2(move, boxes, group[1]):
                    scoreMax = self.heuristic2(move, boxes, group[1])
                    newMoves2 = [move]

        i = randint(0,len(newMoves2)-1)
        # print len(boxes)
        # print Brain.deleteZeroMoves(newMoves2)
        return newMoves2[i]

    def heuristic1(self, move):
        score = 0
        targets = self.currentmap.humans
        goodTargets = []
        for subgroup in move:
            if self.side == 1:
                enemies = self.currentmap.vampires
            else:
                enemies = self.currentmap.werewolves
            for target in targets:
                distTargetEnemy = []
                for enemy in enemies:
                    distTargetEnemy += [max(abs(target[1][0]-enemy[1][0]),abs(target[1][1]-enemy[1][1]))]
                distMinEnemy = min(distTargetEnemy)
                if distMinEnemy <= max(abs(target[1][0]-subgroup[1][0]),abs(target[1][1]-subgroup[1][1])): # Distance subgroup target
                    score += 0
                else:
                    if subgroup[0] < target[0]:
                        score += 0
                    else:
                        if not self.arrayIsInList(target[1], goodTargets):
                            score += target[0]
                            goodTargets += [target[1]]
        return score

    def heuristic2(self, move, boxes, previousCoord):
        boxWithTargetHumans = self.findTargetHumans(boxes, previousCoord)
        score = 0
        for subgroup in move:
            for boxWithTarget in boxWithTargetHumans:
                if subgroup[1] == boxWithTarget[0]:
                    peopleInTargets = []
                    for target in boxWithTarget[1]:
                        peopleInTargets += [target[0]]
                    if subgroup[0] >= min(peopleInTargets):
                        score += min(sum(peopleInTargets), subgroup[0])

        return score

    # This function takes a move defined by index and the corresponding array of tuples
    # and returns the sum of characters of that move
    @staticmethod
    def sumOfMove(indexMove, tuples):
        total = 0
        for index in indexMove:
            total += tuples[index][0] # the first elem of a tuple [n, [x,y]] is the number of character
        return total

    # This function generates an array containing boxNumber arrays of groupSize elements
    # each element is and index in range 0 -- boxNumber*groupSize -1
    @staticmethod
    def generateIndexArray(boxNumber, groupSize):
        index = 0
        result = []
        for i in range(0, boxNumber):
            subarray = []
            for j in range(0, groupSize+1):
                subarray += [index]
                index += 1
            result += [subarray]
        return result

    # This function is used to generate an array containing all possibilities of one pick in n arrays
    # of m integer elements. (on possibility is equivalent to a move)
    # ex : [[1,2],[3,4]] => [[1,3],[1,4],[2,3],[2,4]]
    @staticmethod
    def generateMoves(list):
        result = []
        if list == []:
            result +=[]
        else:
            for i in list[0]:
                result+=Brain.distribute(i,  Brain.generateMoves(list[1:]))
        return result

    # This function is used to distribute a value on an array of arrays
    # ex : [1,[1,2],[3,4]] => [[1,1,2],[1,3,4]]
    @staticmethod
    def distribute(element,lists):
        newList = []
        if lists==[]:
            return [[element]]
        elif  isinstance( lists[0], int )==True:
            newList = [lists+[element]]
            return newList
        else :
            for list in lists:
                list +=[element]
                newList+=[list]
            return newList

    # This function transforms and array of array into a simple array
    # ex: [[a,b],[c,d]] => [a,b,c,d]
    @staticmethod
    def standardizeArray(list):
        resultList = []
        for array in list:
            for elem in array:
                resultList += [elem]
        return resultList

    # This function finds the closest group of humans (and biggest if equality) from each box in boxes
    # the paramater previousCoord is used to keep consistancy in moves : if a group of human is closer than other groups
    # from a box but farer than the previous box, then the goal is not to got toward this group of human
    def findTargetHumans(self, boxes, previousCoord):
        H=self.currentmap.humans
        boxWithTargetHumans = []
        for box in boxes:
            targetHumans = []
            closestHumans = []
            for h in H:
                if max(abs(previousCoord[0] - h[1][0]),abs(previousCoord[1] - h[1][1])) > max(abs(box[0] - h[1][0]), abs(box[1] - h[1][1])):
                    if closestHumans == []:
                        closestHumans = [h[0],[h[1][0], h[1][1]]]
                        targetHumans = [[h[0],[h[1][0], h[1][1]]]]
                    else:
                        if max(abs(box[0] - closestHumans[1][0]), abs(box[1] - closestHumans[1][1])) == max(abs(box[0] - h[1][0]), abs(box[1] - h[1][1])):
                            targetHumans.append([h[0],[h[1][0], h[1][1]]])
                        elif max(abs(box[0] - closestHumans[1][0]), abs(box[1] - closestHumans[1][1])) >= max(abs(box[0] - h[1][0]), abs(box[1] - h[1][1])):
                            closestHumans = [h[0],[h[1][0], h[1][1]]]
                            targetHumans = [[h[0],[h[1][0], h[1][1]]]]

            boxWithTargetHumans += [[box, targetHumans]]

        return boxWithTargetHumans

    def arrayIsInList(self, array, list):
        for elem in list:
            if np.array_equal(np.array(array), np.array(elem)):
                return True
        return False

    # This function create MOV that can be sent to server from an array of moves
    def createMOV(self, moves):
        movCmd = []
        movNb = 0
        if self.side==1:
            groups = self.currentmap.werewolves
        else:
            groups = self.currentmap.vampires

        for i in range(len(groups)):
            for el in moves[i]:
                movCmd += [groups[i][1][0], groups[i][1][1], el[0], el[1][0], el[1][1]]
                movNb += 1

        return [movNb, movCmd]

    @staticmethod
    def deleteZeroMoves(moves):
        nonZeroMoves = []
        for move in moves:
            nonZeroMove = []
            for tuple in move:
                if tuple[0] != 0:
                    nonZeroMove += [tuple]
            nonZeroMoves += [nonZeroMove]

        return nonZeroMoves

    # Returns moves to the server
    def returnMoves(self):
        moves=[]
        if self.side==1:
            for i in range(len(self.currentmap.werewolves)):
                boxes = self.generateValueBoxes(i)
                valueMoves = self.generateValueMoves(boxes, self.currentmap.werewolves[i][0])
                moves += [self.chooseMove(valueMoves, boxes, self.currentmap.werewolves[i])]
        else:
            for i in range(len(self.currentmap.vampires)):
                boxes = self.generateValueBoxes(i)
                valueMoves = self.generateValueMoves(boxes, self.currentmap.vampires[i][0])
                moves += [self.chooseMove(valueMoves, boxes, self.currentmap.vampires[i])]

        # print Brain.deleteZeroMoves(moves)

        return self.createMOV(Brain.deleteZeroMoves(moves))
