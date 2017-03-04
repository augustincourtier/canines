# -*- coding: utf-8 -*-
from src.brain import Brain
from scoring_folder.scoring_tools import *


class Score(Brain):

    def scoring(self):
        # Initialize groups
        if self.side == 1:
            humans, allies, enemies = self.currentmap.humans, self.currentmap.werewolves, self.currentmap.vampires
        else:
            humans, allies, enemies = self.currentmap.humans, self.currentmap.vampires, self.currentmap.werewolves

        # Compute some basics infos
        count_allies, count_enemies = count_people(allies), count_people(enemies)
        dist_allies_to_humans = sum_dist_nearest_humans(allies, humans)
        dist_enemies_to_humans = sum_dist_nearest_humans(enemies, humans)

        # Initialize score
        score = 0

        # First iteration for the score
        score += dist_allies_to_humans - dist_enemies_to_humans + count_allies - count_enemies

        # CHECK SURROUNDINGS
        # Check surroundings, if dangerous, bad score is given to the map
        if check_surroundings_for_danger(allies, enemies) != 0:
            return check_surroundings_for_danger(allies, enemies)
        # Check surroundings, if a good opportunity to kill humans, go
        score += check_surroundings_for_easy_humans(allies, humans)

        return score


