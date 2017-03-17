# -*- coding: utf-8 -*-

import socket
import struct
import array
from src.map import Map
from src.brain import Brain
import sys, getopt
import time
from src.server_commands import *
from scoring_folder.scoring import Score
from random import randint


if __name__ == '__main__':
    try:
        server_address, server_port = sys.argv[1], sys.argv[2]
        # Connexion au server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_address, int(server_port)))
    except:
        raise ValueError('Connexion impossible : main.py <SERVER_ADDRESS> <SERVER_PORT>')

        # Implementation du protocole

        # SENDING NAME WITH NME COMMAND
    name = "JOHNCANINE"
    send_command(sock, "NME", 7, name)

    # RECEIVING DIMENSIONS (SET)
    commande1 = get_command(sock)
    if commande1 != "SET":
        raise ValueError("Erreur protocole: attendu SET (cote client)")
    else:
        dimensions = get_set(sock)
        n = dimensions[0]
        m = dimensions[1]
        print("Received dimensions! \n")

    # RECEIVING HOUSES INFOS (HUM)
    commande2 = get_command(sock)
    if commande2 != "HUM":
        raise ValueError("Erreur protocole: attendu HUM (cote client)")
    else:
        house_coords = get_hum(sock)
        print("Received initial houses! \n")

    # RECEIVING INITIAL POSITION (HME)
    commande3 = get_command(sock)
    if commande3 != "HME":
        raise ValueError("Erreur protocole: attendu HME (cote client)")
    else:
        initial_coords = get_hme(sock)
        initial_x = initial_coords[0]
        initial_y = initial_coords[1]
        print("Received initial coords! \n")

    # RECEIVING 1ST MAP (MAP)
    commande4 = get_command(sock)
    if commande4 != "MAP":
        raise ValueError("Erreur protocole: attendu MAP (cote client)")
    else:
        map_infos = get_map(sock)
        print("Received first map! : ", map_infos, "\n")

    # Initialize map with initial coords and map
    new_map = Map(vampires=[], werewolves=[], humans=[], size_x=m, size_y=n)
    new_map.initialize_map(map_infos)
    team = new_map.find_grp(initial_x, initial_y)

    # Initialize
    brain = Brain(new_map, team[1])

    while True:
        commande5 = get_command(sock)
        if commande5 not in ["UPD", "END"]:
            raise ValueError("Erreur protocole: mauvaise commande reçue.")

        elif commande5 == "END":
            break

        elif commande5 == "UPD":
            # get updates
            numbers = number_of_changes(sock)
            changes = get_changes(sock, numbers)
            if len(changes) > 0:
                new_map.update_map(changes)

            print("Nouvelle map, nouveau score : ", Score.scoring(Score(new_map, team[1])))

            # Update brain with the new map ==> Returns possible maps
            brain = Brain(new_map, team[1])
            team_maps = brain.compute_next_move()  # returning 1st step of minimax

            maps = []
            # Enemy brain ==> Returns possible enemies maps
            if brain.is_werewolf():
                for i in range(len(team_maps)):
                    enemy_brain = Brain(team_maps[i], -1)
                    enemy_maps = enemy_brain.compute_next_move()
                    # print("Enemy maps:", enemy_maps)
                    maps.append([team_maps[i], [enemy_maps]])
            else:
                for i in range(len(team_maps)):
                    enemy_brain = Brain(team_maps[i], 1)
                    enemy_maps = enemy_brain.compute_next_move()
                    # print("Enemy maps:", enemy_maps)
                    maps.append([team_maps[i], [enemy_maps]])
            # print("Maps:", maps)

            next_map = maps[0][0]

            print("Next map", next_map)
            if brain.is_werewolf():
                print(next_map.old_werewolves)
                next_moves = brain.return_moves(next_map.old_werewolves)
            else:
                next_moves = brain.return_moves(next_map.old_vampires)
            print("Next moves", next_moves)
            send_command(sock, "MOV", next_moves[0], next_moves[1])

            time.sleep(1)
        else:
            raise ValueError("commande inconnue")
