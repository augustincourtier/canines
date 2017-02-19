from brain import Brain
import numpy as np
import map

vampire=[[4,[2,5]]]
werewolf=[[4,[4,5]]]
humans=[[4,[3,3]],[2,[1,10]], [1,[3,10]], [2,[5,10]]]
mapTest=map.Map(vampire,werewolf,humans,10,10)

# print mapTest

brain=Brain(mapTest,-1)
maps=brain.test(-1)

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
