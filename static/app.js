const state = {
  user: null,
  page: 'home',
  products: [],
  category: '',
  search: '',
  sort: '',
  product: null,
  cart: [],
  serverOk: null
};

function $(id) {
  return document.getElementById(id);
}

async function api(url, body) {
  let options = {};
  if (body !== undefined) {
    options = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    };
  }
  let response;
  try {
    response = await fetch(url, options);
  } catch (error) {
    throw new Error('Нет связи с сервером');
  }
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || 'Ошибка запроса');
  }
  return data;
}

let toastTimer = null;

function toast(message, type) {
  const box = $('toast');
  box.textContent = message;
  box.classList.toggle('error', type === 'error');
  box.classList.remove('hidden');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(function () {
    box.classList.add('hidden');
  }, 3000);
}

function money(value) {
  return Number(value).toLocaleString('ru-RU', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function makeCell(text, className) {
  const td = document.createElement('td');
  td.textContent = text;
  if (className) {
    td.className = className;
  }
  return td;
}

function isStaff() {
  if (state.user === null) {
    return false;
  }
  return state.user.role === 'Менеджер' || state.user.role === 'Администратор';
}

function showStatus() {
  if (state.serverOk === null) {
    $('server-status').textContent = 'Проверяю связь с сервером...';
  } else if (state.serverOk) {
    $('server-status').textContent = 'Связь с сервером: есть';
  } else {
    $('server-status').textContent = 'Связь с сервером: нет';
  }
}

async function checkServer() {
  state.serverOk = null;
  showStatus();
  try {
    const answer = await api('/api/echo', { ping: 'привет, сервер' });
    state.serverOk = answer.ok === true;
  } catch (error) {
    state.serverOk = false;
    toast(error.message, 'error');
  }
  showStatus();
}

function openLogin() {
  $('login-input').value = '';
  $('login-modal').classList.remove('hidden');
  $('login-input').focus();
}

function closeLogin() {
  $('login-modal').classList.add('hidden');
}

async function login(event) {
  event.preventDefault();
  const loginText = $('login-input').value.trim();
  if (loginText === '') {
    toast('Введите логин', 'error');
    return;
  }
  try {
    const user = await api('/api/login?login=' + encodeURIComponent(loginText));
    state.user = { id: user.id, fio: user.fio, role: user.role, login: loginText };
    state.page = 'home';
    closeLogin();
    render();
    toast('Вы вошли как ' + user.fio);
  } catch (error) {
    toast(error.message, 'error');
  }
}

function logout() {
  state.user = null;
  state.page = 'home';
  render();
}

function showOrders() {
  state.page = 'orders';
  render();
}

function showCatalog() {
  state.page = 'home';
  render();
}

function addButton(parent, text, onClick, className) {
  const button = document.createElement('button');
  button.textContent = text;
  if (className) {
    button.className = className;
  }
  button.addEventListener('click', onClick);
  parent.append(button);
}

function renderHeader() {
  const bar = $('userbar');
  bar.textContent = '';
  addButton(bar, 'Корзина (' + state.cart.length + ')', openCart, 'secondary');
  if (!state.user) {
    addButton(bar, 'Войти', openLogin);
    return;
  }
  const name = document.createElement('span');
  name.textContent = state.user.fio + ' (' + state.user.role + ')';
  bar.append(name);
  if (isStaff()) {
    addButton(bar, 'Каталог', showCatalog, 'secondary');
    addButton(bar, 'Заказы', showOrders);
  }
  addButton(bar, 'Выйти', logout, 'secondary');
}

function getWelcomeText() {
  if (!state.user) {
    return 'Войдите в систему, чтобы продолжить.';
  }
  if (isStaff()) {
    return 'Вы вошли как ' + state.user.fio + '. Нажмите «Заказы», чтобы открыть список заказов.';
  }
  return 'Вы вошли как ' + state.user.fio + '. Раздел заказов доступен менеджеру и администратору.';
}

function render() {
  renderHeader();
  const onOrders = isStaff() && state.page === 'orders';
  $('welcome').classList.toggle('hidden', onOrders);
  $('orders-box').classList.toggle('hidden', !onOrders);
  $('catalog').classList.toggle('hidden', onOrders);
  $('welcome-text').textContent = getWelcomeText();
}

async function loadCategories() {
  try {
    const names = await api('/api/categories');
    const select = $('category-select');
    select.append(new Option('Все категории', ''));
    for (const name of names) {
      select.append(new Option(name, name));
    }
  } catch (error) {
    toast(error.message, 'error');
  }
}

async function loadProducts() {
  const params = new URLSearchParams({ category: state.category, search: state.search, sort: state.sort });
  try {
    state.products = await api('/api/products?' + params);
    renderCatalog();
  } catch (error) {
    toast(error.message, 'error');
  }
}

function priceBlock(parent, product) {
  if (product.discount) {
    const old = document.createElement('s');
    old.textContent = money(product.price) + ' руб.';
    parent.append(old, ' ');
  }
  const now = document.createElement('b');
  now.textContent = money(product.price_final) + ' руб.';
  parent.append(now);
}

function setImage(img, name) {
  img.onerror = function () {
    img.onerror = null;
    img.src = 'uploads/picture.png';
  };
  img.src = 'uploads/' + name;
}

function renderCatalog() {
  const list = $('catalog-list');
  list.textContent = '';
  $('catalog-empty').classList.toggle('hidden', state.products.length > 0);
  for (const product of state.products) {
    const card = document.createElement('div');
    card.className = 'product';
    if (product.level === 'мало') {
      card.classList.add('low');
    }
    const img = document.createElement('img');
    setImage(img, product.image);
    const name = document.createElement('h3');
    name.textContent = product.name;
    const info = document.createElement('p');
    info.textContent = product.category + ', ' + product.manufacturer;
    const price = document.createElement('p');
    priceBlock(price, product);
    const stock = document.createElement('p');
    stock.className = 'stock';
    stock.textContent = 'На складе: ' + product.total + ' шт. (' + product.level + ')';
    card.append(img, name, info, price, stock);
    card.addEventListener('click', function () {
      openProduct(product.id);
    });
    list.append(card);
  }
}

async function openProduct(id) {
  try {
    state.product = await api('/api/product?id=' + id);
    renderProduct();
    $('product-modal').classList.remove('hidden');
  } catch (error) {
    toast(error.message, 'error');
  }
}

function renderProduct() {
  const product = state.product;
  setImage($('product-img'), product.image);
  $('product-name').textContent = product.name;
  $('product-meta').textContent = product.category + ' / ' + product.subcategory + '. Производитель: ' + product.manufacturer;
  $('product-descr').textContent = product.description;
  $('product-composition').textContent = 'Состав: ' + product.composition;
  $('product-price').textContent = '';
  priceBlock($('product-price'), product);
  const box = $('size-list');
  box.textContent = '';
  for (const size of product.sizes) {
    const label = document.createElement('label');
    label.className = 'size';
    const radio = document.createElement('input');
    radio.type = 'radio';
    radio.name = 'size';
    radio.value = size.stock_id;
    radio.disabled = size.quantity === 0;
    label.append(radio, ' ' + size.value + ' (' + size.quantity + ' шт.)');
    box.append(label);
  }
  $('qty-input').value = 1;
}

function closeProduct() {
  $('product-modal').classList.add('hidden');
}

function addToCart() {
  const checked = document.querySelector('input[name="size"]:checked');
  if (!checked) {
    toast('Выберите размер', 'error');
    return;
  }
  const size = state.product.sizes.find(function (s) {
    return String(s.stock_id) === checked.value;
  });
  const quantity = Number($('qty-input').value);
  if (!Number.isInteger(quantity) || quantity < 1) {
    toast('Количество должно быть целым числом от 1', 'error');
    return;
  }
  if (quantity > size.quantity) {
    toast('На складе только ' + size.quantity + ' шт. этого размера', 'error');
    return;
  }
  const same = state.cart.find(function (item) {
    return item.stock_id === size.stock_id;
  });
  if (same) {
    if (same.quantity + quantity > size.quantity) {
      toast('В корзине уже ' + same.quantity + ' шт., больше ' + size.quantity + ' на складе нет', 'error');
      return;
    }
    same.quantity += quantity;
  } else {
    state.cart.push({
      stock_id: size.stock_id,
      name: state.product.name,
      size: size.value,
      quantity: quantity,
      price: state.product.price_final
    });
  }
  closeProduct();
  renderHeader();
  toast('Товар добавлен в корзину');
}

function cartTotal() {
  let total = 0;
  for (const item of state.cart) {
    total += item.price * item.quantity;
  }
  return total;
}

function openCart() {
  renderCart();
  $('cart-modal').classList.remove('hidden');
}

function closeCart() {
  $('cart-modal').classList.add('hidden');
}

function renderCart() {
  const tbody = $('cart-table').querySelector('tbody');
  tbody.textContent = '';
  $('cart-empty').classList.toggle('hidden', state.cart.length > 0);
  for (const item of state.cart) {
    const row = document.createElement('tr');
    row.append(makeCell(item.name));
    row.append(makeCell(item.size));
    row.append(makeCell(item.quantity, 'num'));
    row.append(makeCell(money(item.price), 'num'));
    row.append(makeCell(money(item.price * item.quantity), 'num'));
    const buttonCell = document.createElement('td');
    addButton(buttonCell, 'Удалить', function () {
      removeFromCart(item.stock_id);
    }, 'danger');
    row.append(buttonCell);
    tbody.append(row);
  }
  $('cart-total').textContent = money(cartTotal());
}

function removeFromCart(stockId) {
  state.cart = state.cart.filter(function (item) {
    return item.stock_id !== stockId;
  });
  renderCart();
  renderHeader();
}

async function makeOrder() {
  if (state.cart.length === 0) {
    toast('Корзина пуста', 'error');
    return;
  }
  if (!state.user) {
    toast('Войдите в систему, чтобы оформить заказ', 'error');
    return;
  }
  const items = state.cart.map(function (item) {
    return { stock_id: item.stock_id, quantity: item.quantity };
  });
  try {
    const answer = await api('/api/order/create', { login: state.user.login, items: items });
    state.cart = [];
    closeCart();
    renderHeader();
    loadProducts();
    toast('Заказ № ' + answer.order_id + ' оформлен');
  } catch (error) {
    toast(error.message, 'error');
  }
}

$('check-btn').addEventListener('click', checkServer);
$('login-form').addEventListener('submit', login);
$('login-cancel').addEventListener('click', closeLogin);
$('category-select').addEventListener('change', function (event) {
  state.category = event.target.value;
  loadProducts();
});
$('sort-select').addEventListener('change', function (event) {
  state.sort = event.target.value;
  loadProducts();
});

let searchTimer = null;
$('search-input').addEventListener('input', function (event) {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(function () {
    state.search = event.target.value.trim();
    loadProducts();
  }, 300);
});
$('add-btn').addEventListener('click', addToCart);
$('product-close').addEventListener('click', closeProduct);
$('make-order-btn').addEventListener('click', makeOrder);
$('cart-close').addEventListener('click', closeCart);
render();
loadCategories();
loadProducts();
checkServer();
