import json
import sys
import urllib.error
import urllib.request
from urllib.parse import quote

BASE = 'http://localhost:8000'

def call(method, path, body=None, show_body=True):
    data = None
    headers = {}
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    request = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as error:
        response = error
    except urllib.error.URLError as error:
        print('Сервер не отвечает ({}). Запущен ли python server.py?'.format(error.reason))
        sys.exit(1)
    status = response.status if hasattr(response, 'status') else response.code
    raw = response.read()
    content_type = response.headers.get('Content-Type', '')
    print(method, path)
    print('  -> {}  {}'.format(status, content_type))
    if show_body:
        text = raw.decode('utf-8', errors='replace')
        print('  ' + (text if len(text) < 600 else text[:600] + ' ...'))
    else:
        print('  размер ответа: {} байт'.format(len(raw)))
    print()
    try:
        return json.loads(raw.decode('utf-8'))
    except ValueError:
        return None

def group_static():
    call('GET', '/', show_body=False)
    call('GET', '/style.css', show_body=False)
    call('GET', '/logo.png', show_body=False)
    call('GET', '/net-takogo-faila.html')

def group_echo():
    call('POST', '/api/echo', {'привет': 'мир', 'числа': [1, 2, 3]})
    call('GET', '/api/net-takogo')

def group_login():
    for login in ('isivanov', 'papetrov', 'asidorova', 'ekuznetsova', 'apopov'):
        call('GET', '/api/login?login=' + login)
    call('GET', '/api/login?login=nobody')

def show_products(path, limit=4):
    items = call('GET', path, show_body=False)
    print('  товаров в ответе:', len(items))
    for item in items[:limit]:
        print('  {:>2} {:36} {:>8} -> {:>8}  {} ({})'.format(item['id'], item['name'][:34], item['price'], item['price_final'], item['level'], item['total']))
    print()

def group_products():
    show_products('/api/products')
    show_products('/api/products?category=' + quote('Женская обувь'))
    show_products('/api/products?search=' + quote('кроссовки'))
    show_products('/api/products?sort=price_asc')
    show_products('/api/products?sort=price_desc')
    show_products('/api/products?category=' + quote('Мужская обувь') + '&search=' + quote('ботинки') + '&sort=price_desc')
    show_products('/api/products?search=' + quote('такого товара нет'))

GROUPS = {
    'static': group_static,
    'echo': group_echo,
    'login': group_login,
    'products': group_products,
}

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in GROUPS:
        print('Запуск: python check_api.py группа')
        print('Группы:', ', '.join(GROUPS))
        sys.exit(1)
    GROUPS[sys.argv[1]]()
