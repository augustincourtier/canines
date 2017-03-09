# -*- coding: utf-8 -*-
import struct
import array

SERVER_ADDRESS = "138.195.105.47"
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
