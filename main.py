
import json
from datetime import datetime
from pathlib import Path

PASTA = Path(__file__).parent
ARQUIVO_PRODUTOS = PASTA / "produtos.json"
ARQUIVO_MOVIMENTACOES = PASTA / "movimentacoes.json"

ESTOQUE_MINIMO_PADRAO = 5


def carregar_json(caminho):
    if not caminho.exists():
        return []

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()

        if not conteudo:
            return []

        dados = json.loads(conteudo)

        if not isinstance(dados, list):
            print(f"Aviso: formato inválido em {caminho.name}.")
            return []

        return dados

    except (json.JSONDecodeError, OSError):
        print(f"Aviso: não foi possível ler {caminho.name}.")
        return []


def salvar_json(caminho, dados):
    try:
        with caminho.open("w", encoding="utf-8") as arquivo:
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4
            )
        return True

    except OSError:
        print(f"Erro ao salvar {caminho.name}.")
        return False


def carregar_produtos():
    produtos = carregar_json(ARQUIVO_PRODUTOS)

    for produto in produtos:
        produto.setdefault(
            "estoque_minimo",
            ESTOQUE_MINIMO_PADRAO
        )

    return produtos


def carregar_movimentacoes():
    return carregar_json(ARQUIVO_MOVIMENTACOES)


def mostrar_menu():
    print("\n" + "=" * 42)
    print("               STOCKFLOW")
    print("        SISTEMA DE CONTROLE DE ESTOQUE")
    print("=" * 42)
    print("1. Cadastrar produto")
    print("2. Listar produtos")
    print("3. Registrar entrada")
    print("4. Registrar saída")
    print("5. Consultar estoque baixo")
    print("6. Consultar histórico de movimentações")
    print("0. Sair")
    print("=" * 42)


def cadastrar_produto(produtos):
    print("\n--- CADASTRAR PRODUTO ---")

    nome = input("Nome do produto: ").strip()

    if not nome:
        print("O nome não pode ficar vazio.")
        return

    try:
        quantidade = int(input("Quantidade inicial: "))
        preco = float(
            input("Preço unitário (R$): ").replace(",", ".")
        )
        estoque_minimo = int(
            input(
                f"Estoque mínimo (Enter para "
                f"{ESTOQUE_MINIMO_PADRAO}): "
            ) or ESTOQUE_MINIMO_PADRAO
        )

        if quantidade < 0 or preco < 0 or estoque_minimo < 0:
            print("Os valores não podem ser negativos.")
            return

    except ValueError:
        print("Digite valores válidos.")
        return

    produto = {
        "id": max((p["id"] for p in produtos), default=0) + 1,
        "nome": nome,
        "quantidade": quantidade,
        "preco": preco,
        "estoque_minimo": estoque_minimo
    }

    produtos.append(produto)

    if salvar_json(ARQUIVO_PRODUTOS, produtos):
        print(f"Produto '{nome}' cadastrado com sucesso!")
    else:
        produtos.pop()
        print("O cadastro não foi concluído.")


def listar_produtos(produtos):
    print("\n--- PRODUTOS CADASTRADOS ---")

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    for produto in produtos:
        total = produto["quantidade"] * produto["preco"]

        print("-" * 42)
        print(f"ID: {produto['id']}")
        print(f"Nome: {produto['nome']}")
        print(f"Quantidade: {produto['quantidade']}")
        print(f"Preço unitário: R$ {produto['preco']:.2f}")
        print(f"Valor em estoque: R$ {total:.2f}")
        print(f"Estoque mínimo: {produto['estoque_minimo']}")

        if produto["quantidade"] <= produto["estoque_minimo"]:
            print("ALERTA: ESTOQUE BAIXO!")


def consultar_estoque_baixo(produtos):
    print("\n--- ALERTAS DE ESTOQUE BAIXO ---")

    produtos_baixos = [
        p for p in produtos
        if p["quantidade"] <= p["estoque_minimo"]
    ]

    if not produtos_baixos:
        print("Nenhum produto com estoque baixo.")
        return

    for produto in produtos_baixos:
        print("-" * 42)
        print(f"ID: {produto['id']}")
        print(f"Produto: {produto['nome']}")
        print(f"Quantidade atual: {produto['quantidade']}")
        print(f"Estoque mínimo: {produto['estoque_minimo']}")
        print("Situação: ESTOQUE BAIXO!")


