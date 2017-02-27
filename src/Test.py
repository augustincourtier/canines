from brain import Brain
import numpy as np
import map

vampire=[[6, [1, 7]]]
werewolf=[[5, [7, 3]]]
humans=[[5, [2, 1]], [3, [7, 8]], [3, [4, 7]], [5, [5, 2]], [8, [3, 6]], [10, [6, 3]], [1, [0, 5]], [1, [9, 4]]]

# vampire=[[4, [9, 0]], [4, [9, 4]]]
# werewolf=[[8, [6, 0]]]
# humans=[[1, [9, 2]]]

mapTest=map.Map(vampire,werewolf,humans,10,10)

# print mapTest

brain=Brain(mapTest,1)
maps=brain.return_moves()

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
