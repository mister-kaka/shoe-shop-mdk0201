import logging
import os
import sqlite3
import sys

from create_db import DB_PATH
from read_excel import BASE_DIR, read_xlsx

log = logging.getLogger('import_refs')


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def number_text(value):
    try:
        n = float(value)
    except ValueError:
        return value
    if n == int(n):
        return str(int(n))
    return str(n)

def get_or_create(cur, table, column, value):
    cur.execute('INSERT OR IGNORE INTO %s (%s) VALUES (?)' % (table, column), (value,))
    cur.execute('SELECT id FROM %s WHERE %s = ?' % (table, column), (value,))
    return cur.fetchone()[0]


def import_sizes(cur):
    rows = read_xlsx(os.path.join(BASE_DIR, 'Sizes_import.xlsx'))
    for row in rows[1:]:
        if row and row[0]:
            get_or_create(cur, 'Sizes', 'value', number_text(row[0]))
    log.info('Размеры загружены')


def import_users(cur):
    rows = read_xlsx(os.path.join(BASE_DIR, 'Users_import.xlsx'))
    for row in rows[1:]:
        if len(row) < 5 or not row[3]:
            continue
        cur.execute('INSERT OR IGNORE INTO Users (last_name, first_name, middle_name, login, role) VALUES (?, ?, ?, ?, ?)',
                    (row[0], row[1], row[2], row[3], row[4]))
    log.info('Пользователи загружены')


def import_categories_and_manufacturers(cur):
    rows = read_xlsx(os.path.join(BASE_DIR, 'Products_import.xlsx'))
    for row in rows[1:]:
        if len(row) < 5 or not row[0] or not row[4]:
            continue
        get_or_create(cur, 'Categories', 'name', row[0])
        get_or_create(cur, 'Manufacturers', 'name', row[4])
    log.info('Категории и производители загружены')


def print_counts(cur, tables):
    print('Записей в таблицах:')
    for t in tables:
        print(' ', t, cur.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0])


def main():
    if not os.path.exists(DB_PATH):
        log.error('Нет файла shop.db. Сначала выполните: python create_db.py')
        return 1
    conn = connect_db()
    cur = conn.cursor()
    try:
        import_sizes(cur)
        import_users(cur)
        import_categories_and_manufacturers(cur)
        conn.commit()
        print_counts(cur, ('Categories', 'Manufacturers', 'Sizes', 'Users'))
    except (sqlite3.Error, OSError) as e:
        conn.rollback()
        log.error('Ошибка импорта, изменения отменены: %s', e)
        return 1
    finally:
        conn.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
