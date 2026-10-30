const state = {
  user: null,
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

function renderHeader() {
  if (state.user) {
    $('userbar').textContent = state.user.fio;
  } else {
    $('userbar').textContent = 'Гость';
  }
}

$('check-btn').addEventListener('click', checkServer);
renderHeader();
checkServer();
