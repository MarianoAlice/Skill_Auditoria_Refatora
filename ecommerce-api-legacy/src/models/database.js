const sqlite3 = require('sqlite3').verbose();
const settings = require('../config/settings');

class Database {
  constructor() {
    this.db = new sqlite3.Database(settings.dbPath);
  }

  run(sql, params = []) {
    return new Promise((resolve, reject) => {
      this.db.run(sql, params, function onRun(err) {
        if (err) reject(err);
        else resolve({ lastID: this.lastID, changes: this.changes });
      });
    });
  }

  get(sql, params = []) {
    return new Promise((resolve, reject) => {
      this.db.get(sql, params, (err, row) => (err ? reject(err) : resolve(row)));
    });
  }

  all(sql, params = []) {
    return new Promise((resolve, reject) => {
      this.db.all(sql, params, (err, rows) => (err ? reject(err) : resolve(rows)));
    });
  }

  async init() {
    await this.run('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, pass TEXT)');
    await this.run('CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY, title TEXT, price REAL, active INTEGER)');
    await this.run('CREATE TABLE IF NOT EXISTS enrollments (id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER)');
    await this.run('CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY, enrollment_id INTEGER, amount REAL, status TEXT)');
    await this.run('CREATE TABLE IF NOT EXISTS audit_logs (id INTEGER PRIMARY KEY, action TEXT, created_at DATETIME)');

    const row = await this.get('SELECT COUNT(*) as count FROM users');
    if (row.count === 0) {
      const crypto = require('crypto');
      const hash = (pwd) => {
        const salt = crypto.randomBytes(8).toString('hex');
        return `${salt}:${crypto.scryptSync(pwd, salt, 32).toString('hex')}`;
      };
      await this.run("INSERT INTO users (name, email, pass) VALUES ('Leonan', 'leonan@fullcycle.com.br', ?)", [hash('123')]);
      await this.run("INSERT INTO courses (title, price, active) VALUES ('Clean Architecture', 997.00, 1), ('Docker', 497.00, 1)");
      await this.run('INSERT INTO enrollments (user_id, course_id) VALUES (1, 1)');
      await this.run("INSERT INTO payments (enrollment_id, amount, status) VALUES (1, 997.00, 'PAID')");
    }
  }
}

module.exports = new Database();
