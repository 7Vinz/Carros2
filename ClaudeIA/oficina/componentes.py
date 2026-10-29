"""Diagnóstico: árvore de componentes do veículo (árvore geral, pré-definida)."""
from estruturas.arvore import NoArvore


class Componente:
    def __init__(self, nome, codigo=None, defeito=False):
        self.nome = nome
        self.codigo = codigo          # só peças têm código
        self.defeito = defeito

    @property
    def estado(self):
        return "Com defeito" if self.defeito else "OK"


class ArvoreComponentes:
    def __init__(self):
        self.raiz = NoArvore(Componente("Veículo"))
        self._construir_padrao()

    def _construir_padrao(self):
        """Hierarquia fixa do enunciado: Veículo > Sistemas > Subconjuntos > Peças."""
        r = self.raiz
        motor = r.adicionar_filho(Componente("Motor"))
        ign = motor.adicionar_filho(Componente("Sistema de ignição"))
        ign.adicionar_filho(Componente("Vela", "VELA-01"))
        ign.adicionar_filho(Componente("Bobina", "BOB-01"))
        motor.adicionar_filho(Componente("Correia dentada", "COR-01"))
        freios = r.adicionar_filho(Componente("Freios"))
        freios.adicionar_filho(Componente("Pastilha dianteira", "PAST-01"))
        freios.adicionar_filho(Componente("Disco dianteiro", "DISC-01"))
        susp = r.adicionar_filho(Componente("Suspensão"))
        susp.adicionar_filho(Componente("Amortecedor", "AMORT-01"))
        susp.adicionar_filho(Componente("Bandeja", "BAND-01"))

    def exibir(self):
        """Texto indentado gerado por percurso em profundidade (pré-ordem)."""
        linhas = []

        def visitar(no, nivel):
            c = no.dado
            cod = f" [{c.codigo}]" if c.codigo else ""
            linhas.append("    " * nivel + f"- {c.nome}{cod} ({c.estado})")

        self.raiz.percorrer_pre_ordem(visitar)
        return "\n".join(linhas)

    def marcar_defeito(self, nome):
        no = self.raiz.buscar(lambda c: c.nome.lower() == nome.lower())
        if no is None:
            raise ValueError(f"Componente '{nome}' não existe")
        no.dado.defeito = True

    def pecas_com_defeito(self):
        """Devolve as peças (nós com código) marcadas como defeituosas."""
        from estruturas.lista_encadeada import ListaEncadeada
        achadas = ListaEncadeada()
        self.raiz.percorrer_pre_ordem(
            lambda no, _n: achadas.adicionar_fim(no.dado)
            if no.dado.codigo and no.dado.defeito else None)
        return achadas
