#!/usr/bin/python3
# -*- coding:utf-8 -*
from src.map import Map
import copy


class MapGenerator:
    """Class generating possible maps to send them to minmax"""
    def __init__(self, enemies_coords, humans, size_x, size_y, team):

        self.enemies_coords = enemies_coords
        self.humans = humans
        self.team_possible_maps = []
        self.size_x = size_x
        self.size_y = size_y
        self.team = team

    def update_team_maps(self, subgroup_possible_moves):
        """Method creating new maps according to each group possibilities
        :param subgroup_possible_moves = list des splits possible
        [
            [[nb1, [x1, y1]], [nb2, [x2, y2]]],
                [[nb1', [x1', y1']], [nb2', [x2', y2']]], ...
                                                                ]"""
        if len(self.team_possible_maps) == 0:
            # first iteration
            for move in subgroup_possible_moves:
                self.team_possible_maps += [[move]]
                print("new map", self.team_possible_maps)
        else:
            maps = []
            # combining each possibility of each group with each other
            for map_i in range(len(self.team_possible_maps)):
                for move in subgroup_possible_moves:
                    maps += [[self.team_possible_maps[map_i][0], move[0]]]
                    print("new new map", maps)

            self.team_possible_maps = maps

    def generate_maps_objects(self):
        """Method generating maps object from the possible maps"""

        maps = []
        for i in range(len(self.team_possible_maps)):
            next_map = []
            for j in range(len(self.team_possible_maps[i][0])):
                next_map += [copy.deepcopy(self.team_possible_maps[i][0][j])]
            if self.team == 1:
                # if werewolves
                imap = Map(vampires=self.enemies_coords, werewolves=next_map, humans=self.humans,
                            size_x=self.size_x, size_y=self.size_y)
            else:
                # if vampires
                imap = Map(vampires=next_map, werewolves=self.enemies_coords, humans=self.humans,
                            size_x=self.size_x, size_y=self.size_y)
            imap.delete_duplicate_in_next_map()
            print("Map", i, ":", imap)
            maps += [imap]
        return maps
