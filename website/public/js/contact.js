const form = document.getElementById('contact-form');
const status = document.getElementById('form-status');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  status.textContent = 'Envoi en cours…';
  status.className = 'form-status';

  const payload = {
    name: form.name.value.trim(),
    email: form.email.value.trim(),
    message: form.message.value.trim(),
  };

  try {
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Erreur inconnue.');

    status.textContent = 'Message envoyé, merci !';
    status.className = 'form-status ok';
    form.reset();
  } catch (err) {
    status.textContent = err.message;
    status.className = 'form-status err';
  }
});
