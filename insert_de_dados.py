import sqlite3

# conn: é a váriavel para conexão com o banco de dados
conn = sqlite3.connect("C:\kayky\python_sqlite\meu_banco_de_dados.db")

cursor = conn.cursor()

# definição em uma tupla com os dados
dados_cliente = ("João Silva", 30)

# Placeholders (?, ?): Os pontos de interrogação são usados como
# "espaços reservados". Eles serão substituídos pelos valores
# tupla dados_cliente (ou seja, "joão silva" e 30).
# Por quê: Usar placeholders é uma prática recomendada,
# pois previne ataques de injeção de SQL.
cursor.execute("insert into clientes (nome, idade) values (?, ?)", dados_cliente)

conn.commit() # Salva a transação no banco de dados
conn.close() # fecha conexão

