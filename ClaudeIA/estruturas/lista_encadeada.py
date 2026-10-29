"""Lista encadeada simples, com ponteiro para o fim (inserção no fim em O(1))."""
from estruturas.no import No


class ListaEncadeada:
    def __init__(self):
        self._inicio = None
        self._fim = None      # evita percorrer a lista toda para inserir no fim
        self._tamanho = 0

    def adicionar_fim(self, dado):
        """O(1): liga o novo nó depois do último."""
        novo = No(dado)
        if self._fim is None:
            self._inicio = self._fim = novo
        else:
            self._fim.proximo = novo
            self._fim = novo
        self._tamanho += 1

    def buscar(self, condicao):
        """O(n): devolve o primeiro dado que satisfaz `condicao(dado)` ou None."""
        atual = self._inicio
        while atual is not None:
            if condicao(atual.dado):
                return atual.dado
            atual = atual.proximo
        return None

    def remover(self, condicao):
        """O(n): remove o primeiro dado que satisfaz a condição e o devolve (ou None)."""
        anterior, atual = None, self._inicio
        while atual is not None:
            if condicao(atual.dado):
                if anterior is None:          # removendo o primeiro nó
                    self._inicio = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                if atual is self._fim:        # removendo o último: atualiza o fim
                    self._fim = anterior
                self._tamanho -= 1
                return atual.dado
            anterior, atual = atual, atual.proximo
        return None

    def esta_vazia(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        """Permite usar `for item in lista` percorrendo os nós."""
        atual = self._inicio
        while atual is not None:
            yield atual.dado
            atual = atual.proximo
