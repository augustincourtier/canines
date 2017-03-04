# -*- coding: utf-8 -*-


def sum_dist_nearest_humans(groups, humans):
    distance = 0
    for group in groups:
        dist_group_to_human = 100000
        for human_group in humans:
            if group[0] > human_group[0]:
                local_min_dist = max(abs(group[1][0] - human_group[1][0]), abs(group[1][1] - human_group[1][1]))
                if local_min_dist < dist_group_to_human:
                    dist_group_to_human = local_min_dist
        if dist_group_to_human != 100000:
            distance += dist_group_to_human
    return distance


def count_people(groups):
    nb_people = 0
    for group in groups:
        nb_people += int(group[0])
    return nb_people


def check_surroundings_for_danger(allies, enemies):
    """This function checks surroundings of our groups: if it's dangerous,
    it gives a bad score to the map: we should not choose this map"""
    for ally in allies:
        for enemy in enemies:
            if max(abs(ally[1][0] - enemy[1][0]), abs(ally[1][1] - enemy[1][1])) == 1:
                # Si les ennemies sont beaucoup plus nombreux : ne pas aller par là
                if enemy[0] > 1.5 * ally[0]:
                    return -1000
    return 0


# TODO pas encore utilisée : checker si vraiment intéressante
def check_surroundings_for_easy_enemies(allies, enemies):
    """This function checks surroundings of our groups: if it's an opportunity,
    it gives a high score to go there"""
    for ally in allies:
        for enemy in enemies:
            if max(abs(ally[1][0] - enemy[1][0]), abs(ally[1][1] - enemy[1][1])) == 1:
                # Si les ennemies sont beaucoup moins nombreux : go, go, go !
                if ally[0] > 1.5 * enemy[0]:
                    return 1000
    return 0


# TODO : check qu'il n'y a pas des ennemis qui vont manger les humains avant nous
def check_surroundings_for_easy_humans(allies, humans):
    """If humans are next to our groups, it increases the score we give to the map"""
    for ally in allies:
        for human_group in humans:
            if max(abs(ally[1][0] - human_group[1][0]), abs(ally[1][1] - human_group[1][1])) == 1:
                if ally[0] >= human_group[0]:
                    return human_group[0]
    return 0
