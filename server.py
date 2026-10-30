import json
import mimetypes
import os
import sqlite3
from datetime import date
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'shop.db')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
HOST = '127.0.0.1'
PORT = 8000
# заказы в файле за апрель и май 2026, поэтому сегодня для скидок беру из этих данных
TODAY = '2026-05-20'
DISCOUNT = 0.25

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

class ApiError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message

class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_static(self, url_path):
        if url_path == '/':
            url_path = '/index.html'
        full_path = os.path.normpath(os.path.join(STATIC_DIR, url_path.lstrip('/')))
        # не отдаём файлы за пределами static (../)
        if not full_path.startswith(STATIC_DIR + os.sep) or not os.path.isfile(full_path):
            self.send_json({'error': 'Файл не найден'}, 404)
            return
        content_type = mimetypes.guess_type(full_path)[0] or 'application/octet-stream'
        with open(full_path, 'rb') as f:
            data = f.read()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def read_json(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode('utf-8'))
        except ValueError:
            raise ApiError(400, 'Тело запроса не является корректным JSON')

    def do_GET(self):
        url = urlparse(self.path)
        params = {}
        for key, values in parse_qs(url.query).items():
            params[key] = values[0]
        routes = {}
        routes['/api/login'] = self.api_login
        routes['/api/products'] = self.api_products
        routes['/api/product'] = self.api_product
        routes['/api/categories'] = self.api_categories
        if url.path.startswith('/api/'):
            self.run_api(routes.get(url.path), params)
        else:
            self.send_static(url.path)

    def do_POST(self):
        url = urlparse(self.path)
        routes = {'/api/echo': self.api_echo}
        routes['/api/order/create'] = self.api_order_create
        try:
            data = self.read_json()
        except ApiError as error:
            self.send_json({'error': error.message}, error.status)
            return
        self.run_api(routes.get(url.path), data)

    def run_api(self, func, data):
        if func is None:
            self.send_json({'error': 'Такого адреса нет'}, 404)
            return
        try:
            result = func(data)
        except ApiError as error:
            self.send_json({'error': error.message}, error.status)
            return
        except sqlite3.Error as error:
            self.send_json({'error': 'Ошибка базы данных: {}'.format(error)}, 500)
            return
        except Exception:
            self.send_json({'error': 'Внутренняя ошибка сервера'}, 500)
            return
        self.send_json(result)

    def api_echo(self, data):
        return {'ok': True, 'received': data}

    def get_user(self, conn, login):
        row = conn.execute('SELECT id, last_name, first_name, middle_name, role FROM Users WHERE login = ?',
                           ((login or '').strip(),)).fetchone()
        if row is None:
            raise ApiError(404, 'Логин не найден')
        return row

    def api_login(self, params):
        conn = connect()
        try:
            user = self.get_user(conn, params.get('login'))
            return {'id': user['id'], 'fio': make_fio(user), 'role': user['role']}
        finally:
            conn.close()

    def api_products(self, params):
        category = params.get('category', '')
        search = params.get('search', '').strip().lower()
        sort = params.get('sort', '')
        conn = connect()
        try:
            rows = conn.execute(
                'SELECT p.id, p.name, p.price, p.image, p.description, c.name AS category, m.name AS manufacturer, '
                'COALESCE(SUM(s.quantity), 0) AS total '
                'FROM Products p '
                'JOIN Categories c ON c.id = p.category_id '
                'JOIN Manufacturers m ON m.id = p.manufacturer_id '
                'LEFT JOIN Stock s ON s.product_id = p.id '
                'WHERE ? = \'\' OR c.name = ? '
                'GROUP BY p.id',
                (category, category)).fetchall()
            ordered = ordered_last_month(conn)
        finally:
            conn.close()
        products = []
        for row in rows:
            text = (row['name'] + ' ' + row['manufacturer'] + ' ' + (row['description'] or '')).lower()
            if search and search not in text:
                continue
            discount = row['id'] not in ordered
            products.append({
                'id': row['id'],
                'name': row['name'],
                'category': row['category'],
                'manufacturer': row['manufacturer'],
                'image': row['image'],
                'price': row['price'],
                'discount': discount,
                'price_final': final_price(row['price'], discount),
                'total': row['total'],
                'level': 'мало' if row['total'] <= 3 else 'много'
            })
        if sort == 'price_asc':
            products.sort(key=lambda x: x['price_final'])
        elif sort == 'price_desc':
            products.sort(key=lambda x: x['price_final'], reverse=True)
        return products

    def api_product(self, params):
        try:
            product_id = int(params.get('id', ''))
        except ValueError:
            raise ApiError(400, 'Нужен числовой параметр id')
        conn = connect()
        try:
            row = conn.execute(
                'SELECT p.id, p.name, p.subcategory, p.description, p.composition, p.price, p.image, '
                'c.name AS category, m.name AS manufacturer '
                'FROM Products p JOIN Categories c ON c.id = p.category_id '
                'JOIN Manufacturers m ON m.id = p.manufacturer_id WHERE p.id = ?', (product_id,)).fetchone()
            if row is None:
                raise ApiError(404, 'Товар не найден')
            sizes = conn.execute(
                'SELECT s.id AS stock_id, z.value, s.quantity FROM Stock s JOIN Sizes z ON z.id = s.size_id '
                'WHERE s.product_id = ?', (product_id,)).fetchall()
            ordered = ordered_last_month(conn)
        finally:
            conn.close()
        product = dict(row)
        product['discount'] = product_id not in ordered
        product['price_final'] = final_price(row['price'], product['discount'])
        product['sizes'] = sorted([dict(s) for s in sizes], key=lambda s: float(s['value']))
        return product

    def api_categories(self, params):
        conn = connect()
        try:
            rows = conn.execute('SELECT name FROM Categories ORDER BY id').fetchall()
            return [row['name'] for row in rows]
        finally:
            conn.close()

    def api_order_create(self, data):
        items = data.get('items')
        if not isinstance(items, list) or len(items) == 0:
            raise ApiError(400, 'Корзина пуста')
        conn = connect()
        try:
            if not data.get('login'):
                raise ApiError(401, 'Войдите в систему, чтобы оформить заказ')
            user = self.get_user(conn, data.get('login'))
            user_id = user['id']
            ordered = ordered_last_month(conn)
            try:
                cur = conn.execute('INSERT INTO Orders (order_date, user_id) VALUES (?, ?)', (date.today().isoformat(), user_id))
                order_id = cur.lastrowid
                for item in items:
                    quantity = item.get('quantity')
                    if not isinstance(quantity, int) or quantity <= 0:
                        raise ApiError(400, 'Количество должно быть целым числом больше нуля')
                    stock = conn.execute('SELECT s.id, s.quantity, p.id AS product_id, p.name, p.price '
                                         'FROM Stock s JOIN Products p ON p.id = s.product_id WHERE s.id = ?',
                                         (item.get('stock_id'),)).fetchone()
                    if stock is None:
                        raise ApiError(404, 'Позиция склада не найдена')
                    if stock['quantity'] < quantity:
                        raise ApiError(400, 'Не хватает товара на складе: {} (есть {})'.format(stock['name'], stock['quantity']))
                    price = final_price(stock['price'], stock['product_id'] not in ordered)
                    conn.execute('UPDATE Stock SET quantity = quantity - ? WHERE id = ?', (quantity, stock['id']))
                    conn.execute('INSERT INTO OrderItems (order_id, stock_id, quantity, unit_price) VALUES (?, ?, ?, ?)',
                                 (order_id, stock['id'], quantity, price))
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            return {'ok': True, 'order_id': order_id}
        finally:
            conn.close()

def make_fio(row):
    parts = [row['last_name'], row['first_name'], row['middle_name']]
    return ' '.join(part for part in parts if part)

# товары, на которые были заказы в прошлом месяце (скидки у них нет)
def ordered_last_month(conn):
    year = int(TODAY[:4])
    month = int(TODAY[5:7]) - 1
    if month == 0:
        year -= 1
        month = 12
    rows = conn.execute('SELECT DISTINCT s.product_id FROM OrderItems oi '
                        'JOIN Orders o ON o.id = oi.order_id JOIN Stock s ON s.id = oi.stock_id '
                        'WHERE substr(o.order_date, 1, 7) = ?', ('%04d-%02d' % (year, month),)).fetchall()
    return set(row['product_id'] for row in rows)

def final_price(price, discount):
    if discount:
        return round(price * (1 - DISCOUNT), 2)
    return price

def main():
    server = HTTPServer((HOST, PORT), Handler)
    print('Сервер запущен: http://localhost:{}  (остановить: Ctrl+C)'.format(PORT))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nСервер остановлен')
    server.server_close()

if __name__ == '__main__':
    main()
