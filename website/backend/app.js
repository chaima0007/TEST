const path = require('path');
const express = require('express');
const session = require('express-session');
const bcrypt = require('bcryptjs');
const rateLimit = require('express-rate-limit');
const createDb = require('./db');

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function createApp({ dbPath, sessionSecret } = {}) {
  const db = createDb(dbPath);
  const app = express();

  app.use(express.json());
  app.use(
    session({
      secret: sessionSecret || process.env.SESSION_SECRET || 'dev-only-secret-change-me',
      resave: false,
      saveUninitialized: false,
      cookie: { maxAge: 1000 * 60 * 60 * 4, sameSite: 'lax' }, // 4h
    })
  );
  app.use(express.static(path.join(__dirname, '..', 'public')));

  function requireAuth(req, res, next) {
    if (req.session && req.session.userId) return next();
    return res.status(401).json({ error: 'Authentification requise.' });
  }

  const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    limit: 20,
    standardHeaders: true,
    legacyHeaders: false,
    message: { error: 'Trop de tentatives de connexion, réessayez plus tard.' },
  });

  const contactLimiter = rateLimit({
    windowMs: 15 * 60 * 1000,
    limit: 10,
    standardHeaders: true,
    legacyHeaders: false,
    message: { error: 'Trop de messages envoyés, réessayez plus tard.' },
  });

  // --- Contact (site vitrine) ------------------------------------------------
  app.post('/api/contact', contactLimiter, (req, res) => {
    const { name, email, message } = req.body || {};
    if (!name || !email || !message) {
      return res.status(400).json({ error: 'Nom, email et message sont requis.' });
    }
    if (name.length > 100 || email.length > 150 || message.length > 2000) {
      return res.status(400).json({ error: 'Champ trop long.' });
    }
    if (!EMAIL_RE.test(String(email).trim())) {
      return res.status(400).json({ error: 'Adresse email invalide.' });
    }
    db.prepare('INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)').run(
      String(name).trim(),
      String(email).trim(),
      String(message).trim()
    );
    res.status(201).json({ ok: true });
  });

  // --- Authentification (démo portail infrastructure) ------------------------
  app.post('/api/login', loginLimiter, (req, res) => {
    const { username, password } = req.body || {};
    if (typeof username !== 'string' || typeof password !== 'string') {
      return res.status(400).json({ error: 'Identifiants invalides.' });
    }
    const user = db.prepare('SELECT * FROM users WHERE username = ?').get(username);
    if (!user || !bcrypt.compareSync(password, user.password_hash)) {
      return res.status(401).json({ error: 'Identifiants invalides.' });
    }
    req.session.userId = user.id;
    req.session.username = user.username;
    res.json({ ok: true, username: user.username });
  });

  app.post('/api/logout', (req, res) => {
    req.session.destroy(() => res.json({ ok: true }));
  });

  app.get('/api/session', (req, res) => {
    res.json({ loggedIn: !!(req.session && req.session.userId), username: req.session?.username || null });
  });

  // --- Démo infrastructure modernisée (portail protégé) -----------------------
  app.get('/api/dashboard', requireAuth, (req, res) => {
    const row = db.prepare('SELECT * FROM metrics WHERE id = 1').get();

    // Petite variation aléatoire à chaque appel pour donner une impression de
    // tableau de bord "vivant", sans avoir de vraie infrastructure à monitorer.
    const jitter = (v, spread) => Math.round((v + (Math.random() - 0.5) * spread) * 10) / 10;

    res.json({
      uptimePct: Math.min(100, Math.max(95, jitter(row.uptime_pct, 0.3))),
      migrationPct: row.migration_pct,
      openTickets: Math.max(0, Math.round(jitter(row.open_tickets, 2))),
      securityAlerts: Math.max(0, Math.round(jitter(row.security_alerts, 1))),
      usersOnline: Math.max(0, Math.round(jitter(row.users_online, 6))),
      generatedAt: new Date().toISOString(),
    });
  });

  app.locals.db = db;
  return app;
}

module.exports = createApp;
