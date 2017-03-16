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

