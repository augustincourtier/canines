#!/usr/bin/python3
# -*- coding: utf-8 -*-

from src.map import Map
from src.arbre import Arbre
from src.heuristics import heuristic2

def minmaxDecision(a):
    """Décide la nouvelle carte avec algo minmax"""
    carte_suivante = []
    carte_actuelle = a.racine
    # print(carte_actuelle)
    fils = a.lesfils()
    Max = -1000
    for l in fils:
        if valeurMin(l) > Max:
            Max = valeurMin(l)
            carte_suivante = l.racine
            # print(carte_suivante)
    next_map = Map(vampires=carte_suivante[0][0], werewolves=carte_suivante[0][1], humans=carte_suivante[0][2],
                   size_x=carte_suivante[0][3], size_y=carte_suivante[0][4])
    return next_map

#def valeurMax(a):
    """Calcule valeur d'un noeud Max"""
    #if a.racine.__label == None: #Faire une fonction pour vérifier que c'est une feuille, c'est bon
    #    return heuristic2(a) #Faire une fonction heuristique d'évaluation de la carte
    #k = -1000
    #fils = a.lesfils()
    #for l in range(len(fils)):
        #k = max(k, valeurMin(l))
    #return k


def valeurMin(a):
    """Calcule la valeur d'un noeud Min"""
    #if a.racine.__label == None: #Faire une fonction pour vérifier que c'est une feuille
        #return heuristic2(a) #Faire une fonction heuristique d'évaluation de la carte
    # for l in range(len(fils)):
    #    k = min(k, valeurMax(l))
    k = 1000
    fils = a.lesfils()
    for j in range(len(fils)):
        racine = fils[j].racine
        score = heuristic2(racine)
        k = min(k, score)
    return k


#def valeurMin(a):
    """Calcule la valeur d'un noeud Min"""
    #if a.racine.__label == None: #Faire une fonction pour vérifier que c'est une feuille
        #return heuristic2(a) #Faire une fonction heuristique d'évaluation de la carte
    # for l in range(len(fils)):
    #    k = min(k, valeurMax(l))
    #k = 1000
    #fils = a.lesfils()
    #for i in range(len(fils)):
        #fils_de_fils = fils[i].lesfils()
        #print(fils[i])
        #print(fils_de_fils)
        #for j in range(len(fils_de_fils)):
            #racine = fils_de_fils[j].racine
            #print(racine)
            #score = heuristic2(racine)
            #print(score)
            #k = min(k, score)
            #print(k)
    #return k

#if __name__=='__main__':
    #premiere_carte = Arbre(([[4, [4, 3]], [[4, [4, 1]]], [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10],
                            #[[[4, [4, 3]], [[3, [4, 1]], [1, [5, 1]]],
                             # [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10],
                             #[[[[1, [4, 3]], [3, [5, 3]]], [[3, [4, 1]], [1, [5, 1]]],
                              #[[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]],
                             #[[[[2, [4, 3]], [2, [5, 3]]], [[3, [4, 1]], [1, [5, 1]]],
                             # [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]]
                             #],
                            #[[[4, [4, 3]], [[2, [4, 1]], [2, [5, 1]]],
                             # [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10],
                             #[[[[1, [4, 3]], [3, [5, 3]]], [[2, [4, 1]], [2, [5, 1]]],
                             # [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]],
                             #[[[[2, [4, 3]], [2, [5, 3]]], [[2, [4, 1]], [2, [5, 1]]],
                              #[[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]]
                             #],
                            #[[[4, [4, 3]], [[1, [4, 1]], [3, [5, 1]]],
                             # [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10],
                             #[[[[1, [4, 3]], [3, [5, 3]]], [[1, [4, 1]], [3, [5, 1]]],
                             # [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]],
                             #[[[[2, [4, 3]], [2, [5, 3]]], [[1, [4, 1]], [3, [5, 1]]],
                            # [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]]
                             #],
                            #[[[4, [4, 3]], [[4, [5, 1]]], [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5,
                             # 10],
                             #[[[[1, [4, 3]], [3, 5, 3]], [[4, [5, 1]]], [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5,
                             # 10]],
                             #[[[[2, [4, 3]], [2, 5, 3]], [[4, [5, 1]]],
                              #[[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5,
                              #10]]
                             #]))
    #minmaxDecision(premiere_carte)