def movimentar_estoque(produtos, movimentacoes, tipo):
    if not produtos:
        print("\nNenhum produto cadastrado.")
        return

    listar_produtos(produtos)

    try:
        produto_id = int(input("\nDigite o ID do produto: "))
        quantidade = int(
            input("Quantidade da movimentação: ")
        )

        if quantidade <= 0:
            print("A quantidade deve ser maior que zero.")
            return

    except ValueError:
        print("Digite números inteiros válidos.")
        return

    produto = next(
        (p for p in produtos if p["id"] == produto_id),
        None
    )

    if produto is None:
        print("Produto não encontrado.")
        return

    quantidade_anterior = produto["quantidade"]

    if tipo == "entrada":
        produto["quantidade"] += quantidade
    else:
        if quantidade > produto["quantidade"]:
            print("Estoque insuficiente para essa saída.")
            return

        produto["quantidade"] -= quantidade

    registro = {
        "id": max(
            (m["id"] for m in movimentacoes),
            default=0
        ) + 1,
        "produto_id": produto["id"],
        "produto": produto["nome"],
        "tipo": tipo,
        "quantidade": quantidade,
        "data_hora": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "estoque_anterior": quantidade_anterior,
        "estoque_atual": produto["quantidade"]
    }

    movimentacoes.append(registro)

    # Salva os dois arquivos. Se houver falha,
    # tenta desfazer a alteração.
    if not salvar_json(ARQUIVO_PRODUTOS, produtos):
        produto["quantidade"] = quantidade_anterior
        movimentacoes.pop()
        print("Movimentação cancelada.")
        return

    if not salvar_json(ARQUIVO_MOVIMENTACOES, movimentacoes):
        produto["quantidade"] = quantidade_anterior
        movimentacoes.pop()
        salvar_json(ARQUIVO_PRODUTOS, produtos)
        print("Não foi possível salvar o histórico.")
        print("A movimentação foi cancelada.")
        return

    print("\nMovimentação registrada com sucesso!")
    print(f"Produto: {produto['nome']}")
    print(f"Tipo: {tipo}")
    print(f"Quantidade movimentada: {quantidade}")
    print(f"Estoque atual: {produto['quantidade']}")

    if produto["quantidade"] <= produto["estoque_minimo"]:
        print("ATENÇÃO: este produto está com estoque baixo!")


def consultar_historico(movimentacoes):
    print("\n--- HISTÓRICO DE MOVIMENTAÇÕES ---")

    if not movimentacoes:
        print("Nenhuma movimentação registrada ainda.")
        return

    for registro in reversed(movimentacoes):
        print("-" * 42)
        print(f"Movimentação ID: {registro['id']}")
        print(f"Data e hora: {registro['data_hora']}")
        print(f"Produto: {registro['produto']}")
        print(f"ID do produto: {registro['produto_id']}")
        print(f"Tipo: {registro['tipo']}")
        print(f"Quantidade movimentada: {registro['quantidade']}")
        print(f"Estoque anterior: {registro['estoque_anterior']}")
        print(f"Estoque atual: {registro['estoque_atual']}")


def executar():
    produtos = carregar_produtos()
    movimentacoes = carregar_movimentacoes()

    while True:
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_produto(produtos)
        elif opcao == "2":
            listar_produtos(produtos)
        elif opcao == "3":
            movimentar_estoque(
                produtos, movimentacoes, "entrada"
            )
        elif opcao == "4":
            movimentar_estoque(
                produtos, movimentacoes, "saida"
            )
        elif opcao == "5":
            consultar_estoque_baixo(produtos)
        elif opcao == "6":
            consultar_historico(movimentacoes)
        elif opcao == "0":
            print("Obrigado por utilizar o StockFlow!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    executar()
