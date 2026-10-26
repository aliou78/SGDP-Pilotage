# Configuration des bases de données et déploiement sur Render

PostgreSQL est le moteur par défaut, en local comme en production. La connexion
est configurée par variables d’environnement et aucun mot de passe de base de
données n’est stocké dans le dépôt. SQLite reste disponible en la sélectionnant
explicitement avec `DB_ENGINE=sqlite`, notamment pour les tests isolés.

## Déploiement Render

Le fichier `render.yaml` décrit le service web et sa base PostgreSQL Render.
Pour lancer le déploiement :

1. Pousser le projet dans un dépôt Git accessible par Render.
2. Dans Render, créer une **Blueprint** et sélectionner ce dépôt.
3. Vérifier les offres et coûts proposés pour le service web et PostgreSQL,
   puis appliquer le Blueprint.
4. Attendre la fin du build : les fichiers statiques sont collectés, les
   migrations sont appliquées et Gunicorn démarre Django.
5. Créer le compte administrateur depuis le Shell du service Render avec
   `python manage.py createsuperuser`.

Render génère `SECRET_KEY`, fournit `DATABASE_URL` pour PostgreSQL et active
`DEBUG=False` ainsi que la redirection HTTPS. Les options de facturation et la
disponibilité des offres dépendent du compte Render ; vérifier le récapitulatif
avant de confirmer.

Si un nom de domaine personnalisé est configuré, l’ajouter aux variables
`ALLOWED_HOSTS` et `CSRF_TRUSTED_ORIGINS` du service Render. Activer HSTS
uniquement après avoir confirmé que le site et tous ses sous-domaines sont
définitivement servis en HTTPS.

## Variables de connexion

| Variable | Valeur par défaut | Description |
| --- | --- | --- |
| `DATABASE_URL` | vide | URL fournie par l’hébergeur ; utilisée avec PostgreSQL |
| `DB_ENGINE` | `django.db.backends.postgresql` | Backend Django ; choisir `sqlite` explicitement pour utiliser SQLite, ce qui est prioritaire sur `DATABASE_URL` |
| `DB_NAME` | `sgdp` | Nom de la base |
| `DB_USER` | `sgdp` | Utilisateur PostgreSQL |
| `DB_PASSWORD` | vide | Mot de passe PostgreSQL ; à définir dans l’environnement du serveur |
| `DB_HOST` | `127.0.0.1` | Hôte PostgreSQL |
| `DB_PORT` | `5432` | Port PostgreSQL |
| `DB_CONN_MAX_AGE` | `60` | Durée de réutilisation d’une connexion, en secondes |
| `SECRET_KEY` | clé de développement locale | Obligatoire lorsque `DEBUG=False` |
| `DEBUG` | `True` | Passer à `False` en production |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Hôtes autorisés, séparés par des virgules |
| `CSRF_TRUSTED_ORIGINS` | vide | Origines HTTPS autorisées, séparées par des virgules |
| `SECURE_SSL_REDIRECT` | `False` | Activer la redirection HTTPS en production |

Installer les dépendances du projet :

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Au premier lancement de `python manage.py runserver` dans un terminal
interactif, Django demande le mot de passe PostgreSQL à l’écran de saisie
masquée, puis l’enregistre dans `.env` sans l’afficher. Pour créer cette
configuration séparément, exécuter `python setup_local_db.py`.
`settings.py` charge automatiquement `.env` au démarrage ; ce fichier est
ignoré par Git et ne doit jamais être publié. Si `DATABASE_URL` est définie
dans l’environnement PowerShell, la supprimer pour utiliser la configuration
PostgreSQL locale :

```powershell
Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
python manage.py migrate
python manage.py runserver
```

Créer un rôle et une base dédiés dans PostgreSQL (choisir un mot de passe et le
configurer dans l’environnement, sans le placer dans le dépôt) :

```sql
CREATE ROLE sgdp LOGIN;
CREATE DATABASE sgdp OWNER sgdp;
```

Démarrer le service PostgreSQL, puis préparer le schéma et contrôler
l’application :

```powershell
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py runserver
```

Pour forcer SQLite lors d’un développement local ou de tests isolés :

```powershell
$env:DB_ENGINE = "sqlite"
.\venv\Scripts\python.exe manage.py test
Remove-Item Env:DB_ENGINE
```

## Reprise des données SQLite existantes

La configuration PostgreSQL ne supprime ni ne modifie `db.sqlite3`. Sauvegarder
ce fichier avant toute opération et ne lancer l’import qu’une seule fois dans
une base PostgreSQL vide. Le fixture contient les utilisateurs et leurs
empreintes de mots de passe : le conserver dans un emplacement privé et ne pas
le publier.

```powershell
$env:DB_ENGINE = "sqlite"
Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
.\venv\Scripts\python.exe manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.permission --indent 2 --output sgdp-data.json

$env:DB_ENGINE = "django.db.backends.postgresql"
# Créer au préalable le rôle et la base PostgreSQL, puis définir DB_PASSWORD.
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py loaddata sgdp-data.json
```

Vérifier les enregistrements et les comptes dans l’application avant de supprimer
le fixture de manière sûre. Ne pas supprimer la base SQLite avant d’avoir
confirmé l’import.
