/**
 * Order Routes
 * Order management and viewing endpoints
 */

const express = require('express');
const orderService = require('../services/orderService');
const emailService = require('../services/emailService');
const authMiddleware = require('../middleware/auth');
const { adminOnly } = require('../middleware/roleCheck');

const router = express.Router();

// All order routes require authentication
router.use(authMiddleware);

/**
 * GET /api/orders
 * Get current user's orders
 */
router.get('/', async (req, res) => {
  try {
    const { page, limit } = req.query;

    const result = await orderService.getUserOrders(req.user.userId, {
      page: parseInt(page) || 1,
      limit: parseInt(limit) || 20
    });

    res.status(200).json({
      success: true,
      ...result
    });

  } catch (error) {
    console.error('Get user orders error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * GET /api/orders/:id
 * Get specific order
 */
router.get('/:id', async (req, res) => {
  try {
    const orderId = parseInt(req.params.id);
    
    // Users can only see their own orders
    // Admins can see any order (handled by passing null for userId check)
    const userId = req.user.role === 'admin' ? null : req.user.userId;
    
    const order = await orderService.getOrderById(orderId, userId);

    if (!order) {
      return res.status(404).json({
        success: false,
        message: 'Order not found'
      });
    }

    res.status(200).json({
      success: true,
      order
    });

  } catch (error) {
    console.error('Get order error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * GET /api/orders/admin/all
 * Get all orders (admin only)
 */
router.get('/admin/all', adminOnly, async (req, res) => {
  try {
    const { page, limit, status } = req.query;

    const result = await orderService.getAllOrders({
      page: parseInt(page) || 1,
      limit: parseInt(limit) || 20,
      status: status || null
    });

    res.status(200).json({
      success: true,
      ...result
    });

  } catch (error) {
    console.error('Get all orders error:', error);
    res.status(500).json({
      success: false,
      message: 'Server error'
    });
  }
});

/**
 * PUT /api/orders/:id/status
 * Update order status (admin only)
 */
router.put('/:id/status', adminOnly, async (req, res) => {
  try {
    const orderId = parseInt(req.params.id);
    const { status, message } = req.body;

    if (!status) {
      return res.status(400).json({
        success: false,
        message: 'Status is required'
      });
    }

    // Get order details before update
    const order = await orderService.getOrderById(orderId);
    if (!order) {
      return res.status(404).json({
        success: false,
        message: 'Order not found'
      });
    }

    // Update status
    const updatedOrder = await orderService.updateOrderStatus(orderId, status);

    // Get user email
    const db = require('../utils/database');
    const userQuery = 'SELECT email FROM users WHERE id = $1';
    const userResult = await db.query(userQuery, [order.userId]);
    const userEmail = userResult.rows[0]?.email;

    // Send status update email
    if (userEmail && ['processing', 'shipped', 'delivered'].includes(status)) {
      try {
        await emailService.sendOrderStatusUpdate({
          userEmail,
          orderId,
          status,
          message
        });
      } catch (emailError) {
        console.error('Failed to send status email:', emailError);
        // Don't fail the request if email fails
      }
    }

    res.status(200).json({
      success: true,
      order: updatedOrder
    });

  } catch (error) {
    console.error('Update order status error:', error);
    res.status(500).json({
      success: false,
      message: error.message || 'Server error'
    });
  }
});

module.exports = router;

