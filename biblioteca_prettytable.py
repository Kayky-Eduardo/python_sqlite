import os
import sqlite3
from prettytable import PrettyTable

conn = sqlite3.connect("sql\meu_banco_de_dados.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM clientes")
resultado = cursor.fetchall()

os.system('cls')

# Cria tabela PrettyTable e define os nomes das colunas
tabela = PrettyTable()
# Obtém os nomes das colunas a partir de cursor.description
colunas = [descricao[0] for descricao in cursor.description]
# Define os nomes das colunas na tabela PrettyTable
tabela.field_names = colunas

# Adiciona as linhas à tabela
for row in resultado:
    tabela.add_row(row)

print(tabela)
conn.close()