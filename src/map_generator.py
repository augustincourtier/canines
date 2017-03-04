#!/usr/bin/python3
# -*- coding:utf-8 -*


class MapGenerator:
    """Class generating possible maps to send them to minmax"""
    def __init__(self, enemies_coords):
        """:param possible_moves = [[group index, [move1, move2,...], ...]"""

        self.enemies_coords = enemies_coords
        self.team_possible_maps = []

    def generate_maps(self, possible_moves):
        """Method creating maps
        :param possible_moves = [(group_id, [list of lists of possible splits],), ...]"""
        # the length of possible_moves is the number of subgroups
        for i in range(len(possible_moves)):
            # iterating on all moves for all groups
            for splits_possibility_of_group_i in possible_moves[i][1]:
                self.team_possible_maps += [[splits_possibility_of_group_i, self.generate_maps(possible_moves[1:])]]
        else:
                self.team_possible_maps += [[possible_moves[0][1]]]

    def update_maps(self, subgroup_possible_moves):
        """Method creating new maps according to each group possibilities"""
        if len(self.team_possible_maps) == 0:
            # first iteration
            for move in subgroup_possible_moves:
                self.team_possible_maps += [[move]]
        else:
            maps = [[]]
            for other_subgroups_move in self.team_possible_maps:
                for move in subgroup_possible_moves:
                    maps += [[move, other_subgroups_move]]
            self.maps = maps
