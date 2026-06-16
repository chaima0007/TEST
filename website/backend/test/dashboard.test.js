const { test, describe } = require('node:test');
const assert = require('node:assert/strict');
const request = require('supertest');
const createApp = require('../app');

async function loggedInAgent(app) {
  const agent = request.agent(app);
  await agent.post('/api/login').send({ username: 'admin', password: 'moonbow2026' });
  return agent;
}

describe('GET /api/dashboard payload shape', () => {
  test('returns plausible, bounded simulated infrastructure metrics', async () => {
    const app = createApp({ dbPath: ':memory:' });
    const agent = await loggedInAgent(app);

    const res = await agent.get('/api/dashboard');
    const body = res.body;

    assert.ok(body.uptimePct >= 95 && body.uptimePct <= 100, `uptimePct out of range: ${body.uptimePct}`);
    assert.ok(body.migrationPct >= 0 && body.migrationPct <= 100);
    assert.ok(body.openTickets >= 0);
    assert.ok(body.securityAlerts >= 0);
    assert.ok(body.usersOnline >= 0);
    assert.ok(!Number.isNaN(new Date(body.generatedAt).getTime()));
  });

  test('varies slightly between calls to feel "live"', async () => {
    const app = createApp({ dbPath: ':memory:' });
    const agent = await loggedInAgent(app);

    const samples = [];
    for (let i = 0; i < 8; i++) {
      samples.push((await agent.get('/api/dashboard')).body.usersOnline);
    }
    assert.ok(new Set(samples).size > 1, 'expected usersOnline to vary across repeated calls');
  });
});
