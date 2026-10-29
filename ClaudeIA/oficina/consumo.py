"""Controle do que foi consumido: quem (cliente/veículo) usou qual peça, e quanto pagou."""
from estruturas.lista_encadeada import ListaEncadeada


class RegistroConsumo:
    def __init__(self, cpf, nome_cliente, placa, numero_os, codigo, nome_peca, quantidade, valor):
        self.cpf, self.nome_cliente, self.placa = cpf, nome_cliente, placa
        self.numero_os, self.codigo, self.nome_peca = numero_os, codigo, nome_peca
        self.quantidade, self.valor = quantidade, valor


class ControleConsumo:
    def __init__(self):
        self._registros = ListaEncadeada()

    def registrar(self, registro):
        self._registros.adicionar_fim(registro)

    def por_placa(self, placa):
        """Devolve ListaEncadeada com o consumo de um veículo."""
        resultado = ListaEncadeada()
        for r in self._registros:
            if r.placa == placa.upper():
                resultado.adicionar_fim(r)
        return resultado

    def total_pecas(self):
        return sum(r.valor for r in self._registros)

    def __iter__(self):
        return iter(self._registros)
