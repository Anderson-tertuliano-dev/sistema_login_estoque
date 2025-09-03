import sqlite3

conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                celular TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL    
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               produto TEX NOT NULL,
               codigo TEXT NOT NULL UNIQUE,
               quantidade INTEGER NOT NULL,
               preco REAL NOT NULL
)
""")

# cursor.execute("""
#                 INSERT OR IGNORE INTO usuarios (nome, email, cpf, celular, senha)
#                 VALUES (?, ?, ?, ?, ?)
# """ , ("Ander", "ander@mail.com", "12345678900", "11999999999", "12345"))

conn.commit()
conn.close()
print('"Banco de dados e tabelas criado!"')