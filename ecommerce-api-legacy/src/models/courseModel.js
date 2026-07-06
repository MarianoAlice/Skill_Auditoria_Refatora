const db = require('./database');

async function findActiveById(courseId) {
  return db.get('SELECT * FROM courses WHERE id = ? AND active = 1', [courseId]);
}

async function getAllWithRevenue() {
  return db.all(`
    SELECT c.id, c.title, c.price,
           u.name AS student_name, u.email AS student_email,
           p.amount, p.status
    FROM courses c
    LEFT JOIN enrollments e ON e.course_id = c.id
    LEFT JOIN users u ON u.id = e.user_id
    LEFT JOIN payments p ON p.enrollment_id = e.id
    ORDER BY c.id
  `);
}

module.exports = { findActiveById, getAllWithRevenue };
