# Configuration PostgreSQL et déploiement sur Render

PostgreSQL est le moteur utilisé par défaut. La connexion est configurée par
variables d’environnement ; aucun mot de passe de base de données n’est stocké
dans le dépôt.

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
| `DATABASE_URL` | vide | URL fournie par l’hébergeur ; prioritaire lorsqu’elle est définie |
| `DB_ENGINE` | `django.db.backends.postgresql` | Backend Django ; choisir `sqlite` seulement pour un usage local explicite |
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

Créer un rôle et une base dédiés dans PostgreSQL (choisir le mot de passe au
moment du déploiement, sans le placer dans les commandes enregistrées ou dans
le dépôt) :

```sql
CREATE ROLE sgdp LOGIN;
CREATE DATABASE sgdp OWNER sgdp;
```

Définir `DB_PASSWORD` dans l’environnement du processus Django, ainsi que les
autres variables si la base n’est pas sur `127.0.0.1:5432`, puis préparer le
schéma et contrôler l’application :

```powershell
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py check
```

Pour sélectionner SQLite explicitement lors d’un développement local ou de
tests isolés :

```powershell
$env:DB_ENGINE = "sqlite"
.\venv\Scripts\python.exe manage.py test
Remove-Item Env:DB_ENGINE
```

## Reprise des données SQLite existantes

La configuration PostgreSQL ne supprime ni ne modifie `db.sqlite3`. Sauvegarder
ce fichier avant toute opération et ne pas exécuter ces étapes sur la seule
copie des données. Exporter le contenu SQLite vers un fichier fixture protégé,
puis créer les tables PostgreSQL et charger cette fixture :

```powershell
$env:DB_ENGINE = "sqlite"
.\venv\Scripts\python.exe manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.permission --indent 2 --output sgdp-data.json

$env:DB_ENGINE = "django.db.backends.postgresql"
# Définir DB_NAME, DB_USER, DB_PASSWORD, DB_HOST et DB_PORT avant ces étapes.
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py loaddata sgdp-data.json
```

Le fixture contient des données utilisateurs et des empreintes de mots de
passe : le conserver dans un emplacement privé, ne pas le publier et le
supprimer de manière sûre après vérification de l’import. Vérifier les
enregistrements et les comptes dans l’application avant de basculer le service.
