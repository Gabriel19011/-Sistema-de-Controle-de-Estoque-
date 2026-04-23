# Importa as bibliotecas para o funcionamento do sistema
# Usado para criar classes puras de dados (DTO) sem precisar escrever o __init__
from dataclasses import dataclass
#Usado no controle de validade
from datetime import datetime
#Usado no codigo para limpar o terminal
import os

# =========================
# EXCEÇÕES PERSONALIZADAS -- Aula Semana 8
# =========================

#Hierarquia de erros especificos '
#Permite tratar falhas de estoque de forma isolada de erros genericos do Python
class Erro(Exception):
    """Classe base para todas as exceções no sistema."""
    #"""X"""Docstrings
    pass

# Erros para produtos
class ProdutoVencidoErro(Erro):
    pass
class ProdutoNaoEncontradoErro(Erro):
    pass
class EstoqueInsuficienteErro(Erro):
    pass
class ProdutoDuplicadoErro(Erro):
    pass
class NenhumProdutoEstoqueErro(Erro):
    pass

# Erros para categorias
class CategoriaDuplicadaErro(Erro):
    pass
class CategoriaNaoEncontradaErro(Erro):
    pass
class NenhumaCategoriaCadastradaErro(Erro):
    pass

# Erros para fornecedores
class NenhumFornecedorCadastradoErro(Erro):
    pass
class FornecedorDuplicadoErro(Erro):
    pass
class FornecedorNaoEncontradoErro(Erro):
    pass
class EmailInvalidoErro(Erro):
    pass
class TelefoneInvalidoErro(Erro):
    pass

# =========================
# DATACLASS (DTO) -- Aula Semana 4 
# =========================

# Entidade 1
@dataclass
class ProdutoDTO:
    """DTO = Data Transfer Object (objeto de transferência de dados).
    Serve apenas como um 'recipiente' para transportar as informações cruas do produto. 
    """
    id: int
    nome: str
    preco: float
    quantidade: int

# Entidade 2
@dataclass
class CategoriaDTO:
    id: int
    nome: str
    descricao: str
    
# Entidade 3
@dataclass
class FornecedorDTO:
    id: int
    nome: str
    endereco: str
    telefone: str
    email: str
    
# =========================
# HERANÇA (3 níveis) -- Aula Semana 6
# =========================

class ItemBase:
    """Nível 1: A fundação mais básica de qualquer item, garantindo que todos tenham um ID."""
    def __init__(self, id: int):
        self.id = id

class Produto(ItemBase):
    """Nível 2: Produto físico genérico. Herda o ID do ItemBase e adiciona os atributos de negócio."""
    def __init__(self, dto: ProdutoDTO):
        super().__init__(dto.id)
        self.nome = dto.nome
        self.preco = dto.preco
        self.quantidade = dto.quantidade
        
    def adicionar_estoque(self, qtd: int):
        """Adiciona uma quantidade específica ao saldo atual do estoque."""
        self.quantidade += qtd
        
    def remover_estoque(self, qtd: int):
        """Remove uma quantidade do estoque, validando se o saldo não ficará negativo."""
        if qtd > self.quantidade:
            raise EstoqueInsuficienteErro("Estoque insuficiente!")
        self.quantidade -= qtd

    def exibir_info(self):
        """Retorna uma string formatada com as informações do produto."""
        return f"[Produto] Codigo: {self.id} | {self.nome} | R${self.preco} | Qtd: {self.quantidade}"

# Classe categoria
class Categoria(ItemBase):
    def __init__(self, dto: CategoriaDTO):
        super().__init__(dto.id)
        self.nome = dto.nome
        self.descricao = dto.descricao
        
    def exibir_info(self):
        return f"[Categoria] Codigo: {self.id} | {self.nome} | {self.descricao}"

# Classe fornecedor
class Fornecedor(ItemBase):
    def __init__(self, dto: FornecedorDTO):
        super().__init__(dto.id)
        self.nome = dto.nome
        self.endereco = dto.endereco
        self.telefone = dto.telefone
        self.email = dto.email

    def exibir_info(self):
        return f"[Fornecedor] Codigo: {self.id} | {self.nome} | {self.endereco} | {self.telefone} | {self.email} "

# =========================
# HERANÇA MÚLTIPLA -- Aula Semana 6
# =========================

