const express = require('express');
const checkoutRoutes = require('./checkoutRoutes');
const adminRoutes = require('./adminRoutes');
const userRoutes = require('./userRoutes');

const router = express.Router();
router.use('/api', checkoutRoutes);
router.use('/api/admin', adminRoutes);
router.use('/api/users', userRoutes);

module.exports = router;
