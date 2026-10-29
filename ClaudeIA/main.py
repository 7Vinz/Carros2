"""Simulação de um atendimento completo na Oficina Mecânica.

Execute com:  python main.py
"""
from datetime import date, timedelta
from oficina.oficina import Oficina
from oficina.estoque import Lote


def titulo(texto):
    print(f"\n{'=' * 60}\n{texto}\n{'=' * 60}")


def main():
    hoje = date.today()
    of = Oficina(qtd_boxes=1)       # 1 box só, para mostrar a fila funcionando

    # ---------- Cadastro de clientes e veículos ----------
    titulo("0) Cadastro de clientes e veículos")
    of.clientes.cadastrar_cliente("Ana Souza", "111.111.111-11", "(19) 99999-0001")
    of.clientes.cadastrar_cliente("Bruno Lima", "222.222.222-22", "(19) 99999-0002")
    of.clientes.cadastrar_cliente("Carla Dias", "333.333.333-33", "(19) 99999-0003")
    of.clientes.adicionar_veiculo("111.111.111-11", "ABC1D23", "Onix", "Chevrolet", 2019)
    of.clientes.adicionar_veiculo("111.111.111-11", "XYZ9K88", "HB20", "Hyundai", 2021)  # 2º carro
    of.clientes.adicionar_veiculo("222.222.222-22", "DEF4G56", "Gol", "Volkswagen", 2015)
    of.clientes.adicionar_veiculo("333.333.333-33", "GHI7J10", "Corolla", "Toyota", 2020)
    cliente, veiculo = of.clientes.buscar_por_placa("xyz9k88")
    print(f"Busca por placa XYZ9K88 -> {cliente.nome}: {veiculo}")

    # ---------- Estoque ----------
    titulo("Estoque: dois lotes de pastilha e um lote de óleo vencido")
    e = of.estoque
    e.cadastrar_produto("Pastilha de freio", "PAST-01", minimo=3)
    e.cadastrar_produto("Óleo 5W30", "OLEO-01", minimo=2)
    # Lote antigo mais barato e lote novo mais caro: a saída deve usar o antigo primeiro.
    e.registrar_compra("PAST-01", Lote("AutoPeças SA", 50, 90, hoje - timedelta(days=60), 4))
    e.registrar_compra("PAST-01", Lote("AutoPeças SA", 60, 110, hoje - timedelta(days=5), 4))
    e.registrar_compra("OLEO-01", Lote("LubriMax", 30, 55, hoje - timedelta(days=200), 5,
                                       validade=hoje - timedelta(days=10)))   # já vencido
    e.registrar_compra("OLEO-01", Lote("LubriMax", 32, 58, hoje - timedelta(days=3), 3,
                                       validade=hoje + timedelta(days=365)))
    e.descartar_vencidos()
    for p in e.perdas:
        print(f"Perda registrada: {p.nome} x{p.quantidade} (prejuízo R$ {p.prejuizo:.2f})")

    # ---------- 1) Chegada ----------
    titulo("1) Chegada dos veículos")
    at = of.atendimento
    at.registrar_chegada("ABC1D23", "Ana Souza", "Barulho no freio")
    at.registrar_chegada("DEF4G56", "Bruno Lima", "Motor falhando")
    at.registrar_chegada("GHI7J10", "Carla Dias", "Não liga", guincho=True)  # chegou por último
    print(f"Veículos aguardando: {at.tamanho_espera()}")
    prox = at.proximo_da_espera()
    print(f"Próximo da fila: {prox.placa} ({'guincho' if prox.guincho else 'normal'})")

    # ---------- 2) Chamada + abertura da OS ----------
    titulo("2) Box livre -> chama o próximo e abre a OS")
    os_ = of.chamar_proximo_e_abrir_os("Mecânico Zé")
    print(f"OS #{os_.numero} aberta para {os_.placa} ({os_.nome_cliente}) no box {os_.box}")
    print("Guincho passou na frente dos que chegaram antes.")

    # ---------- 3) Diagnóstico ----------
    titulo("3) Diagnóstico na árvore de componentes")
    os_.arvore.marcar_defeito("Pastilha dianteira")
    print(os_.arvore.exibir())
    print("\nPeças com defeito:", ", ".join(c.nome for c in os_.arvore.pecas_com_defeito()))

    # ---------- 4) Peças e serviços ----------
    titulo("4) Peças e serviços na OS")
    of.adicionar_peca_na_os(os_.numero, "PAST-01", 6)       # 4 do lote antigo + 2 do novo
    os_.adicionar_servico("Troca de pastilhas", 150.0)
    os_.adicionar_servico("Alinhamento", 80.0)
    os_.adicionar_servico("Balanceamento", 50.0)
    os_.remover_servico("Balanceamento")                    # removido sem querer...
    os_.desfazer_ultima_acao()                              # ...a PILHA desfaz a última ação
    print("Balanceamento removido por engano e restaurado via desfazer (pilha).")
    os_.remover_servico("Alinhamento")                      # cliente não autorizou este
    print("Serviços na OS:", ", ".join(s.descricao for s in os_.servicos))

    try:
        of.fechar_os(os_.numero, "pix")
    except ValueError as erro:
        print(f"Tentativa de fechar antes da remontagem -> bloqueado: {erro}")
    os_.concluir_remontagem()

    # ---------- 5) Fechamento ----------
    titulo("5) Fechamento da OS e pagamento")
    pag, proximo = of.fechar_os(os_.numero, "cartao", parcelas=3)
    print(f"Pago por {pag.pagador}: peças R$ {pag.valor_pecas:.2f} + mão de obra "
          f"R$ {pag.valor_mao_obra:.2f} = R$ {pag.valor_total:.2f} ({pag.forma} {pag.parcelas}x)")
    print("  (peças: 4 x R$90 do lote antigo + 2 x R$110 do lote novo = R$580)")
    print(f"Box liberado. Próximo indicado: {proximo.placa if proximo else 'ninguém'}")
    for a in e.alertas:
        print(a)

    # ---------- Segundo atendimento rapidamente ----------
    titulo("Segundo atendimento (Ana, fila normal)")
    os2 = of.chamar_proximo_e_abrir_os("Mecânico Zé")
    print(f"OS #{os2.numero} aberta para {os2.placa}")
    of.adicionar_peca_na_os(os2.numero, "OLEO-01", 1)
    os2.adicionar_servico("Troca de óleo", 60.0)
    os2.concluir_remontagem()
    pag2, _ = of.fechar_os(os2.numero, "pix")
    print(f"Total pago: R$ {pag2.valor_total:.2f} ({pag2.forma})")

    # ---------- Conferência ----------
    titulo("Conferência: consumo por veículo e total recebido")
    for r in of.consumo:
        print(f"OS {r.numero_os} | {r.nome_cliente} | {r.placa} | {r.nome_peca} x{r.quantidade} "
              f"= R$ {r.valor:.2f}")
    print(f"Total recebido pela oficina: R$ {of.pagamentos.total_recebido():.2f}")

    # ---------- Ajuste de inventário ----------
    titulo("Ajuste de inventário (pastilhas contadas: 1 unidade)")
    e.ajustar_quantidade("PAST-01", 1)
    print("Total agora:", e.quantidade_total("PAST-01"))
    print("Alertas já emitidos:", len(e.alertas))


if __name__ == "__main__":
    main()
