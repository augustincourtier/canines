from server.main import *
import socket
from threading import Thread
import struct


class PartyThread(Thread):

    def __init__(self, sock):
        Thread.__init__(self)
        if not isinstance(sock, socket.socket) or sock is None:
            raise TypeError("Necessite une vraie socket")
        self.__socket = sock
        self.map = current_map

    def __getcommand(self):
        data = bytes()
        while len(data) < 3:
            data += self.__socket.recv(3 - len(data))
        return data.decode()

    def __number_of_changes(self):
        data = bytes()
        while len(data) < 1:
            data += self.__socket.recv(1 - len(data))
        return struct.unpack("d", data)[0]

    def __get_changes(self, n):
        changes = []
        for i in range(n):
            data = bytes()
            while len(data) < 5:
                data += self.__socket.recv(5 - len(data))
            changes.append(data)
        return changes

    def __sendresult(self, res):
        # juste pour etre sur
        res = float(res)
        # TODO implement ATK
        self.__socket.send(struct.pack("MOV", res))

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
                self.__sendresult(res)
            else:
                raise ValueError("commande inconnue")

        self.__socket.close()
