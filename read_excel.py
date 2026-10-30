import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
FILES = ['Products_import.xlsx', 'Stock_Items_import.xlsx', 'Sizes_import.xlsx', 'Orders_import.xlsx', 'Users_import.xlsx']


# A -> 0, B -> 1, Z -> 25, AA -> 26
def col_to_index(letters):
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - ord('A') + 1)
    return n - 1


def read_xlsx(path):
    with zipfile.ZipFile(path) as z:
        shared = []
        if 'xl/sharedStrings.xml' in z.namelist():
            root = ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in root.findall(NS + 'si'):
                shared.append(''.join(t.text or '' for t in si.iter(NS + 't')))
        sheet = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
    rows = []
    for row in sheet.iter(NS + 'row'):
        cells = {}
        for c in row.findall(NS + 'c'):
            letters = re.match(r'[A-Z]+', c.get('r')).group()
            v = c.find(NS + 'v')
            if v is None or v.text is None:
                value = ''
            elif c.get('t') == 's':
                value = shared[int(v.text)]
            else:
                value = v.text
            # неразрывные пробелы меняю на обычные, иначе названия не совпадут
            cells[col_to_index(letters)] = value.replace('\xa0', ' ').strip()
        if cells:
            rows.append([cells.get(i, '') for i in range(max(cells) + 1)])
    return rows


def main():
    for name in FILES:
        try:
            rows = read_xlsx(os.path.join(BASE_DIR, name))
        except FileNotFoundError:
            print('Файл не найден:', name)
            return 1
        except (zipfile.BadZipFile, KeyError, ET.ParseError) as e:
            print('Не удалось прочитать %s: %s' % (name, e))
            return 1
        print('%s: строк с данными %d, столбцов %d' % (name, len(rows) - 1, len(rows[0])))
        for row in rows[:3]:
            print('   ', ' | '.join(c[:25] for c in row))
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
