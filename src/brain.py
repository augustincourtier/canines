# -*- coding: utf-8 -*-

import src.map
import numpy as np
from copy import deepcopy
from random import randint
from .prepare_moves import *
from more_itertools import unique_everseen
from .map_generator import MapGenerator


class Brain:
    def __init__(self, currentmap, side):
        self.currentmap = currentmap
        self.side = side

    def is_werewolf(self):
        return self.side == 1

    def generate_value_boxes_and_weight(self, given_group):
        """this function gives interesting boxes around one group and the weight of the humans / enemies
        targeted on this boxes"""
        value_boxes_and_weight = [] # this arrays stores the weights
        friend_coords = [] # this arrays stores the coords of the allies

        H = self.currentmap.humans
        given_map = self.currentmap
        max_x, max_y = given_map.size_x, given_map.size_y

        # looking for the size information
        if Brain.is_werewolf(self):
            group, enemies = given_map.werewolves[given_group], given_map.vampires
            for werewolf in given_map.werewolves:
                friend_coords.append(werewolf[1])
        else:
            group, enemies = given_map.vampires[given_group], given_map.werewolves
            for vampire in given_map.vampires:
                friend_coords.append(vampire[1])

        coordX, coordY = group[1][0], group[1][1]

        for k in [-1, 0, 1]:
            for l in [-1, 0, 1]:
                is_value_box = False # Coodr tested is a value box
                weight_for_this_coord = []
                if len(H) > 0:
                    for h in H:
                        # box is interesting if going there make a group closer to humans
                        if max(abs(coordX - h[1][0]), abs(coordY - h[1][1])) > max(abs(coordX + k - h[1][0]), abs(coordY + l - h[1][1])):
                            if (0 <= coordX + k <= max_x-1) and (0 <= coordY + l <= max_y-1):
                                if not list_in_list_of_lists([coordX + k, coordY + l], friend_coords):
                                    is_value_box = True
                                    if not h[0] in weight_for_this_coord:
                                        weight_for_this_coord += [h[0]]

                        for e in enemies:
                            if max(abs(coordX + k - e[1][0]), abs(coordY + l - e[1][1])) == 0:
                                is_value_box = True
                                if not e[0] in weight_for_this_coord:
                                    weight_for_this_coord += [e[0]]
                # box is interesting if going there make a group closer to enemies TODO : allies
                else:
                    for e in enemies:
                        if max(abs(coordX - e[1][0]),abs(coordY - e[1][1])) > max(abs(coordX + k - e[1][0]), abs(coordY + l - e[1][1])):
                            if (0 <= coordX + k <= max_x - 1) and (0 <= coordY + l <= max_y - 1):
                                if not list_in_list_of_lists([coordX + k, coordY + l], friend_coords):
                                    is_value_box = True
                                    if not e[0] in weight_for_this_coord:
                                        weight_for_this_coord += [e[0]]
                if is_value_box == True:
                    value_boxes_and_weight.append([[coordX + k,coordY + l ]] +[weight_for_this_coord+[0]+[group[0]]]) # Create a list of weights and value boxes
        # print(value_boxes_and_weight)
        return value_boxes_and_weight

    def join_allies(self, given_group):
        """this function gives a move that allow to join a group of allies"""
        given_map = self.currentmap
        max_x, max_y = given_map.size_x, given_map.size_y
        coordX, coordY = given_group[1][0], given_group[1][1]
        allies = []

        if Brain.is_werewolf(self):
            for werewolf in given_map.werewolves:
                allies.append(werewolf)
        else:
            for vampire in given_map.vampires:
                allies.append(vampire)

        minDist = 0
        move = []
        for k in [-1, 0, 1]:
            for l in [-1, 0, 1]:
                for allie in allies:
                    if max(abs(coordX - allie[1][0]),abs(coordY - allie[1][1])) > max(abs(coordX + k - allie[1][0]), abs(coordY + l - allie[1][1])):
                        if (0 <= coordX + k <= max_x - 1) and (0 <= coordY + l <= max_y - 1):
                            if (minDist == 0) or (max(abs(coordX + k - allie[1][0]), abs(coordY + l - allie[1][1])) < minDist):
                                minDist = max(abs(coordX + k - allie[1][0]), abs(coordY + l - allie[1][1]))
                                move = [given_group[0], [coordX + k, coordY + l]]

        return [[move]]

    def generate_value_boxes(self, given_group):
        """this function gives interesting boxes around one group"""
        boxes = []  # this arrays stores interesting boxes around a group
        friend_coords = []
        H = self.currentmap.humans
        given_map = self.currentmap
        max_x, max_y = given_map.size_x, given_map.size_y

        if Brain.is_werewolf(self):
            group, enemies = given_map.werewolves[given_group], given_map.vampires
            for werewolf in given_map.werewolves:
                friend_coords.append(werewolf[1])
        else:
            group, enemies = given_map.vampires[given_group], given_map.werewolves
            for vampire in given_map.vampires:
                friend_coords.append(vampire[1])
        coordX, coordY = group[1][0], group[1][1]

        for j in range(1, group[0]+1):
            for k in [-1, 0, 1]:
                for l in [-1, 0, 1]:
                    if len(H) > 0:
                        for h in H:
                            # box is interesting if going there make a group closer to humans
                            # TODO: also to ennemies or allies
                            if max(abs(coordX - h[1][0]), abs(coordY - h[1][1])) > max(abs(coordX + k - h[1][0]), abs(coordY + l - h[1][1])):
                                if (0 <= coordX + k <= max_x-1) and (0 <= coordY + l <= max_y-1):
                                    if not list_in_list_of_lists([coordX + k, coordY + l], boxes):
                                        if not list_in_list_of_lists([coordX + k, coordY + l], friend_coords):
                                            boxes += [[coordX + k, coordY + l]]
                            for e in enemies:
                                if max(abs(coordX - e[1][0]),abs(coordY - e[1][1])) > max(abs(coordX + k - e[1][0]), abs(coordY + l - e[1][1])):
                                    if (0 <= coordX + k <= max_x - 1) and (0 <= coordY + l <= max_y - 1):
                                        if not list_in_list_of_lists([coordX + k, coordY + l], boxes):
                                            if not list_in_list_of_lists([coordX + k, coordY + l], friend_coords):
                                                boxes += [[coordX + k, coordY + l]]
                    else:
                        for e in enemies:
                            if max(abs(coordX - e[1][0]),abs(coordY - e[1][1])) > max(abs(coordX + k - e[1][0]), abs(coordY + l - e[1][1])):
                                if (0 <= coordX + k <= max_x - 1) and (0 <= coordY + l <= max_y - 1):
                                    if not list_in_list_of_lists([coordX + k, coordY + l], boxes):
                                        if not list_in_list_of_lists([coordX + k, coordY + l], friend_coords):
                                            boxes += [[coordX + k, coordY + l]]
        return boxes

    def choose_move(self, value_moves, boxes, group):
        """Generating moves according to adjacent enemies (if any) or humans on the map."""
        if len(self.currentmap.humans) > 0:  # If there are still humans on the map

            # Filters moves to first keep those which allow to kill an adjacent group of enemy (if any)
            value_moves_filtered = []
            print('move 0 :', len(value_moves))
            for move in value_moves:
                filtered_move = self.enemy_filter(move)
                if len(filtered_move) > 0:
                    value_moves_filtered.append(filtered_move)

            # Storing moves in move_filtered
            # Will only attack if adjacent enemies !
            if len(value_moves_filtered) > 0:
                move_filtered = value_moves_filtered
            else:
                move_filtered = value_moves

            # # first heuristic
            # new_moves1 = []
            # score_max = 0
            # score_distance_max = 0
            # for move in move_filtered:
            #     heuristic1 = self.heuristic1(move)
            #     if score_max == 0:
            #         score_max = heuristic1[0]
            #         score_distance_max = heuristic1[1]
            #         new_moves1 = [move]
            #     else:
            #         if score_max == heuristic1[0]:
            #             if score_distance_max == heuristic1[1]:
            #                 new_moves1.append(move)
            #             elif score_distance_max < heuristic1[1]:
            #                 score_distance_max = heuristic1[1]
            #                 new_moves1 = [move]
            #         elif score_max < heuristic1[0]:
            #             score_max = heuristic1[0]
            #             score_distance_max = heuristic1[1]
            #             new_moves1 = [move]
            # print('new move 1 :' ,len(new_moves1))

            # second heuristic
            heuristic_move = []
            score_max = 0
            for move in move_filtered:
                heuristic = self.heuristic(move, boxes, group[1])
                if score_max == 0:
                    score_max = heuristic
                    heuristic_move = [move]
                else:
                    if score_max == heuristic:
                        heuristic_move.append(move)
                    elif score_max < heuristic:
                        score_max = heuristic
                        heuristic_move = [move]
            heuristic_move = split_filter(delete_zero_moves(heuristic_move))

            if len(heuristic_move) == 0:
                heuristic_move = self.join_allies(group)

            # i = randint(0, len(heuristic_move)-1)  # Move is chosen randomly into the last sublist

            # print('new move 2 :' ,len(heuristic_move))
            # print(heuristic_move[i])
            return heuristic_move
        else:
            if Brain.is_werewolf(self):
                if len(self.currentmap.werewolves) > 1:
                    value_moves = self.join_allies(group)
                else:
                    value_moves = split_filter(delete_zero_moves(value_moves))
            else:
                if len(self.currentmap.vampires) > 1:
                    value_moves = self.join_allies(group)
                else:
                    value_moves = split_filter(delete_zero_moves(value_moves))

            # i = randint(0, len(value_moves) - 1)  # Move is chosen randomly into the last sublist

            # print(value_moves[i])
            return value_moves

    def enemy_filter(self, move):
        """This filter chooses moves that allow to kill directly a group of enemies"""
        if Brain.is_werewolf(self):
            enemies = self.currentmap.vampires
        else:
            enemies = self.currentmap.werewolves
        for subgroup in move:
            for enemy in enemies:
                if float(subgroup[0]) >= 1.5*float(enemy[0]) \
                        and max(abs(subgroup[1][0]-enemy[1][0]), abs(subgroup[1][1]-enemy[1][1])) == 0:
                    return move
        return []

    # def heuristic1(self, move):
    #     """This heuristic evulates what groups of human can the group reach before the ennemy and which of these
    #     groups can be beaten with the amount of allies"""
    #     score, good_targets = 0, []
    #     targets = self.currentmap.humans
    #     for subgroup in move:
    #         if Brain.is_werewolf(self):
    #             enemies = self.currentmap.vampires
    #         else:
    #             enemies = self.currentmap.werewolves
    #         for target in targets:
    #             dist_target_enemy = []
    #             for enemy in enemies:
    #                 dist_target_enemy += [max(abs(target[1][0]-enemy[1][0]), abs(target[1][1]-enemy[1][1]))]
    #             dist_min_enemy = min(dist_target_enemy)
    #             if dist_min_enemy <= max(abs(target[1][0]-subgroup[1][0]), abs(target[1][1]-subgroup[1][1])):
    #                 score += 0
    #             else:
    #                 if subgroup[0] < target[0]:
    #                     score += 0
    #                 else:
    #                     if not list_in_list_of_lists(target[1], [x[0][1] for x in good_targets]) and subgroup[0] > 0:
    #                         dist_target = float(max(abs(target[1][0]-subgroup[1][0]), abs(target[1][1]-subgroup[1][1]))) + 1
    #                         good_targets += [[target, dist_target]]
    #                         score += target[0]
    #                     else:
    #                         for targetWithDistance in good_targets:
    #                             if targetWithDistance[0] == target:
    #                                 dist_target = float(max(abs(target[1][0]-subgroup[1][0]), abs(target[1][1]-subgroup[1][1]))) + 1
    #                                 if dist_target < targetWithDistance[1]:
    #                                     targetWithDistance[1] = dist_target
    #
    #     # Taking distances into account
    #     distance_score = 0
    #     for targetWithDistance in good_targets:
    #         distance_score += float(targetWithDistance[0][0])/float(targetWithDistance[1])
    #
    #     return [score, distance_score]

    def heuristic(self, move, boxes, previousCoord):
        """This heuristic finds what group of human is naturally targeted on each box and evaluate the number of
        human that can be eaten when placing a group on a box, considering distances and the amount of the group"""
        box_with_target_humans = self.find_target_humans(boxes, previousCoord)
        targets = self.currentmap.humans
        score = 0
        visited_target = []
        for subgroup in move:
            if Brain.is_werewolf(self):
                enemies = self.currentmap.vampires
            else:
                enemies = self.currentmap.werewolves
            for target in targets:
                dist_target_enemy = []

                # Getting minimal distance between all enemies and the group of humans
                for enemy in enemies:
                    dist_target_enemy += [max(abs(target[1][0]-enemy[1][0]), abs(target[1][1]-enemy[1][1]))]
                dist_min_enemy = min(dist_target_enemy)

                # Comparing this distance to our group position
                # If inferior, not interesting
                if dist_min_enemy <= max(abs(target[1][0]-subgroup[1][0]), abs(target[1][1]-subgroup[1][1])):
                    score += 0
                else:
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

    def find_enemies(self):
        """This function returns the coords of enemies groups with the form of a list of lists : [number, [x, y]]"""
        if Brain.is_werewolf(self):
            return self.currentmap.vampires
        else:
            return self.currentmap.werewolves

    def find_our_teams(self):
        """This function returns the coords of enemies groups with the form of a list of lists : [number, [x, y]]"""
        if Brain.is_werewolf(self):
            return self.currentmap.werewolves
        else:
            return self.currentmap.vampires

    # This function create MOV that can be sent to server from an array of moves
    def createMOV(self, moves):
        movCmd = []
        movNb = 0
        if Brain.is_werewolf(self):
            groups = self.currentmap.werewolves
        else:
            groups = self.currentmap.vampires
        # TODO remove print statements when error solved
        # print("Initial groups: ", groups)
        # print("Moves: ", moves)
        for i in range(len(groups)):
            try:
                for el in moves[i]:
                    if check_move_permission(groups[i][0], el[0]):
                        movCmd += [groups[i][1][0], groups[i][1][1], el[0], el[1][0], el[1][1]]
                        movNb += 1
            except KeyError:
                continue

        return [movNb, movCmd]

    def clean_double_moves(self, moves):
        if Brain.is_werewolf(self):
            groups = self.currentmap.werewolves
        else:
            groups = self.currentmap.vampires

        dict_moves = {k: v for k, v in enumerate(moves)}

        for move in moves:
            for el in move:
                for i in range(len(groups)):
                    if el[1][0] == groups[i][1][0] and el[1][1] == groups[i][1][1]:
                        if len(dict_moves) > 1:
                            dict_moves.pop(i, None)

        return dict_moves

    # Returns moves to the server
    def return_moves(self):
        """Returns moves to the server"""
        possible_moves = []
        map_generator = MapGenerator(enemies_coords=self.find_enemies())
        print(Brain.is_werewolf(self))
        if Brain.is_werewolf(self):
            for i in range(len(self.currentmap.werewolves)):
                # Interesting boxes close to human
                boxes = self.generate_value_boxes(i)
                box_and_weight = self.generate_value_boxes_and_weight(i)

                # All possibities of split in those boxes
                value_moves = generate_value_moves(box_and_weight, self.currentmap.werewolves[i][0],
                                                   self.currentmap.humans, self.currentmap.vampires)

                # Calculating most interesting split possibilities for this group
                group_possible_moves = self.choose_move(value_moves, boxes, self.currentmap.werewolves[i])

                # Generating possibility maps
                map_generator.update_maps(subgroup_possible_moves=group_possible_moves)

                # description possible_moves = [ (group_i, [[[split1, [newX1, newY1]], [split1', [newX1', newY1']],
                #                                  [split2, [newX2, newY2]], [split2', [newX2', newY2']]] ), ... ]
                possible_moves += [(i, group_possible_moves, )]
        else:
            for i in range(len(self.currentmap.vampires)):
                # Interesting boxes close to human
                boxes = self.generate_value_boxes(i)
                box_and_weight = self.generate_value_boxes_and_weight(i)

                # All possibities of split in those boxes
                value_moves = generate_value_moves(box_and_weight, self.currentmap.vampires[i][0],
                                                   self.currentmap.humans, self.currentmap.werewolves)

                # Calculating most interesting split possibilities for this group
                group_possible_moves = self.choose_move(value_moves, boxes, self.currentmap.vampires[i])

                # Generating possibility maps
                map_generator.update_maps(subgroup_possible_moves=group_possible_moves)

                # description possible_moves = [ (group_i, [[[split1, [newX1, newY1]], [split1', [newX1', newY1']],
                #                                  [split2, [newX2, newY2]], [split2', [newX2', newY2']]] ), ... ]
                possible_moves += [(i, group_possible_moves,)]

        print("Possible moves :", possible_moves)
        return self.createMOV(self.clean_double_moves(delete_zero_moves(possible_moves)))