# Verifica a validade do produto
class ControlaValidade:
    """Converte strings de data e checa a validade do produto."""
    def __init__(self, validade: str):
        self.validade = datetime.strptime(validade, "%d/%m/%Y")

    def esta_vencido(self):
        """Retorna True se o produto estiver vencido, False caso contrário."""
        return datetime.now() > self.validade

class ProdutoPerecivel(Produto, ControlaValidade):
    """Nivel 3: Herda Produto(comportamento de estoque) e ControlaValidade(comportamento de datas)"""
    def __init__(self, dto: ProdutoDTO, validade: str):
        #Inicia os construtores de ambas a classe pai
        Produto.__init__(self, dto)
        ControlaValidade.__init__(self, validade)
    
    # =========================
    # POLIMORFISMO (override) -- Aula Semana 6
    # =========================
    
    # POLIMORFISMO 1
    def exibir_info(self):
        """Sobrescreve o método original de Produto para exibir também a validade e o status."""
        status = "\033[31mVENCIDO\033[0m" if self.esta_vencido() else "\033[32mNa validade\033[0m"
        return f"[Perecível] Codigo: {self.id} | {self.nome} | R${self.preco} | Quantidade: {self.quantidade} | Validade: {self.validade.date()} | {status} "
    
    # POLIMORFISMO 2
    def adicionar_estoque(self, qtd: int):
        """Não permite adicionar estoque se o produto estiver vencido."""
        if self.esta_vencido():
            raise ProdutoVencidoErro("Não é possível adicionar estoque a um produto vencido!")
        super().adicionar_estoque(qtd)

    # POLIMORFISMO 3
    def remover_estoque(self, qtd: int):
        """Para produtos perecíveis, impede retirada se estiver vencido."""
        if self.esta_vencido():
            raise ProdutoVencidoErro("Produto vencido não pode ter saída de estoque!")
        super().remover_estoque(qtd)
    
# =========================
# GERENCIADOR -- Aula Semana 5
# =========================

# Gerenciador de estoque
class Estoque:
    """Gerencia a coleção de produtos no estoque e aplica as regras de negócio antes de realizar ações."""
    def __init__(self):
        self.produtos: dict[int, Produto] = {}

    def adicionar(self, produto: Produto):
        """Verifica se o produto já existe no dicionário; se não, adiciona."""
        if produto.id in self.produtos:
            raise ProdutoDuplicadoErro("Produto já existe!")
        #Protege a regra de negócio (caso alguém use a classe direto no futuro), que no caso é popular
        self.produtos[produto.id] = produto
        
    def remover(self, id: int):
        """Tenta encontrar e deletar o produto pela chave ID."""
        if id not in self.produtos:
            raise ProdutoNaoEncontradoErro("Produto não encontrado!")
        del self.produtos[id]
        
    def buscar(self, id: int) -> Produto:
        """Busca direta por chave ID no dicionário."""
        if id not in self.produtos:
            raise ProdutoNaoEncontradoErro("Produto não encontrado!")
        return self.produtos[id]
        
    def listar(self):
        """Retorna uma lista formatada de todos os produtos, ou erro se estiver vazio."""
        if not self.produtos:
            raise NenhumProdutoEstoqueErro("Nenhum produto no estoque!")
        return [p.exibir_info() for p in self.produtos.values()]
    
    def buscar_por_nome(self, nome: str):
        """Usa List Comprehension para varrer os valores procurando o texto em letras minúsculas."""
        produto_encontrado = [p for p in self.produtos.values() if nome.lower() in p.nome.lower()]
        if not produto_encontrado:
            raise ProdutoNaoEncontradoErro("Produto não encontrado!")
        return produto_encontrado
        
    def popular_dados_estoque(self):
        """Popula o estoque rapidamente com itens de exemplo para facilitar testes."""
        lista = [
            ProdutoDTO(1, "Mel", 15.74, 25),
            ProdutoDTO(2, "Sal", 1.70, 50),
            ProdutoDTO(3, "Vodka", 70.99, 15)
        ]
        for item in lista:
            produto = Produto(item)
            self.adicionar(produto)
    
    # Verificacoes extras que vao ser feitas antes das verificacoes de adicionar é uma camada de reforco extra

    def validar_id(self, id: int):
        """Verificar se o id esta livre na hora do cadastro do id"""
        if id in self.produtos:
            raise ProdutoDuplicadoErro(
                f"Produto {self.produtos[id].nome} já existe!"
            )
        
    def nome_valido(self, nome: str):
        """Verificar se o nome esta livre na hora do cadastro do nome"""
        for p in self.produtos.values():
            if p.nome.lower() == nome.lower():
                raise ProdutoDuplicadoErro(f"Produto {p.nome} já existe!")

