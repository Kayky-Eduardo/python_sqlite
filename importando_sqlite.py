import sqlite3

# conn: é a váriavel para conexão com o banco de dados
conn = sqlite3.connect("C:\kayky\python_sqlite\meu_banco_de_dados2.db")

# Para operações no banco de dados, você também precisará de um cursor,
# que é um objeto que permite executar comandos SQL.
cursor = conn.cursor()

cursor.execute("""
    create table if not exists clientes (
        id integer primary key autoincrement,
        nome text not null,
        idade integer
    )
""")

cursor.execute("""
    create table if not exists servico (
        servicoid integer primary key autoincrement,
        servico text,
        integer,
        genero text
    )
""")

cursor.execute("""
    create table if not exists contato (
        contatoid integer primary key autoincrement,
        tel1 integer,
        tel2 integer,
        email text
        )
""")
