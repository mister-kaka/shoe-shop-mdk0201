import logging
import os
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'shop.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
log = logging.getLogger('create_db')


def create_database():
    log.info('Читаю схему: %s', SCHEMA_PATH)
    with open(SCHEMA_PATH, encoding='utf-8') as f:
        script = f.read()
    conn = sqlite3.connect(DB_PATH)
    try:
        log.info('Создаю базу: %s', DB_PATH)
        conn.executescript(script)
        conn.commit()
        rows = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
    finally:
        conn.close()
    return [r[0] for r in rows]


def main():
    try:
        tables = create_database()
    except FileNotFoundError as e:
        log.error('Файл не найден: %s', e)
        return 1
    except sqlite3.Error as e:
        log.error('Ошибка SQLite: %s', e)
        return 1
    log.info('Создано таблиц: %d', len(tables))
    for t in tables:
        print(' -', t)
    return 0


if __name__ == '__main__':
    sys.exit(main())
