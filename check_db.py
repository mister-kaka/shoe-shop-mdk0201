# в windows нет sqlite3, поэтому проверяю базу через python
# python check_db.py apply schema.sql - выполнить sql-файл
# python check_db.py - таблицы и число строк
# python check_db.py schema Products - как создана таблица
# python check_db.py indexes - индексы
# python check_db.py rules - проверка ограничений
# python check_db.py query "SELECT ..." - любой select
import os
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'shop.db')


def check_rules(conn):
    tests = [
        ('CHECK: неизвестная роль', "INSERT INTO Users (last_name, first_name, login, role) VALUES ('Тест', 'Тест', 'test_a', 'Гость')"),
        ('UNIQUE: повторный логин', "INSERT INTO Users (last_name, first_name, login, role) VALUES ('Тест', 'Тест', 'test_user', 'Менеджер')"),
        ('NOT NULL: пользователь без логина', "INSERT INTO Users (last_name, first_name, role) VALUES ('Тест', 'Тест', 'Менеджер')"),
        ('FOREIGN KEY: заказ несуществующего клиента', "INSERT INTO Orders (order_date, user_id) VALUES ('2026-01-01', 9999)"),
    ]
    user_id = conn.execute("INSERT INTO Users (last_name, first_name, login, role) VALUES ('Тест', 'Тест', 'test_user', 'Менеджер')").lastrowid
    for title, sql in tests:
        try:
            conn.execute(sql)
            print('[НЕТ ОШИБКИ]', title, '- ограничение не сработало!')
        except sqlite3.IntegrityError as e:
            print('[ошибка, так и надо]', title)
            print('   ', e)
            
    # тестовые данные 
    cat = conn.execute("INSERT INTO Categories (name) VALUES ('Тест')").lastrowid
    man = conn.execute("INSERT INTO Manufacturers (name) VALUES ('Тест')").lastrowid
    size = conn.execute("INSERT INTO Sizes (value) VALUES ('99')").lastrowid
    prod = conn.execute("INSERT INTO Products (category_id, manufacturer_id, name, price) VALUES (?, ?, 'Тестовый товар', 100)", (cat, man)).lastrowid
    stock = conn.execute("INSERT INTO Stock (product_id, size_id, quantity) VALUES (?, ?, 5)", (prod, size)).lastrowid
    order = conn.execute("INSERT INTO Orders (order_date, user_id) VALUES ('2026-01-01', ?)", (user_id,)).lastrowid
    conn.execute("INSERT INTO OrderItems (order_id, stock_id, quantity, unit_price) VALUES (?, ?, 1, 100)", (order, stock))
    before = conn.execute('SELECT COUNT(*) FROM OrderItems WHERE order_id = ?', (order,)).fetchone()[0]
    conn.execute('DELETE FROM Orders WHERE id = ?', (order,))
    after = conn.execute('SELECT COUNT(*) FROM OrderItems WHERE order_id = ?', (order,)).fetchone()[0]
    print('[каскад] позиций заказа до удаления заказа: %d, после: %d' % (before, after))
    before = conn.execute('SELECT COUNT(*) FROM Stock WHERE product_id = ?', (prod,)).fetchone()[0]
    conn.execute('DELETE FROM Products WHERE id = ?', (prod,))
    after = conn.execute('SELECT COUNT(*) FROM Stock WHERE product_id = ?', (prod,)).fetchone()[0]
    print('[каскад] строк склада до удаления товара: %d, после: %d' % (before, after))
    conn.rollback()
    print('Все временные данные отменены (rollback).')


args = sys.argv[1:]
try:
    if len(args) == 2 and args[0] == 'apply':
        conn = sqlite3.connect(DB_PATH)
        conn.executescript(open(os.path.join(BASE_DIR, args[1]), encoding='utf-8').read())
        conn.commit()
        conn.close()
        print('Скрипт выполнен без ошибок:', args[1])
        sys.exit(0)
    if not os.path.exists(DB_PATH):
        print('Файл shop.db не найден. Сначала создайте базу.')
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON')
    if len(args) == 0:
        names = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
        print('Таблицы в базе:', len(names))
        for n in names:
            count = conn.execute('SELECT COUNT(*) FROM ' + n[0]).fetchone()[0]
            print(' ', n[0], 'строк:', count)
    elif args[0] == 'schema' and len(args) == 2:
        row = conn.execute("SELECT sql FROM sqlite_master WHERE type = 'table' AND name = ?", (args[1],)).fetchone()
        if row is None:
            print('Такой таблицы нет:', args[1])
        else:
            print(row[0])
            print('\nВнешние ключи:')
            for k in conn.execute('PRAGMA foreign_key_list(' + args[1] + ')').fetchall():
                print(' ', k[3], '->', k[2] + '(' + k[4] + '), при удалении:', k[6])
    elif args[0] == 'indexes':
        rows = conn.execute("SELECT name, tbl_name FROM sqlite_master WHERE type = 'index' AND name NOT LIKE 'sqlite_%' ORDER BY name").fetchall()
        print('Индексы:', len(rows))
        for r in rows:
            print(' ', r[0], '- таблица', r[1])
    elif args[0] == 'rules':
        check_rules(conn)
    elif args[0] == 'query' and len(args) == 2:
        if not args[1].strip().upper().startswith('SELECT'):
            print('Разрешены только запросы SELECT')
        else:
            cur = conn.execute(args[1])
            print(' | '.join(c[0] for c in cur.description))
            for row in cur.fetchall():
                print(' | '.join(str(v) for v in row))
    else:
        print('Команды: apply файл.sql, schema таблица, indexes, rules, query "SELECT ..."')
    conn.close()
except FileNotFoundError as e:
    print('Файл не найден:', e)
    sys.exit(1)
except sqlite3.Error as e:
    print('Ошибка SQLite:', e)
    sys.exit(1)
