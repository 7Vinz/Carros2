"""Árvore GERAL (não binária, não de busca): cada nó tem de 0 a N filhos."""
from estruturas.lista_encadeada import ListaEncadeada


class NoArvore:
    def __init__(self, dado):
        self.dado = dado
        self.filhos = ListaEncadeada()   # lista de filhos => quantidade ilimitada

    def adicionar_filho(self, dado):
        """Cria um filho com o dado informado e o devolve (facilita montar a árvore)."""
        filho = NoArvore(dado)
        self.filhos.adicionar_fim(filho)
        return filho

    def percorrer_pre_ordem(self, visitar, nivel=0):
        """Profundidade em PRÉ-ORDEM: visita o pai ANTES dos filhos. O(n).
        `visitar(no, nivel)` recebe o nó e a profundidade (usada na indentação)."""
        visitar(self, nivel)
        for filho in self.filhos:
            filho.percorrer_pre_ordem(visitar, nivel + 1)

    def buscar(self, condicao):
        """Busca em pré-ordem; devolve o primeiro NoArvore que satisfaz a condição."""
        if condicao(self.dado):
            return self
        for filho in self.filhos:
            achado = filho.buscar(condicao)
            if achado is not None:
                return achado
        return None
