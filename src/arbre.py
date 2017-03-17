#!/usr/bin/python3
# -*- coding:utf-8 -*

class Arbre:
    """Classe pour représenter les arbres"""

    def __fromList(self, liste):
        """Construit arbre à partir de liste"""
        assert (isinstance(liste, list) or isinstance(liste, tuple))
        assert (len(liste)>=1)
        self.__label = liste [0]
        for sous_arbre in liste[1:]:
            self._fils.append(Arbre(sous_arbre))


    def __init__(self, premier, **kwargs):
        """Crée un arbre à partir de:
        1)Un label et d'une liste de sous arbres eventuels
        2)Un autre arbre"""
        assert (premier != None)
        self.__label = None
        self._fils = []
        if isinstance(premier, list) or isinstance(premier, tuple):  #Création d'un arbre à partir d'un label et d'une liste de sous arbres
            self.__fromList(premier)
        elif isinstance(premier, Arbre):
            self.__label = premier.racine
            for sous_arbre in premier._fils:
                if sous_arbre == None:
                    self._fils.append(None)
                else:
                    self._fils.append.Arbre(sous_arbre)
        else:
            self.__label = premier
            self._fils = kwargs.get('fils', [])

    def __get_racine(self):
        return self.__label

    def __set_racine(self, label):
        self.__label = label

    racine = property(__get_racine, __set_racine, doc = "Accède ou modifie le label de la racine")

    #Fonctions de modification de l'arbre

    def ajoute (self, a):
        """ Ajoute l'arbre a comme nouveau fils de la racine """
        assert(isinstance(a, Arbre))
        self._fils.append(a)

    def remplace(self, pos, a) :
        """ Remplace le fils de la racine situé en position pos par l'arbre a """
        if pos<0:
            pos=len(self._fils)-pos
        if pos<0:
            raise IndexError('Position '+pos+' incorrecte')
        if pos>=len(self._fils):
            raise IndexError('Position '+pos+' incorrecte')
        self._fils[pos] = a

    def __iter__(self) :
        """ Itère sur les fils. Si un fils vaut 'None' il est ignoré """
        for l in self._fils :
            if l!= None :
                yield l  #Yield retourne une valeur mais ne sort pas de la boucle

    def lesfils(self):
        return self._fils

    def __getitem__(self,i) :
        """ Renvoie une référence vers le fils numéro i
        Lève IndexError si l'indice es incorrect
        """
        if i<0:
            i<len(self._fils)-i
        if i not in range(len(self._fils)):
            raise IndexError('Pas de fils '+str(i))
        return self._fils[i]

    def __setitem__(self, i ,v ) :
        """ Modifie le fils numéro i s'il existe et l'ajoute sinon"""
        if i<0:
            i<len(self._fils)-i
        if i<0:
            raise IndexError('Pas de fils '+str(i))
        while len(self._fils)<=i:
            self._fils.append(None)
        if v.__class__==self.__class__ :
            self._fils[i]=v
        else :
            self._fils[i]=self.__class__(v)

    def __str__(self) :
        """ Renvoie une représentation lisible de l'objet sous forme de chaîne de caractères """
        s=[]
        for l in self._fils:
            if l==None:
                s.append('')
            else:
                s.append(str(l))
        s = ",".join(s)
        if s!="" :
            return "("+str(self.__label)+"-("+s+"))"
        else:
            return str(self.__label)

    def __len__(self) :
        """ Renvoie le nombre de fils (différents de None) """
        return len([f for f in self._fils if f != None])

    def __repr__(self) :
        if len(self._fils)==0:
            return self.__class__.__name__+"("+repr(self.racine)+")"
        f=[]
        for l in self._fils:
            if l==None:
                f.append(repr(None))
            else:
                f.append(repr(l))
            pass
        return self.__class__.__name__+"(("+repr(self.racine)+","+",".join(f)+"))"


#if __name__=='__main__' :
    #premiere_carte = Arbre(([[4, [4, 3]], [[4, [4, 1]]], [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10],
                            #[[[4, [4, 3]], [[3, [4, 1]], [1, [5, 1]]], [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]],
                            #[[[4, [4, 3]], [[2, [4, 1]], [2, [5, 1]]], [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]],
                            #[[[4, [4, 3]], [[1, [4, 1]], [3, [5, 1]]], [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]],
                            #[[[4, [4, 3]], [[4, [5, 1]]], [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]]))
    #deuxieme_carte = Arbre(([[4, [4, 3]], [[4, [4, 1]]], [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10],
                            #[[[4, [4, 3]], [[3, [4, 1]], [1, [5, 1]]],
                              #[[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10],
                             #[[[1, [4, 3]], [3, [5, 3]], [[3, [4, 1]], [1, [5, 1]]],
                              #[[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]],
                             #[[[2, [4, 3]], [2, [5, 3]], [[3, [4, 1]], [1, [5, 1]]],
                              #[[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]]
                             #],
                            #[[[4, [4, 3]], [[2, [4, 1]], [2, [5, 1]]],
                              #[[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10],
                             #[[[[1, [4, 3]], [3, [5, 3]]], [[2, [4, 1]], [2, [5, 1]]],
                              #[[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]],
                             #[[[2, [4, 3]], [2, [5, 3]]], [[2, [4, 1]], [2, [5, 1]]],
                              #[[[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]]
                             #],
                            #[[[4, [4, 3]], [[1, [4, 1]], [3, [5, 1]]],
                              #[[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10],
                             #[[[[1, [4, 3]], [3, [5, 3]]], [[1, [4, 1]], [3, [5, 1]]],
                              #[[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]],
                             #[[[[2, [4, 3]], [2, [5, 3]]], [[1, [4, 1]], [3, [5, 1]]],
                              #[[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5, 10]]
                             #],
                            #[[[4, [4, 3]], [[4, [5, 1]]], [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5,
                              #10],
                             #[[[[1, [4, 3]], [3, 5, 3]], [[4, [5, 1]]], [[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5,
                              #10]],
                             #[[[[2, [4, 3]], [2, 5, 3]], [[4, [5, 1]]],
                              #[[2, [9, 4]], [1, [9, 2]], [2, [9, 0]], [4, [2, 2]]], 5,
                              #10]]
                             #]))

    #print(premiere_carte)
    #print(deuxieme_carte)
