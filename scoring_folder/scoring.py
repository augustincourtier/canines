from src.brain import Brain
from scoring_folder.scoring_tools import *


class Score(Brain):

    def scoring(self):
        if self.side == 1:
            humans, allies, enemies = self.currentmap.humans, self.currentmap.werewolves, self.currentmap.vampires
        else:
            humans, allies, enemies = self.currentmap.humans, self.currentmap.vampires, self.currentmap.werewolves
        count_allies, count_enemies = count_people(allies), count_people(enemies)
        dist_allies_to_humans = dist_to_nearest_humans(allies, humans)
        dist_enemies_to_humans = dist_to_nearest_humans(enemies, humans)
        return dist_allies_to_humans - dist_enemies_to_humans + count_allies - count_enemies
