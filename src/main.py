# -*- coding: utf-8 -*-

import socket
import struct
import array
import map
import brain

SERVER_ADDRESS = "138.195.110.234"
SERVER_PORT = 5555


def get_command(sock):
    commande = bytes()
    while len(commande) < 3:
        commande += sock.recv(3-len(commande))
    return commande.decode()


def get_set(sock):
    """Command to get map dimensions"""
    n = bytes()
    m = bytes()
    n += sock.recv(1)
    m += sock.recv(1)
    return [struct.unpack('b', n)[0], struct.unpack('b', m)[0]]


def get_hme(sock):
    """Command to get initial coords"""
    x = bytes()
    y = bytes()
    x += sock.recv(1)
    y += sock.recv(1)
    return [struct.unpack('b', x)[0], struct.unpack('b', y)[0]]


def get_hum(sock):
    """"Command to get houses info"""
    n = bytes()
    n += sock.recv(1)
    coords = []
    n = struct.unpack('b', n)[0]

    for i in range(n):
        x = bytes()
        y = bytes()

        x += sock.recv(1)
        y += sock.recv(1)

        coords.append([struct.unpack('b', x)[0], struct.unpack('b', y)[0]])
    return coords


def get_map(sock):
    """"Command to get houses info"""
    n = bytes()
    n += sock.recv(1)
    initial_map = []
    n = struct.unpack('b', n)[0]
    for i in range(n):
        x = bytes()
        y = bytes()
        nhumans = bytes()
        nvampires = bytes()
        nwerewolves = bytes()

        x += sock.recv(1)
        y += sock.recv(1)
        nhumans += sock.recv(1)
        nvampires += sock.recv(1)
        nwerewolves += sock.recv(1)
        while len(y) < 1:
            y += sock.recv(1 - len(y))
        while len(nhumans) < 1:
            nhumans += sock.recv(1 - len(y))
        while len(nvampires) < 1:
            nvampires += sock.recv(1 - len(y))
        while len(nwerewolves) < 1:
            nwerewolves += sock.recv(1 - len(y))

        initial_map.append([struct.unpack('b', x)[0], struct.unpack('b', y)[0], struct.unpack('b', nhumans)[0],
                            struct.unpack('b', nvampires)[0], struct.unpack('b', nwerewolves)[0]])
    return initial_map


def send_command(sock, commande, data1, data2):
    paquet = bytes()
    paquet += commande.encode()
    if type(data1) in (str,):
        paquet += data1.encode()
    else:
        paquet += struct.pack("=B", data1)
    if type(data2) in (str,):
        paquet += data2.encode()
    else:
        paquet += array.array('B', data2).tostring()

    sock.send(paquet)


def number_of_changes(sock):
    data = bytes()
    while len(data) < 1:
        data += sock.recv(1 - len(data))
    return struct.unpack("b", data)[0]


def get_changes(sock, n):
    changes = []
    for i in range(n):
        x = bytes()
        y = bytes()
        people = bytes()
        new_x = bytes()
        new_y = bytes()

        x += sock.recv(1)
        y += sock.recv(1)
        people += sock.recv(1)
        new_x += sock.recv(1)
        new_y += sock.recv(1)
        while len(y) < 1:
            y += sock.recv(1 - len(y))
        while len(people) < 1:
            people += sock.recv(1 - len(y))
        while len(new_x) < 1:
            new_x += sock.recv(1 - len(y))
        while len(new_y) < 1:
            new_y += sock.recv(1 - len(y))

        changes.append([struct.unpack('b', x)[0], struct.unpack('b', y)[0], struct.unpack('b', people)[0],
                            struct.unpack('b', new_x)[0], struct.unpack('b', new_y)[0]])
    return changes

if __name__ == '__main__':
    # Connexion au server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_ADDRESS, SERVER_PORT))

    # Implementation du protocole

    # SENDING NAME WITH NME COMMAND
    name = "VAMPIRE"
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
    new_map = Map(vampires=[], werewolves=[], humans=[], size_x=n, size_y=m, initial_coords=initial_coords)
    new_map.initialize_map(map_infos)
    team = new_map.find_grp(initial_x, initial_y)


    # Initialize
    brain = Brain(new_map, team[1])
    # testing a move
    # send_command(sock, "MOV", 1, [4,3,3,3,3])

    while True:
        commande5 = get_command(sock)
        if commande5 not in ["UPD", "END"]:
            raise ValueError("Erreur protocole: mauvaise commande reçue.")

        elif commande5 == "END":
            break

        elif commande5 == "UPD":
            # get updates
            print(type(sock))
            numbers = number_of_changes(sock)
            changes = get_changes(sock, numbers)

            print(changes)

            # TODO, call AI with the map and receive new map updated
            # res = call_ai(map, changes)
            send_command(sock, "MOV", 1, [initial_x, initial_y, 2, initial_x+1, initial_y+1])
        else:
            raise ValueError("commande inconnue")
