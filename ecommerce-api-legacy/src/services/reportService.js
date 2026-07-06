const courseModel = require('../models/courseModel');

async function getFinancialReport() {
  const rows = await courseModel.getAllWithRevenue();
  const reportMap = {};

  for (const row of rows) {
    if (!reportMap[row.id]) {
      reportMap[row.id] = { course: row.title, revenue: 0, students: [] };
    }
    if (row.student_name) {
      const paid = row.status === 'PAID' ? (row.amount || 0) : 0;
      if (row.status === 'PAID') {
        reportMap[row.id].revenue += paid;
      }
      reportMap[row.id].students.push({
        student: row.student_name,
        paid: row.amount || 0,
      });
    }
  }

  return Object.values(reportMap);
}

module.exports = { getFinancialReport };