# Gerenciador de categoria
class CategoriaGerenciador:
    def __init__(self):
        self.categorias: dict[int, Categoria] = {}

    def adicionar(self, categoria: Categoria):
        if categoria.id in self.categorias:
            raise CategoriaDuplicadaErro("Categoria já registrada!")
        self.categorias[categoria.id] = categoria

    def remover(self, id: int):
        if id not in self.categorias:
            raise CategoriaNaoEncontradaErro("Categoria não encontrada!")
        del self.categorias[id]

    def buscar(self, id: int) -> Categoria:
        if id not in self.categorias:
            raise CategoriaNaoEncontradaErro("Categoria não encontrada!")
        return self.categorias[id]

    def listar(self):
        if not self.categorias:
            raise NenhumaCategoriaCadastradaErro("Nenhuma categoria cadastrada!")
        return [c.exibir_info() for c in self.categorias.values()]
    
    def popular_dados_categoria(self):
        """Popula a categoria rapidamente com exemplos para facilitar testes."""
        lista = [
            CategoriaDTO(1, "Categoria1", "Categoria de 1 teste"),
            CategoriaDTO(2, "Categoria2", "Categoria de 2 teste"),
            CategoriaDTO(3, "Categoria3", "Categoria de 3 teste")
        ]
        for item in lista:
            categoria = Categoria(item)
            self.adicionar(categoria)

    # Verificacoes extras que vao ser feitas antes das verificacoes de adicionar é uma camada de reforco extra

    def validar_id(self, id: int):
        """Verifica se o ID já existe"""
        if id in self.categorias:
            raise CategoriaDuplicadaErro(
                f"Categoria {self.categorias[id].nome} já existe!"
            )
            
    def nome_valido(self, nome: str):
        """Verifica se o nome já existe"""
        for p in self.categorias.values():
            if p.nome.lower() == nome.lower():
                raise CategoriaDuplicadaErro(f"Categoria {p.nome} já existe!")
    
# Gerenciador de Fornecedor          

