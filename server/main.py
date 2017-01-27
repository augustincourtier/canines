# -*- coding: utf-8 -*-
import socket
import struct
from Map.map import Map
from Server.PartyThread import PartyThread

SERVER_ADDRESS = "192.168.43.166"
SERVER_PORT = 5555


def getcommand(sock):
    commande = bytes()
    while len(commande) < 3:
        commande += sock.recv(3-len(commande))
    return commande.decode()


def getset(sock):
    """Command to get map dimensions"""
    n = bytes()
    m = bytes()
    n += sock.recv(1)
    m += sock.recv(1)
    return [struct.unpack('b', n)[0], struct.unpack('b', m)[0]]


def gethme(sock):
    """Command to get initial coords"""
    x = bytes()
    y = bytes()
    x += sock.recv(1)
    y += sock.recv(1)
    return [struct.unpack('b', x)[0], struct.unpack('b', y)[0]]


def gethum(sock):
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


def getmap(sock):
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


def sendcommand(sock, commande, data1, data2):
    paquet = bytes()
    paquet += commande.encode()
    if type(data1) in (str,):
        paquet += data1.encode()
    else:
        paquet += struct.pack("=B", data1)
    if type(data2) in (str,):
        paquet += data2.encode()
    else:
        paquet += struct.pack("=B", data2)
    sock.send(paquet)


if __name__ == '__main__':
    # Connexion au server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_ADDRESS, SERVER_PORT))

    # Implementation du protocole

    # SENDING NAME WITH NME COMMAND
    name = "VAMPIRE"
    sendcommand(sock, "NME", 7, name)

    # RECEIVING DIMENSIONS (SET)
    commande1 = getcommand(sock)
    if commande1 != "SET":
        raise ValueError("Erreur protocole: attendu SET (cote client)")
    else:
        dimensions = getset(sock)
        n = dimensions[0]
        m = dimensions[1]
        print("Received dimensions! \n")

    # RECEIVING HOUSES INFOS (HUM)
    commande2 = getcommand(sock)
    if commande2 != "HUM":
        raise ValueError("Erreur protocole: attendu HUM (cote client)")
    else:
        house_coords = gethum(sock)
        print("Received initial houses! \n")

    # RECEIVING INITIAL POSITION (HME)
    commande3 = getcommand(sock)
    if commande3 != "HME":
        raise ValueError("Erreur protocole: attendu HME (cote client)")
    else:
        initial_coords = gethme(sock)
        x = initial_coords[0]
        y = initial_coords[1]
        print("Received initial coords! \n")

    # RECEIVING 1ST MAP (MAP)
    commande4 = getcommand(sock)
    if commande4 != "MAP":
        raise ValueError("Erreur protocole: attendu MAP (cote client)")
    else:
        map_infos = getmap(sock)
        print("Received first map! : ", map_infos, "\n")

    new_map = Map(vampire=[], werewolf=[], humans=[], sizeX=n, sizeY=m)
    # Initialize IA with initial coords and map
    new_map.updatemap(map_infos)

    # INITIALIZING THREAD
    partyThread = PartyThread(sock).run()
