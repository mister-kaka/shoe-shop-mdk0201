import logging
import os
import sqlite3
import sys
from datetime import date, timedelta

from create_db import DB_PATH
from import_refs import connect_db, number_text
from import_stock import find_product_id
from read_excel import BASE_DIR, read_xlsx

log = logging.getLogger('import_orders')

def excel_date(value):
    try:
        days = int(float(value))
    except ValueError:
        return value
    return (date(1899, 12, 30) + timedelta(days=days)).isoformat()


def find_stock_id(cur, name, manufacturer, size):
    product_id = find_product_id(cur, name, manufacturer)
    if product_id is None:
        return None
    cur.execute('SELECT s.id FROM Stock s JOIN Sizes z ON z.id = s.size_id WHERE s.product_id = ? AND z.value = ?', (product_id, size))
    row = cur.fetchone()
    if row is None:
        return None
    return row[0]


def import_orders(cur):
    rows = read_xlsx(os.path.join(BASE_DIR, 'Orders_import.xlsx'))
    orders = {} 
    for row in rows[1:]:
        if len(row) < 9 or not row[0]:
            continue
        number = row[0]
        fio = row[2].split()
        last_name = fio[0] if len(fio) > 0 else ''
        first_name = fio[1] if len(fio) > 1 else ''
        middle_name = fio[2] if len(fio) > 2 else ''
        cur.execute('SELECT id FROM Users WHERE last_name = ? AND first_name = ? AND middle_name = ?', (last_name, first_name, middle_name))
        user = cur.fetchone()
        if user is None:
            cur.execute("INSERT INTO Users (last_name, first_name, middle_name, login, role) VALUES (?, ?, ?, ?, 'Авторизованный пользователь')",
                        (last_name, first_name, middle_name, 'guest_' + number))
            user_id = cur.lastrowid
            log.info('Клиента нет в списке пользователей, создан гость: %s %s', last_name, first_name)
        else:
            user_id = user[0]
        if number not in orders:
            cur.execute('INSERT INTO Orders (order_date, user_id) VALUES (?, ?)', (excel_date(row[1]), user_id))
            orders[number] = cur.lastrowid
        stock_id = find_stock_id(cur, row[4], row[5], number_text(row[6]))
        if stock_id is None:
            log.warning('В заказе %s нет такого товара на складе: %s, размер %s', number, row[4], row[6])
            continue
        cur.execute('INSERT INTO OrderItems (order_id, stock_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
                    (orders[number], stock_id, int(float(row[7] or 1)), float(row[8] or 0)))
    log.info('Заказы загружены: %d', len(orders))
    return len(orders)


def main():
    if not os.path.exists(DB_PATH):
        log.error('Нет файла shop.db. Сначала выполните: python create_db.py')
        return 1
    conn = connect_db()
    cur = conn.cursor()
    try:
        old_count = cur.execute('SELECT COUNT(*) FROM Orders').fetchone()[0]
        if old_count > 0:
            # у заказов нет уникального ключа, повторный импорт создал бы копии
            log.error('В таблице Orders уже есть заказы (%d). Повторная загрузка создала бы дубли. '
                      'Чтобы загрузить заново, начните с python create_db.py', old_count)
            return 1
        import_orders(cur)
        conn.commit()
        orders = cur.execute('SELECT COUNT(*) FROM Orders').fetchone()[0]
        items = cur.execute('SELECT COUNT(*) FROM OrderItems').fetchone()[0]
        print('Заказов: %d, позиций заказов: %d' % (orders, items))
        rows = cur.execute('SELECT o.id, o.order_date, u.last_name, p.name, z.value, oi.quantity, oi.unit_price '
                           'FROM OrderItems oi JOIN Orders o ON o.id = oi.order_id JOIN Users u ON u.id = o.user_id '
                           'JOIN Stock s ON s.id = oi.stock_id JOIN Products p ON p.id = s.product_id '
                           'JOIN Sizes z ON z.id = s.size_id ORDER BY o.id, oi.id LIMIT 6').fetchall()
        print('Первые позиции (заказ, дата, клиент, товар, размер, кол-во, цена):')
        for r in rows:
            print(' ', r[0], '|', r[1], '|', r[2], '|', r[3][:34], '|', r[4], '|', r[5], '|', r[6])
    except (sqlite3.Error, OSError, ValueError) as e:
        conn.rollback()
        log.error('Ошибка импорта, изменения отменены: %s', e)
        return 1
    finally:
        conn.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
