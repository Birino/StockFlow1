
# 📦 StockFlow — Sistema de Controle de Estoque

Um sistema de controle de estoque desenvolvido em Python, com cadastro de produtos, movimentações de entrada e saída, alertas de estoque baixo e armazenamento local em arquivos JSON.

> Projeto desenvolvido para praticar lógica de programação, funções, estruturas de dados, validação de entradas e persistência de informações.

## 🚀 Funcionalidades

- ✅ Cadastro de produtos com nome, quantidade, preço e estoque mínimo
- ✅ Listagem de produtos cadastrados
- ✅ Registro de entradas de estoque
- ✅ Registro de saídas com validação de quantidade disponível
- ✅ Alertas de estoque baixo
- ✅ Histórico de movimentações com data e hora
- ✅ Persistência de produtos e movimentações em arquivos JSON
- ✅ Validação de dados informados pelo usuário

## 🛠️ Tecnologias utilizadas

- **Python** — linguagem de programação
- **JSON** — armazenamento local dos dados
- **Git e GitHub** — versionamento e publicação do projeto

## 📋 Pré-requisitos

- Python instalado
- Visual Studio Code ou outro editor de código
- Terminal para executar o programa

## ▶️ Como executar

1. Clone este repositório ou baixe os arquivos.
2. Abra a pasta do projeto no terminal.
3. Execute o comando:

   ```bash
   python main.py
   ```

4. Siga as opções exibidas no menu do StockFlow.

> Em alguns ambientes Windows, pode ser necessário utilizar `py main.py` em vez de `python main.py`.

## 💾 Armazenamento de dados

O projeto utiliza arquivos JSON para manter as informações entre execuções:

- `produtos.json` — armazena os produtos cadastrados e suas quantidades.
- `movimentacoes.json` — registra as entradas e saídas realizadas.

Mantenha esses arquivos na pasta principal do projeto para que o programa consiga encontrá-los.

## 📚 Aprendizados

Este projeto permite praticar:

- Variáveis, condições e laços de repetição
- Funções e organização do código
- Listas e dicionários
- Leitura e gravação de arquivos JSON
- Validação e tratamento de erros
- Controle de estoque e registro de operações

## 🔮 Próximas melhorias

- [ ] Criar testes automatizados
- [ ] Separar o código em módulos
- [ ] Desenvolver uma interface gráfica
- [ ] Adicionar relatórios de estoque
- [ ] Implementar banco de dados
- [ ] Melhorar a experiência de uso

## 👨‍💻 Autor

Desenvolvido por **Birino** como projeto de aprendizado em desenvolvimento de software.

- GitHub: [@Birino](https://github.com/Birino)

---

⭐ Se este projeto foi útil ou interessante, considere deixar uma estrela no repositório.
