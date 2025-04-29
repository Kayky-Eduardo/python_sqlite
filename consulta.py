import os
import sqlite3

conn = sqlite3.connect("sql\meu_banco_de_dados.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM clientes")
resultado = cursor.fetchall()

os.system('cls')
for row in resultado:
    print(row)
conn.close()