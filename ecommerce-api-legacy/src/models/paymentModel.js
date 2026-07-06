const db = require('./database');

async function create(enrollmentId, amount, status) {
  await db.run(
    'INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)',
    [enrollmentId, amount, status],
  );
}

module.exports = { create };
