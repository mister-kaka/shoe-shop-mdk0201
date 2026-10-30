import logging
import os
import sqlite3
import sys

from create_db import DB_PATH
from import_refs import connect_db, get_or_create
from read_excel import BASE_DIR, read_xlsx

log = logging.getLogger('import_products')


def import_products(cur):
    rows = read_xlsx(os.path.join(BASE_DIR, 'Products_import.xlsx'))
    count = 0
    for row in rows[1:]:
        if len(row) < 8 or not row[3]:
            continue
        category_id = get_or_create(cur, 'Categories', 'name', row[0])
        manufacturer_id = get_or_create(cur, 'Manufacturers', 'name', row[4])
        # если такой товар уже есть, обновляем цену и картинку
        cur.execute('INSERT INTO Products (category_id, manufacturer_id, name, subcategory, description, composition, price, image) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?) '
                    'ON CONFLICT (name, manufacturer_id) DO UPDATE SET price = excluded.price, image = excluded.image',
                    (category_id, manufacturer_id, row[3], row[1], row[5], row[6], float(row[7]), row[2]))
        count += 1
    log.info('Товары загружены')
    return count


def main():
    if not os.path.exists(DB_PATH):
        log.error('Нет файла shop.db. Сначала выполните: python create_db.py')
        return 1
    conn = connect_db()
    cur = conn.cursor()
    try:
        before = cur.execute('SELECT COUNT(*) FROM Products').fetchone()[0]
        count = import_products(cur)
        conn.commit()
        after = cur.execute('SELECT COUNT(*) FROM Products').fetchone()[0]
    except (sqlite3.Error, OSError, ValueError) as e:
        conn.rollback()
        log.error('Ошибка импорта, изменения отменены: %s', e)
        return 1
    finally:
        conn.close()
    added = after - before
    print('Строк в файле: %d. Добавлено новых: %d. Обновлено существующих: %d.' % (count, added, count - added))
    print('Всего товаров в таблице Products:', after)
    return 0


if __name__ == '__main__':
    sys.exit(main())
