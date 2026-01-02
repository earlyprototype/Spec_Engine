/**
 * Main Server Entry Point
 * Boutique Handcrafted Scarf Shop API
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
require('dotenv').config();

// Import routes
const authRoutes = require('./routes/auth');
const productRoutes = require('./routes/products');
const cartRoutes = require('./routes/cart');
const paymentRoutes = require('./routes/payments');
const orderRoutes = require('./routes/orders');

// Initialize app
const app = express();
const PORT = process.env.PORT || 3001;

// Security middleware
app.use(helmet());

// CORS configuration
const corsOptions = {
  origin: process.env.FRONTEND_URL || 'http://localhost:5173',
  credentials: true
};
app.use(cors(corsOptions));

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check endpoint
app.get('/', (req, res) => {
  res.json({
    status: 'ok',
    message: 'Boutique Scarf Shop API',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/products', productRoutes);
app.use('/api/cart', cartRoutes);
app.use('/api/payments', paymentRoutes);
app.use('/api/orders', orderRoutes);

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: 'Route not found'
  });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({
    success: false,
    message: 'Internal server error',
    error: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`
╔════════════════════════════════════════════════╗
║   Boutique Handcrafted Scarf Shop API          ║
║   Running on port ${PORT}                       ║
║   Environment: ${process.env.NODE_ENV || 'development'}              ║
║   Frontend: ${process.env.FRONTEND_URL || 'http://localhost:5173'}    ║
╚════════════════════════════════════════════════╝
  `);
  console.log(`Server ready at http://localhost:${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/`);
  console.log('\nAPI Endpoints:');
  console.log('  POST /api/auth/register');
  console.log('  POST /api/auth/login');
  console.log('  GET  /api/products');
  console.log('  GET  /api/cart (protected)');
  console.log('  POST /api/payments/create-checkout-session (protected)');
  console.log('  GET  /api/orders (protected)');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  server.close(() => {
    console.log('HTTP server closed');
    process.exit(0);
  });
});

module.exports = app;

