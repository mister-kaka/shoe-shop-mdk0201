import logging
import sqlite3
import sys

from create_db import create_database
from import_orders import import_orders
from import_products import import_products
from import_refs import connect_db, import_categories_and_manufacturers, import_sizes, import_users, print_counts
from import_stock import import_stock

TABLES = ('Categories', 'Manufacturers', 'Sizes', 'Users', 'Products', 'Stock', 'Orders', 'OrderItems')
log = logging.getLogger('import_data')


def main():
    try:
        create_database()
    except (OSError, sqlite3.Error) as e:
        log.error('Не удалось создать базу: %s', e)
        return 1
    conn = connect_db()
    cur = conn.cursor()
    try:
        import_sizes(cur)
        import_users(cur)
        import_categories_and_manufacturers(cur)
        import_products(cur)
        import_stock(cur)
        import_orders(cur)
        conn.commit()
        log.info('Импорт завершён успешно')
        print_counts(cur, TABLES)
    except Exception as e:
        conn.rollback()
        log.error('Ошибка импорта, изменения отменены: %s', e)
        return 1
    finally:
        conn.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
