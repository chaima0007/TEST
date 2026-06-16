const path = require('path');
const Database = require('better-sqlite3');
const bcrypt = require('bcryptjs');

function createDb(dbPath) {
  const target = dbPath || path.join(__dirname, 'moonbow.db');
  const db = new Database(target);
  db.pragma('journal_mode = WAL');

  db.exec(`
    CREATE TABLE IF NOT EXISTS contacts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      email TEXT NOT NULL,
      message TEXT NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT NOT NULL UNIQUE,
      password_hash TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS metrics (
      id INTEGER PRIMARY KEY CHECK (id = 1),
      uptime_pct REAL NOT NULL,
      migration_pct REAL NOT NULL,
      open_tickets INTEGER NOT NULL,
      security_alerts INTEGER NOT NULL,
      users_online INTEGER NOT NULL
    );
  `);

  const userCount = db.prepare('SELECT COUNT(*) AS n FROM users').get().n;
  if (userCount === 0) {
    // Identifiants de démonstration uniquement, affichés sur la page de connexion.
    const hash = bcrypt.hashSync('moonbow2026', 10);
    db.prepare('INSERT INTO users (username, password_hash) VALUES (?, ?)').run('admin', hash);
  }

  const metricsRow = db.prepare('SELECT id FROM metrics WHERE id = 1').get();
  if (!metricsRow) {
    db.prepare(`
      INSERT INTO metrics (id, uptime_pct, migration_pct, open_tickets, security_alerts, users_online)
      VALUES (1, 99.6, 42, 7, 1, 23)
    `).run();
  }

  return db;
}

module.exports = createDb;
