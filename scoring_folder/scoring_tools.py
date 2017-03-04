def dist_to_nearest_humans(groups, humans):
    distance = 0
    for group in groups:
        dist_group_to_human = 100000
        for human_group in humans:
            if group[0] > human_group[0]:
                local_min_dist = max(abs(group[1][0] - human_group[1][0]), abs(group[1][1] - human_group[1][1]))
                if local_min_dist < dist_group_to_human:
                    dist_group_to_human = local_min_dist
        distance += dist_group_to_human
    return distance


def count_people(groups):
    nb_people = 0
    for group in groups:
        nb_people += int(group[0])
    return nb_people
