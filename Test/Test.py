from Brain import brain
from Map import map

vampire=[[10,[1,5]]]
werewolf=[[2,[4,4]]]
humans=[[25,[5,5]],[1000,[6,7]]]
mapTest=map.map(vampire,werewolf,humans,25,25)
print mapTest

brain=brain.brain(mapTest,0)
maps=brain.createMapsfromMap(0)

print maps