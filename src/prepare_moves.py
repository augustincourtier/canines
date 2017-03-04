from utils import *


def sum_of_move(index_move, tuples):
    """This function takes a move defined by an index and the corresponding array of tuples
    and returns the sum of characters of that move"""
    total = 0
    for index in index_move:
        total += tuples[index][0]  # the first elem of a tuple [n, [x,y]] is the number of character
    return total


def generate_index_array(box_number, group_size):
    """This function generates an array containing box_number arrays of group_size elements
    each element is and index in range 0 -- box_number*group_size -1"""
    index = 0
    result = []
    for i in range(0, box_number):
        subarray = []
        for j in range(0, group_size + 1):
            subarray += [index]
            index += 1
        result += [subarray]
    return result


def generate_moves(l):
    """This function is used to generate an array containing all possibilities of one pick in n arrays
    of m integer elements. (on possibility is equivalent to a move)
    ex : [[1,2],[3,4]] => [[1,3],[1,4],[2,3],[2,4]]"""
    result = []
    if not l:
        result += []
    else:
        for i in l[0]:
            result += distribute(i, generate_moves(l[1:]))
    return result


def generate_value_moves(value_boxes, size_of_original_group):
    """this function generates all possibles subgroups from one original group,
    and then choose valid possibilities (n subgroups with a total of people =  sizeOfOriginalGroup)"""
    possible_tuples = []  # store each possible tuples for one valid box (ex 1 guy on the box, 2 guys etc..)
    for i in range(len(value_boxes)):
        possible_tuples_for_one_box = []
        for j in range(0, size_of_original_group + 1):
            possible_tuples_for_one_box += [[j, [value_boxes[i][0], value_boxes[i][1]]]]
        possible_tuples += [possible_tuples_for_one_box]

    # this array contains the list of possibilities for each valueBoxes (0 on the first box, or 1 or 2 and so on..)
    possible_tuples = list_of_lists_to_list(possible_tuples)
    # this array represents "possible_tuples" with index (integers) instead of tuples
    index_array = generate_index_array(len(value_boxes), size_of_original_group)
    # this array still contains indexes
    possible_moves = generate_moves(index_array)

    value_moves = []
    for indexMove in possible_moves:
        # eliminating with sumOfMove() combinations that don't give exactly sizeOfOriginalGroup characters in total
        if sum_of_move(indexMove, possible_tuples) == size_of_original_group:
            real_move = []
            # converting indexes into tuples [n, [x,y]]
            for index in indexMove:
                real_move += [possible_tuples[index]]
            value_moves += [real_move]

    return value_moves


# TODO Does the function do what it says?
def split_filter(moves):
    """This function takes equivalent moves and return those where the group is the less splitted"""
    filtered_moves = []
    min_split = 0
    for move in moves:
        if len(filtered_moves) == 0:
            filtered_moves = [move]
            min_split = len(move)
        else:
            if len(move) == min_split:
                filtered_moves += [move]
            elif len(move) < min_split:
                filtered_moves = [move]
    return filtered_moves


def check_move_permission(initial, intended):
    """Checks if a move is allowed: enough people in the box to move them?"""
    if intended > initial:
        return False
    return True
