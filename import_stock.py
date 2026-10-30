import logging
import os
import sqlite3
import sys

from create_db import DB_PATH
from import_refs import connect_db, get_or_create, number_text
from read_excel import BASE_DIR, read_xlsx

log = logging.getLogger('import_stock')


def find_product_id(cur, name, manufacturer):
    cur.execute('SELECT p.id FROM Products p JOIN Manufacturers m ON m.id = p.manufacturer_id WHERE p.name = ? AND m.name = ?',
                (name, manufacturer))
    row = cur.fetchone()
    if row is None:
        cur.execute("SELECT p.id FROM Products p JOIN Manufacturers m ON m.id = p.manufacturer_id WHERE p.name LIKE ? || '%' AND m.name = ?",
                    (name, manufacturer))
        row = cur.fetchone()
    if row is None:
        return None
    return row[0]


def import_stock(cur):
    rows = read_xlsx(os.path.join(BASE_DIR, 'Stock_Items_import.xlsx'))
    skipped = 0
    for row in rows[1:]:
        if len(row) < 4 or not row[0]:
            continue
        product_id = find_product_id(cur, row[0], row[1])
        if product_id is None:
            log.warning('Товар не найден, строка пропущена: %s / %s', row[0], row[1])
            skipped += 1
            continue
        size_id = get_or_create(cur, 'Sizes', 'value', number_text(row[2]))
        cur.execute('INSERT INTO Stock (product_id, size_id, quantity) VALUES (?, ?, ?) '
                    'ON CONFLICT (product_id, size_id) DO UPDATE SET quantity = excluded.quantity',
                    (product_id, size_id, int(float(row[3] or 0))))
    log.info('Склад загружен (пропущено строк: %d)', skipped)
    return skipped


def main():
    if not os.path.exists(DB_PATH):
        log.error('Нет файла shop.db. Сначала выполните: python create_db.py')
        return 1
    conn = connect_db()
    cur = conn.cursor()
    try:
        skipped = import_stock(cur)
        conn.commit()
        rows_count, total = cur.execute('SELECT COUNT(*), SUM(quantity) FROM Stock').fetchone()
    except (sqlite3.Error, OSError, ValueError) as e:
        conn.rollback()
        log.error('Ошибка импорта, изменения отменены: %s', e)
        return 1
    finally:
        conn.close()
    print('Строк в таблице Stock: %d. Всего пар на складе (SUM(quantity)): %d. Пропущено строк файла: %d.' % (rows_count, total, skipped))
    return 0


if __name__ == '__main__':
    sys.exit(main())
