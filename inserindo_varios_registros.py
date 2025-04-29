import sqlite3

# conn: é a váriavel para conexão com o banco de dados
conn = sqlite3.connect("sql\meu_banco_de_dados.db")

cursor = conn.cursor()

dados_varios_clientes = [
    ("Maria Souza", 25),
    ("Carlos Pereira", 35),
    ("Pedro José", 28),
    ("Ana Costa", 28),
    ("Luis Gomes", 30),
    ("Juliana Almeida", 33),
    ("Roberto Silva", 40),
    ("Fernanda Lima", 22),
    ("Lucas Martins", 27),
    ("Sofia Ferreira", 31)
]
cursor.executemany(
    "insert into clientes (nome, idade) values (?, ?)", dados_varios_clientes)
conn.commit()
conn.close()