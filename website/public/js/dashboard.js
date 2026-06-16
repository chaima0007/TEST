async function checkSession() {
  const res = await fetch('/api/session');
  const data = await res.json();
  if (!data.loggedIn) {
    window.location.href = './login.html';
    return null;
  }
  return data;
}

function setMetricLevel(el, value, warnAt, dangerAt, higherIsWorse) {
  el.classList.remove('good', 'warn', 'danger');
  const isBad = higherIsWorse ? value >= dangerAt : value <= dangerAt;
  const isWarn = higherIsWorse ? value >= warnAt : value <= warnAt;
  el.classList.add(isBad ? 'danger' : isWarn ? 'warn' : 'good');
}

async function refreshDashboard() {
  const res = await fetch('/api/dashboard');
  if (res.status === 401) {
    window.location.href = './login.html';
    return;
  }
  const data = await res.json();

  const uptimeEl = document.getElementById('m-uptime');
  uptimeEl.textContent = `${data.uptimePct.toFixed(1)} %`;
  setMetricLevel(uptimeEl, data.uptimePct, 98, 97, false);

  document.getElementById('m-migration').textContent = `${data.migrationPct.toFixed(0)} %`;
  document.getElementById('m-migration-bar').style.width = `${data.migrationPct}%`;

  const ticketsEl = document.getElementById('m-tickets');
  ticketsEl.textContent = data.openTickets;
  setMetricLevel(ticketsEl, data.openTickets, 10, 15, true);

  const alertsEl = document.getElementById('m-alerts');
  alertsEl.textContent = data.securityAlerts;
  setMetricLevel(alertsEl, data.securityAlerts, 2, 4, true);

  document.getElementById('m-users').textContent = data.usersOnline;

  document.getElementById('updated-at').textContent =
    `Dernière mise à jour : ${new Date(data.generatedAt).toLocaleTimeString('fr-FR')}`;
}

document.getElementById('logout-btn').addEventListener('click', async () => {
  await fetch('/api/logout', { method: 'POST' });
  window.location.href = './login.html';
});

(async () => {
  const session = await checkSession();
  if (!session) return;
  document.getElementById('welcome').textContent = `Connecté en tant que ${session.username}`;
  await refreshDashboard();
  setInterval(refreshDashboard, 4000);
})();
