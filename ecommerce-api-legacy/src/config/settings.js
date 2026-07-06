module.exports = {
  port: parseInt(process.env.PORT || '3000', 10),
  dbPath: process.env.DB_PATH || './lms.db',
  paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || '',
};
