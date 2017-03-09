from brain import Brain
import numpy as np
import map
import time

a = time.time()
vampire=[[16, [8, 3]]]
werewolf=[[16, [10, 9]]]
humans=[[17, [2, 9]], [17, [9, 2]] , [3, [2, 3]], [3, [9, 3]], [15, [0, 1]],[15, [11, 10]], [11, [1, 10]],[11, [10, 1]], [19, [5, 1]],[19, [6, 10]]]
# humans = []
# humans=[[15, [0, 1]],[15, [11, 10]], [11, [1, 10]],[11, [10, 1]], [19, [5, 1]],[19, [6, 10]]]


# vampire=[[9, [9, 2]]]
# werewolf=[[8, [2, 8]]]

# humans = [[2, [9, 0]],[1,[9,2]],[2,[9,4]],[4,[2,2]]]

mapTest=map.Map(vampire,werewolf,humans,15,15)

# print mapTest

brain=Brain(mapTest,-1)
maps=brain.return_moves()

print(maps)

b = time.time()

print(b-a)

# for i in maps:
#     print ("new map")
#     print(i)
# print len(maps)

# brain =Brain(maps[0],-1)
# maps=brain.createMapsfromMap(-1)
#
# for i in maps:
#     print ("new map")
#     i.displayMap()
# print len(maps)