class RegrasFornecedor:    
    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida se o email tem formato básico válido."""
        return "@" in email and "." in email.split("@")[-1]

    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        """Valida se o telefone tem apenas dígitos e tamanho mínimo."""
        return telefone.isdigit() and len(telefone) >= 8

class GerenciadorFornecedor:
    def __init__(self):
        self.fornecedores: dict[int, Fornecedor] = {}

    def adicionar(self, fornecedor: Fornecedor):
        if fornecedor.id in self.fornecedores:
            raise FornecedorDuplicadoErro("Fornecedor já existe!")

        if not RegrasFornecedor.validar_email(fornecedor.email):
            raise EmailInvalidoErro("Email inválido!")

        if not RegrasFornecedor.validar_telefone(fornecedor.telefone):
            raise TelefoneInvalidoErro("Telefone inválido!")

        self.fornecedores[fornecedor.id] = fornecedor

    def listar(self):
        if not self.fornecedores:
            raise NenhumFornecedorCadastradoErro("Nenhum fornecedor cadastrado!")
        return [f.exibir_info() for f in self.fornecedores.values()]
    
    def buscar(self, id: int) -> Fornecedor:
        if id not in self.fornecedores:
           raise FornecedorNaoEncontradoErro("Fornecedor não encontrado!")
        return self.fornecedores[id]
    
    def remover(self, id: int):
       if id not in self.fornecedores:
          raise FornecedorNaoEncontradoErro("Fornecedor não encontrado!")
       del self.fornecedores[id]

    def popular_dados_fornecedor(self):
        """Fornecedores ja cadasreados."""
        lista = [
            FornecedorDTO(1, "Fornecedor A", "Rua São João", "27999999999", "contato@fornecedorA.com"),
            FornecedorDTO(2, "Fornecedor B", "Rua Boa Esperança", "27988888888", "suporte@fornecedorB.com"),
            FornecedorDTO(3, "Fornecedor C", "Rua chapel preto", "27977777777", "vendas@fornecedorC.com"),
        ]
        for item in lista:
            fornecedor = Fornecedor(item)
            self.adicionar(fornecedor)

    # Verificacoes extras que vao ser feitas antes das verificacoes de adicionar é uma camada de reforco extra
    def validar_id(self, id: int):
        """Verifica se o ID já existe"""
        if id in self.fornecedores:
            raise FornecedorDuplicadoErro(
                f"Fornecedor {self.fornecedores[id].nome} já existe!"
            )

    def nome_valido(self, nome: str):
        """Verifica se o nome já existe"""
        for f in self.fornecedores.values():
            if f.nome.lower() == nome.lower():
                raise FornecedorDuplicadoErro(
                    f"Fornecedor {f.nome} já existe!"
                )

# =========================
# MENU CLI (match/case) -- Aula Semana 2
# =========================

def menu():
    estoque = Estoque()
    categoria = CategoriaGerenciador()
    fornecedor = GerenciadorFornecedor()

    while True:
        print("\033[1;37;44m\nC O N T R O L E   D E   E S T O Q U E \033[0m")
        print("\033[1;31;40m--------------- PRODUTOS -------------\033[0m")
        print("\033[1;36;40m1 - Adicionar Produto                 \033[0m")
        print("\033[1;36;40m2 - Listar Produtos                   \033[0m")
        print("\033[1;36;40m3 - Buscar Produto                    \033[0m")
        print("\033[1;36;40m4 - Remover Produto                   \033[0m")
        print("\033[1;36;40m5 - Entrada de Estoque                \033[0m")
        print("\033[1;36;40m6 - Saída de Estoque                  \033[0m")
        print("\033[1;36;40m7 - Buscar por nome                   \033[0m")
        print("\033[1;36;40m8 - Popular dados produto             \033[0m")

        print("\033[1;31;40m------------- CATEGORIAS -------------\033[0m")
        print("\033[1;36;40m9  - Adicionar Categoria              \033[0m")
        print("\033[1;36;40m10 - Listar Categorias                \033[0m")
        print("\033[1;36;40m11 - Buscar Categoria                 \033[0m")
        print("\033[1;36;40m12 - Remover Categoria                \033[0m")
        print("\033[1;36;40m13 - Popular dados categoria          \033[0m")

        print("\033[1;31;40m------------ FORNECEDORES ------------\033[0m")
        print("\033[1;36;40m14 - Adicionar Fornecedor             \033[0m")
        print("\033[1;36;40m15 - Listar Fornecedores              \033[0m")
        print("\033[1;36;40m16 - Buscar Fornecedor                \033[0m")
        print("\033[1;36;40m17 - Remover Fornecedor               \033[0m")
        print("\033[1;36;40m18 - Popular dados fornecedor         \033[0m")
        print("\033[1;36;40m0  - Sair                             \033[0m")
        print("\033[44m" + " "*38 + "\033[0m")

        try:
            #Captura a escolha do usuario
            opcao = int(input("\033[33mEscolha: \033[0m"))
            #Limpa o terminal para deixar a tela organizada após a escolha
            os.system("cls" if os.name == "nt" else "clear")
            
            match opcao:
                ##Opcao 1 adicionar produto no estoque
                case 1:
                    #Loop de validacao do ID
                    print("\033[43m\033[31mAdicionar Produto\033[0m\033[0m")  
                    while True:
                        try:
                            id = int(input("ID: "))
                            estoque.validar_id(id)
                            break
                        except ProdutoDuplicadoErro as e:
                            print(f"\033[31m{e}\033[0m")
                        except ValueError:
                            print("\033[31mDigite um número válido!\033[0m")
                    #Loop de validacao do Nome
                    while True:
                        try:
                            nome = input("Nome: ")
                            estoque.nome_valido(nome)
                            break
                        except ProdutoDuplicadoErro as e:
                            print(f"\033[31m{e}\033[0m")  
                        except ValueError:
                            print("\033[31mDigite um nome válido!\033[0m")

                    while True:
                        try:
                            preco = float(input("Preço: "))
                            break
                        except ValueError:
                            print("\033[31mDigite um preço válido!\033[0m")
                    
                    while True:
                        try:
                            qtd = int(input("Quantidade: "))
                            break
                        except ValueError:
                            print("\033[31mDigite uma quantidade válida!\033[0m")
                                        
                    tipo = input("É perecível? (s/n): ")
                    
                    # Cria o DTO com os dados basicos 
                    dto = ProdutoDTO(id, nome, preco, qtd)
                    
                    # Verifica a classe a ser instanciada (Produto comum ou Perecível)
                    if tipo.lower() == "s":
                        while True:
                            try:
                                validade = input("Validade (dd/mm/yyyy): ")
                                # Tenta criar; se a data for absurda, o strptime lá dentro lança um erro
                                produto = ProdutoPerecivel(dto, validade)
                                break
                            except ValueError:
                                print("\033[31mFormato de data inválido!\033[0m")
                    else:
                        produto = Produto(dto)
                    # Finalmente, cadastra o objeto montado no gerenciador
                    estoque.adicionar(produto)
                    print("\033[32mProduto adicionado!\033[0m")

                # Opcao 2 listar produtos no estoque
                case 2:
                    print("\033[43m\033[31mProdutos Cadastrados\033[0m\033[0m")  
                    for p in estoque.listar():
                        print(p)

                # Opcao 3 busca produto no estoque pelo ID
                case 3:
                    print("\033[43m\033[31mBuscar Produto\033[0m\033[0m")  
                    id = int(input("ID: "))
                    produto = estoque.buscar(id)
                    print(produto.exibir_info())

                # Opcao 4 remove produto no estoque pelo ID
                case 4:
                    print("\033[43m\033[31mRemover Produto\033[0m\033[0m")  
                    id = int(input("ID: "))
                    estoque.remover(id)
                    print("\033[31mRemovido!\033[0m")

                # Opcao 5 entrada de estoque
                # [ ENTRADA (+ SALDO) ]
                case 5:
                    print("\033[43m\033[31mEntrada de Produto\033[0m\033[0m")  
                    id = int(input("ID: "))
                    qtd = int(input("Quantidade: "))
                    estoque.buscar(id).adicionar_estoque(qtd)
                    print("\033[32mEstoque atualizado!\033[0m")

                # Opcao 6 saida de estoque
                # [ SAÍDA (- SALDO) ]
                case 6:
                    print("\033[43m\033[31mSaida de Produto\033[0m\033[0m")  
                    id = int(input("ID: "))
                    qtd = int(input("Quantidade: "))
                    estoque.buscar(id).remover_estoque(qtd)
                    print("\033[31mSaída registrada!\033[0m")
                
                # Opcao 7 busca pelo nome no Estoque
                case 7:
                    print("\033[43m\033[31mBuscar Produto por Nome\033[0m\033[0m")  
                    nome = input("Nome: ")
                    for p in estoque.buscar_por_nome(nome):
                        print(p.exibir_info())
                
                # Opcao 8 adicionar lista no estoque
                case 8:
                    estoque.popular_dados_estoque()
                    print("\033[32mEstoque populado com sucesso!\033[0m")

                # =========================
                #          Categoria
                # =========================

                case 9:
                    #- Adicionar Categoria
                    print("\033[43m\033[31mAdicionar Categoria\033[0m\033[0m")  

                    while True:
                        try:
                            id = int(input("ID: "))
                            categoria.validar_id(id)
                            break
                        except CategoriaDuplicadaErro as e:
                            print(f"\033[31m{e}\033[0m")
                        except ValueError:
                            print("\033[31mDigite um número válido!\033[0m")
                    #Loop de validacao do Nome
                    while True:
                        try:
                            nome = input("Nome: ")
                            categoria.nome_valido(nome)
                            break
                        except CategoriaDuplicadaErro as e:
                            print(f"\033[31m{e}\033[0m")  
                        except ValueError:
                            print("\033[31mDigite um nome válido!\033[0m")
                    descricao = input("Descrição: ")
                    dto = CategoriaDTO(id, nome, descricao)
                    categoria.adicionar(Categoria(dto))
                    print("\033[32mCategoria adicionada!\033[0m")

                case 10:
                    # - Listar Categorias
                    print("\033[43m\033[31mCategorias Cadastradas\033[0m\033[0m")  
                    for c in categoria.listar():
                        print(c)

                case 11:
                    # - Buscar Categoria
                    print("\033[43m\033[31mBuscar Categoria por ID\033[0m\033[0m")  
                    id = int(input("ID: "))
                    c = categoria.buscar(id)
                    print(c.exibir_info())

                case 12:
                    # - Remover Categoria
                    print("\033[43m\033[31mRemovedor Categoria\033[0m\033[0m")  
                    id = int(input("ID: "))
                    categoria.remover(id)
                    print("\033[31mRemovido!\033[0m")

                case 13:
                    # - Popular dados categoria
                    categoria.popular_dados_categoria()
                    print("\033[32mCategoria populada com sucesso!\033[0m")

                # =========================
                #          Fornecedor
                # =========================
                
                case 14:
                    print("\033[43mAdicionar Fornecedor\033[0m\033[0m")
                    # Validação de ID
                    while True:
                        try:
                            id = int(input("ID: "))
                            fornecedor.validar_id(id)
                            break
                        except FornecedorDuplicadoErro as e:
                            print(f"\033[31m{e}\033[0m")
                        except ValueError:
                            print("\033[31mDigite um número válido!\033[0m")

                    # Validação de Nome
                    while True:
                        try:
                            nome = input("Nome: ")
                            fornecedor.nome_valido(nome)
                            break
                        except FornecedorDuplicadoErro as e:
                            print(f"\033[31m{e}\033[0m")

                    endereco = input("Endereço: ")

                    # Validação de Telefone
                    while True:
                        telefone = input("Telefone: ")
                        if RegrasFornecedor.validar_telefone(telefone):
                            break
                        else:
                            print("\033[31mTelefone inválido!\033[0m")

                    # Validação de Email
                    while True:
                        email = input("Email: ")
                        if RegrasFornecedor.validar_email(email):
                            break
                        else:
                            print("\033[31mEmail inválido!\033[0m")

                    dto = FornecedorDTO(id, nome, endereco, telefone, email)
                    fornecedor.adicionar(Fornecedor(dto))
                    print("\033[32mFornecedor adicionado com sucesso!\033[0m")

                case 15:
                    # - Listar Fornecedor
                    print("\033[43m\033[31mFornecedores Cadastrados\033[0m\033[0m")  
                    for f in fornecedor.listar():
                        print(f)

                case 16:
                    # - Buscar Fornecedor
                    print("\033[43m\033[31mBuscar Fornecedor por ID\033[0m\033[0m")  
                    id = int(input("ID: "))
                    f = fornecedor.buscar(id)
                    print(f.exibir_info())
                    
                case 17:
                    # - Remover Fornecedor
                    print("\033[43m\033[31mRemover Fornecedor\033[0m\033[0m")  
                    id = int(input("ID: "))
                    fornecedor.remover(id)
                    print("\033[31mRemovido!\033[0m")

                case 18:
                    # - Popular dados fornecedor
                    fornecedor.popular_dados_fornecedor()
                    print("\033[32mFornecedor populado com sucesso!\033[0m")

                ##Opcao 0 encerrar o sistema
                case 0:
                    print("\033[31mSaindo...\033[0m") 
                    print("\033[1;37;44m\n"+" "*10 +"I N T E G R A N T E S"+" "*9 +"\033[0m")
                    print("\033[1;31;40m" + "-"*40 + "\033[0m")
                    print("\033[1;36;40m"+" "*9 +"Gabriel Smarzaro Santos"+" "*8 +"\033[0m")
                    print("\033[1;31;40m" + "-"*40 + "\033[0m")
                    print("\033[1;36;40m"+" "*7 +"Giuseppe Pedruzzi Scherrer"+" "*7 +"\033[0m")
                    print("\033[1;31;40m" + "-"*40 + "\033[0m")
                    print("\033[1;36;40m"+" "*5 +"Ewerton Decoté de Aguiar Gomes"+" "*5 +"\033[0m")
                    print("\033[1;31;40m" + "-"*40 + "\033[0m")
                    print("\033[1;36;40m"+" "*11 +"Igor Schuina Xavier"+" "*10 +"\033[0m")
                    print("\033[1;31;40m" + "-"*40 + "\033[0m")
                    print("\033[44m" + " "*40 + "\033[0m")
                    break

                #Tratamanto de opção inexistente
                case _:
                    print("Opção inválida!")
        
        except Erro as e:
            print(f"\033[31mErro de negócio: {e}\033[0m")

        except ValueError:
            print("\033[31mEntrada inválida!\033[0m")

        except Exception as e:
            print(f"\033[31mErro inesperado: {e}\033[0m")

        else:
            # print("\033[32mEntrada válida!\033[0m")
            pass

        # O finally sempre roda, independente de dar erro ou sucesso.
        finally:
            print("\033[32mOperação finalizada.\033[0m")

#Isso é para garantir que o script só rode o menu se for executado diretamente
if __name__ == "__main__":
    menu()
    
    



