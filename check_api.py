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
    call('GET', '/app.js', show_body=False)
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

def group_orders():
    call('GET', '/api/orders?login=papetrov')
    call('GET', '/api/order?id=1&login=papetrov')
    call('GET', '/api/orders?login=asidorova')
    call('GET', '/api/orders?login=nobody')

def group_update():
    order = call('GET', '/api/order?id=2&login=isivanov', show_body=False)
    old_date = order['order_date']
    print('Дата заказа 2 до изменения:', old_date, '\n')
    call('POST', '/api/order/update', {'login': 'isivanov', 'order_id': 2, 'order_date': '2026-05-20'})
    changed = call('GET', '/api/order?id=2&login=isivanov', show_body=False)
    print('Дата заказа 2 после изменения:', changed['order_date'], '\n')
    call('POST', '/api/order/update', {'login': 'papetrov', 'order_id': 2, 'order_date': '2026-05-21'})
    call('POST', '/api/order/update', {'login': 'isivanov', 'order_id': 2, 'order_date': '20.05.2026'})
    call('POST', '/api/order/update', {'login': 'isivanov', 'order_id': 2, 'remove_items': [9999]})

    call('POST', '/api/order/update', {'login': 'isivanov', 'order_id': 2, 'order_date': old_date})

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

def show_product(product_id):
    card = call('GET', '/api/product?id=' + product_id, show_body=False)
    if card is None or 'error' in card:
        print('  ' + str(card))
        print()
        return
    print('  {} ({}, {})'.format(card['name'], card['category'], card['manufacturer']))
    print('  цена {} -> {}, скидка: {}'.format(card['price'], card['price_final'], 'да' if card['discount'] else 'нет'))
    print('  размеры:', ', '.join('{}:{}'.format(z['value'], z['quantity']) for z in card['sizes']))
    print()

def group_product():
    for product_id in ('1', '14', '29', '9999', 'abc'):
        show_product(product_id)

def group_create():
    before = call('GET', '/api/product?id=2', show_body=False)
    stock = before['sizes'][0]
    print('Остаток размера {} до заказа: {}\n'.format(stock['value'], stock['quantity']))
    call('POST', '/api/order/create', {'login': 'asidorova', 'items': [{'stock_id': stock['stock_id'], 'quantity': 1}]})
    after = call('GET', '/api/product?id=2', show_body=False)
    print('Остаток размера {} после заказа: {}\n'.format(stock['value'], after['sizes'][0]['quantity']))
    call('POST', '/api/order/create', {'login': 'asidorova', 'items': [{'stock_id': stock['stock_id'], 'quantity': 500}]})
    call('POST', '/api/order/create', {'login': 'asidorova', 'items': []})
    call('POST', '/api/order/create', {'login': 'nobody', 'items': [{'stock_id': stock['stock_id'], 'quantity': 1}]})

def group_robust():
    call('GET', '/api/products?sort=' + quote('что-то'), show_body=False)
    call('GET', '/api/product?id=')
    call('GET', '/api/login?login=')
    call('POST', '/api/order/create', {'login': 'asidorova', 'items': [{'stock_id': 3, 'quantity': '5'}]})
    call('POST', '/api/order/create', {'login': 'asidorova', 'items': [{'stock_id': 3, 'quantity': -1}]})
    call('POST', '/api/order/create', {'login': 'asidorova', 'items': 'всё'})
    call('POST', '/api/order/create', {})
    call('GET', '/uploads/' + quote('нет-такой-картинки.png'))

GROUPS = {
    'static': group_static,
    'echo': group_echo,
    'login': group_login,
    'orders': group_orders,
    'update': group_update,
    'products': group_products,
    'product': group_product,
    'create': group_create,
    'robust': group_robust,
}

if __name__ == '__main__':
    if len(sys.argv) != 2 or sys.argv[1] not in GROUPS:
        print('Запуск: python check_api.py группа')
        print('Группы:', ', '.join(GROUPS))
        sys.exit(1)
    GROUPS[sys.argv[1]]()
