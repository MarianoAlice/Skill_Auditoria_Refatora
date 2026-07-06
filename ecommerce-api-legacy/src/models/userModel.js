const crypto = require('crypto');
const db = require('./database');

function hashPassword(password) {
  const salt = crypto.randomBytes(8).toString('hex');
  const hash = crypto.scryptSync(password, salt, 32).toString('hex');
  return `${salt}:${hash}`;
}

async function findByEmail(email) {
  return db.get('SELECT * FROM users WHERE email = ?', [email]);
}

async function create(name, email, password) {
  const result = await db.run(
    'INSERT INTO users (name, email, pass) VALUES (?, ?, ?)',
    [name, email, hashPassword(password || '123456')],
  );
  return result.lastID;
}

async function remove(userId) {
  await db.run(
    'DELETE FROM payments WHERE enrollment_id IN (SELECT id FROM enrollments WHERE user_id = ?)',
    [userId],
  );
  await db.run('DELETE FROM enrollments WHERE user_id = ?', [userId]);
  await db.run('DELETE FROM users WHERE id = ?', [userId]);
}

module.exports = { findByEmail, create, remove };
