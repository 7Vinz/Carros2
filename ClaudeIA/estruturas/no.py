"""Nó simples usado pelas estruturas encadeadas (lista, fila e pilha)."""


class No:
    """Guarda um dado e a referência para o próximo nó da cadeia."""
    __slots__ = ("dado", "proximo")

    def __init__(self, dado):
        self.dado = dado
        self.proximo = None
