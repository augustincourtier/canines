from threading import Thread
import socket
import struct


class CalculatorThread(Thread):

    def __init__(self, sock):
        Thread.__init__(self)
        if not isinstance(sock, socket.socket) or sock is None:
            raise TypeError("Necessite une vraie socket")
        self.__socket = sock

    def __getcommand(self):
        data = bytes()
        while len(data)<3:
            data += self.__socket.recv(3 - len(data))
        return data.decode()

    def __getfloat(self):
        data = bytes()
        while len(data)<8:
            data += self.__socket.recv(8 - len(data))
        return struct.unpack("d", data)[0]

    def __sendresult(self, res):
        # juste pour etre sur
        res = float(res)
        self.__socket.send(struct.pack("d", res))

    def __printerror(self, message):
        print(message)
        try:
            self.__socket.close()
        except:
            print("erreur lors de la fermeture de la socket")

    def run(self):
        print("Just connected")

        # implementation du protocole
        self.__socket.send("HLO".encode())
        commande = self.__getcommand()
        if commande != "HLO":
            self.__printerror("Erreur de protocole: attendu HLO")
            return

        while True:
            commande = self.__getcommand()
            if commande == "QUT":
                print("fin de la communication")
                break
            elif commande not in ["ADD", "MIN", "TIM", "DIV"]:
                self.__printerror("Erreur protocole: attendu une opération")

            # recherche de 2 operandes
            op1 = self.__getfloat()
            op2 = self.__getfloat()

            if commande == "ADD":
                self.__sendresult(op1 + op2)
            elif commande == "MIN":
                self.__sendresult(op1 - op2)
            elif commande == "TIM":
                self.__sendresult(op1 * op2)
            elif commande == "DIV":
                self.__sendresult(op1 / op2)
            else:
                raise ValueError("commande inconnue")

        self.__socket.close()
