#!/usr/bin/env python
import django
import os
import sqlite3

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.apps import apps
from django.db.backends.sqlite3.schema import DatabaseSchemaEditor

# Créer les tables pour tous les models
schema_editor = DatabaseSchemaEditor(connection)

for app_config in apps.get_app_configs():
    for model in app_config.get_models():
        table_name = model._meta.db_table
        
        # Vérifier si la table existe déjà avec SQLite directement
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        exists = cursor.fetchone()
        conn.close()
        
        if not exists:
            try:
                # Créer la table
                schema_editor.create_model(model)
                print(f"✓ Table {table_name} créée")
            except Exception as e:
                print(f"✗ Erreur pour {table_name}: {e}")
        else:
            print(f"→ Table {table_name} existe déjà")

print("\nTous les modèles ont été traités!")
