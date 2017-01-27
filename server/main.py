# -*- coding: utf-8 -*-
import socket
import struct

SERVER_ADDRESS = "138.195.110.0"
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
    while len(n)<3:
        n += sock.recv(1-len(n))
    while len(m)<3:
        m += sock.recv(1-len(m))
    return [n.decode(), m.decode()]


def gethme(sock):
    """Command to get initial coords"""
    x = bytes()
    y = bytes()
    while len(x) < 1:
        x += sock.recv(1-len(x))
    while len(y) < 1:
        y += sock.recv(1-len(y))
    return [x.decode(), y.decode()]


def gethum(sock):
    """"Command to get houses info"""
    n = bytes()
    while len(n) < 1:
        n += sock.recv(1-len(n))
    coords = []
    i = 0

    while i < n:
        x = bytes()
        y = bytes()
        while len(x) < 1:
            x += sock.recv(1 - len(x))
        while len(y) < 1:
            y += sock.recv(1 - len(y))
        coords.append([x.decode(), y.decode()])
        i += 1
    return coords


def getmap(sock):
    """"Command to get houses info"""
    n = bytes()
    while len(n) < 1:
        n += sock.recv(1-len(n))
    initial_map = []
    i = 0

    while i < n:
        x = bytes()
        y = bytes()
        nhumans = bytes()
        nvampires = bytes()
        nwerewolves = bytes()

        while len(x) < 1:
            x += sock.recv(1 - len(x))
        while len(y) < 1:
            y += sock.recv(1 - len(y))
        while len(nhumans) < 1:
            nhumans += sock.recv(1 - len(y))
        while len(nvampires) < 1:
            nvampires += sock.recv(1 - len(y))
        while len(nwerewolves) < 1:
            nwerewolves += sock.recv(1 - len(y))

        initial_map.append([x.decode(), y.decode(), nhumans.decode(), nvampires.decode(), nwerewolves.decode()])
        i += 1
    return initial_map


def getresult(sock):
    data = bytes()
    while len(data) != 8:
        data += sock.recv(8 - len(data))
    return struct.unpack("d", data)[0]


def sendcommand(sock, commande, data1, data2):
    paquet = bytes()
    paquet += commande.encode()
    paquet += struct.pack("d", float(data1))
    paquet += struct.pack("d", float(data2))
    sock.send(paquet)


if __name__ == '__main__':
    # Connexion au server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_ADDRESS, SERVER_PORT))

    # Implementation du protocole

    # SENDING NAME WITH NME COMMAND
    name = u"VAMPIRE"
    sendcommand(sock, u"NME", len(name.encode()), name)

    # RECEIVING DIMENSIONS (SET)
    commande1 = getcommand(sock)
    if commande1 != u"SET":
        raise ValueError("Erreur protocole: attendu SET (cote client)")
    else:
        dimensions = getset(sock)
        n = dimensions[0]
        m = dimensions[1]
        print("Received dimensions! \n")

    # RECEIVING INITIAL POSITION (HME)
    commande2 = getcommand(sock)
    if commande2 != u"HME":
        raise ValueError("Erreur protocole: attendu HME (cote client)")
    else:
        initial_coords = gethme(sock)
        x = initial_coords[0]
        y = initial_coords[1]
        print("Received initial coords! \n")

    # RECEIVING HOUSES INFOS (HUM)
    commande3 = getcommand(sock)
    if commande3 != u"HUM":
        raise ValueError("Erreur protocole: attendu HUM (cote client)")
    else:
        house_coords = gethum(sock)
        print("Received initial houses! \n")

    # RECEIVING 1ST MAP (MAP)
    commande4 = getcommand(sock)
    if commande4 != u"MAP":
        raise ValueError("Erreur protocole: attendu MAP (cote client)")
    else:
        map_infos = getmap(sock)
        print("Received first map! \n")

    # INITIALIZING THREAD
    # partyThread = PartyThread(sock).run()

    # while partyThread.
