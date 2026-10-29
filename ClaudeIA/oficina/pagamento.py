"""Controle de Pagamento: um registro por OS fechada."""
from datetime import datetime
from estruturas.lista_encadeada import ListaEncadeada

FORMAS = ("PIX", "CARTAO", "DINHEIRO")


class Pagamento:
    def __init__(self, pagador, numero_os, forma, parcelas, valor_pecas, valor_mao_obra):
        forma = forma.upper()
        if forma not in FORMAS:
            raise ValueError(f"Forma de pagamento inválida: {forma}")
        if forma == "CARTAO":
            if parcelas < 1:
                raise ValueError("Cartão exige ao menos 1 parcela (1 = à vista)")
        else:
            parcelas = 0                      # parcelas só existem no cartão
        self.pagador = pagador
        self.numero_os = numero_os
        self.forma = forma
        self.parcelas = parcelas
        self.valor_pecas = valor_pecas
        self.valor_mao_obra = valor_mao_obra
        self.valor_total = valor_pecas + valor_mao_obra
        self.data_hora = datetime.now()


class HistoricoPagamentos:
    def __init__(self):
        self._pagamentos = ListaEncadeada()

    def registrar(self, pagamento):
        self._pagamentos.adicionar_fim(pagamento)

    def total_recebido(self):
        return sum(p.valor_total for p in self._pagamentos)

    def __iter__(self):
        return iter(self._pagamentos)
