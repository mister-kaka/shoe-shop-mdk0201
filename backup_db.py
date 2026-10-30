import os
import sqlite3

TABLES = ['Categories', 'Manufacturers', 'Sizes', 'Users', 'Products', 'Stock', 'Orders', 'OrderItems']


def count_rows(path):
    conn = sqlite3.connect(path)
    result = {}
    for table in TABLES:
        result[table] = conn.execute('SELECT COUNT(*) FROM ' + table).fetchone()[0]
    conn.close()
    return result


def main():
    if not os.path.exists('shop.db'):
        print('Нет файла shop.db, сначала python import_data.py')
        return
    for name in ('shop_backup.db', 'restored.db', 'from_dump.db', 'dump.sql'):
        if os.path.exists(name):
            os.remove(name)

    src = sqlite3.connect('shop.db')

    # резервная копия
    copy = sqlite3.connect('shop_backup.db')
    src.backup(copy)
    copy.close()
    print('Резервная копия: shop_backup.db')

    # восстановление из копии в новый файл
    copy = sqlite3.connect('shop_backup.db')
    restored = sqlite3.connect('restored.db')
    copy.backup(restored)
    restored.close()
    copy.close()
    print('Восстановлено из копии: restored.db')

    # дамп в SQL
    with open('dump.sql', 'w', encoding='utf-8') as f:
        for line in src.iterdump():
            f.write(line + '\n')
    src.close()
    print('Дамп: dump.sql')

    # чистая база из дампа
    with open('dump.sql', encoding='utf-8') as f:
        script = f.read()
    conn = sqlite3.connect('from_dump.db')
    conn.executescript(script)
    conn.close()
    print('Развёрнуто из дампа: from_dump.db')
    print()

    # сравнение
    base = count_rows('shop.db')
    others = {'shop_backup.db': count_rows('shop_backup.db'), 'restored.db': count_rows('restored.db'),
              'from_dump.db': count_rows('from_dump.db')}
    print('{:14}{:>9}'.format('таблица', 'shop.db') + ''.join('{:>16}'.format(n) for n in others))
    ok = True
    for table in TABLES:
        line = '{:14}{:>9}'.format(table, base[table])
        for name in others:
            line += '{:>16}'.format(others[name][table])
            if others[name][table] != base[table]:
                ok = False
        print(line)
    print()
    print('Количество записей совпадает везде' if ok else 'ЕСТЬ РАЗЛИЧИЯ в количестве записей')


main()
