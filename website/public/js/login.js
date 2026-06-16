const form = document.getElementById('login-form');
const status = document.getElementById('login-status');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  status.textContent = 'Connexion…';
  status.className = 'form-status';

  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: form.username.value, password: form.password.value }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Connexion refusée.');

    window.location.href = './dashboard.html';
  } catch (err) {
    status.textContent = err.message;
    status.className = 'form-status err';
  }
});
