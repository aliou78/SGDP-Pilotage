#!/usr/bin/env python
import sqlite3
from datetime import datetime

# Connecter directement à la base de données SQLite
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Insérer la migration accounts.0001_initial comme déjà appliquée
try:
    cursor.execute(
        "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)",
        ('accounts', '0001_initial', datetime.now())
    )
    print("Migration accounts.0001_initial insertée")
except Exception as e:
    print(f"Erreur accounts: {e}")

# Insérer aussi la migration debarquements.0002_debarquement_agent
try:
    cursor.execute(
        "INSERT INTO django_migrations (app, name, applied) VALUES (?, ?, ?)",
        ('debarquements', '0002_debarquement_agent', datetime.now())
    )
    print("Migration debarquements.0002_debarquement_agent insertée")
except Exception as e:
    print(f"Erreur debarquements: {e}")

conn.commit()
conn.close()
print("Toutes les migrations marquées comme appliquées")
