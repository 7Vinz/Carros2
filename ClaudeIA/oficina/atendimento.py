"""Controle de Atendimento: espera de veículos e boxes (elevadores).

COMBINAÇÃO 2: Fila + Fila. Guincho tem fila própria e sempre é chamada primeiro;
só se estiver vazia olhamos a fila normal.
"""
from datetime import datetime
from estruturas.fila import Fila


class Chegada:
    def __init__(self, placa, nome_cliente, queixa, guincho, data_hora):
        self.placa = placa.upper()
        self.nome_cliente = nome_cliente
        self.queixa = queixa
        self.guincho = guincho
        self.data_hora = data_hora


class Atendimento:
    def __init__(self, qtd_boxes):
        self._fila_guincho = Fila()
        self._fila_normal = Fila()
        # Boxes: vetor fixo e pequeno, usado só internamente (None = livre,
        # senão guarda a Chegada em atendimento).
        self._boxes = [None] * qtd_boxes

    def registrar_chegada(self, placa, nome_cliente, queixa, guincho=False, data_hora=None):
        chegada = Chegada(placa, nome_cliente, queixa, guincho, data_hora or datetime.now())
        # Cada fila já preserva a ordem de chegada (FIFO) entre os seus membros.
        (self._fila_guincho if guincho else self._fila_normal).enfileirar(chegada)
        return chegada

    def proximo_da_espera(self):
        """Indica (sem remover) quem é o próximo: guincho primeiro, depois normal."""
        if not self._fila_guincho.esta_vazia():
            return self._fila_guincho.primeiro()
        return self._fila_normal.primeiro()

    def _box_livre(self):
        for numero, ocupante in enumerate(self._boxes):
            if ocupante is None:
                return numero
        return None

    def chamar_proximo(self):
        """Se há box livre e alguém esperando, aloca o box. Devolve (n_box, Chegada) ou None."""
        box = self._box_livre()
        if box is None or self.proximo_da_espera() is None:
            return None
        fila = self._fila_guincho if not self._fila_guincho.esta_vazia() else self._fila_normal
        chegada = fila.desenfileirar()
        self._boxes[box] = chegada
        return box, chegada

    def liberar_box(self, numero_box):
        """Libera o box e INDICA automaticamente o próximo veículo (ou None)."""
        self._boxes[numero_box] = None
        return self.proximo_da_espera()

    def tamanho_espera(self):
        return len(self._fila_guincho) + len(self._fila_normal)
