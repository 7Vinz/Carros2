"""Fachada da oficina: orquestra as estruturas e aplica as regras do fluxo completo."""
from estruturas.lista_encadeada import ListaEncadeada
from oficina.clientes import RepositorioClientes
from oficina.atendimento import Atendimento
from oficina.componentes import ArvoreComponentes
from oficina.estoque import Estoque
from oficina.ordem_servico import GerenciadorOS
from oficina.pagamento import Pagamento, HistoricoPagamentos
from oficina.consumo import ControleConsumo, RegistroConsumo


class Oficina:
    def __init__(self, qtd_boxes=2):
        self.clientes = RepositorioClientes()
        self.atendimento = Atendimento(qtd_boxes)
        self.estoque = Estoque()
        self.ordens = GerenciadorOS()
        self.pagamentos = HistoricoPagamentos()
        self.consumo = ControleConsumo()

    def chamar_proximo_e_abrir_os(self, mecanico):
        """Passos 2 do fluxo: aloca o box e abre a OS (com árvore de diagnóstico própria)."""
        resultado = self.atendimento.chamar_proximo()
        if resultado is None:
            return None
        box, chegada = resultado
        return self.ordens.abrir(chegada.placa, chegada.nome_cliente, mecanico, box,
                                 ArvoreComponentes())

    def adicionar_peca_na_os(self, numero_os, codigo, quantidade):
        """Inclui peça na OS validando se há estoque (a baixa efetiva ocorre no fechamento,
        assim remover uma peça antes de fechar não exige estornar o estoque)."""
        os_ = self._obter_os(numero_os)
        produto = self.estoque.buscar_produto(codigo)
        if produto is None:
            raise ValueError("Produto inexistente")
        self.estoque.descartar_vencidos()
        ja_na_os = os_.pecas.buscar(lambda p: p.codigo == codigo)
        total_pedido = quantidade + (ja_na_os.quantidade if ja_na_os else 0)
        if produto.quantidade_total() < total_pedido:
            raise ValueError(f"Estoque insuficiente de {produto.nome}")
        os_.adicionar_peca(codigo, produto.nome, quantidade)

    def fechar_os(self, numero_os, forma, parcelas=1, hoje=None):
        """Passo 5: baixa de estoque + pagamento + registro de consumo, tudo junto.
        Valida tudo ANTES de alterar qualquer coisa (evita fechar pela metade)."""
        os_ = self._obter_os(numero_os)
        if not os_.remontagem_concluida:
            raise ValueError("A OS só pode ser fechada após a remontagem do veículo")
        self.estoque.descartar_vencidos(hoje)
        for item in os_.pecas:                           # 1) pré-validação do estoque
            if self.estoque.quantidade_total(item.codigo) < item.quantidade:
                raise ValueError(f"Estoque insuficiente de {item.nome}")

        achado = self.clientes.buscar_por_placa(os_.placa)
        cliente = achado[0] if achado else None

        valor_pecas = 0.0                                # 2) baixa pelo lote mais antigo
        for item in os_.pecas:
            consumos = self.estoque.dar_baixa(item.codigo, item.quantidade, hoje)
            valor_item = sum(c.quantidade * c.preco_venda for c in consumos)
            valor_pecas += valor_item
            self.consumo.registrar(RegistroConsumo(
                cliente.cpf if cliente else "-", os_.nome_cliente, os_.placa, os_.numero,
                item.codigo, item.nome, item.quantidade, valor_item))

        pagamento = Pagamento(os_.nome_cliente, os_.numero, forma, parcelas,   # 3) pagamento
                              valor_pecas, os_.valor_mao_de_obra())
        self.pagamentos.registrar(pagamento)

        os_.fechada = True                               # 4) encerra e libera o box
        self.ordens.encerrar(numero_os)
        proximo = self.atendimento.liberar_box(os_.box)  # indica o próximo automaticamente
        return pagamento, proximo

    def _obter_os(self, numero):
        os_ = self.ordens.buscar(numero)
        if os_ is None:
            raise ValueError(f"OS {numero} não encontrada entre as abertas")
        return os_
