"""Fila (FIFO) encadeada: entra no fim, sai pelo início. Tudo em O(1)."""
from estruturas.no import No


class Fila:
    def __init__(self):
        self._inicio = None
        self._fim = None
        self._tamanho = 0

    def enfileirar(self, dado):
        novo = No(dado)
        if self._fim is None:
            self._inicio = self._fim = novo
        else:
            self._fim.proximo = novo
            self._fim = novo
        self._tamanho += 1

    def desenfileirar(self):
        if self._inicio is None:
            raise IndexError("Fila vazia")
        dado = self._inicio.dado
        self._inicio = self._inicio.proximo
        if self._inicio is None:
            self._fim = None
        self._tamanho -= 1
        return dado

    def primeiro(self):
        """Espia quem está na frente sem remover (None se vazia)."""
        return None if self._inicio is None else self._inicio.dado

    def ultimo(self):
        """Espia quem está no fim sem remover (None se vazia)."""
        return None if self._fim is None else self._fim.dado

    def esta_vazia(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        atual = self._inicio
        while atual is not None:
            yield atual.dado
            atual = atual.proximo
