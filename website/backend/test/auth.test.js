const { test, describe } = require('node:test');
const assert = require('node:assert/strict');
const request = require('supertest');
const createApp = require('../app');

describe('authentication and the protected dashboard', () => {
  test('GET /api/session reports logged out by default', async () => {
    const app = createApp({ dbPath: ':memory:' });
    const res = await request(app).get('/api/session');
    assert.equal(res.status, 200);
    assert.equal(res.body.loggedIn, false);
  });

  test('GET /api/dashboard is rejected without a session', async () => {
    const app = createApp({ dbPath: ':memory:' });
    const res = await request(app).get('/api/dashboard');
    assert.equal(res.status, 401);
  });

  test('POST /api/login rejects wrong credentials', async () => {
    const app = createApp({ dbPath: ':memory:' });
    const res = await request(app).post('/api/login').send({ username: 'admin', password: 'wrong' });
    assert.equal(res.status, 401);
  });

  test('POST /api/login with the demo credentials grants access to the dashboard', async () => {
    const app = createApp({ dbPath: ':memory:' });
    const agent = request.agent(app); // keeps the session cookie across requests

    const loginRes = await agent.post('/api/login').send({ username: 'admin', password: 'moonbow2026' });
    assert.equal(loginRes.status, 200);
    assert.equal(loginRes.body.username, 'admin');

    const sessionRes = await agent.get('/api/session');
    assert.equal(sessionRes.body.loggedIn, true);

    const dashRes = await agent.get('/api/dashboard');
    assert.equal(dashRes.status, 200);
    assert.ok(typeof dashRes.body.uptimePct === 'number');
  });

  test('POST /api/logout ends the session and re-locks the dashboard', async () => {
    const app = createApp({ dbPath: ':memory:' });
    const agent = request.agent(app);

    await agent.post('/api/login').send({ username: 'admin', password: 'moonbow2026' });
    assert.equal((await agent.get('/api/dashboard')).status, 200);

    await agent.post('/api/logout');

    const dashAfterLogout = await agent.get('/api/dashboard');
    assert.equal(dashAfterLogout.status, 401);
  });
});
