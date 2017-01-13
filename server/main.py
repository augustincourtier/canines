import socket
from server.server_config import Server
from time import sleep
import struct


def getcommand(sock):
    commande = bytes()
    while len(commande)<3:
        commande += sock.recv(3-len(commande))
    return commande.decode()


def getresult(sock):
    data = bytes()
    while len(data) != 8:
        data += sock.recv(8 - len(data))
    return struct.unpack("d", data)[0]


def sendcommand(sock, commande, op1, op2):
    paquet = bytes()
    paquet += commande.encode()
    paquet += struct.pack("d", float(op1))
    paquet += struct.pack("d", float(op2))
    sock.send(paquet)


if __name__ == '__main__':
    # lancement du serveur
    server = Server(555)
    server.start()

    # on attend un peu
    sleep(1)

    # connexion au server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 555))

    # implementation du protocole
    commande = getcommand(sock)

    if commande != u"HLO":
        raise ValueError("Erreur protocole: attendu HLO (cote client)")

    sock.send(u"HLO".encode())

    # tests des commandes
    sendcommand(sock, "ADD", 7, 2)
    res = getresult(sock)
    print("Addition OK ? %s" % (res == 7+2))

    sendcommand(sock, "MIN", 7, 2)
    res = getresult(sock)
    print("Soustraction OK ? %s" % (res == 7 - 2))

    sendcommand(sock, "TIM", 7, 2)
    res = getresult(sock)
    print("Multiplication OK ? %s" % (res == 7 * 2))

    sendcommand(sock, "DIV", 7, 2)
    res = getresult(sock)
    print("Division OK ? %s" % (res == 7.0 / 2))

    sock.send("QUT".encode())
    sleep(1)
    server.stoplistening()
    server.join()