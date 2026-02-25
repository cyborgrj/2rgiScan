import sqlite3

db = sqlite3.connect('./db/banco.db')
acessos = ['administrador', 'digitalização']
cursor = db.cursor()

# cursor.execute('''DROP TABLE IF EXISTS users''')

cursor.execute('''CREATE TABLE IF NOT EXISTS users(user CHAR, username CHAR, password CHAR, access CHAR)''')

cursor.close()
db.commit()
db.close()

