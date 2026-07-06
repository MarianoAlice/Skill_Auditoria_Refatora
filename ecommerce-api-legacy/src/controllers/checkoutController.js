const checkoutService = require('../services/checkoutService');

async function checkout(req, res, next) {
  try {
    const { usr, eml, pwd, c_id, card } = req.body;
    if (!usr || !eml || !c_id || !card) {
      return res.status(400).send('Bad Request');
    }
    const result = await checkoutService.processCheckout({
      userName: usr,
      email: eml,
      password: pwd,
      courseId: c_id,
      cardNumber: card,
    });
    res.status(200).json(result);
  } catch (err) {
    next(err);
  }
}

module.exports = { checkout };
