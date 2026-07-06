function errorHandler(err, req, res, next) {
  const status = err.status || 500;
  const message = status < 500 ? err.message : 'Erro interno do servidor';
  if (status >= 500) {
    console.error(err.message);
  }
  res.status(status).send(message);
}

module.exports = errorHandler;
