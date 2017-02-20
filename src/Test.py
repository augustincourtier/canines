from brain import Brain
import numpy as np
import map

vampire=[[4, [4, 1]]]
werewolf=[[4, [4, 3]]]
humans=[[2, [9, 0]], [4, [2, 2]], [1, [9, 2]], [2, [9, 4]]]
mapTest=map.Map(vampire,werewolf,humans,10,5)

# print mapTest

brain=Brain(mapTest,1)
maps=brain.returnMoves()

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
