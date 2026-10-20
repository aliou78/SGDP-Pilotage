import sqlite3

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()
print("Tables existantes:")
for table in tables:
    print(f"  - {table[0]}")
    
print("\nVérification de la table accounts_user:")
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='accounts_user';")
result = cursor.fetchone()
if result:
    print("Structure:")
    print(result[0])
else:
    print("Table n'existe pas!")

conn.close()
