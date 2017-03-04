from brain import Brain
import numpy as np
import map

vampire=[[6, [1, 7]]]
werewolf=[[5, [7, 3]],[5, [7, 2]]]
humans=[[5, [7, 1]]]

# vampire=[[4, [9, 0]], [4, [9, 4]]]
# werewolf=[[8, [6, 0]]]
# humans=[[1, [9, 2]]]

mapTest=map.Map(vampire,werewolf,humans,10,10)

# print mapTest

brain=Brain(mapTest,1)
maps=brain.return_moves()

print(maps)

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
