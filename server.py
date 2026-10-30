import json
import mimetypes
import os
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'shop.db')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
HOST = '127.0.0.1'
PORT = 8000


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
        routes = {
            '/api/login': self.api_login,
        }
        if url.path.startswith('/api/'):
            self.run_api(routes.get(url.path), params)
        else:
            self.send_static(url.path)

    def do_POST(self):
        url = urlparse(self.path)
        routes = {
            '/api/echo': self.api_echo,
        }
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
        self.send_json(result)

    def api_echo(self, data):
        return {'ok': True, 'received': data}

    def get_user(self, conn, login):
        row = conn.execute(
            'SELECT id, last_name, first_name, middle_name, role FROM Users WHERE login = ?',
            ((login or '').strip(),)
        ).fetchone()
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

def make_fio(row):
    parts = [row['last_name'], row['first_name'], row['middle_name']]
    return ' '.join(part for part in parts if part)


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
