const settings = require('../config/settings');
const courseModel = require('../models/courseModel');
const userModel = require('../models/userModel');
const enrollmentModel = require('../models/enrollmentModel');
const paymentModel = require('../models/paymentModel');
const db = require('../models/database');

async function processCheckout({ userName, email, password, courseId, cardNumber }) {
  const course = await courseModel.findActiveById(courseId);
  if (!course) {
    const err = new Error('Curso não encontrado');
    err.status = 404;
    throw err;
  }

  const status = cardNumber.startsWith('4') ? 'PAID' : 'DENIED';
  if (status === 'DENIED') {
    const err = new Error('Pagamento recusado');
    err.status = 400;
    throw err;
  }

  let user = await userModel.findByEmail(email);
  const userId = user ? user.id : await userModel.create(userName, email, password);

  const enrollmentId = await enrollmentModel.create(userId, courseId);
  await paymentModel.create(enrollmentId, course.price, status);
  await db.run(
    "INSERT INTO audit_logs (action, created_at) VALUES (?, datetime('now'))",
    [`Checkout curso ${courseId} por ${userId}`],
  );

  return { msg: 'Sucesso', enrollment_id: enrollmentId };
}

module.exports = { processCheckout };
