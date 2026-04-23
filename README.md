# 🧾 Sistema de Controle de Estoque

> **Sistema CLI completo em Python para gerenciamento de estoque com foco em Programação Orientada a Objetos**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![OOP](https://img.shields.io/badge/POO-Herança%20%7C%20Polimorfismo%20%7C%20Exceções-green.svg)]()
[![CLI](https://img.shields.io/badge/Interface-CLI-orange.svg)]()

---

## 👥 Integrantes

| Nome                              | Função Principal                     |
|-----------------------------------|--------------------------------------|
| **Gabriel Smarzaro Santos**       | Menu CLI e interface                 |
| **Ewerton Decoté de Aguiar Gomes**    | Lógica de negócio e exceções         |
| **Igor Schuina Xavier**| Modelagem de classes e herança       |
| **Giuseppe Pedruzzi Scherrer**           | Documentação e testes                |

---

## 📌 Descrição do Tema Escolhido

**Tema:** Sistema de Controle de Estoque

Desenvolvemos um sistema completo de gerenciamento de estoque via linha de comando (CLI) que permite o controle total de três entidades principais:

### Entidades Gerenciadas

- **Produtos** — Cadastro, listagem, busca, remoção, entrada e saída de estoque. Suporte especial para **produtos perecíveis** com controle automático de validade.
- **Categorias** — Organização dos produtos em categorias com descrição.
- **Fornecedores** — Cadastro completo com validação de e-mail e telefone.

### Principais Funcionalidades

- ✅ **CRUD completo** para Produtos, Categorias e Fornecedores
- ✅ **Controle de validade** para produtos perecíveis (bloqueio automático de operações em produtos vencidos)
- ✅ **Validações robustas** (ID duplicado, nome duplicado, estoque insuficiente, e-mail e telefone inválidos)
- ✅ **Tratamento de exceções personalizadas** (12 tipos de erros específicos)
- ✅ **Interface amigável** com cores no terminal e menu interativo usando `match/case`

O sistema foi projetado seguindo boas práticas de **Programação Orientada a Objetos**, demonstrando na prática os conceitos estudados em sala de aula.

---

## 🧠 Conceitos de POO Aplicados

| Conceito              | Implementação                                                                 |
|-----------------------|-------------------------------------------------------------------------------|
| **Dataclasses (DTO)** | `ProdutoDTO`, `CategoriaDTO` e `FornecedorDTO` para transferência de dados    |
| **Herança (3 níveis)**| `ItemBase` → `Produto` → `ProdutoPerecivel`                                   |
| **Herança Múltipla**  | `ProdutoPerecivel(Produto, ControlaValidade)`                                 |
| **Polimorfismo**      | 3 métodos sobrescritos (`exibir_info`, `adicionar_estoque`, `remover_estoque`)|
| **Exceções**          | Hierarquia completa de erros personalizados (`Erro` → exceções específicas)   |
| **Encapsulamento**    | Regras de negócio protegidas dentro das classes gerenciadoras                 |

---

## ⚙️ Como Executar o Sistema

### Pré-requisitos

- Python **3.10 ou superior** instalado

### Passos

1. Clone ou baixe o repositório
2. Abra o terminal na pasta do projeto
3. Execute:

```bash
python main.py
```

O menu interativo será exibido com todas as opções disponíveis.

---

## 💡 O que achamos mais desafiador na transição para o Python?

A transição de linguagens mais verbais ou de baixo nível (como C/C++) para o Python trouxe desafios que foram além da simples troca de comandos. Identificamos três pontos principais:

### 1. Lógica de Interpretação vs. Sintaxe
O maior desafio não foi escrever o código, mas **interpretar o problema**.  
Em Python o foco muda da "burocracia da máquina" para a **lógica da solução**. Adaptar o raciocínio para esse nível de abstração exigiu um esforço mental diferente do que estávamos acostumados.

### 2. Adaptação Estrutural: `self` vs `this`
Um ponto técnico que gerou estranheza foi a mudança de referência de instância:
- **C/C++**: Usávamos `this` para referenciar o objeto atual.
- **Python**: Precisamos adotar o `self` explícito em todos os métodos, o que altera completamente a forma como visualizamos a estrutura das classes.

### 3. O Desafio da Concisão (Código Enxuto)
Python é muito mais direto e exige menos linhas de código. Essa agilidade também é um desafio:
- **C**: Exige especificações constantes de tipos e parâmetros → código extenso, mas muito detalhado.
- **Python**: Linguagem enxuta que exige confiança nas bibliotecas e estruturas nativas.

**Resumo da transição:**  
Deixamos de lado a verbosidade do C para abraçar a agilidade e simplicidade do Python, focando mais no **"o que fazer"** do que no **"como configurar"**.

---

## 📁 Estrutura do Projeto

```
├── main.py          # Arquivo principal com todo o sistema
├── README.md        # Este arquivo
└── __pycache__/     # Cache do Python
```

---

**Desenvolvido com ❤️ pelos alunos da disciplina de Programação Orientada a Objetos**

*Professor Edgard da Cunha Pontes*  
*2026*
