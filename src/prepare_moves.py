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
    # for each box generated for one group in main
    for i in range(0, box_number):
        subarray = []
        # for all possibilities of splitting (from 0 to number of our elements in the initial square)
        for j in range(0, group_size + 1):
            subarray += [index]
            index += 1
        result += [subarray]

    # Ex: 3 possible boxes generated for a group of 5 werewolves
    # returns [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11], [12, 13, 14, 15, 16, 17]]
    return result


def generate_moves(l):
    """This function is used to generate an array containing all possibilities of one pick in n arrays
    of m integer elements. (on possibility is equivalent to a move)
    ex : for 3 boxes for a group of 5 werewolves
    [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11], [12, 13, 14, 15, 16, 17]]
     returns [[0, [6, 12]], ..., [0, [11, 17]],  ..., [5, [11, 17]]]
     for example the first list means moving 0 people on first box, 6 on the second, 12 on third ?"""
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
        # List of lists (each box) of lists (each possibilities for each box)
        possible_tuples += [possible_tuples_for_one_box]

    # this array contains the list of possibilities for each valueBoxes (0 on the first box, or 1 or 2 and so on..)
    # [[0, new_x1, new_y1], [1, new_x1, new_y1], ..., [3, new_x4, new_y4], ...]
    possible_tuples = list_of_lists_to_list(possible_tuples)

    # this array represents "possible_tuples" with index (integers) instead of tuples
    # list of lists containing indexes of possible moves
    # Ex: 3 possible boxes generated for a group of 5 werewolves
    # returns [[0, 1, 2, 3, 4, 5], [6, 7, 8, 9, 10, 11], [12, 13, 14, 15, 16, 17]]
    index_array = generate_index_array(len(value_boxes), size_of_original_group)

    # array of move possibilities in each box
    # ex: for 3 box [[0, 5, 3]....]
    # first list means doing move 0 in first box, move 5 in the second one, move 3 in the third
    possible_moves = generate_moves(index_array)

    value_moves = []
    for indexMove in possible_moves:
        # TODO: limit of subgroups possible so that groups don't split too much
        # eliminating with sumOfMove() combinations that don't give exactly sizeOfOriginalGroup characters in total
        if sum_of_move(indexMove, possible_tuples) == size_of_original_group:
            real_move = []
            # converting indexes into tuples [n, [x,y]]
            for index in indexMove:
                real_move += [possible_tuples[index]]
            value_moves += [real_move]
    return value_moves


def split_filter(moves):
    """This function takes equivalent moves and return those where the group is the less splitted"""
    filtered_moves = []
    min_split = 0
    for move in moves:
        # first iteration
        if len(filtered_moves) == 0:
            filtered_moves = [move]
            min_split = len(move)
        else:
            # adding moves if split is the same
            if len(move) == min_split:
                filtered_moves += [move]
            # replacing others move if less splits
            # TODO : is it always preferable?
            elif len(move) < min_split:
                filtered_moves = [move]
    return filtered_moves


def check_move_permission(initial, intended):
    """Checks if a move is allowed: enough people in the box to move them?"""
    if intended > initial:
        return False
    return True
