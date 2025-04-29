import os
import sqlite3 # Biblioteca para trabalhar com bancos de dados SQLite
from prettytable import PrettyTable # Bibliotea para exibir tabelas formatadas
# importar o módulo pathlib para trabalhar com caminhos relativos ou absolutos
from pathlib import Path

# Conexão com o banco de dados (arquivo será criado se não existir)

# Caminho Relativo
db_path = Path('sql') / 'bd_rel_1_n.db'
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Criação da tabela 'Clientes' (tabela principal)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT, -- ID único para o cliente
    nome TEXT NOT NULL,                           -- Nome do cliente
    email TEXT UNIQUE NOT NULL,                   -- Email único
    telefone TEXT,                                -- Telefone do cliente
    cidade TEXT                                   -- Cidade onde mora
)
""")

# Criação da tabela 'Pedidos' (Tabela relacionada)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Pedidos (
               id_pedido INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único para o pedido
               id_cliente INTEGER NOT NULL,     -- Relacionamento com a tabela Cliente
               produto TEXT NOT NULL,           -- nome do produto pedido
               quantidade INTEGER NOT NULL,     -- Quantidade do produto
               data TEXT NOT NULL,              -- Data do pedido
               valor_total REAL NOT NULL,       -- Valor total do pedido
               FOREIGN KEY (id_cliente) REFERENCES Cliente (id_cliente) -- Chave estrangeira
               
)
""")

# Função para verificar se um cliente existe no banco de dados

def cliente_existe(id_cliente):
    cursor.execute(
        'SELECT 1 FROM Clientes WHERE id_cliente = ?', (id_cliente,))
    # Retorna True se o cliente existir, False caso contrário
    return cursor.fetchone() is not None

# Função para inserir dados na tabela Clientes

def inserir_cliente():
    nome = input('Digite o nome do cliente: ')
    email = input('Digite o email do cliente: ')
    telefone = input('Digite o telefone do cliente: ')
    cidade = input('Digite a cidade do cliente: ')
    cursor.execute("""
    INSERT INTO Clientes (nome, email, telefone, cidade)
    VALUES (?, ?, ?, ?)
    """, (nome, email, telefone, cidade))
    conn.commit()
    print('Cliente inserido com sucesso!')


# Função para inserir dados na tabela Pedidos

def inserir_pedido():
    # listando os clientes
    cursor.execute("""
    SELECT * from clientes
    """)
    resultado = cursor.fetchall()
    # Não posso fazer pedidos sem clientes
    if not resultado:
        print('-'*70)
        print('Nenhum cliente encontrado. Cadastre um cliente primeiro.')
        print('-'*70)
        return
    
    # Criar e formatar a tabela para exibição
    tabela = PrettyTable(['id_cliente', 'Nome', 'Email', 'Telefone', 'Cidade'])
    for linha in resultado:
        tabela.add_row(linha)
    print(tabela)

    try:
        # Garantir que o ID seja um número inteiro
        id_cliente = int(input('Digite o ID do cliente: '))

        # Verificar se o cliente existe antes de prosseguir
        if not cliente_existe(id_cliente):
            print('-'*70)
            print(f'Erro: Cliente com ID {id_cliente} não encontrado!')
            print('Por favor, cadastre o cliente primeiro.')
            print('-'*70)
            # Retorna ao menu se o cliente não existir
            return
        # Solicitar os dados do pedido
        produto = input('Digite o nome do produto: ')
        quantidade = int(input('Digite a quantidade: '))
        # ISO 8601 (YYY-MM-DD)
        data = input('Digite a data do pedido (YYYY-MM-DD): ')
        valor_total = float(input('Digite o valor total: '))

        # Inserir o pedido no banco de dados
        cursor.execute("""
        INSERT INTO Pedidos (id_cliente, produto, quantidade, data, valor_total)
        VALUES (?, ?, ?, ?, ?)
        """, (id_cliente, produto, quantidade, data, valor_total))
        conn.commit()
        print('Pedido inserido com sucesso!')
    except ValueError:
        print('-'*70)
        print('Erro: ID do cliente deve ser um número inteiro.')
        print('-'*70)

# Funções para realizar uma consulta com JOIN e exibir resultados
def consultar_pedidos():
    cursor.execute("""
    SELECT
        Clientes.nome, Clientes.email, Clientes.cidade, -- Campos da tabela Clientes
        Pedidos.produto, Pedidos.quantidade, Pedidos.valor_total -- Campos de tabela pedidos
    FROM
        Clientes
    JOIN
        Pedidos ON Cliente.id_cliente = Pedidos.id_cliente
    """)
    resultados = cursor.fetchall()

    # Criar e formatar a tabela para exibição
    tabela = PrettyTable(
        ['Nome', 'Email', 'Cidade', 'Produto', 'Qunatidade', 'Valor total'])
    for linha in resultados:
        tabela.add_row(linha)
    print(tabela)


# Função para alterar Pedido
# Função para alterar um pedido
def alterar_pedido():
    try:
        # Solicitar e id no pedido
        id_pedido = int(input('Digite o ID do pedido que deseja alterar: '))

        # Verificar se o pedido existe
        cursor.execute(
            'SELECT * FROM Pedidos WHERE id_pedido =?', (id_pedido))
        pedido = cursor.fetchone()
        if not pedido:
            print('-'*70)
            print(f'Erro: Pedido com ID {id_pedido} não encontrado!')
            print('-'*70)
            return
        # Exibir os dados atuais do pedido
        print('-'*70)
        print('Dados atuais do pedido: ')
        print(f'Produto: {pedido[2]}')
        print(f'Quantidade: {pedido[3]}')
        print(f'Data: {pedido[4]}')
        print(f'Valor total: {pedido[5]}')
        print('-'*70)

        # Solicitar novos dados do pedido
        produto = input(
            'Digite o novo nome do produto (ou pressione Enter para manter o atual): ') or pedido[2]
        quantidade = input(
            'Digite a nova quantidade (ou pressione Enter para manter a atual): ') or pedido[3]
        data = input(
            'Digite a nova data (YYYY-MM-DD) (ou pressione Enter para manter a atual)') or pedido[4]
        valor_total = input(
            'Ditie o novo valor total (ou pressione Enter para manter o atual): ') or pedido[5]
        
        # Atualizar os dados do pedido
        cursor.execute("""
        UPDATE Pedidos
        SET produto = ?, quantidade = ?, data = ?, valor_total = ?
        WHERE id_pedido = ?
        """, (produto, int(quantidade), data, float(valor_total), id_pedido))
        conn.commit()
        print('Pedido atualizado com sucesso!')
    except ValueError:
        print('-'*70)
        print('Erro: Entrada inválida.')
        print('-'*70)

    while True:
        print('\nMenu')
        print('1. Inserir Cliente')
        print('2. Inserir Pedido')
        print('3. Consultar Pedidos')
        print('4. Alterar Pedido')
        print('5. Sair')
        opcao = input('Escolher uma opção: ')

        if opcao == '1':
            inserir_cliente()
        elif opcao == '2':
            inserir_pedido()
        elif opcao == '3':
            consultar_pedidos()
        elif opcao == '4':
            alterar_pedido()
        elif opcao == '5':
            print('Saindo...')
            break
        else:
            print('-'*70)
            print('Opção inválida. Tente novamente.')
            print('-'*70)
    
    # Fechar a conexão com o banco de dados
    conn.close()