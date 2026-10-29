"""Controle de Estoque de Peças e Fluidos.

COMBINAÇÃO 3: ListaEncadeada de Produto, onde cada Produto contém uma
Fila de Lote. A fila garante FIFO: a saída consome sempre o lote mais antigo.
"""
from datetime import date
from estruturas.fila import Fila
from estruturas.lista_encadeada import ListaEncadeada


class Lote:
    def __init__(self, fornecedor, preco_compra, preco_venda, data_compra, quantidade, validade=None):
        self.fornecedor = fornecedor
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda
        self.data_compra = data_compra
        self.validade = validade          # None = produto sem validade
        self.quantidade = quantidade

    def vencido(self, hoje):
        return self.validade is not None and self.validade < hoje


class Produto:
    def __init__(self, nome, codigo, minimo):
        self.nome = nome
        self.codigo = codigo
        self.minimo = minimo
        self.lotes = Fila()               # frente da fila = lote mais antigo
        self.em_alerta = False            # evita repetir o mesmo alerta várias vezes

    def quantidade_total(self):
        return sum(l.quantidade for l in self.lotes)


class Perda:
    """Registro de lote descartado por validade."""
    def __init__(self, produto, lote, data):
        self.codigo, self.nome = produto.codigo, produto.nome
        self.quantidade = lote.quantidade
        self.prejuizo = lote.quantidade * lote.preco_compra
        self.data = data


class ConsumoLote:
    """Quanto saiu de qual lote, e a que preço de venda (para valorar a OS)."""
    def __init__(self, quantidade, preco_venda, preco_compra):
        self.quantidade = quantidade
        self.preco_venda = preco_venda
        self.preco_compra = preco_compra


class Estoque:
    def __init__(self):
        self._produtos = ListaEncadeada()
        self.perdas = ListaEncadeada()
        self.alertas = ListaEncadeada()   # mensagens de estoque baixo

    def cadastrar_produto(self, nome, codigo, minimo):
        if self.buscar_produto(codigo):
            raise ValueError("Produto já cadastrado")
        produto = Produto(nome, codigo, minimo)
        self._produtos.adicionar_fim(produto)
        return produto

    def buscar_produto(self, codigo):
        return self._produtos.buscar(lambda p: p.codigo == codigo)

    def _obter(self, codigo):
        produto = self.buscar_produto(codigo)
        if produto is None:
            raise ValueError(f"Produto {codigo} não existe")
        return produto

    def registrar_compra(self, codigo, lote):
        """Novo lote entra no FIM da fila (compras chegam em ordem cronológica)."""
        self._obter(codigo).lotes.enfileirar(lote)

    def descartar_vencidos(self, hoje=None):
        """Remove lotes vencidos (inclusive no meio da fila) e registra a perda.
        Reconstrói a fila mantendo a ordem dos lotes válidos. O(L) por produto."""
        hoje = hoje or date.today()
        for produto in self._produtos:
            for _ in range(len(produto.lotes)):
                lote = produto.lotes.desenfileirar()
                if lote.vencido(hoje):
                    self.perdas.adicionar_fim(Perda(produto, lote, hoje))
                else:
                    produto.lotes.enfileirar(lote)   # volta ao fim, ordem preservada
            self._verificar_alerta(produto)

    def quantidade_total(self, codigo):
        return self._obter(codigo).quantidade_total()

    def dar_baixa(self, codigo, quantidade, hoje=None):
        """Consome `quantidade` começando pelo lote mais antigo.
        Devolve ListaEncadeada de ConsumoLote. Levanta erro se faltar estoque."""
        hoje = hoje or date.today()
        self.descartar_vencidos(hoje)
        produto = self._obter(codigo)
        if produto.quantidade_total() < quantidade:
            raise ValueError(f"Estoque insuficiente de {produto.nome}")
        consumos = ListaEncadeada()
        restante = quantidade
        while restante > 0:
            lote = produto.lotes.primeiro()          # sempre o mais antigo
            usado = min(restante, lote.quantidade)
            lote.quantidade -= usado
            restante -= usado
            consumos.adicionar_fim(ConsumoLote(usado, lote.preco_venda, lote.preco_compra))
            if lote.quantidade == 0:                 # lote esgotado sai da fila
                produto.lotes.desenfileirar()
        self._verificar_alerta(produto)
        return consumos

    def ajustar_quantidade(self, codigo, nova_quantidade):
        """Ajuste de inventário: leva o total para `nova_quantidade`.
        Sobra -> soma no lote mais novo; falta -> retira dos mais antigos."""
        produto = self._obter(codigo)
        diferenca = nova_quantidade - produto.quantidade_total()
        if diferenca > 0:
            if produto.lotes.esta_vazia():
                raise ValueError("Sem lote para receber o ajuste; registre uma compra")
            produto.lotes.ultimo().quantidade += diferenca
        elif diferenca < 0:
            self.dar_baixa(codigo, -diferenca)
        self._verificar_alerta(produto)

    def _verificar_alerta(self, produto):
        abaixo = produto.quantidade_total() < produto.minimo
        if not abaixo:
            produto.em_alerta = False     # reabasteceu: rearma o alerta
        elif not produto.em_alerta:
            produto.em_alerta = True      # só alerta na transição para "abaixo"
            self.alertas.adicionar_fim(
                f"ALERTA: {produto.nome} ({produto.codigo}) com {produto.quantidade_total()} "
                f"un., abaixo do mínimo de {produto.minimo}")
