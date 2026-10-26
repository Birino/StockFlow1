
import json
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk

# --------------------------------------------------
# CONFIGURAÇÕES
# --------------------------------------------------

PASTA = Path(__file__).parent
ARQUIVO_PRODUTOS = PASTA / "produtos.json"
ARQUIVO_MOVIMENTACOES = PASTA / "movimentacoes.json"
ESTOQUE_MINIMO_PADRAO = 5

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FUNDO = "#0B1120"
PAINEL = "#111B2E"
CARTAO = "#17243A"
BORDA = "#263750"
AZUL = "#3B82F6"
AZUL_HOVER = "#2563EB"
TEXTO = "#F1F5F9"
SECUNDARIO = "#94A3B8"
VERDE = "#22C55E"
VERMELHO = "#F87171"
AMARELO = "#FBBF24"


# --------------------------------------------------
# DADOS
# --------------------------------------------------

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
            messagebox.showwarning(
                "Arquivo inválido",
                f"O arquivo {caminho.name} não contém uma lista."
            )
            return []

        return dados

    except (json.JSONDecodeError, OSError) as erro:
        messagebox.showerror(
            "Erro ao ler dados",
            f"Não foi possível ler {caminho.name}.\n{erro}"
        )
        return []


def salvar_json(caminho, dados):
    try:
        temporario = caminho.with_suffix(caminho.suffix + ".tmp")

        with temporario.open("w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

        temporario.replace(caminho)
        return True

    except OSError as erro:
        messagebox.showerror(
            "Erro ao salvar",
            f"Não foi possível salvar {caminho.name}.\n{erro}"
        )
        return False


def carregar_produtos():
    produtos = carregar_json(ARQUIVO_PRODUTOS)

    for produto in produtos:
        produto.setdefault("estoque_minimo", ESTOQUE_MINIMO_PADRAO)

    return produtos


def carregar_movimentacoes():
    return carregar_json(ARQUIVO_MOVIMENTACOES)


def proximo_id(registros):
    return max((item.get("id", 0) for item in registros), default=0) + 1


def moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# --------------------------------------------------
# APLICATIVO
# --------------------------------------------------

class StockFlowApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("StockFlow | Controle de Estoque")
        self.geometry("1250x780")
        self.minsize(950, 620)
        self.configure(fg_color=FUNDO)

        self.produtos = carregar_produtos()
        self.movimentacoes = carregar_movimentacoes()
        self.pagina_atual = "Painel"

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_menu()
        self.criar_area_principal()
        self.mostrar_pagina("Painel")

    # --------------------------------------------------
    # ESTRUTURA VISUAL
    # --------------------------------------------------

    def criar_menu(self):
        self.menu = ctk.CTkFrame(
            self, width=225, corner_radius=0, fg_color=PAINEL
        )
        self.menu.grid(row=0, column=0, sticky="nsew")
        self.menu.grid_propagate(False)
        self.menu.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.menu,
            text="◆  StockFlow",
            font=ctk.CTkFont(size=25, weight="bold"),
            text_color=AZUL
        ).grid(row=0, column=0, padx=22, pady=(30, 4), sticky="w")

        ctk.CTkLabel(
            self.menu,
            text="CONTROLE DE ESTOQUE",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=SECUNDARIO
        ).grid(row=1, column=0, padx=24, pady=(0, 30), sticky="w")

        self.botoes_menu = {}

        opcoes = [
            ("Painel", "▦"),
            ("Produtos", "□"),
            ("Movimentações", "↔"),
            ("Estoque baixo", "!"),
            ("Histórico", "◷"),
        ]

        for indice, (nome, simbolo) in enumerate(opcoes, start=2):
            botao = ctk.CTkButton(
                self.menu,
                text=f"  {simbolo}   {nome}",
                anchor="w",
                height=44,
                corner_radius=9,
                fg_color="transparent",
                hover_color=CARTAO,
                text_color=SECUNDARIO,
                font=ctk.CTkFont(size=14),
                command=lambda pagina=nome: self.mostrar_pagina(pagina)
            )
            botao.grid(
                row=indice, column=0, padx=13, pady=4, sticky="ew"
            )
            self.botoes_menu[nome] = botao

        self.menu.grid_rowconfigure(8, weight=1)

        ctk.CTkLabel(
            self.menu,
            text="STOCKFLOW  •  V1.0",
            text_color=SECUNDARIO,
            font=ctk.CTkFont(size=10)
        ).grid(row=9, column=0, padx=20, pady=22, sticky="w")

    def criar_area_principal(self):
        self.conteudo = ctk.CTkFrame(
            self, corner_radius=0, fg_color=FUNDO
        )
        self.conteudo.grid(row=0, column=1, sticky="nsew")
        self.conteudo.grid_columnconfigure(0, weight=1)
        self.conteudo.grid_rowconfigure(1, weight=1)

        self.topo = ctk.CTkFrame(
            self.conteudo, fg_color=FUNDO, corner_radius=0
        )
        self.topo.grid(
            row=0, column=0, sticky="ew", padx=30, pady=(24, 12)
        )
        self.topo.grid_columnconfigure(0, weight=1)

        self.titulo = ctk.CTkLabel(
            self.topo,
            text="Painel",
            font=ctk.CTkFont(size=27, weight="bold"),
            text_color=TEXTO
        )
        self.titulo.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            self.topo,
            text="Sistema de controle de estoque",
            text_color=SECUNDARIO,
            font=ctk.CTkFont(size=12)
        ).grid(row=1, column=0, sticky="w", pady=(3, 0))

        ctk.CTkButton(
            self.topo,
            text="+ Novo produto",
            width=145,
            height=38,
            fg_color=AZUL,
            hover_color=AZUL_HOVER,
            command=self.formulario_produto
        ).grid(row=0, column=1, rowspan=2, padx=(15, 0))

        self.area = ctk.CTkScrollableFrame(
            self.conteudo,
            fg_color=FUNDO,
            corner_radius=0
        )
        self.area.grid(
            row=1, column=0, sticky="nsew", padx=30, pady=(5, 25)
        )
        self.area.grid_columnconfigure(0, weight=1)

    def limpar_area(self):
        for widget in self.area.winfo_children():
            widget.destroy()

    def mostrar_pagina(self, pagina):
        self.pagina_atual = pagina
        self.titulo.configure(text=pagina)

        for nome, botao in self.botoes_menu.items():
            selecionado = nome == pagina
            botao.configure(
                fg_color=CARTAO if selecionado else "transparent",
                text_color=TEXTO if selecionado else SECUNDARIO
            )

        self.limpar_area()

        if pagina == "Painel":
            self.pagina_painel()
        elif pagina == "Produtos":
            self.pagina_produtos()
        elif pagina == "Movimentações":
            self.pagina_movimentacoes()
        elif pagina == "Estoque baixo":
            self.pagina_estoque_baixo()
        elif pagina == "Histórico":
            self.pagina_historico()

    # --------------------------------------------------
    # COMPONENTES REUTILIZÁVEIS
    # --------------------------------------------------

    def secao(self, texto, linha=0):
        ctk.CTkLabel(
            self.area,
            text=texto,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXTO
        ).grid(
            row=linha, column=0, sticky="w", pady=(15, 12)
        )

    def cartao_indicador(self, pai, coluna, titulo, valor, detalhe, cor):
        cartao = ctk.CTkFrame(
            pai, fg_color=CARTAO, corner_radius=13,
            border_width=1, border_color=BORDA
        )
        cartao.grid(
            row=0, column=coluna, padx=6, sticky="nsew"
        )

        ctk.CTkLabel(
            cartao, text=titulo, text_color=SECUNDARIO,
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=17, pady=(17, 7))

        ctk.CTkLabel(
            cartao, text=valor, text_color=cor,
            font=ctk.CTkFont(size=25, weight="bold")
        ).pack(anchor="w", padx=17)

        ctk.CTkLabel(
            cartao, text=detalhe, text_color=SECUNDARIO,
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", padx=17, pady=(5, 17))

    def criar_tabela(self, cabecalhos, linhas, larguras=None):
        tabela = ctk.CTkFrame(
            self.area, fg_color=PAINEL, corner_radius=10
        )
        tabela.grid(sticky="ew", padx=1, pady=(0, 12))
        tabela.grid_columnconfigure(0, weight=1)

        for coluna, titulo in enumerate(cabecalhos):
            tabela.grid_columnconfigure(coluna, weight=1)

            ctk.CTkLabel(
                tabela,
                text=titulo,
                text_color=SECUNDARIO,
                fg_color=CARTAO,
                corner_radius=4,
                anchor="w",
                font=ctk.CTkFont(size=11, weight="bold")
            ).grid(
                row=0, column=coluna, sticky="ew",
                padx=3, pady=4, ipady=8
            )

        if not linhas:
            ctk.CTkLabel(
                tabela,
                text="Nenhum registro para exibir.",
                text_color=SECUNDARIO
            ).grid(
                row=1, column=0, columnspan=len(cabecalhos),
                padx=12, pady=22
            )
            return tabela

        for indice, linha in enumerate(linhas, start=1):
            for coluna, valor in enumerate(linha):
                ctk.CTkLabel(
                    tabela,
                    text=str(valor),
                    text_color=TEXTO,
                    anchor="w",
                    font=ctk.CTkFont(size=12)
                ).grid(
                    row=indice, column=coluna, sticky="ew",
                    padx=8, pady=10
                )

        for indice, linha in enumerate(linhas, start=1):
            for coluna, valor in enumerate(linha):
                ctk.CTkLabel(
                    tabela,
                    text=str(valor),
                    text_color=TEXTO,
                    anchor="w",
                    font=ctk.CTkFont(size=12)
                ).grid(
                    row=indice, column=coluna, sticky="ew",
                    padx=8, pady=10
                )

        return tabela


    def botao(self, pai, texto, comando, cor=AZUL):
        return ctk.CTkButton(
            pai, text=texto, command=comando,
            fg_color=cor,
            hover_color=AZUL_HOVER if cor == AZUL else BORDA,
            height=36, corner_radius=8
        )

    # --------------------------------------------------
    # PAINEL
    # --------------------------------------------------

    def pagina_painel(self):
        total_produtos = len(self.produtos)
        unidades = sum(p["quantidade"] for p in self.produtos)
        valor_total = sum(
            p["quantidade"] * p["preco"] for p in self.produtos
        )
        baixos = [
            p for p in self.produtos
            if p["quantidade"] <= p["estoque_minimo"]
        ]

        indicadores = ctk.CTkFrame(self.area, fg_color="transparent")
        indicadores.grid(row=0, column=0, sticky="ew")
        for coluna in range(4):
            indicadores.grid_columnconfigure(coluna, weight=1)

        self.cartao_indicador(
            indicadores, 0, "PRODUTOS CADASTRADOS",
            str(total_produtos), "Itens diferentes", AZUL
        )
        self.cartao_indicador(
            indicadores, 1, "UNIDADES EM ESTOQUE",
            str(unidades), "Quantidade total", VERDE
        )
        self.cartao_indicador(
            indicadores, 2, "VALOR EM ESTOQUE",
            moeda(valor_total), "Valor estimado", TEXTO
        )
        self.cartao_indicador(
            indicadores, 3, "ESTOQUE BAIXO",
            str(len(baixos)), "Precisam de atenção",
            VERMELHO if baixos else VERDE
        )

        self.secao("Produtos recentes", 1)
        recentes = sorted(
            self.produtos, key=lambda p: p["id"], reverse=True
        )[:6]

        linhas = [
            (
                p["id"], p["nome"], p["quantidade"],
                moeda(p["preco"]),
                "Baixo" if p["quantidade"] <= p["estoque_minimo"]
                else "Normal"
            )
            for p in recentes
        ]

        self.criar_tabela(
            ["ID", "Produto", "Quantidade", "Preço unitário", "Situação"],
            linhas
        )

        
        botao_produtos = self.botao(
            self.area,
            "Ver todos os produtos",
            lambda: self.mostrar_pagina("Produtos"),
        )

        botao_produtos.grid(
            row=7,
            column=0,
            sticky="w",
            pady=(8, 16),
        )

        # Resumo das movimentações recentes
        self.secao("Movimentações recentes", 8)

        recentes_movimentacoes = list(
            reversed(self.movimentacoes)
        )[:5]

        linhas_movimentacoes = []

        for movimento in recentes_movimentacoes:
            try:
                data = datetime.fromisoformat(
                    movimento["data_hora"]
                ).astimezone().strftime("%d/%m/%Y %H:%M")
            except (ValueError, KeyError):
                data = movimento.get("data_hora", "—")

            tipo_movimento = movimento.get("tipo", "")

            if tipo_movimento == "entrada":
                tipo_exibido = "↑ Entrada"
            else:
                tipo_exibido = "↓ Saída"

            linhas_movimentacoes.append(
                (
                    data,
                    movimento.get("produto", "—"),
                    tipo_exibido,
                    movimento.get("quantidade", "—"),
                    movimento.get("estoque_atual", "—"),
                )
            )

        self.criar_tabela(
            [
                "Data e hora",
                "Produto",
                "Movimentação",
                "Quantidade",
                "Estoque final",
            ],
            linhas_movimentacoes,
        )

        self.botao(
            self.area,
            "Ver histórico completo",
            lambda: self.mostrar_pagina("Histórico"),
        ).grid(
            row=10,
            column=0,
            sticky="w",
            pady=(4, 16),
        )


    # --------------------------------------------------
    # PRODUTOS
    # --------------------------------------------------

    def pagina_produtos(self):
        barra = ctk.CTkFrame(self.area, fg_color="transparent")
        barra.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        barra.grid_columnconfigure(0, weight=1)

        self.busca = ctk.CTkEntry(
            barra, placeholder_text="Buscar produto por nome ou ID...",
            height=38
        )
        self.busca.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.busca.bind("<KeyRelease>", lambda evento: self.atualizar_tabela_produtos())

        self.botao(
            barra, "+ Cadastrar produto", self.formulario_produto
        ).grid(row=0, column=1)

        self.tabela_produtos = ctk.CTkFrame(
            self.area, fg_color="transparent"
        )
        self.tabela_produtos.grid(row=1, column=0, sticky="ew")
        self.tabela_produtos.grid_columnconfigure(0, weight=1)

        self.atualizar_tabela_produtos()

 
    def atualizar_tabela_produtos(self):
        if not hasattr(self, "tabela_produtos"):
            return

        for widget in self.tabela_produtos.winfo_children():
            widget.destroy()

        termo = (
            self.busca.get().strip().lower()
            if hasattr(self, "busca")
            else ""
        )

        filtrados = [
            p for p in self.produtos
            if termo in p["nome"].lower()
            or termo == str(p["id"])
        ]

        cabecalhos = [
            "ID",
            "Produto",
            "Qtd.",
            "Preço",
            "Total",
            "Situação",
            "Ações",
        ]

        tabela = ctk.CTkFrame(
            self.tabela_produtos,
            fg_color=PAINEL,
            corner_radius=10,
        )
        tabela.grid(row=0, column=0, sticky="ew")

        for coluna in range(len(cabecalhos)):
            tabela.grid_columnconfigure(coluna, weight=1)

        for coluna, titulo in enumerate(cabecalhos):
            ctk.CTkLabel(
                tabela,
                text=titulo,
                text_color=SECUNDARIO,
                fg_color=CARTAO,
                anchor="w",
                font=ctk.CTkFont(size=11, weight="bold"),
            ).grid(
                row=0,
                column=coluna,
                sticky="ew",
                padx=3,
                pady=4,
                ipady=8,
            )

        if not filtrados:
            ctk.CTkLabel(
                tabela,
                text="Nenhum produto encontrado.",
                text_color=SECUNDARIO,
            ).grid(
                row=1,
                column=0,
                columnspan=len(cabecalhos),
                pady=20,
            )
            return

        for indice, produto in enumerate(filtrados, start=1):
            baixo = (
                produto["quantidade"]
                <= produto["estoque_minimo"]
            )

            valores = [
                produto["id"],
                produto["nome"],
                produto["quantidade"],
                moeda(produto["preco"]),
                moeda(
                    produto["quantidade"] * produto["preco"]
                ),
                "Estoque baixo" if baixo else "Normal",
            ]

            for coluna, valor in enumerate(valores):
                ctk.CTkLabel(
                    tabela,
                    text=str(valor),
                    text_color=(
                        VERMELHO
                        if baixo and coluna == 5
                        else TEXTO
                    ),
                    anchor="w",
                    font=ctk.CTkFont(size=12),
                ).grid(
                    row=indice,
                    column=coluna,
                    sticky="ew",
                    padx=8,
                    pady=10,
                )

            acoes = ctk.CTkFrame(
                tabela,
                fg_color="transparent",
            )
            acoes.grid(
                row=indice,
                column=6,
                padx=5,
                pady=4,
            )

           
            ctk.CTkButton(
                acoes,
                text="Editar",
                width=75,
                height=30,
                fg_color=AZUL,
                hover_color=AZUL_HOVER,
                command=lambda pid=produto["id"]: (
                    self.editar_produto(pid)
                ),
            ).pack(side="left", padx=3)

            ctk.CTkButton(
                acoes,
                text="Excluir",
                width=75,
                height=30,
                fg_color=VERMELHO,
                hover_color="#B91C1C",
                command=lambda pid=produto["id"]: (
                    self.excluir_produto(pid)
                ),
            ).pack(side="left", padx=3)


            # As ações ficam disponíveis na página Movimentações.

    def formulario_produto(self):
        janela = ctk.CTkToplevel(self)
        janela.title("Cadastrar produto")
        janela.geometry("430x530")
        janela.resizable(False, False)
        janela.configure(fg_color=FUNDO)
        janela.transient(self)
        janela.grab_set()

        ctk.CTkLabel(
            janela, text="Novo produto",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(anchor="w", padx=28, pady=(25, 6))

        ctk.CTkLabel(
            janela, text="Preencha os dados do produto.",
            text_color=SECUNDARIO
        ).pack(anchor="w", padx=28, pady=(0, 18))

        campos = {}
        definicoes = [
            ("Nome do produto", "Ex.: Teclado"),
            ("Quantidade inicial", "Ex.: 10"),
            ("Preço unitário (R$)", "Ex.: 89,90"),
            ("Estoque mínimo", str(ESTOQUE_MINIMO_PADRAO))
        ]

        for titulo, placeholder in definicoes:
            ctk.CTkLabel(
                janela, text=titulo, text_color=SECUNDARIO
            ).pack(anchor="w", padx=28, pady=(8, 4))

            entrada = ctk.CTkEntry(
                janela, placeholder_text=placeholder, height=38
            )
            entrada.pack(fill="x", padx=28)
            campos[titulo] = entrada

        def salvar():
            nome = campos["Nome do produto"].get().strip()

            if not nome:
                messagebox.showwarning("Validação", "Informe o nome do produto.", parent=janela)
                return

            try:
                quantidade = int(campos["Quantidade inicial"].get())
                preco = float(
                    campos["Preço unitário (R$)"].get().replace(",", ".")
                )
                minimo_texto = campos["Estoque mínimo"].get().strip()
                minimo = int(minimo_texto) if minimo_texto else ESTOQUE_MINIMO_PADRAO

                if quantidade < 0 or preco < 0 or minimo < 0:
                    raise ValueError

            except ValueError:
                messagebox.showwarning(
                    "Valores inválidos",
                    "Informe quantidades inteiras e preço válido. "
                    "Os valores não podem ser negativos.",
                    parent=janela
                )
                return

            produto = {
                "id": proximo_id(self.produtos),
                "nome": nome,
                "quantidade": quantidade,
                "preco": preco,
                "estoque_minimo": minimo
            }

            self.produtos.append(produto)

            if salvar_json(ARQUIVO_PRODUTOS, self.produtos):
                janela.destroy()
                self.mostrar_pagina("Produtos")
                messagebox.showinfo(
                    "Sucesso", f"Produto '{nome}' cadastrado!"
                )
            else:
                self.produtos.pop()

        ctk.CTkButton(
            janela, text="Salvar produto", height=42,
            fg_color=AZUL, hover_color=AZUL_HOVER,
            command=salvar
        ).pack(fill="x", padx=28, pady=22)

        
    def editar_produto(self, produto_id):
        produto = next(
            (
                p for p in self.produtos
                if p["id"] == produto_id
            ),
            None,
        )

        if produto is None:
            messagebox.showerror(
                "Produto não encontrado",
                "Não foi possível localizar esse produto.",
                parent=self,
            )
            return

        janela = ctk.CTkToplevel(self)
        janela.title("Editar produto")
        janela.geometry("430x470")
        janela.resizable(False, False)
        janela.configure(fg_color=FUNDO)
        janela.transient(self)
        janela.grab_set()

        ctk.CTkLabel(
            janela,
            text="Editar produto",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=TEXTO,
        ).pack(anchor="w", padx=28, pady=(25, 6))

        ctk.CTkLabel(
            janela,
            text=f"ID do produto: {produto['id']}",
            text_color=SECUNDARIO,
        ).pack(anchor="w", padx=28, pady=(0, 18))

        ctk.CTkLabel(
            janela,
            text="Nome do produto",
            text_color=SECUNDARIO,
        ).pack(anchor="w", padx=28, pady=(8, 4))

        campo_nome = ctk.CTkEntry(
            janela,
            height=38,
        )
        campo_nome.pack(fill="x", padx=28)
        campo_nome.insert(0, produto["nome"])

        ctk.CTkLabel(
            janela,
            text="Preço unitário (R$)",
            text_color=SECUNDARIO,
        ).pack(anchor="w", padx=28, pady=(12, 4))

        campo_preco = ctk.CTkEntry(
            janela,
            height=38,
        )
        campo_preco.pack(fill="x", padx=28)
        campo_preco.insert(
            0,
            str(produto["preco"]).replace(".", ","),
        )

        ctk.CTkLabel(
            janela,
            text="Estoque mínimo",
            text_color=SECUNDARIO,
        ).pack(anchor="w", padx=28, pady=(12, 4))

        campo_minimo = ctk.CTkEntry(
            janela,
            height=38,
        )
        campo_minimo.pack(fill="x", padx=28)
        campo_minimo.insert(
            0,
            str(produto["estoque_minimo"]),
        )

        def salvar_edicao():
            nome = campo_nome.get().strip()

            if not nome:
                messagebox.showwarning(
                    "Validação",
                    "Informe o nome do produto.",
                    parent=janela,
                )
                return

            try:
                preco = float(
                    campo_preco.get().strip().replace(",", ".")
                )
                minimo = int(campo_minimo.get().strip())

                if preco < 0 or minimo < 0:
                    raise ValueError

            except ValueError:
                messagebox.showwarning(
                    "Valores inválidos",
                    "Informe um preço válido e um estoque mínimo "
                    "que seja um número inteiro não negativo.",
                    parent=janela,
                )
                return

            dados_anteriores = {
                "nome": produto["nome"],
                "preco": produto["preco"],
                "estoque_minimo": produto["estoque_minimo"],
            }

            produto["nome"] = nome
            produto["preco"] = preco
            produto["estoque_minimo"] = minimo

            if not salvar_json(
                ARQUIVO_PRODUTOS,
                self.produtos,
            ):
                produto.update(dados_anteriores)
                return

            janela.destroy()
            self.mostrar_pagina("Produtos")

            messagebox.showinfo(
                "Sucesso",
                f"Produto '{nome}' atualizado!",
                parent=self,
            )

        ctk.CTkButton(
            janela,
            text="Salvar alterações",
            height=42,
            fg_color=AZUL,
            hover_color=AZUL_HOVER,
            command=salvar_edicao,
        ).pack(fill="x", padx=28, pady=24)


    def excluir_produto(self, produto_id):
        produto = next(
            (
                p for p in self.produtos
                if p["id"] == produto_id
            ),
            None,
        )

        if produto is None:
            messagebox.showerror(
                "Produto não encontrado",
                "Não foi possível localizar esse produto.",
                parent=self,
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            (
                f"Tem certeza que deseja excluir "
                f"'{produto['nome']}'?\n\n"
                "Essa ação não poderá ser desfeita.\n"
                "O histórico de movimentações será preservado."
            ),
            parent=self,
        )

        if not confirmar:
            return

        indice = self.produtos.index(produto)
        produto_removido = self.produtos.pop(indice)

        if not salvar_json(
            ARQUIVO_PRODUTOS,
            self.produtos,
        ):
            self.produtos.insert(indice, produto_removido)
            return

        self.mostrar_pagina("Produtos")

        messagebox.showinfo(
            "Produto excluído",
            f"'{produto['nome']}' foi excluído com sucesso.",
            parent=self,
        )


    # --------------------------------------------------
    # MOVIMENTAÇÕES
    # --------------------------------------------------

    def pagina_movimentacoes(self):
        ctk.CTkLabel(
            self.area,
            text="Registre entradas e saídas do estoque.",
            text_color=SECUNDARIO
        ).grid(row=0, column=0, sticky="w", pady=(0, 15))

        cartao = ctk.CTkFrame(
            self.area, fg_color=CARTAO, corner_radius=12
        )
        cartao.grid(row=1, column=0, sticky="ew", padx=1, pady=5)

        ctk.CTkLabel(
            cartao, text="Nova movimentação",
            font=ctk.CTkFont(size=19, weight="bold")
        ).pack(anchor="w", padx=22, pady=(20, 15))

        ctk.CTkLabel(
            cartao, text="Produto", text_color=SECUNDARIO
        ).pack(anchor="w", padx=22, pady=(0, 5))

        opcoes = [
            f"{p['id']} - {p['nome']} (estoque: {p['quantidade']})"
            for p in self.produtos
        ]

        produto_combo = ctk.CTkComboBox(
            cartao, values=opcoes, height=38, width=400
        )
        produto_combo.pack(anchor="w", padx=22, pady=(0, 15))

        ctk.CTkLabel(
            cartao, text="Tipo de movimentação",
            text_color=SECUNDARIO
        ).pack(anchor="w", padx=22, pady=(0, 5))

        tipo = ctk.CTkSegmentedButton(
            cartao, values=["Entrada", "Saída"], height=36
        )
        tipo.pack(anchor="w", padx=22, pady=(0, 15))
        tipo.set("Entrada")

        ctk.CTkLabel(
            cartao, text="Quantidade",
            text_color=SECUNDARIO
        ).pack(anchor="w", padx=22, pady=(0, 5))

        quantidade = ctk.CTkEntry(
            cartao, placeholder_text="Digite a quantidade",
            height=38, width=400
        )
        quantidade.pack(anchor="w", padx=22, pady=(0, 18))

        def registrar():
            if not self.produtos:
                messagebox.showwarning(
                    "Sem produtos", "Cadastre um produto primeiro."
                )
                return

            selecao = produto_combo.get().strip()
            try:
                produto_id = int(selecao.split(" - ", 1)[0])
                qtd = int(quantidade.get())
            except (ValueError, IndexError):
                messagebox.showwarning(
                    "Dados inválidos",
                    "Selecione um produto e informe uma quantidade inteira."
                )
                return

            if qtd <= 0:
                messagebox.showwarning(
                    "Quantidade inválida",
                    "A quantidade deve ser maior que zero."
                )
                return

            produto = next(
                (p for p in self.produtos if p["id"] == produto_id), None
            )

            if produto is None:
                messagebox.showerror("Erro", "Produto não encontrado.")
                return

            tipo_mov = "entrada" if tipo.get() == "Entrada" else "saida"
            anterior = produto["quantidade"]

            if tipo_mov == "saida" and qtd > anterior:
                messagebox.showwarning(
                    "Estoque insuficiente",
                    f"Estoque disponível: {anterior}."
                )
                return

            produto["quantidade"] = (
                anterior + qtd if tipo_mov == "entrada" else anterior - qtd
            )

            registro = {
                "id": proximo_id(self.movimentacoes),
                "produto_id": produto["id"],
                "produto": produto["nome"],
                "tipo": tipo_mov,
                "quantidade": qtd,
                "data_hora": datetime.now().astimezone().isoformat(
                    timespec="seconds"
                ),
                "estoque_anterior": anterior,
                "estoque_atual": produto["quantidade"]
            }

            self.movimentacoes.append(registro)

            if not salvar_json(ARQUIVO_PRODUTOS, self.produtos):
                produto["quantidade"] = anterior
                self.movimentacoes.pop()
                return

            if not salvar_json(ARQUIVO_MOVIMENTACOES, self.movimentacoes):
                produto["quantidade"] = anterior
                self.movimentacoes.pop()
                salvar_json(ARQUIVO_PRODUTOS, self.produtos)
                return

            messagebox.showinfo(
                "Movimentação registrada",
                f"{tipo.get()} registrada para {produto['nome']}.\n"
                f"Estoque atual: {produto['quantidade']}."
            )
            self.mostrar_pagina("Movimentações")

        self.botao(
            cartao, "Registrar movimentação", registrar
        ).pack(anchor="w", padx=22, pady=(0, 22))

        self.secao("Estoque atual", 2)
        self.criar_tabela(
            ["ID", "Produto", "Quantidade", "Mínimo", "Situação"],
            [
                (
                    p["id"], p["nome"], p["quantidade"],
                    p["estoque_minimo"],
                    "Baixo" if p["quantidade"] <= p["estoque_minimo"]
                    else "Normal"
                )
                for p in self.produtos
            ]
        )

    # --------------------------------------------------
    # ESTOQUE BAIXO E HISTÓRICO
    # --------------------------------------------------

    def pagina_estoque_baixo(self):
        baixos = [
            p for p in self.produtos
            if p["quantidade"] <= p["estoque_minimo"]
        ]

        ctk.CTkLabel(
            self.area,
            text=f"{len(baixos)} produto(s) precisam de atenção.",
            text_color=AMARELO if baixos else VERDE
        ).grid(row=0, column=0, sticky="w", pady=(0, 15))

        self.criar_tabela(
            ["ID", "Produto", "Quantidade atual", "Estoque mínimo"],
            [
                (p["id"], p["nome"], p["quantidade"], p["estoque_minimo"])
                for p in baixos
            ]
        )

    def pagina_historico(self):
        registros = list(reversed(self.movimentacoes))

        linhas = []
        for m in registros:
            try:
                data = datetime.fromisoformat(m["data_hora"]).strftime(
                    "%d/%m/%Y %H:%M"
                )
            except (ValueError, KeyError):
                data = m.get("data_hora", "—")

            linhas.append((
                m.get("id", "—"),
                data,
                m.get("produto", "—"),
                "Entrada" if m.get("tipo") == "entrada" else "Saída",
                m.get("quantidade", "—"),
                m.get("estoque_atual", "—")
            ))

        self.criar_tabela(
            ["ID", "Data e hora", "Produto", "Tipo", "Qtd.", "Estoque final"],
            linhas
        )


if __name__ == "__main__":
    app = StockFlowApp()
    app.mainloop()
