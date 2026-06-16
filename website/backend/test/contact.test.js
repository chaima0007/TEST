const { test, describe } = require('node:test');
const assert = require('node:assert/strict');
const request = require('supertest');
const createApp = require('../app');

describe('POST /api/contact', () => {
  test('accepts a valid message', async () => {
    const app = createApp({ dbPath: ':memory:' });
    const res = await request(app)
      .post('/api/contact')
      .send({ name: 'Chaima', email: 'chaima@example.com', message: 'Bonjour Moonbow' });

    assert.equal(res.status, 201);
    assert.deepEqual(res.body, { ok: true });
  });

  test('rejects a missing field', async () => {
    const app = createApp({ dbPath: ':memory:' });
    const res = await request(app).post('/api/contact').send({ name: 'Chaima', email: 'chaima@example.com' });

    assert.equal(res.status, 400);
    assert.ok(res.body.error);
  });

  test('rejects an over-long field', async () => {
    const app = createApp({ dbPath: ':memory:' });
    const res = await request(app)
      .post('/api/contact')
      .send({ name: 'x'.repeat(200), email: 'a@b.com', message: 'hi' });

    assert.equal(res.status, 400);
  });

  test('rejects a malformed email address', async () => {
    const app = createApp({ dbPath: ':memory:' });
    const res = await request(app)
      .post('/api/contact')
      .send({ name: 'Chaima', email: 'not-an-email', message: 'Bonjour Moonbow' });

    assert.equal(res.status, 400);
    assert.ok(res.body.error);
  });

  test('throttles repeated submissions from the same client', async () => {
    const app = createApp({ dbPath: ':memory:' });
    const agent = request.agent(app);
    let lastRes;
    for (let i = 0; i < 11; i++) {
      lastRes = await agent
        .post('/api/contact')
        .send({ name: 'Chaima', email: 'chaima@example.com', message: 'Bonjour Moonbow' });
    }
    assert.equal(lastRes.status, 429);
  });

  test('persists the message in the database', async () => {
    const app = createApp({ dbPath: ':memory:' });
    await request(app)
      .post('/api/contact')
      .send({ name: 'Chaima', email: 'chaima@example.com', message: 'Bonjour Moonbow' });

    const row = app.locals.db.prepare('SELECT * FROM contacts').get();
    assert.equal(row.name, 'Chaima');
    assert.equal(row.email, 'chaima@example.com');
    assert.equal(row.message, 'Bonjour Moonbow');
  });
});
