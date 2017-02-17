# -*- coding: utf-8 -*-
class Map:
    """Object storing the map of the current turn."""

    def __init__(self, vampires, werewolves, humans, size_x, size_y, initial_coords):
        """
        :param vampires: list of lists [number, [x,y]]
        :param werewolves: list of lists [number, [x,y]]
        :param humans: list of lists [number, [x,y]]
        :param size_x: integer
        :param size_y: integer
        """
        self.size_x = size_x
        self.size_y = size_y
        self.humans = humans
        self.vampires = vampires
        self.werewolves = werewolves
        self.initial_coords = initial_coords

    def initialize_map(self, update_data):
        """update_data = [[X, Y, humans, vampires, werewolves], ...]"""
        for case_data in update_data:
            # if humans
            if case_data[2] != 0:
                self.add_humans(number=case_data[2], coord_x=case_data[0], coord_y=case_data[1])

            # if vampires
            if case_data[3] != 0:
                self.add_vampires(number=case_data[3], coord_x=case_data[0], coord_y=case_data[1])

            # if werewolves
            if case_data[4] != 0:
                self.add_werewolves(number=case_data[4], coord_x=case_data[0], coord_y=case_data[1])

    def add_vampires(self, number, coord_x, coord_y):
        self.vampires += [number, [coord_x, coord_y]]

    def add_werewolves(self, number, coord_x, coord_y):
        self.werewolves += [number, [coord_x, coord_y]]

    def add_humans(self, number, coord_x, coord_y):
        self.humans += [number, [coord_x, coord_y]]

    def move_vampires(self, number, coord_x, coord_y, idgrp):
        if self.vampires[idgrp][0] <= number:
            self.vampires[idgrp][1] = [coord_x, coord_y]
        else:
            self.vampires[idgrp][0] -= number
            self.add_vampires(number, coord_x, coord_y)

    def move_werewolves(self, number, coord_x, coord_y, idgrp):
        if self.werewolves[idgrp][0] <= number:
            self.werewolves[idgrp][1] = [coord_x, coord_y]
        else:
            self.werewolves[idgrp][0] -= number
            self.add_werewolves(number, coord_x, coord_y)

    def find_grp(self, coord_x, coord_y):
        for i in range(len(self.vampires)):
            if self.vampires[1] == [coord_x, coord_y]:
                return [i, -1]
        for i in range(len(self.werewolves)):
            if self.werewolves[1] == [coord_x, coord_y]:
                return [i, 1]
        for i in range(len(self.humans)):
            if self.vampires[1] == [coord_x, coord_y]:
                return [i, 0]
