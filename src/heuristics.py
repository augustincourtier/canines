from src.utils import *


def heuristic(map):
    H, V, W = map.humans, map.vampires, map.werewolves
    nb_hum, nb_vamp, nb_ww = len(H), len(V), len(W)

    # calcul des distances entre tous les groupes
    dist_HW = []
    dist_VW = []
    dist_HV = []
    for i in range(nb_hum):
        dist_HW[i] = []
        for j in range(nb_ww):
            dist_HW[i][j] = max(abs(H[i][1][0] - W[i][1][0]), abs(H[i][1][1] - W[i][1][1]))
    for i in range(nb_vamp):
        dist_VW[i] = []
        for j in range(nb_ww):
            dist_VW[i][j] = max(abs(V[i][1][0] - W[i][1][0]), abs(V[i][1][1] - W[i][1][1]))
    for i in range(nb_hum):
        dist_HV[i] = []
        for j in range(nb_vamp):
            dist_HV[i][j] = max(abs(H[i][1][0] - V[i][1][0]), abs(H[i][1][1] - V[i][1][1]))

    # calcul des proba de gagner les humains
    probaW = []
    probaV = []
    for i in range(nb_hum):
        probaW[i] = []
        for j in range(nb_ww):
            probaW[i][j] = prob_against_humans(W[i][0], H[j][0])
    for i in range(nb_hum):
        probaV[i] = []
        for j in range(nb_vamp):
            probaV[i][j] = prob_against_humans(V[i][0], H[j][0])

    # calcul des scores
    captureH = []
    for i in range(nb_hum):
        captureH[i] = []
        if min(dist_HV[i]) < min(dist_HW):
            captureH[i][0] = 'V'
            index = min_index(dist_HV[i])
            captureH[i][1] = min(dist_HV[i]) * pow(probaV[i][index], 2)
        elif min(dist_HV[i]) > min(dist_HW):
            captureH[i][0] = 'W'
            index = min_index(dist_HW[i])
            captureH[i][1] = min(dist_HW[i]) * pow(probaW[i][index], 2)
        else:
            captureH[i][0] = 'E'

def heuristic1(map):
    V, W = map.vampires, map.werewolves
    nb_vamp, nb_ww = len(V), len(W)
    pop_vamp = 0
    pop_ww = 0
    pop_vamp_moyenne = pop_vamp/len(V)
    pop_ww_moyenne = pop_ww/len(W)
    for i in range(nb_vamp):
        pop_vamp = pop_vamp + V[i][0]
        pop_vamp_moyenne = pop_vamp/len(V)
    for j in range(nb_ww):
        pop_ww = pop_ww + W[j][0]
        pop_ww_moyenne = pop_ww/len(W)
    # print(pop_vamp_moyenne)
    # print(pop_ww_moyenne)

def heuristic2(map):
    V, W = map[0], map[1]
    nb_vamp, nb_ww = len(V), len(W)
    pop_vamp = 0
    pop_ww = 0
    pop_vamp_moyenne = pop_vamp/len(V)
    pop_ww_moyenne = pop_ww/len(W)
    for i in range(nb_vamp):
        pop_vamp = pop_vamp + int(V[i][0])
        pop_vamp_moyenne = pop_vamp/len(V)
    for j in range(nb_ww):
        pop_ww = pop_ww + int(W[j][0])
        pop_ww_moyenne = pop_ww/len(W)
    # print(pop_ww_moyenne)
    # print(pop_vamp_moyenne)
    return pop_vamp_moyenne - pop_ww_moyenne

