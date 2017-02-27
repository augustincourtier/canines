import map
import numpy as np
from copy import deepcopy
from random import randint
import operator
from src.utils import min_index, prob_against_humans
from src.heuristics import *


class Brain:

    def __init__(self, currentmap, side):
        self.currentmap = currentmap
        self.side = side  # 1=werewolf, -1=vampires

    ####
    # GENERAL FUNCTIONS OF BRAIN
    ####

    def score(self):
        ww = self.currentmap.werewolf
        vamp = self.currentmap.vamp
        nb_ww = 0
        nb_vamp = 0
        for i in ww:
            nb_ww = nb_ww + i[2]
        for j in vamp:
            nb_vamp = nb_vamp + j[2]
        return self.side * (nb_ww - nb_vamp)

    ####
    # ALEX AND PIERRE tests
    ####

    def movegrpCond(self, i):
        maps = []
        H = self.currentmap.humans
        map = self.currentmap
        if self.side == 1:
            player_pawns = map.werewolves[i]
        else:
            player_pawns = map.vampires[i]
        coordX = player_pawns[1][0]
        coordY = player_pawns[1][1]
        for j in range(1,player_pawns[0]+1):
            for k in [-1,0,1]:
                for l in [-1,0,1]:
                    for h in H:
                        if max(abs(coordX - h[1][0]),abs(coordY - h[1][1])) > max(abs(coordX + k - h[1][0]), abs(coordY + l - h[1][1])):
                            tempmap = deepcopy(map)
                            #TODO: Rassembler les fonctions move_vampires/move_werewolves add_vampires/add_werewolves etc en une avec param
                            if self.side == 1:
                                tempmap.move_vampires(j, coordX + k, coordY + l, i)
                            else:
                                tempmap.move_werewolves(j, coordX + k, coordY + l, i)
                            if not list_in_list_of_lists(tempmap, maps):
                                maps.append(tempmap)
        return maps

    def create_maps_from_map(self):
        maps = []
        if self.side == 1:
            for i in range(len(self.currentmap.werewolves)):
                maps += (self.movegrpCond(i))
        elif self.side == 0:
            for i in range(len(self.currentmap.vampires)):
                maps += (self.movegrpCond(i))
        return maps

    ####
    # ALEX AND ELIE tests
    ####

    # this function gives interesting boxes around one group
    def generateValueBoxes(self, i):
        boxes = [] # this arrays stores interesting boxes around a group
        H = self.currentmap.humans
        map = self.currentmap
        if self.side == 1:
            group, enemies = map.werewolves[i], map.vampires
        else:
            group, enemies = map.vampires[i], map.werewolves
        coordX = group[1][0]
        coordY = group[1][1]

        for j in range(1,group[0]+1):
            for k in [-1,0,1]:
                for l in [-1,0,1]:
                    if len(H) > 0:
                        for h in H:
                            # box is interesting if going there make a group closer to humans TODO: also to ennemies or allies
                            if max(abs(coordX - h[1][0]),abs(coordY - h[1][1])) > max(abs(coordX + k - h[1][0]), abs(coordY + l - h[1][1])):
                                if coordX + k <= map.size_x-1 and coordX + k >= 0 and coordY + l <= map.size_y-1 and coordY + l >= 0:
                                    if not list_in_list_of_lists([coordX + k, coordY + l], boxes):
                                        boxes += [[coordX + k, coordY + l]]
                            for e in enemies:
                                if max(abs(coordX - e[1][0]),abs(coordY - e[1][1])) > max(abs(coordX + k - e[1][0]), abs(coordY + l - e[1][1])):
                                    if coordX + k <= map.size_x-1 and coordX + k >= 0 and coordY + l <= map.size_y-1 and coordY + l >= 0:
                                        if not list_in_list_of_lists([coordX + k, coordY + l], boxes):
                                            boxes += [[coordX + k, coordY + l]]
                    else:
                        for e in enemies:
                            if max(abs(coordX - e[1][0]),abs(coordY - e[1][1])) > max(abs(coordX + k - e[1][0]), abs(coordY + l - e[1][1])):
                                if coordX + k <= map.size_x-1 and coordX + k >= 0 and coordY + l <= map.size_y-1 and coordY + l >= 0:
                                    if not list_in_list_of_lists([coordX + k, coordY + l], boxes):
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
        possibleTuples = list_of_lists_to_list(possibleTuples)

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

        if len(self.currentmap.humans) > 0:
            # Filters move to keep first those which allow to kill an adjacent group of enemy
            valueMovesFiltered = []
            for move in valueMoves:
                filteredMove = self.enemyFilter(move)
                if len(filteredMove) > 0:
                    valueMovesFiltered.append(filteredMove)

            if len(valueMovesFiltered) > 0:
                moveFiltered = valueMovesFiltered
            else:
                moveFiltered = valueMoves

            # print len(deleteZeroMoves(moveFiltered))
            # #
            # print "-------------------"
            # print "heuristic 1"
            # print "-------------------"

            # first heuristic
            newMoves1 = []
            scoreMax = 0
            scoreDistanceMax = 0
            for move in moveFiltered:

                heuristic1 =  self.heuristic1(move)
                # if heuristic1[0] == 14:
                #     print "-----------"
                #     print deleteZeroMoves([move])
                #     print self.heuristic1(move)
                #     print "-----------"

                # print "-----------"
                # print deleteZeroMoves([move])
                # print self.heuristic1(move)
                # print "-----------"

                if scoreMax == 0:
                    scoreMax = heuristic1[0]
                    scoreDistanceMax = heuristic1[1]
                    newMoves1 = [move]
                else:
                    if scoreMax == heuristic1[0]:
                        if scoreDistanceMax == heuristic1[1]:
                            newMoves1.append(move)
                        elif scoreDistanceMax < heuristic1[1]:
                            scoreDistanceMax = heuristic1[1]
                            newMoves1 = [move]
                    elif scoreMax < heuristic1[0]:
                        scoreMax = heuristic1[0]
                        scoreDistanceMax = heuristic1[1]
                        newMoves1 = [move]
            #
            print("results")
            print(delete_zero_moves(newMoves1))
            print(len(newMoves1))
            #
            # print "-------------------"
            # print "heuristic 2"
            # print "-------------------"

            # second heuristic
            newMoves2 = []
            scoreMax = 0
            for move in newMoves1:
                # print deleteZeroMoves([move])
                # print self.heuristic2(move, boxes, group[1])
                heuristic2 = self.heuristic2(move, boxes, group[1])
                if scoreMax == 0:
                    scoreMax = heuristic2
                    newMoves2 = [move]
                else:
                    if scoreMax == heuristic2:
                        newMoves2.append(move)
                    elif scoreMax < heuristic2:
                        scoreMax = heuristic2
                        newMoves2 = [move]

            # print "results"
            # print deleteZeroMoves(newMoves2)
            # print len(newMoves2)

            newMoves2 = self.splitFilter(delete_zero_moves(newMoves2))
            # print "---------------------"
            # print newMoves2

            # Move is chosen randomly into the last sublist
            i = randint(0,len(newMoves2)-1)
            # print len(newMoves2)
            return newMoves2[i]
        else:
            valueMoves = self.splitFilter(delete_zero_moves(valueMoves))
            # Move is chosen randomly into the last sublist
            i = randint(0,len(valueMoves)-1)
            # print len(newMoves2)
            return valueMoves[i]

    # This filter chooses moves that allow to kill directly a group of ennemy
    def enemyFilter(self, move):

        if self.side == 1:
            enemies = self.currentmap.vampires
        else:
            enemies = self.currentmap.werewolves

        for subgroup in move:
            for enemy in enemies:
                if float(subgroup[0]) >= 1.5*float(enemy[0]) and max(abs(subgroup[1][0]-enemy[1][0]),abs(subgroup[1][1]-enemy[1][1])) == 0:
                    return move

        return []

    # This function takes equivalent moves and return those where the group is the less splitted
    def splitFilter(self, moves):
        filteredMoves = []
        minSplit = 0

        for move in moves:
            if len(filteredMoves) == 0:
                filteredMoves = [move]
                minSplit = len(move)
            else:
                if len(move) == minSplit:
                    filteredMoves += [move]
                elif len(move) < minSplit:
                    filteredMoves = [move]

        return filteredMoves

    # This heuristic evulates what groups of human can the group reach before the ennemy and which of these
    # groups can be beaten with the amount of allies
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
                        if not list_in_list_of_lists(target[1], [x[0][1] for x in goodTargets]) and subgroup[0] > 0:
                            distTarget = float(max(abs(target[1][0]-subgroup[1][0]),abs(target[1][1]-subgroup[1][1]))) + 1
                            goodTargets += [[target, distTarget]]
                            score += target[0]
                        else:
                            for targetWithDistance in goodTargets:
                                if targetWithDistance[0] == target:
                                    distTarget = float(max(abs(target[1][0]-subgroup[1][0]),abs(target[1][1]-subgroup[1][1]))) + 1
                                    if distTarget < targetWithDistance[1]:
                                        targetWithDistance[1] = distTarget

        # Taking distances into account
        distanceScore = 0
        for targetWithDistance in goodTargets:
            distanceScore += float(targetWithDistance[0][0])/float(targetWithDistance[1])

        return [score, distanceScore]

    # This heuristic finds what group of human is naturally targeted on each box and evaluate the number of
    # human that can be eaten when placing a group on a box, considering distances and the amount of the group
    def heuristic2(self, move, boxes, previousCoord):
        boxWithTargetHumans = self.findTargetHumans(boxes, previousCoord)
        score = 0
        visitedTarget = []
        for subgroup in move:
            attack = subgroup[0]
            for boxWithTarget in boxWithTargetHumans:
                if len(boxWithTarget[1]) == 0:
                    score += 0
                elif subgroup[1] == boxWithTarget[0]:
                    peopleInTargets = []
                    for target in sort_human_by_number(boxWithTarget[1]):
                        if not list_in_list_of_lists(target[1], visitedTarget):
                            if attack >= target[0]:
                                attack -= target[0]
                                visitedTarget += [target[1]]

                                distanceTargets = max(abs(target[1][0]-subgroup[1][0]),abs(target[1][1]-subgroup[1][1])) + 1
                                score += float(target[0])/float(distanceTargets)

        # print ('score final', score)
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
                result += Brain.distribute(i, Brain.generateMoves(list[1:]))
        return result

    # This function is used to distribute a value on an array of arrays
    # ex : [1,[1,2],[3,4]] => [[1,1,2],[1,3,4]]
    @staticmethod
    def distribute(element, lists):
        new_list = []
        if not lists:
            return [[element]]
        elif isinstance(lists[0], int):
            new_list = [lists+[element]]
            return new_list
        else:
            for list in lists:
                list += [element]
                new_list += [list]
            return new_list

    # This function finds the closest group of humans (and biggest if equality) from each box in boxes
    # the paramater previousCoord is used to keep consistancy in moves : if a group of human is closer than other groups
    # from a box but farer than the previous box, then the goal is not to got toward this group of human
    def findTargetHumans(self, boxes, previousCoord):
        H = self.currentmap.humans
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

    # Returns moves to the server
    def return_moves(self):
        moves = []
        if self.side == 1:
            for i in range(len(self.currentmap.werewolves)):
                boxes = self.generateValueBoxes(i)
                valueMoves = self.generateValueMoves(boxes, self.currentmap.werewolves[i][0])
                moves += [self.chooseMove(valueMoves, boxes, self.currentmap.werewolves[i])]
        else:
            for i in range(len(self.currentmap.vampires)):
                boxes = self.generateValueBoxes(i)
                valueMoves = self.generateValueMoves(boxes, self.currentmap.vampires[i][0])
                moves += [self.chooseMove(valueMoves, boxes, self.currentmap.vampires[i])]

        return self.createMOV(delete_zero_moves(moves))
