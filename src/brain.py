# -*- coding: utf-8 -*-

import src.map
import numpy as np
from copy import deepcopy
from random import randint
from src.prepare_moves import *
from more_itertools import unique_everseen
import operator
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
                        if max(abs(coordX - e[1][0]),abs(coordY - e[1][1])) != 2 and max(abs(coordX - e[1][0]),abs(coordY - e[1][1])) > max(abs(coordX + k - e[1][0]), abs(coordY + l - e[1][1])):
                            if (0 <= coordX + k <= max_x - 1) and (0 <= coordY + l <= max_y - 1):
                                if not list_in_list_of_lists([coordX + k, coordY + l], friend_coords):
                                    is_value_box = True
                                    if not e[0] in weight_for_this_coord:
                                        weight_for_this_coord += [e[0]]
                if is_value_box == True:
                    value_boxes_and_weight.append([[coordX + k,coordY + l ]] +[weight_for_this_coord+[0]+[group[0]]]) # Create a list of weights and value boxes
        return value_boxes_and_weight

    def attack_weakest_enemy(self, given_group):
        """this function gives a move that allow to attack the weakest group of enemy"""
        given_map = self.currentmap
        max_x, max_y = given_map.size_x, given_map.size_y
        moves = []
        if Brain.is_werewolf(self):
            enemies = given_map.vampires
        else:
            enemies = given_map.werewolves

        coordX, coordY = given_group[1][0], given_group[1][1]

        weakest_enemy = min(enemies, key=operator.itemgetter(0))
        for k in [-1, 0, 1]:
            for l in [-1, 0, 1]:
                if max(abs(coordX - weakest_enemy[1][0]),abs(coordY - weakest_enemy[1][1])) != 2 and max(abs(coordX - weakest_enemy[1][0]),abs(coordY - weakest_enemy[1][1])) > max(abs(coordX + k - weakest_enemy[1][0]), abs(coordY + l - weakest_enemy[1][1])):
                    if (0 <= coordX + k <= max_x - 1) and (0 <= coordY + l <= max_y - 1):
                        moves.append([[given_group[0], [coordX + k, coordY + l]]])

        return moves

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

        if (move == []):
            return []
        else:
            return [[move]]

    def find_group_allies(self, group_coord):
        """Find allies of a group"""
        given_map = self.currentmap
        allies = []
        if Brain.is_werewolf(self):
            for werewolf in given_map.werewolves:
                if (werewolf[1] != group_coord):
                    allies.append(werewolf)
        else:
            for vampire in given_map.vampires:
                if (vampire[1] != group_coord):
                    allies.append(vampire)

        return allies

    def find_target_humans(self, boxes, previous_coord, previous_size):
        """This function finds the closest group of humans (and biggest if equality) from each box in boxes
        the paramater previous_coord is used to keep consistancy in moves : if a group of human is closer than other groups
        from a box but farer than the previous box, then the goal is not to got toward this group of human"""
        H = self.currentmap.humans
        box_with_target_humans = []
        for box in boxes:
            target_humans = []
            closest_humans = []
            for h in H:
                if previous_size >= h[0] and max(abs(previous_coord[0] - h[1][0]), abs(previous_coord[1] - h[1][1])) > max(abs(box[0] - h[1][0]), abs(box[1] - h[1][1])):
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

    def choose_move(self, value_moves, box_and_weight, group):
        """this function chose among good moves based on many filter and a heuristic value"""

        # Retrieving boxes from box_and_weight
        boxes = [x[0] for x in box_and_weight]

        if len(self.currentmap.humans) > 0: # If there are still humans on the map
            # Filters move to keep first those which allow to kill an adjacent group of enemy
            value_moves_filtered = []
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

            # Heuristic
            heuristic_move = []
            score_max = -1
            for move in move_filtered:
                heuristic = self.heuristic(move, boxes, group[1], group[0])
                if score_max == -1:
                    score_max = heuristic
                    heuristic_move = [move]
                else:
                    if score_max == heuristic:
                        heuristic_move.append(move)
                    elif score_max < heuristic:
                        score_max = heuristic
                        heuristic_move = [move]

            heuristic_move = split_filter(delete_zero_moves(heuristic_move))

            # Filters move to prevent a subgroup to suicide on a big group of human
            for move in heuristic_move:
                if not self.survival_filter(move):
                    heuristic_move.remove(move)

            # If Heuristic filter all results OR best heuristic score is null => join allies
            if (len(heuristic_move) == 0 or score_max == 0):
                join_allies_move = self.join_allies(group)
                # If no allies to join, attack weakest enemy !!
                if (len(join_allies_move) == 0):
                    heuristic_move = self.attack_weakest_enemy(group)
                else:
                    heuristic_move = join_allies_move

            # Move is chosen randomly into the last sublist
            if len(heuristic_move) > 0:
                # i = randint(0, len(heuristic_move) - 1)
                return heuristic_move
            else:
                return []

        else: # No humans left
            if Brain.is_werewolf(self):
                if len(self.currentmap.werewolves) > 1:
                    value_moves = self.join_allies(group)
                else:
                    value_moves = split_filter(value_moves)
            else:
                if len(self.currentmap.vampires) > 1:
                    value_moves = self.join_allies(group)
                else:
                    value_moves = split_filter(value_moves)

            # Move is chosen randomly into the last sublist
            if len(value_moves) > 0:
                # i = randint(0, len(value_moves) - 1)
                return value_moves
            else:
                # if no group to join, attack
                coordX, coordY = group[1][0], group[1][1]
                for e in self.find_enemies():
                    if coordX - e[1][0] == 0:
                        if coordY - e[1][1] >= 1:
                            value_moves += [[[group[0], coordX, coordY - 1]]]
                        elif coordY - e[1][1] <= -1:
                            value_moves += [[[group[0], coordX, coordY + 1]]]

                    elif coordY - e[1][1] == 0:
                        if coordX - e[1][0] >= 1:
                            value_moves += [[[group[0], coordX - 1, coordY]]]
                        elif coordX - e[1][0] <= -1:
                            value_moves += [[[group[0], coordX + 1, coordY]]]

                    elif abs(coordX - e[1][0]) == 1 and abs(coordY - e[1][1]) == 1:
                        value_moves += [[[group[0], e[1][0], e[0]]]]
                    else:
                        if coordX - e[1][0] >= 1:
                            x = coordX - 1
                        elif coordX - e[1][0] <= -1:
                            x = coordX +1
                        if coordY - e[1][1] >= 1:
                            y = coordY - 1
                        elif coordY - e[1][1] <= -1:
                            y = coordY +1
                        value_moves += [[[group[0], x, y]]]
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

    def survival_filter(self, move):
        """This filter removes move that lead to go into a group of human too strong"""
        for subgroup in move:
            for human in self.currentmap.humans:
                if float(subgroup[0]) < float(human[0]) \
                        and max(abs(subgroup[1][0]-human[1][0]), abs(subgroup[1][1]-human[1][1])) == 0:
                    return False
        return True

    def heuristic(self, move, boxes, previous_coord, previous_size):
        """This heuristic finds what group of human is naturally targeted on each box and evaluate the number of
        human that can be eaten when placing a group on a box, considering distances and the amount of the group"""
        box_with_target_humans = self.find_target_humans(boxes, previous_coord, previous_size)
        allies = self.find_group_allies(previous_coord)
        if Brain.is_werewolf(self):
            enemies = self.currentmap.vampires
        else:
            enemies = self.currentmap.werewolves
        score = 0
        visited_target = []
        for subgroup in move:
            attack = subgroup[0]
            for box_with_target in box_with_target_humans:
                for target in box_with_target[1]:
                    # Removing targets which are nearer from an enemy
                    dist_target_enemy = []
                    for enemy in enemies:
                        dist_target_enemy += [max(abs(target[1][0]-enemy[1][0]), abs(target[1][1]-enemy[1][1]))]
                    dist_min_enemy = min(dist_target_enemy)
                    if dist_min_enemy <= max(abs(target[1][0]-subgroup[1][0]), abs(target[1][1]-subgroup[1][1])):
                        box_with_target[1].remove(target)
                        continue
                    # Removing targets which are nearer from a viable ally
                    dist_target_allie = []
                    for allie in allies:
                        dist_target_allie += [[max(abs(target[1][0]-allie[1][0]), abs(target[1][1]-allie[1][1])), allie[0]]]
                    if (len(dist_target_allie) > 0):
                        dist_min_allie = min(dist_target_allie, key=operator.itemgetter(0))
                        if dist_min_allie[0] <= max(abs(target[1][0]-subgroup[1][0]), abs(target[1][1]-subgroup[1][1])) and dist_min_allie[1] >= target[0]:
                            box_with_target[1].remove(target)
                            continue
                if len(box_with_target[1]) == 0:
                    score += 0
                elif subgroup[1] == box_with_target[0]:
                    peopleInTargets = []
                    for target in sort_human_by_number(box_with_target[1]):
                        if not list_in_list_of_lists(target[1], visited_target):
                            if attack >= target[0]:
                                attack -= target[0]
                                visited_target += [target[1]]

                                distanceTargets = max(abs(target[1][0]-subgroup[1][0]),abs(target[1][1]-subgroup[1][1])) + 1
                                score += float(target[0])/float(distanceTargets)
        return score

    # def find_target_humans(self, boxes, previous_coord):
    #     """This function finds the closest group of humans (and biggest if equality) from each box in boxes
    #     the paramater previousCoord is used to keep consistancy in moves : if a group of human is closer than other groups
    #     from a box but farer than the previous box, then the goal is not to got toward this group of human"""
    #     H = self.currentmap.humans
    #     box_with_target_humans = []
    #     for box in boxes:
    #         target_humans = []
    #         closest_humans = []
    #         for h in H:
    #             if max(abs(previous_coord[0] - h[1][0]), abs(previous_coord[1] - h[1][1])) > max(abs(box[0] - h[1][0]), abs(box[1] - h[1][1])):
    #                 if not closest_humans:
    #                     closest_humans = [h[0],[h[1][0], h[1][1]]]
    #                     target_humans = [[h[0],[h[1][0], h[1][1]]]]
    #                 else:
    #                     if max(abs(box[0] - closest_humans[1][0]), abs(box[1] - closest_humans[1][1])) == max(abs(box[0] - h[1][0]), abs(box[1] - h[1][1])):
    #                         target_humans.append([h[0],[h[1][0], h[1][1]]])
    #                     elif max(abs(box[0] - closest_humans[1][0]), abs(box[1] - closest_humans[1][1])) >= max(abs(box[0] - h[1][0]), abs(box[1] - h[1][1])):
    #                         closest_humans = [h[0],[h[1][0], h[1][1]]]
    #                         target_humans = [[h[0],[h[1][0], h[1][1]]]]
    #
    #         box_with_target_humans += [[box, target_humans]]
    #
    #     return box_with_target_humans

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
        """Create MOV command for the server from an array of moves"""
        movCmd = []
        movNb = 0
        sources = []
        destinations = []
        if Brain.is_werewolf(self):
            groups = self.currentmap.werewolves
        else:
            groups = self.currentmap.vampires
        for i in range(len(groups)):
            try:
                for el in moves.keys():
                    if check_move_permission(groups[i][0], moves[el][0]):
                        sources += [groups[i][1][0], groups[i][1][1]]
                        destinations += [moves[el][1][0], moves[el][1][1]]
                        if subfinder(sources, [moves[el][1][0], moves[el][1][1]]) and subfinder(destinations, [groups[i][1][0], groups[i][1][1]]):
                            movCmd += [groups[i][1][0], groups[i][1][1], moves[el][0], moves[el][1][0], moves[el][1][1]]
                            movNb += 1
            except KeyError:
                continue

        return [movNb, movCmd]

    def clean_double_moves(self, moves):
        """Prevent forbiden moves"""
        if Brain.is_werewolf(self):
            groups = self.currentmap.werewolves
        else:
            groups = self.currentmap.vampires

        dict_moves = {k: v for k, v in enumerate(moves)}

        for move in moves:
            # for el in move:
            for i in range(len(groups)):
                if move[1][0] == groups[i][1][0] and move[1][1] == groups[i][1][1]:
                    if len(dict_moves) > 1:
                        dict_moves.pop(i, None)

        return dict_moves

    def compute_next_move(self):
        """Computes next move for the indicated team : 0 (ourself), 1 (enemies)"""
        possible_moves = []
        if Brain.is_werewolf(self):
            map_generator = MapGenerator(enemies_coords=self.find_enemies(), humans=self.currentmap.humans,
                                         size_x=self.currentmap.size_x, size_y=self.currentmap.size_y, team=1)
            for i in range(len(self.currentmap.werewolves)):
                # Interesting boxes close to human
                box_and_weight = self.generate_value_boxes_and_weight(i)

                # All possibities of split in those boxes
                value_moves = generate_value_moves(box_and_weight, self.currentmap.werewolves[i][0],
                                                   self.currentmap.humans, self.currentmap.vampires)

                # Calculating most interesting split possibilities for this group
                group_possible_moves = self.choose_move(value_moves, box_and_weight, self.currentmap.werewolves[i])
                print("Possible moves", group_possible_moves)

                # Generating possibility maps
                map_generator.update_team_maps(subgroup_possible_moves=group_possible_moves)

                # description possible_moves = [ (group_i, [[[split1, [newX1, newY1]], [split1', [newX1', newY1']],
                #                                  [split2, [newX2, newY2]], [split2', [newX2', newY2']]] ), ... ]
                # possible_moves += [group_possible_moves]
        else:
            map_generator = MapGenerator(enemies_coords=self.find_enemies(), humans=self.currentmap.humans,
                                         size_x=self.currentmap.size_x, size_y=self.currentmap.size_y, team=-1)
            for i in range(len(self.currentmap.vampires)):
                # Interesting boxes close to human
                box_and_weight = self.generate_value_boxes_and_weight(i)

                # All possibities of split in those boxes
                value_moves = generate_value_moves(box_and_weight, self.currentmap.vampires[i][0],
                                                   self.currentmap.humans, self.currentmap.werewolves)


                # Calculating most interesting split possibilities for this group
                group_possible_moves = self.choose_move(value_moves, box_and_weight, self.currentmap.vampires[i])
                print("Possible moves", group_possible_moves)
                # Generating possibility maps
                map_generator.update_team_maps(subgroup_possible_moves=group_possible_moves)

                # description possible_moves = [ [[[split1, [newX1, newY1]], [split1', [newX1', newY1']],
                #                                  [split2, [newX2, newY2]], [split2', [newX2', newY2']]], ... ]
                # possible_moves += [group_possible_moves]
        return map_generator.generate_maps_objects()

    def return_moves(self, next_move):
        """Returns moves to the server"""
        print("Clean ", self.clean_double_moves(next_move))
        return self.createMOV(self.clean_double_moves(next_move))

