from threading import Thread
import socket
from calculatorthread import CalculatorThread


class Server(Thread):

    def __init__(self, port):
        Thread.__init__(self)
        if not isinstance(port, int):
            raise TypeError("Le port doit etre un entier")

        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind(('localhost', port))
        self.__continuer = True

    def run(self):
        self.__sock.listen(1)  # on autorise une seule connexion en attente à la fois
        print("En attente d'une connexion sur le serveur")
        while self.__continuer:
            try:
                connexion, client = self.__sock.accept()
                CalculatorThread(connexion).start()
            except OSError:
                # se produit quand on coupe la socket
                pass
            except IOError as e:
                # a priori, il y a eu un probleme
                print(e)

        print("Arret du serveur")

    def stoplistening(self):
        self.__continuer = False
        if self.__sock:
            self.__sock.close()




