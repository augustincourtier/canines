from src.brain import Brain


def count_people(groups):
    nb_people = 0
    for group in groups:
        nb_people += int(group[0])
    return nb_people


class Score(Brain):

    def scoring(self):
        if self.side == 1:
            humans, allies, enemies = self.currentmap.humans, self.currentmap.werewolves, self.currentmap.vampires
        else:
            humans, allies, enemies = self.currentmap.humans, self.currentmap.vampires, self.currentmap.werewolves
        count_allies, count_enemies = count_people(allies), count_people(enemies)
        return count_allies - count_enemies
