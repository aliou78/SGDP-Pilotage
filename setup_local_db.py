from getpass import getpass
from pathlib import Path
import os
import sys

from dotenv import load_dotenv, set_key


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / '.env'


def configure_database(password, env_file=None):
    if not password:
        raise ValueError('PostgreSQL password cannot be empty.')
    env_file = Path(env_file) if env_file is not None else ENV_FILE

    settings = {
        'DB_ENGINE': os.environ.get(
            'DB_ENGINE',
            'django.db.backends.postgresql',
        ),
        'DB_NAME': os.environ.get('DB_NAME', 'sgdp'),
        'DB_USER': os.environ.get('DB_USER', 'sgdp'),
        'DB_HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'DB_PORT': os.environ.get('DB_PORT', '5432'),
    }
    for key, value in settings.items():
        set_key(str(env_file), key, value, quote_mode='never')
    set_key(str(env_file), 'DB_PASSWORD', password, quote_mode='always')
    for key, value in settings.items():
        os.environ.setdefault(key, value)
    os.environ['DB_PASSWORD'] = password


def configure_password_if_missing(env_file=None):
    env_file = Path(env_file) if env_file is not None else ENV_FILE
    load_dotenv(env_file, override=False)

    engine = os.environ.get(
        'DB_ENGINE',
        'django.db.backends.postgresql',
    )
    database_url = os.environ.get('DATABASE_URL')
    engine_is_explicit = 'DB_ENGINE' in os.environ
    if (
        not engine.startswith('django.db.backends.postgresql')
        or os.environ.get('DB_PASSWORD')
        or (database_url and not engine_is_explicit)
        or not sys.stdin.isatty()
    ):
        return False

    password = getpass('Mot de passe PostgreSQL du rôle sgdp : ')
    if not password:
        print('Mot de passe vide : PostgreSQL ne peut pas se connecter.')
        return False

    configure_database(password, env_file)
    print(
        f'Mot de passe enregistré dans {env_file.name} '
        '(fichier local ignoré par Git).'
    )
    return True


def main():
    password = getpass('Mot de passe PostgreSQL du rôle sgdp : ')
    configure_database(password)
    print(f'Configuration PostgreSQL enregistrée dans {ENV_FILE.name}.')
    print('Lancez ensuite : python manage.py migrate')
    print('Puis : python manage.py runserver')


if __name__ == '__main__':
    main()
