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


def distribute(element, lists):
    """This function is used to distribute a value on an array of arrays
    ex : [1,[1,2],[3,4]] => [[1,1,2],[1,3,4]]"""
    new_list = []
    if not lists:
        return [[element]]
    elif isinstance(lists[0], int):
        new_list = [lists + [element]]
        return new_list
    else:
        for list in lists:
            list += [element]
            new_list += [list]
        return new_list