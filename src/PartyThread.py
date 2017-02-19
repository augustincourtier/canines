# -*- coding: utf-8 -*-

import socket
from threading import Thread
import struct


class PartyThread(Thread):

    def __init__(self, sock, current_map):
        Thread.__init__(self)
        if not isinstance(sock, socket.socket) or sock is None:
            raise TypeError("Necessite une vraie socket")
        self.__socket = sock
        self.map = current_map

    def __getcommand(self):
        commande = bytes()
        while len(commande) < 3:
            commande += self.__socket.recv(3 - len(commande))
        return commande.decode()

    def __number_of_changes(self):
        data = bytes()
        while len(data) < 1:
            data += self.__socket.recv(1 - len(data))
        return struct.unpack("b", data)[0]

    def __get_changes(self, n):
        changes = []
        # TODO : séparer
        for i in range(n):
            data = bytes()
            while len(data) < 5:
                data += self.__socket.recv(5 - len(data))
            changes.append(struct.unpack("b", data)[0])
        return changes

    def __sendcommand(self, commande, data1, data2):
        paquet = bytes()
        paquet += commande.encode()
        if type(data1) in (str,):
            paquet += data1.encode()
        else:
            paquet += struct.pack("=B", data1)
        if type(data2) in (str,):
            paquet += data2.encode()
        else:
            # transforms array of integer into string of bytes
            paquet += str(bytearray(data2))
        self.__socket.send(paquet)

    def __printerror(self, message):
        print(message)
        try:
            self.__socket.close()
        except:
            print("erreur lors de la fermeture de la socket")

    def run(self):

        while True:
            commande = self.__getcommand()
            if commande not in ["SET", "HUM", "HME", "MAP", "UPD", "END", "BYE"]:
                self.__printerror("Erreur protocole: mauvaise commande reçue.")

            elif commande == "END":
                # En attente de SET ou de BYE
                pass
                if commande == "BYE":
                    print("fin de la communication – On a gagné !")
                    break
                elif commande == "SET":
                    pass
                else:
                    raise ValueError("Il ne se passe rien, pas normal")

            elif commande == "UPD":
                # get updates
                number_of_changes = self.__number_of_changes()
                changes = self.__get_changes(number_of_changes)

                # TODO, call AI with the map and receive new map updated
                # res = call_ai(map, changes)
                self.__sendcommand(res)
            else:
                raise ValueError("commande inconnue")

        self.__socket.close()
