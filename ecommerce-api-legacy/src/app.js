const express = require('express');
const settings = require('./config/settings');
const db = require('./models/database');
const routes = require('./routes');
const errorHandler = require('./middlewares/errorHandler');

const app = express();
app.use(express.json());

async function bootstrap() {
  await db.init();
  app.use(routes);
  app.use(errorHandler);
  app.listen(settings.port, () => {
    console.log(`LMS API rodando na porta ${settings.port}...`);
  });
}

bootstrap().catch((err) => {
  console.error('Falha ao iniciar aplicação:', err.message);
  process.exit(1);
});
