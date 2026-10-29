"""Pilha (LIFO) encadeada: push/pop pelo topo, tudo em O(1)."""
from estruturas.no import No


class Pilha:
    def __init__(self):
        self._topo = None
        self._tamanho = 0

    def empilhar(self, dado):
        novo = No(dado)
        novo.proximo = self._topo     # o novo nó aponta para o antigo topo
        self._topo = novo
        self._tamanho += 1

    def desempilhar(self):
        if self._topo is None:
            raise IndexError("Pilha vazia")
        dado = self._topo.dado
        self._topo = self._topo.proximo
        self._tamanho -= 1
        return dado

    def esta_vazia(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho
