from .utils import *
import itertools
import time

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
        for j in range(0, group_size):
            subarray += [index]
            index += 1
        result += [subarray]
    return result

def generate_value_moves(value_boxes_and_weight, size_of_original_group, human_group_list,enemy_group_list):
    """this function generates all value subgroups from one original group,
    and then choose valid possibilities (n subgroups with a total of people =  size_of_original_group)"""
    initial_time = time.time()
    possible_tuples = []  # store each possible tuples for one valid box (ex 1 guy on the box, 2 guys etc..)
    group_weight = [] # store weight of each human group

    for box_and_weight in value_boxes_and_weight:
        possible_tuples_per_box = []
        for weight in box_and_weight[1]:
            possible_tuples_per_box.append([weight]+[box_and_weight[0]])
        possible_tuples.append(possible_tuples_per_box)

    good_moves = []

    for possible_move in list(itertools.product(*possible_tuples)) :
        sum_weight = 0
        indexs = []

        for submove_id in range(len(possible_move)) :
            if possible_move[submove_id][0] != 0:
                sum_weight += possible_move[submove_id][0]
                indexs.append(possible_move[submove_id])

        if sum_weight == size_of_original_group:
            good_moves.append(delete_zero_moves([possible_move])[0])

        elif sum_weight < size_of_original_group:
            weight_to_share = size_of_original_group - sum_weight
            tuples_per_value_box = []

            if len(indexs) == 1 :
                good_moves.append([[size_of_original_group,indexs[0][1]]])

            else :
                for index in indexs :
                    tuple_per_value_box =[]
                    # for l in range(0 , weight_to_share+1):
                    #     tuple_per_value_box.append([index[0]+l,index[1]])
                    # tuples_per_value_box.append(tuple_per_value_box)
                    tuples_per_value_box.append([[index[0],index[1]], [index[0]+weight_to_share,index[1]]])

                for possible_move in list(itertools.product(*tuples_per_value_box)):
                    sum_weight = 0
                    indexs = []
                    for submove_id in range(len(possible_move)) :
                        if possible_move[submove_id][0] != 0:
                            sum_weight += possible_move[submove_id][0]
                            indexs.append(submove_id)
                    if sum_weight == size_of_original_group:
                        good_moves.append(possible_move)

    unique_good_moves = []

    for good_move in good_moves:
        is_unique = False
        for unique_good_move in unique_good_moves:
            if good_move ==unique_good_move:
                is_unique = True
        if is_unique == False :
            unique_good_moves.append(good_move)

    return unique_good_moves


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
                min_split = len(move)
    return filtered_moves


def check_move_permission(initial, intended):
    """Checks if a move is allowed: enough people in the box to move them?"""
    if intended > initial:
        return False
    return True
