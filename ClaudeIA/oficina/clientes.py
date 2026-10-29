"""Controle de Clientes e Veículos.

COMBINAÇÃO 1: ListaEncadeada de Cliente, onde cada Cliente contém uma
ListaEncadeada de Veiculo.
"""
from estruturas.lista_encadeada import ListaEncadeada


class Veiculo:
    def __init__(self, placa, modelo, marca, ano):
        self.placa = placa.upper()
        self.modelo = modelo
        self.marca = marca
        self.ano = ano

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo} ({self.ano})"


class Cliente:
    def __init__(self, nome, cpf, telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.veiculos = ListaEncadeada()   # sem limite de veículos por cliente


class RepositorioClientes:
    """Regras de negócio sobre a lista de clientes."""

    def __init__(self):
        self._clientes = ListaEncadeada()

    # ---------- clientes ----------
    def cadastrar_cliente(self, nome, cpf, telefone):
        if self.buscar_por_cpf(cpf) is not None:
            raise ValueError(f"CPF {cpf} já cadastrado")
        cliente = Cliente(nome, cpf, telefone)
        self._clientes.adicionar_fim(cliente)
        return cliente

    def buscar_por_cpf(self, cpf):
        return self._clientes.buscar(lambda c: c.cpf == cpf)

    def remover_cliente(self, cpf):
        """Remove o cliente (e, com ele, toda a lista de veículos)."""
        removido = self._clientes.remover(lambda c: c.cpf == cpf)
        if removido is None:
            raise ValueError("Cliente não encontrado")
        return removido

    # ---------- veículos ----------
    def adicionar_veiculo(self, cpf, placa, modelo, marca, ano):
        cliente = self.buscar_por_cpf(cpf)
        if cliente is None:
            raise ValueError("Cliente não encontrado")
        if self.buscar_por_placa(placa) is not None:   # placa é única na oficina
            raise ValueError(f"Placa {placa} já cadastrada")
        veiculo = Veiculo(placa, modelo, marca, ano)
        cliente.veiculos.adicionar_fim(veiculo)
        return veiculo

    def buscar_por_placa(self, placa):
        """Percorre as DUAS listas: para cada cliente, procura na lista dele.
        Devolve (cliente, veiculo) ou None. Custo O(C + V)."""
        placa = placa.upper()
        for cliente in self._clientes:
            veiculo = cliente.veiculos.buscar(lambda v: v.placa == placa)
            if veiculo is not None:
                return cliente, veiculo
        return None

    def remover_veiculo(self, placa):
        achado = self.buscar_por_placa(placa)
        if achado is None:
            raise ValueError("Veículo não encontrado")
        cliente, _ = achado
        return cliente.veiculos.remover(lambda v: v.placa == placa.upper())
