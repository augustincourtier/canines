#!/usr/bin/python3
# -*- coding:utf-8 -*


class MapGenerator:
    """Class generating possible maps to send them to minmax"""
    def __init__(self, enemies_coords):
        """:param possible_moves = [[group index, [move1, move2,...], ...]"""

        self.enemies_coords = enemies_coords
        self.team_possible_maps = []

    def update_maps(self, subgroup_possible_moves):
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
        else:
            maps = []
            # combining each possibility of each group with each other
            for other_subgroups_move in self.team_possible_maps:
                for move in subgroup_possible_moves:
                    maps += [[move, other_subgroups_move]]
            self.maps = maps
