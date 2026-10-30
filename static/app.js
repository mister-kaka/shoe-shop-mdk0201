const state = {
  user: null,
  page: 'home',
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
  if (!state.user) {
    addButton(bar, 'Войти', openLogin);
    return;
  }
  const name = document.createElement('span');
  name.textContent = state.user.fio + ' (' + state.user.role + ')';
  bar.append(name);
  if (isStaff()) {
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
  $('welcome-text').textContent = getWelcomeText();
}

$('check-btn').addEventListener('click', checkServer);
$('login-form').addEventListener('submit', login);
$('login-cancel').addEventListener('click', closeLogin);
render();
checkServer();
