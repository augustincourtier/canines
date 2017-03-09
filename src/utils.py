import operator


def min_index(l):
    index = 0
    minimum = 0
    for i in range(len(l)):
        if l[i] < minimum:
            index = i
            minimum = l[i]
    return index


def prob_against_humans(ww_or_vamp, hums):
    if ww_or_vamp < hums:
        return ww_or_vamp / (2 * hums)
    elif ww_or_vamp >= hums:
        return 1
    else:
        return 0


def remove_from_list(old_list, new_list):
    for character in old_list:
        if character in new_list:
            old_list.remove(character)
            new_list.remove(character)
    return old_list, new_list


def delete_zero_moves(moves):
    non_zero_moves = []
    for move in moves:
        non_zero_move = []
        for tuple in move:
            if tuple[0] != 0:
                non_zero_move += [tuple]
        non_zero_moves += [non_zero_move]
    return non_zero_moves


def list_of_lists_to_list(list_of_lists):
    """[[a,b],[c,d]] => [a,b,c,d]"""
    return [y for x in list_of_lists for y in x]


def list_in_list_of_lists(liste, list_of_lists):
    return liste in list_of_lists


def sort_human_by_number(humans):
    human_indexes = []
    result = []
    for i in range(len(humans)):
        human_indexes.append([humans[i][0], i])
    human_indexes.sort(key=operator.itemgetter(0))
    human_indexes.reverse()
    for humanIndex in human_indexes:
        result.append(humans[humanIndex[1]])
    return result


