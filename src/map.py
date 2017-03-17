# -*- coding: utf-8 -*-
import copy


class Map:
    """Object storing the map of the current turn."""

    def __init__(self, vampires, werewolves, humans, size_x, size_y):
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

        self.old_werewolves = copy.deepcopy(werewolves)
        self.old_vampires = copy.deepcopy(vampires)

    def __repr__(self):
        return {'humans': self.humans,
                'vampires': self.vampires,
                'werewolves': self.werewolves}.__repr__()

    def initialize_map(self, init_data):
        """update_data = [[X, Y, humans, vampires, werewolves], ...]"""
        for case_data in init_data:
            # if humans
            if case_data[2] != 0:
                self.add_humans(number=case_data[2], coord_x=case_data[0], coord_y=case_data[1])

            # if vampires
            if case_data[3] != 0:
                self.add_vampires(number=case_data[3], coord_x=case_data[0], coord_y=case_data[1])

            # if werewolves
            if case_data[4] != 0:
                self.add_werewolves(number=case_data[4], coord_x=case_data[0], coord_y=case_data[1])

    def update_map(self, update_data):
        for case_data in update_data:
            # Removing first data on concerned boxes
            self.remove_humans(case_data[0], case_data[1])
            self.remove_vampires(case_data[0], case_data[1])
            self.remove_werewolves(case_data[0], case_data[1])

            # Adding new datas
            if case_data[2] != 0:
                self.add_humans(number=case_data[2], coord_x=case_data[0], coord_y=case_data[1])

            # if vampires
            if case_data[3] != 0:
                self.add_vampires(number=case_data[3], coord_x=case_data[0], coord_y=case_data[1])

            # if werewolves
            if case_data[4] != 0:
                self.add_werewolves(number=case_data[4], coord_x=case_data[0], coord_y=case_data[1])

    def add_vampires(self, number, coord_x, coord_y):
        self.vampires.append([number, [coord_x, coord_y]])

    def add_werewolves(self, number, coord_x, coord_y):
        self.werewolves.append([number, [coord_x, coord_y]])

    def add_humans(self, number, coord_x, coord_y):
        self.humans.append([number, [coord_x, coord_y]])

    def remove_vampires(self, coord_x, coord_y):
        for vampire in self.vampires:
            if vampire[1] == [coord_x, coord_y]:
                self.vampires.remove(vampire)

    def remove_werewolves(self, coord_x, coord_y):
        for werewolve in self.werewolves:
            if werewolve[1] == [coord_x, coord_y]:
                self.werewolves.remove(werewolve)

    def remove_humans(self, coord_x, coord_y):
        for human in self.humans:
            if human[1] == [coord_x, coord_y]:
                self.humans.remove(human)

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
            if self.vampires[i][1] == [coord_x, coord_y]:
                return [i, -1]
        for i in range(len(self.werewolves)):
            if self.werewolves[i][1] == [coord_x, coord_y]:
                return [i, 1]
        for i in range(len(self.humans)):
            if self.vampires[i][1] == [coord_x, coord_y]:
                return [i, 0]

    def displayMap(self):
        print(self.humans)
        print(self.vampires)
        print(self.werewolves)

    def convert_into_array(self):
        return [self.vampires, self.werewolves, self.humans, self.size_x, self.size_y]

    def delete_duplicate_in_next_map(self):
        """Method checking if we ate humans or killed enemies in artificially generated maps:
        same [x, y] cannot contain two teams"""
        i = 0
        cut = False
        while i < len(self.humans):
            # comparing humans coordinates to werewolves
            for j in range(len(self.werewolves)):
                if self.humans[i][1][0] == self.werewolves[j][1][0] and self.humans[i][1][1] == self.werewolves[j][1][1]:
                    self.werewolves[j][0] += self.humans[i][0]
                    print("Replaced humans by werewolves")
                    self.humans = self.humans[:i] + self.humans[i+1:]
                    cut = True
                    break
            if not cut:
                # comparing humans coordinates to vampires
                for k in range(len(self.vampires)):
                    if self.humans[i][1][0] == self.vampires[k][1][0] and self.humans[i][1][1] == self.vampires[k][1][1]:
                        self.vampires[k][0] += self.humans[i][0]
                        self.humans = self.humans[:i] + self.humans[i+1:]
                        cut = True
                        # print("Replaced humans by vampires")
                        break
            if cut:
                # as we sliced the list
                cut = False
            else:
                i += 1

        # comparing werewolves coordinates to vampires
        i = 0
        j = 0
        cut_w = False
        cut_v = False
        while i < len(self.vampires) and j < len(self.werewolves):
            if self.vampires[i][1][0] == self.werewolves[j][1][0] and self.vampires[i][1][1] == self.werewolves[j][1][1]:
                if self.vampires[i][0] >= 1.5*self.werewolves[j][0]:
                    self.vampires[i][0] += self.werewolves[j][0]
                    self.werewolves = self.werewolves[:j] + self.werewolves[j+1:]
                    cut_w = True
                    print("Replaced werewolves by vampires")
                elif self.werewolves[j][0] >= 1.5*self.vampires[i][0]:
                    self.werewolves[j][0] += self.vampires[i][0]
                    self.vampires = self.vampires[:i] + self.vampires[i+1:]
                    cut_v = True
                    print("Replaced vampires by werewolves")
                else:
                    self.werewolves[j][0] += self.vampires[i][0]
                    self.vampires = self.vampires[:i] + self.vampires[i+1:]
                    cut_v = True
                    print("Replaced vampires by werewolves (random battle)")

            if cut_v:
                # as we sliced the list
                j += 1
                cut_v = False
            elif cut_w:
                # as we sliced the list
                i += 1
                cut_w = False
            else:
                i += 1
                j += 1
