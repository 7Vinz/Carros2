# Oficina Mecânica – Estrutura de Dados (Fatec Rio Claro)

Execute a simulação completa: `python main.py` (Python 3.8+, sem dependências).

## Organização
- `estruturas/` – estruturas **genéricas**, feitas do zero: `No`, `ListaEncadeada`, `Fila`, `Pilha`, `NoArvore` (árvore geral).
- `oficina/` – **regras da oficina**: clientes, atendimento, componentes, estoque, OS, pagamento, consumo e a fachada `Oficina`.

## Combinações de estruturas

### 1. Atendimento com prioridade: Fila + Fila
- Classe `Atendimento` (`oficina/atendimento.py`); métodos `registrar_chegada`, `proximo_da_espera`, `chamar_proximo`, `liberar_box`.
- **Por quê:** cada fila preserva a ordem de chegada do seu grupo; a prioridade vira uma regra simples (guincho vazia? usa a normal). Chamar o próximo é O(1).
- **Desvantagem de uma só estrutura:** com uma fila única, o guincho teria de "furar" a fila (inserção no meio, O(n)) ou exigiria busca a cada chamada.

### 2. Estoque: Lista de Produtos + Fila de Lotes
- Classes `Estoque` e `Produto` (`oficina/estoque.py`); métodos `registrar_compra`, `dar_baixa`, `descartar_vencidos`, `ajustar_quantidade`.
- **Por quê:** achar o produto é uma busca (lista, O(P)); consumir o lote mais antigo é FIFO (fila, O(1) por lote).
- **Desvantagem de uma só estrutura:** uma lista única de lotes misturados exigiria ordenar/filtrar por produto e data a cada baixa.

### 3. Clientes e veículos: Lista de Clientes + Lista de Veículos
- Classes `RepositorioClientes`, `Cliente` (`oficina/clientes.py`); método `buscar_por_placa` percorre as duas listas.
- **Por quê:** cada cliente tem quantidade ilimitada de veículos; remover o cliente remove seus veículos junto.
- **Desvantagem de uma só estrutura:** uma lista plana repetiria os dados do cliente em cada veículo (duplicação e inconsistência).

## Outras estruturas
- **Árvore geral** (`estruturas/arvore.py`, `oficina/componentes.py`): cada nó guarda seus filhos numa `ListaEncadeada`; exibição indentada por pré-ordem, O(n).
- **Pilha** (`oficina/ordem_servico.py`): histórico de ações da OS; `desfazer_ultima_acao` reverte a última alteração (LIFO, O(1)).

## Decisões de projeto
- A peça é validada contra o estoque ao entrar na OS, mas a **baixa ocorre no fechamento**, junto com pagamento e registro de consumo. Assim, remover uma peça da OS não exige estorno.
- O fechamento valida tudo antes de alterar qualquer estado (remontagem concluída, estoque suficiente).
- Lotes vencidos são descartados (e registrados em `Estoque.perdas`) antes de qualquer baixa.
- Alertas de estoque mínimo são emitidos apenas na transição para "abaixo do mínimo".
- Valor das peças = soma do preço de venda de cada lote efetivamente consumido.

## Complexidades resumidas
| Operação | Custo |
|---|---|
| Inserir em lista/fila/pilha | O(1) |
| Buscar cliente por CPF | O(C) |
| Buscar veículo por placa | O(C + V) |
| Chamar próximo da espera | O(1) |
| Baixa de estoque | O(P + L consumidos) |
| Descartar vencidos | O(total de lotes) |
| Exibir árvore | O(n) |
