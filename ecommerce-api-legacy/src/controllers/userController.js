const userModel = require('../models/userModel');

async function deleteUser(req, res, next) {
  try {
    await userModel.remove(req.params.id);
    res.send('Usuário deletado com matrículas e pagamentos relacionados removidos.');
  } catch (err) {
    next(err);
  }
}

module.exports = { deleteUser };
