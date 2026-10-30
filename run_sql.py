import sqlite3
import sys


def main():
    name = 'queries.sql'
    first, last = 1, 100
    if len(sys.argv) > 1:
        name = sys.argv[1]
    if len(sys.argv) > 3:
        first, last = int(sys.argv[2]), int(sys.argv[3])
    with open(name, encoding='utf-8') as f:
        text = f.read()
    conn = sqlite3.connect('shop.db')
    number = 0
    for part in text.split(';'):
        part = part.strip()
        if part == '':
            continue
        number += 1
        if number < first or number > last:
            continue
        print(part.split('\n')[0])
        cur = conn.execute(part)
        print(' | '.join(col[0] for col in cur.description))
        rows = cur.fetchall()
        for row in rows:
            print(' | '.join(str(v) for v in row))
        print('строк:', len(rows))
        print()
    conn.close()


main()
