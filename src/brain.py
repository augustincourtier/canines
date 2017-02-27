import map
import numpy as np
from copy import deepcopy
from random import randint
from src.prepare_moves import *


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

    def generate_value_boxes(self, given_group):
        """this function gives interesting boxes around one group"""
        boxes = [] # this arrays stores interesting boxes around a group
        H = self.currentmap.humans
        given_map = self.currentmap
        max_x, max_y = given_map.size_x, given_map.size_y
        if self.side == 1:
            group, enemies = given_map.werewolves[given_group], given_map.vampires
        else:
            group, enemies = given_map.vampires[given_group], given_map.werewolves
        coordX, coordY = group[1][0], group[1][1]

        for j in range(1, group[0]+1):
            for k in [-1, 0, 1]:
                for l in [-1, 0, 1]:
                    if len(H) > 0:
                        for h in H:
                            # box is interesting if going there make a group closer to humans TODO: also to ennemies or allies
                            if max(abs(coordX - h[1][0]), abs(coordY - h[1][1])) > max(abs(coordX + k - h[1][0]), abs(coordY + l - h[1][1])):
                                if (0 <= coordX + k <= max_x-1) and (0 <= coordY + l <= max_y-1):
                                    if not list_in_list_of_lists([coordX + k, coordY + l], boxes):
                                        boxes += [[coordX + k, coordY + l]]
                            for e in enemies:
                                if max(abs(coordX - e[1][0]),abs(coordY - e[1][1])) > max(abs(coordX + k - e[1][0]), abs(coordY + l - e[1][1])):
                                    if (0 <= coordX + k <= max_x - 1) and (0 <= coordY + l <= max_y - 1):
                                        if not list_in_list_of_lists([coordX + k, coordY + l], boxes):
                                            boxes += [[coordX + k, coordY + l]]
                    else:
                        for e in enemies:
                            if max(abs(coordX - e[1][0]),abs(coordY - e[1][1])) > max(abs(coordX + k - e[1][0]), abs(coordY + l - e[1][1])):
                                if (0 <= coordX + k <= max_x - 1) and (0 <= coordY + l <= max_y - 1):
                                    if not list_in_list_of_lists([coordX + k, coordY + l], boxes):
                                        boxes += [[coordX + k, coordY + l]]
        return boxes

    def choose_move(self, value_moves, boxes, group):

        if len(self.currentmap.humans) > 0:  # If there are still humans on the map

            # Filters move to keep first those which allow to kill an adjacent group of enemy
            value_moves_filtered = []
            for move in value_moves:
                filtered_move = self.enemy_filter(move)
                if len(filtered_move) > 0:
                    value_moves_filtered.append(filtered_move)
            if len(value_moves_filtered) > 0:
                move_filtered = value_moves_filtered
            else:
                move_filtered = value_moves

            # first heuristic
            new_moves1 = []
            score_max = 0
            score_distance_max = 0
            for move in move_filtered:
                heuristic1 = self.heuristic1(move)
                if score_max == 0:
                    score_max = heuristic1[0]
                    score_distance_max = heuristic1[1]
                    new_moves1 = [move]
                else:
                    if score_max == heuristic1[0]:
                        if score_distance_max == heuristic1[1]:
                            new_moves1.append(move)
                        elif score_distance_max < heuristic1[1]:
                            score_distance_max = heuristic1[1]
                            new_moves1 = [move]
                    elif score_max < heuristic1[0]:
                        score_max = heuristic1[0]
                        score_distance_max = heuristic1[1]
                        new_moves1 = [move]

            # second heuristic
            new_moves2 = []
            score_max = 0
            for move in new_moves1:
                heuristic2 = self.heuristic2(move, boxes, group[1])
                if score_max == 0:
                    score_max = heuristic2
                    new_moves2 = [move]
                else:
                    if score_max == heuristic2:
                        new_moves2.append(move)
                    elif score_max < heuristic2:
                        score_max = heuristic2
                        new_moves2 = [move]
            new_moves2 = split_filter(delete_zero_moves(new_moves2))

            i = randint(0, len(new_moves2)-1)  # Move is chosen randomly into the last sublist
            return new_moves2[i]
        else:
            value_moves = split_filter(delete_zero_moves(value_moves))
            i = randint(0, len(value_moves) - 1)  # Move is chosen randomly into the last sublist
            return value_moves[i]

    def enemy_filter(self, move):
        """This filter chooses moves that allow to kill directly a group of enemies"""
        if self.side == 1:
            enemies = self.currentmap.vampires
        else:
            enemies = self.currentmap.werewolves
        for subgroup in move:
            for enemy in enemies:
                if float(subgroup[0]) >= 1.5*float(enemy[0]) \
                        and max(abs(subgroup[1][0]-enemy[1][0]), abs(subgroup[1][1]-enemy[1][1])) == 0:
                    return move
        return []

    def heuristic1(self, move):
        """This heuristic evulates what groups of human can the group reach before the ennemy and which of these
        groups can be beaten with the amount of allies"""
        score, good_targets = 0, []
        targets = self.currentmap.humans
        for subgroup in move:
            if self.side == 1:
                enemies = self.currentmap.vampires
            else:
                enemies = self.currentmap.werewolves
            for target in targets:
                dist_target_enemy = []
                for enemy in enemies:
                    dist_target_enemy += [max(abs(target[1][0]-enemy[1][0]), abs(target[1][1]-enemy[1][1]))]
                dist_min_enemy = min(dist_target_enemy)
                if dist_min_enemy <= max(abs(target[1][0]-subgroup[1][0]), abs(target[1][1]-subgroup[1][1])):
                    score += 0
                else:
                    if subgroup[0] < target[0]:
                        score += 0
                    else:
                        if not list_in_list_of_lists(target[1], [x[0][1] for x in good_targets]) and subgroup[0] > 0:
                            dist_target = float(max(abs(target[1][0]-subgroup[1][0]), abs(target[1][1]-subgroup[1][1]))) + 1
                            good_targets += [[target, dist_target]]
                            score += target[0]
                        else:
                            for targetWithDistance in good_targets:
                                if targetWithDistance[0] == target:
                                    dist_target = float(max(abs(target[1][0]-subgroup[1][0]), abs(target[1][1]-subgroup[1][1]))) + 1
                                    if dist_target < targetWithDistance[1]:
                                        targetWithDistance[1] = dist_target

        # Taking distances into account
        distance_score = 0
        for targetWithDistance in good_targets:
            distance_score += float(targetWithDistance[0][0])/float(targetWithDistance[1])

        return [score, distance_score]

    def heuristic2(self, move, boxes, previousCoord):
        """This heuristic finds what group of human is naturally targeted on each box and evaluate the number of
        human that can be eaten when placing a group on a box, considering distances and the amount of the group"""
        box_with_target_humans = self.find_target_humans(boxes, previousCoord)
        score = 0
        visited_target = []
        for subgroup in move:
            attack = subgroup[0]
            for boxWithTarget in box_with_target_humans:
                if len(boxWithTarget[1]) == 0:
                    score += 0
                elif subgroup[1] == boxWithTarget[0]:
                    peopleInTargets = []
                    for target in sort_human_by_number(boxWithTarget[1]):
                        if not list_in_list_of_lists(target[1], visited_target):
                            if attack >= target[0]:
                                attack -= target[0]
                                visited_target += [target[1]]

                                distanceTargets = max(abs(target[1][0]-subgroup[1][0]),abs(target[1][1]-subgroup[1][1])) + 1
                                score += float(target[0])/float(distanceTargets)

        # print ('score final', score)
        return score

    def find_target_humans(self, boxes, previous_coord):
        """This function finds the closest group of humans (and biggest if equality) from each box in boxes
        the paramater previousCoord is used to keep consistancy in moves : if a group of human is closer than other groups
        from a box but farer than the previous box, then the goal is not to got toward this group of human"""
        H = self.currentmap.humans
        box_with_target_humans = []
        for box in boxes:
            target_humans = []
            closest_humans = []
            for h in H:
                if max(abs(previous_coord[0] - h[1][0]), abs(previous_coord[1] - h[1][1])) > max(abs(box[0] - h[1][0]), abs(box[1] - h[1][1])):
                    if not closest_humans:
                        closest_humans = [h[0],[h[1][0], h[1][1]]]
                        target_humans = [[h[0],[h[1][0], h[1][1]]]]
                    else:
                        if max(abs(box[0] - closest_humans[1][0]), abs(box[1] - closest_humans[1][1])) == max(abs(box[0] - h[1][0]), abs(box[1] - h[1][1])):
                            target_humans.append([h[0],[h[1][0], h[1][1]]])
                        elif max(abs(box[0] - closest_humans[1][0]), abs(box[1] - closest_humans[1][1])) >= max(abs(box[0] - h[1][0]), abs(box[1] - h[1][1])):
                            closest_humans = [h[0],[h[1][0], h[1][1]]]
                            target_humans = [[h[0],[h[1][0], h[1][1]]]]

            box_with_target_humans += [[box, target_humans]]

        return box_with_target_humans

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
                boxes = self.generate_value_boxes(i)
                value_moves = generate_value_moves(boxes, self.currentmap.werewolves[i][0])
                moves += [self.choose_move(value_moves, boxes, self.currentmap.werewolves[i])]
        else:
            for i in range(len(self.currentmap.vampires)):
                boxes = self.generate_value_boxes(i)
                value_moves = generate_value_moves(boxes, self.currentmap.vampires[i][0])
                moves += [self.choose_move(value_moves, boxes, self.currentmap.vampires[i])]

        return self.createMOV(delete_zero_moves(moves))
