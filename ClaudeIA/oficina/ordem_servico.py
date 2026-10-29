"""Ordem de Serviço (OS): peças e serviços adicionados ao longo do atendimento."""
from datetime import datetime
from estruturas.lista_encadeada import ListaEncadeada
from estruturas.pilha import Pilha


class ItemPeca:
    def __init__(self, codigo, nome, quantidade):
        self.codigo, self.nome, self.quantidade = codigo, nome, quantidade


class Servico:
    def __init__(self, descricao, valor):
        self.descricao, self.valor = descricao, valor


class OrdemServico:
    def __init__(self, numero, placa, nome_cliente, mecanico, box, arvore):
        self.numero = numero
        self.placa = placa
        self.nome_cliente = nome_cliente
        self.mecanico = mecanico
        self.box = box
        self.arvore = arvore                  # diagnóstico deste veículo
        self.abertura = datetime.now()
        self.pecas = ListaEncadeada()
        self.servicos = ListaEncadeada()
        self.remontagem_concluida = False
        self.fechada = False
        # PILHA de ações: a última ação feita é a primeira a ser desfeita (LIFO)
        self._historico = Pilha()

    def _exigir_aberta(self):
        if self.fechada:
            raise ValueError("OS já fechada")

    # ---------- peças ----------
    def adicionar_peca(self, codigo, nome, quantidade):
        self._exigir_aberta()
        item = self.pecas.buscar(lambda p: p.codigo == codigo)
        if item:                              # mesma peça: soma a quantidade
            item.quantidade += quantidade
        else:
            self.pecas.adicionar_fim(ItemPeca(codigo, nome, quantidade))
        self._historico.empilhar(("add_peca", codigo, nome, quantidade))

    def remover_peca(self, codigo):
        self._exigir_aberta()
        item = self.pecas.remover(lambda p: p.codigo == codigo)
        if item is None:
            raise ValueError("Peça não está na OS")
        self._historico.empilhar(("rem_peca", item.codigo, item.nome, item.quantidade))

    # ---------- serviços ----------
    def adicionar_servico(self, descricao, valor):
        self._exigir_aberta()
        self.servicos.adicionar_fim(Servico(descricao, valor))
        self._historico.empilhar(("add_serv", descricao, valor))

    def remover_servico(self, descricao):
        self._exigir_aberta()
        serv = self.servicos.remover(lambda s: s.descricao == descricao)
        if serv is None:
            raise ValueError("Serviço não está na OS")
        self._historico.empilhar(("rem_serv", serv.descricao, serv.valor))

    def desfazer_ultima_acao(self):
        """Usa a pilha para reverter a última alteração (ex.: remoção por engano)."""
        self._exigir_aberta()
        if self._historico.esta_vazia():
            raise ValueError("Nada para desfazer")
        acao = self._historico.desempilhar()
        tipo = acao[0]
        # Desfazer não pode empilhar de novo, então mexemos direto nas listas.
        if tipo == "add_peca":
            item = self.pecas.buscar(lambda p: p.codigo == acao[1])
            item.quantidade -= acao[3]
            if item.quantidade <= 0:
                self.pecas.remover(lambda p: p.codigo == acao[1])
        elif tipo == "rem_peca":
            self.pecas.adicionar_fim(ItemPeca(acao[1], acao[2], acao[3]))
        elif tipo == "add_serv":
            self.servicos.remover(lambda s: s.descricao == acao[1])
        elif tipo == "rem_serv":
            self.servicos.adicionar_fim(Servico(acao[1], acao[2]))

    def valor_mao_de_obra(self):
        return sum(s.valor for s in self.servicos)

    def concluir_remontagem(self):
        self.remontagem_concluida = True


class GerenciadorOS:
    """Lista de OS abertas + gerador do número sequencial."""

    def __init__(self):
        self._abertas = ListaEncadeada()
        self._proximo_numero = 1

    def abrir(self, placa, nome_cliente, mecanico, box, arvore):
        os_ = OrdemServico(self._proximo_numero, placa, nome_cliente, mecanico, box, arvore)
        self._proximo_numero += 1
        self._abertas.adicionar_fim(os_)
        return os_

    def buscar(self, numero):
        return self._abertas.buscar(lambda o: o.numero == numero)

    def encerrar(self, numero):
        """Tira a OS da lista de abertas (chamado no fechamento)."""
        return self._abertas.remover(lambda o: o.numero == numero)

    def __iter__(self):
        return iter(self._abertas)
